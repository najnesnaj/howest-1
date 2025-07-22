import psycopg2
import pandas as pd
from typing import Optional, Tuple
from pycaret.time_series import *
from dotenv import load_dotenv
import os
import json

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
def get_stock_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    query = """
    SELECT
        data->>'qfs_symbol_v2' AS symbol,
        COALESCE(data->'financials'->'quarterly'->'market_cap', '[]'::jsonb) AS market_cap
    FROM companies
    WHERE data->>'qfs_symbol_v2' = %s;
    """
    params = (symbol,)
    df = fetch_data(query, params)

    # Extract market_cap data from JSONB array
    if df.empty or not df['market_cap'].iloc[0]:
        raise ValueError(f"No market cap data found for symbol {symbol}")

    # Parse the JSONB market_cap array
    market_cap_data = json.loads(df['market_cap'].iloc[0])
    
    # Convert to DataFrame
    data = pd.DataFrame(market_cap_data)
    
    # Ensure 'date' and 'value' columns exist
    if 'date' not in data.columns or 'value' not in data.columns:
        raise ValueError("Market cap data must contain 'date' and 'value' fields")

    # Convert date to datetime and filter by date range
    data['date'] = pd.to_datetime(data['date'])
    data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
    
    # Select only date and value, rename value to market_cap
    data = data[['date', 'value']].rename(columns={'value': 'market_cap'})
    
    # Set date as index
    data.set_index('date', inplace=True)
    
    return data

# Main script
ticker = "DEZ:DE"
start_date = "2000-01-01"
end_date = "2025-07-22"

# Fetch data from the database
stock_data = get_stock_data(ticker, start_date, end_date)

# Prepare the data (use market_cap as the target variable)
data = stock_data[['market_cap']].copy()

# Set frequency to quarterly and forward fill missing values
data = data.asfreq('Q', method='ffill')

# Print head and tail of the data
print(data.head())
print(data.tail())

# Set up PyCaret time series experiment
exp_name = setup(data=data, fh=4, session_id=123, numeric_imputation="ffill")  # fh=4 for 4 quarters

# Check statistics
exp_name.check_stats()

# Plot decomposition
plot_model(plot="decomp_classical")

# Compare models and select the best
best = compare_models()

# Plot forecasts, residuals, and in-sample predictions
plot_model(best, plot='forecast', data_kwargs={'fh': 8})  # Forecast 8 quarters
plot_model(best, plot='residuals')
plot_model(best, plot='insample')

# Finalize the best model
final_best = finalize_model(best)

# Save the model
save_model(final_best, 'final_best_model_DEZ')
