import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
import numpy as np
from dtaidistance import dtw
import json

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

# Fetch data from database
def fetch_data(query, params=None):
    conn = get_db_connection()
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    finally:
        conn.close()

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
            cursor.execute(insert_query, (symbol, distance))
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
def calculate_dtw_to_deutz(symbol='DEZ:DE'):
    # Step 1: Fetch Deutz market cap data
    deutz_df = get_stock_data(symbol)
    if deutz_df.empty:
        raise ValueError(f"No data found for symbol {symbol}")
    
    # Parse market cap JSONB array
    try:
        deutz_market_cap = np.array(json.loads(deutz_df['market_cap'].iloc[0]), dtype=float)
    except Exception as e:
        raise ValueError(f"Error parsing market cap for {symbol}: {str(e)}")
    
    # Check if data has 70 quarters
    if len(deutz_market_cap) != 70:
        print(f"Warning: Deutz market cap data has {len(deutz_market_cap)} quarters, expected 70")

    # Step 2: Fetch all symbols
    all_symbols = get_all_symbols()
    all_symbols = [s for s in all_symbols if s != symbol]  # Exclude Deutz

    # Step 3: Calculate DTW distances
    distances = {}
    for sym in all_symbols:
        df = get_stock_data(sym)
        if df.empty:
            continue
        try:
            market_cap = np.array(json.loads(df['market_cap'].iloc[0]), dtype=float)
            # Ensure same length as Deutz data (70 quarters)
            if len(market_cap) != len(deutz_market_cap):
                continue
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
        calculate_dtw_to_deutz('DEZ:DE')
    except Exception as e:
        print(f"Error: {str(e)}")
