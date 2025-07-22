import psycopg2
import pandas as pd
from typing import Optional, Tuple
from pycaret.time_series import *
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER', 'myuser')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'mypassword')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'mydatabase')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# Updated fetch_data function
def fetch_data(query: str, params: Optional[Tuple] = None) -> pd.DataFrame:
    try:
        conn = psycopg2.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB
        )
        if params:
            df = pd.read_sql(query, conn, params=params)
        else:
            df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

# Fetch and process market cap data from the database
def get_stock_data(symbol: str, start_date: str, end_date: str, last_quarter_date: str = "2025-06-30") -> pd.DataFrame:
    query = """
    SELECT
        data->>'qfs_symbol_v2' AS symbol,
        COALESCE(data->'financials'->'quarterly'->'market_cap', '[]'::jsonb) AS market_cap
    FROM companies
    WHERE data->>'qfs_symbol_v2' = %s;
    """
    params = (symbol,)
    df = fetch_data(query, params)

    # Check if data is empty or market_cap is empty
    if df.empty or not df['market_cap'].iloc[0]:
        raise ValueError(f"No market cap data found for symbol {symbol}")

    # Get market_cap values
    market_cap_values = df['market_cap'].iloc[0]
    
    # Debug: Print the market_cap data
    print("Market cap values:", market_cap_values)
    print("Number of market cap values:", len(market_cap_values))

    # Generate quarterly dates ending at last_quarter_date
    last_quarter = pd.to_datetime(last_quarter_date)  # e.g., 2025-06-30 (Q2 2025)
    num_values = len(market_cap_values)
    quarters = pd.date_range(end=last_quarter, periods=num_values, freq='Q')
    
    # Check if there are enough values for the date range
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    expected_quarters = len(pd.date_range(start=start_date, end=end_date, freq='Q'))
    if num_values > expected_quarters:
        print(f"Warning: More market cap values ({num_values}) than quarters ({expected_quarters}). Truncating to match date range.")
        market_cap_values = market_cap_values[-expected_quarters:]  # Keep latest values
        quarters = quarters[-expected_quarters:]
    elif num_values < expected_quarters:
        print(f"Warning: Fewer market cap values ({num_values}) than quarters ({expected_quarters}). Padding with NaN.")
        market_cap_values = [None] * (expected_quarters - num_values) + market_cap_values
        quarters = pd.date_range(end=last_quarter, periods=expected_quarters, freq='Q')

    # Create DataFrame
    data = pd.DataFrame({
        'date': quarters,
        'market_cap': market_cap_values
    })

    # Filter by date range
    data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    
    # Set date as index
    data.set_index('date', inplace=True)
    
    return data

# Main script
ticker = "DEZ:DE"
start_date = "2009-07-01"  # Adjusted to cover 16 quarters from Q3 2021
end_date = "2025-07-22"    # Ends after Q2 2025 (June 30, 2025)

# Fetch data from the database
stock_data = get_stock_data(ticker, start_date, end_date, last_quarter_date="2025-06-30")

# Prepare the data (use market_cap as the target variable)
data = stock_data[['market_cap']].copy()

# Set frequency to quarterly and forward fill missing values
data = data.asfreq('Q', method='ffill')

# Print head and tail of the data
print(data.head())
print(data.tail())

# Set up PyCaret time series experiment
#exp_name = setup(data=data, fh=4, session_id=123, numeric_imputation="ffill")  # fh=4 for 4 quarters
exp_name = setup(data=data, fh=2, session_id=123)  # fh=2 for 4 quarters

# Check statistics
exp_name.check_stats()

# Plot decomposition
plot_model(plot="decomp_classical")

# Compare models and select the best
best = compare_models()

# Plot forecasts, residuals, and in-sample predictions
plot_model(best, plot='forecast', data_kwargs={'fh': 4})  # Forecast 8 quarters
plot_model(best, plot='residuals')
plot_model(best, plot='insample')

# Finalize the best model
final_best = finalize_model(best)

# Save the model
save_model(final_best, 'final_best_model_DEZ')
