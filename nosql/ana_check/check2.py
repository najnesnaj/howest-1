import requests
import psycopg2
from urllib.parse import quote

# Configuration
DATA_ENDPOINT = "http://localhost:8001/data"
PATTERN_ENDPOINT = "http://localhost:8002/pattern/{}"
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

# Initialize PostgreSQL table
def init_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS symbol_patterns2 (
                symbol VARCHAR(50) PRIMARY KEY,
                patternmatch BOOLEAN
            );
        """)
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        cursor.close()
        conn.close()

# Fetch all symbols from data endpoint
def fetch_symbols():
    try:
        response = requests.get(DATA_ENDPOINT)
        response.raise_for_status()
        data = response.json()
        return list(data.keys())
    except requests.RequestException as e:
        print(f"Error fetching symbols: {e}")
        return []

# Check pattern for a single symbol
def check_pattern(symbol):
    try:
        # URL-encode the symbol to handle special characters
        encoded_symbol = quote(symbol)
        response = requests.get(PATTERN_ENDPOINT.format(encoded_symbol))
        response.raise_for_status()
        pattern_data = response.json()
        # Extract pattern_detected as boolean
        return pattern_data.get("pattern_detected", False)
    except requests.RequestException as e:
        print(f"Error checking pattern for {symbol}: {e}")
        return False

# Store result in PostgreSQL
def store_result(symbol, patternmatch):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Upsert the patternmatch value
        cursor.execute("""
            INSERT INTO symbol_patterns2 (symbol, patternmatch)
            VALUES (%s, %s)
            ON CONFLICT (symbol)
            DO UPDATE SET patternmatch = EXCLUDED.patternmatch;
        """, (symbol, patternmatch))
        conn.commit()
    except Exception as e:
        print(f"Error storing result for {symbol}: {e}")
    finally:
        cursor.close()
        conn.close()

def main():
    # Initialize database
    init_db()
    
    # Fetch all symbols
    symbols = fetch_symbols()
    print(f"Found {len(symbols)} symbols to process.")
    
    # Process each symbol
    for symbol in symbols:
        print(f"Processing {symbol}...")
        patternmatch = check_pattern(symbol)
        store_result(symbol, patternmatch)
        print(f"Stored result for {symbol}")

if __name__ == "__main__":
    main()
