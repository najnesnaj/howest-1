import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
import numpy as np
from dtaidistance import dtw
import json
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER', 'myuser')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'mypassword')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'mydatabase')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# Create SQLAlchemy engine
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)

# Database connection function for psycopg2 (used for non-pandas operations)
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

# Fetch data from database using SQLAlchemy
def fetch_data(query, params=None):
    try:
        df = pd.read_sql(query, engine, params=params)
        return df
    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")

# Create distance2DEZ table
def create_distance_table():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS distance2DEZ (
            symbol VARCHAR(50) PRIMARY KEY,
            distance FLOAT
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error creating distance2DEZ table: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Insert or update distances in distance2DEZ table
def store_distances(distances):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO distance2DEZ (symbol, distance)
        VALUES (%s, %s)
        ON CONFLICT (symbol) DO UPDATE
        SET distance = EXCLUDED.distance;
        """
        for symbol, distance in distances.items():
            cursor.execute(insert_query, (symbol, float(distance)))  # Ensure distance is float
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error storing distances: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Fetch all unique symbols
def get_all_symbols() -> list:
    query = """
    SELECT DISTINCT data->>'qfs_symbol_v2' AS symbol
    FROM companies
    WHERE data->>'qfs_symbol_v2' IS NOT NULL;
    """
    df = fetch_data(query)
    return df['symbol'].tolist()

# Fetch stock data for a specific symbol
def get_stock_data(symbol: str, start_date: str = '2008-01-01', end_date: str = '2025-06-30') -> pd.DataFrame:
    query = """
    SELECT
        data->>'qfs_symbol_v2' AS symbol,
        COALESCE(data->'financials'->'quarterly'->'market_cap', '[]'::jsonb) AS market_cap
    FROM companies
    WHERE data->>'qfs_symbol_v2' = %s;
    """
    df = fetch_data(query, (symbol,))
    return df

# Main function to calculate DTW distances and store in database
def calculate_dtw_to_deutz(symbol='DEZ:DE', n_quarters=65):
    # Step 1: Fetch Deutz market cap data
    deutz_df = get_stock_data(symbol)
    if deutz_df.empty:
        raise ValueError(f"No data found for symbol {symbol}")
    
    # Parse market cap data (handle both JSON string and pre-parsed list)
    market_cap_raw = deutz_df['market_cap'].iloc[0]
    try:
        if isinstance(market_cap_raw, str):
            deutz_market_cap = np.array(json.loads(market_cap_raw), dtype=float)
        elif isinstance(market_cap_raw, list):
            deutz_market_cap = np.array(market_cap_raw, dtype=float)
        else:
            raise ValueError(f"Unexpected market_cap type for {symbol}: {type(market_cap_raw)}")
    except Exception as e:
        raise ValueError(f"Error parsing market cap for {symbol}: {str(e)}")
    
    # Truncate to last n_quarters (65 for Deutz)
    if len(deutz_market_cap) < n_quarters:
        raise ValueError(f"Deutz market cap data has {len(deutz_market_cap)} quarters, need at least {n_quarters}")
    deutz_market_cap = deutz_market_cap[-n_quarters:]  # Take last 65 quarters

    # Step 2: Fetch all symbols
    all_symbols = get_all_symbols()
    all_symbols = [s for s in all_symbols if s != symbol]  # Exclude Deutz
    print ("fetched all symbols")
    # Step 3: Calculate DTW distances
    distances = {}
    for sym in all_symbols:
        df = get_stock_data(sym)
        print ("symbol :", sym)
        if df.empty:
            print ("empty dataframe")
            continue
        try:
            market_cap_raw = df['market_cap'].iloc[0]
            if isinstance(market_cap_raw, str):
                market_cap = np.array(json.loads(market_cap_raw), dtype=float)
            elif isinstance(market_cap_raw, list):
                market_cap = np.array(market_cap_raw, dtype=float)
            else:
                raise ValueError(f"Unexpected market_cap type for {sym}: {type(market_cap_raw)}")
            # Ensure enough data and truncate to last n_quarters
            if len(market_cap) < n_quarters:
                continue
            market_cap = market_cap[-n_quarters:]  # Take last 65 quarters
            # Standardize data to make DTW scale-invariant
            market_cap = (market_cap - np.mean(market_cap)) / np.std(market_cap) if np.std(market_cap) != 0 else market_cap
            deutz_standardized = (deutz_market_cap - np.mean(deutz_market_cap)) / np.std(deutz_market_cap) if np.std(deutz_market_cap) != 0 else deutz_market_cap
            # Calculate DTW distance
            d = dtw.distance_fast(deutz_standardized, market_cap)
            distances[sym] = d
        except Exception as e:
            print(f"Error processing {sym}: {str(e)}")
            continue

    # Step 4: Create distance2DEZ table
    create_distance_table()

    # Step 5: Store distances in database
    store_distances(distances)

# Execute
if __name__ == "__main__":
    try:
        calculate_dtw_to_deutz('DEZ:DE', n_quarters=65)
    except Exception as e:
        print(f"Error: {str(e)}")
