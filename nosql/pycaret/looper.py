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

# Database connection function
def get_db_connection():
    try:
        conn = psycopg2.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB
        )
        return conn
    except Exception as e:
        raise Exception(f"Database connection error: {str(e)}")

# Fetch data from the database
def fetch_data(query: str, params: Optional[Tuple] = None) -> pd.DataFrame:
    conn = get_db_connection()
    try:
        if params:
            df = pd.read_sql(query, conn, params=params)
        else:
            df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        conn.close()
        raise Exception(f"Database query error: {str(e)}")

# Create symbomodel table
def create_symbomodel_table():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS symbomodel (
                symbol TEXT PRIMARY KEY,
                model TEXT
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Table 'symbomodel' created or already exists.")
    except Exception as e:
        conn.close()
        raise Exception(f"Error creating symbomodel table: {str(e)}")

# Insert or update symbol and model in symbomodel table
def insert_model_result(symbol: str, model: str):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO symbomodel (symbol, model)
            VALUES (%s, %s)
            ON CONFLICT (symbol) DO UPDATE
            SET model = EXCLUDED.model;
        """, (symbol, model))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Stored model for {symbol}: {model}")
    except Exception as e:
        conn.close()
        raise Exception(f"Error inserting model result for {symbol}: {str(e)}")

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
        print(f"Warning: No market cap data found for symbol {symbol}. Skipping.")
        return None

    # Get market_cap values
    market_cap_values = df['market_cap'].iloc[0]
    
    # Debug: Print the market_cap data
    print(f"\n{symbol} - Market cap values:", market_cap_values)
    print(f"{symbol} - Number of market cap values:", len(market_cap_values))

    # Generate quarterly dates ending at last_quarter_date
    last_quarter = pd.to_datetime(last_quarter_date)  # e.g., 2025-06-30 (Q2 2025)
    num_values = len(market_cap_values)
    quarters = pd.date_range(end=last_quarter, periods=num_values, freq='Q')
    
    # Check if there are enough values for the date range
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    expected_quarters = len(pd.date_range(start=start_date, end=end_date, freq='Q'))
    if num_values > expected_quarters:
        print(f"Warning: More market cap values ({num_values}) than quarters ({expected_quarters}) for {symbol}. Truncating to match date range.")
        market_cap_values = market_cap_values[-expected_quarters:]  # Keep latest values
        quarters = quarters[-expected_quarters:]
    elif num_values < expected_quarters:
        print(f"Warning: Fewer market cap values ({num_values}) than quarters ({expected_quarters}) for {symbol}. Padding with NaN.")
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

# Function to find and print the best model for a symbol
def find_best_model(symbol: str, data: pd.DataFrame):
    print(f"\nProcessing time series for {symbol}...")
    
    # Set up PyCaret time series experiment
    try:
        #exp_name = setup(data=data, fh=4, session_id=123, numeric_imputation="ffill", verbose=False)
        exp_name = setup(data=data, fh=4, session_id=123, verbose=False)
        
        # Compare models and select the best
        best_model = compare_models()
        
        # Get model details
        model_name = best_model.__class__.__name__
        metrics = pull()  # Get performance metrics from compare_models
        
        # Print best model and metrics
        print(f"Best model for {symbol}: {model_name}")
        print(f"Performance metrics for {symbol}:")
        print(metrics)
        
        return model_name
    except Exception as e:
        print(f"Error processing {symbol}: {str(e)}. Skipping.")
        return None

# Fetch all unique symbols from the companies table
def get_all_symbols() -> list:
    query = """
    SELECT DISTINCT data->>'qfs_symbol_v2' AS symbol
    FROM companies
    WHERE data->>'qfs_symbol_v2' IS NOT NULL;
    """
    df = fetch_data(query)
    return df['symbol'].tolist()

# Main script
start_date = "2011-07-01"  # Adjusted to cover typical data range (e.g., 16 quarters)
end_date = "2025-07-22"    # Ends after Q2 2025 (June 30, 2025)
last_quarter_date = "2025-06-30"

# Create symbomodel table
create_symbomodel_table()

# Get all symbols
symbols = get_all_symbols()
print(f"Found {len(symbols)} symbols: {symbols}")

# Process each symbol
for symbol in symbols:
    # Fetch data
    stock_data = get_stock_data(symbol, start_date, end_date, last_quarter_date=last_quarter_date)
    
    if stock_data is None:
        continue
    
    # Prepare the data (use market_cap as the target variable)
    data = stock_data[['market_cap']].copy()
    
    # Set frequency to quarterly and forward fill missing values
    data = data.asfreq('Q', method='ffill')
    
    # Print head and tail of the data
    print(f"\n{symbol} - Data head:")
    print(data.head())
    print(f"{symbol} - Data tail:")
    print(data.tail())
    
    # Find and store the best model
    best_model_name = find_best_model(symbol, data)
    
    if best_model_name:
        # Store result in symbomodel table
        insert_model_result(symbol, best_model_name)

# Verify results by querying symbomodel table
print("\nContents of symbomodel table:")
query = "SELECT symbol, model FROM symbomodel ORDER BY symbol;"
results = fetch_data(query)
print(results)
