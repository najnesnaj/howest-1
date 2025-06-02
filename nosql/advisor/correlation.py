"""
This script calculates financial correlations and stores the results in a PostgreSQL database.

Modules:
    - psycopg2: For connecting to and interacting with a PostgreSQL database.
    - pandas: For handling and processing tabular data.
    - dotenv: For loading environment variables from a .env file.
    - os: For accessing environment variables.
    - numpy: For numerical operations.

Environment Variables:
    - POSTGRES_USER: PostgreSQL username (default: 'myuser').
    - POSTGRES_PASSWORD: PostgreSQL password (default: 'mypassword').
    - POSTGRES_DB: PostgreSQL database name (default: 'mydatabase').
    - POSTGRES_HOST: PostgreSQL host (default: 'localhost').
    - POSTGRES_PORT: PostgreSQL port (default: '5432').

Functions:
    - fetch_data(query): Fetches data from the PostgreSQL database based on the provided SQL query.
    - calculate_codes(data): Calculates codes based on percentage changes in the data.
        - Code 1: Positive change.
        - Code 0: Small negative or no change (-7% to 0%).
        - Code -1: Large negative change (less than -7%).
    - calculate_correlation(revenue, market_cap, roic): Calculates the correlation between revenue, market cap, and ROIC codes.
        - Correlation is incremented when all three codes are either 1 or -1.
    - calculate_consecutive_ones(data): Calculates the number of periods with more than two consecutive code 1 values.
    - main(): Main function that fetches data, processes it, and stores the results in a PostgreSQL table.

Database Schema:
    - Table: company_correlation
        - symbol (TEXT): Primary key representing the company symbol.
        - revenue (INTEGER[]): Array of calculated revenue codes.
        - market_cap (INTEGER[]): Array of calculated market cap codes.
        - roic (INTEGER[]): Array of calculated ROIC codes.
        - correlation (FLOAT): Correlation value between revenue, market cap, and ROIC.
        - consecutive_ones (INT): Number of periods with more than two consecutive code 1 values.

Usage:
    - Ensure the required environment variables are set in a .env file.
    - Run the script to calculate financial correlations and store the results in the database.
"""
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
import numpy as np

# Load environment variables
load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER', 'myuser')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'mypassword')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'mydatabase')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# Function to fetch data from PostgreSQL
def fetch_data(query):
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to calculate codes based on percentage changes
def calculate_codes(data):
    codes = []
    for i in range(len(data)):
        if i == 0:  # No previous value for the first item
            code = -1
        else:
            if data[i - 1] == 0:
                change = 0
            else:
                change = (data[i] - data[i - 1]) / data[i - 1] * 100  # Percentage change
            if data[i] < 0:
                change = -100  # Negative change
            if change > 0:
                code = 1  # Positive change
            elif -7 <= change <= 0:
                code = 0  # Small negative or no change
            elif change < -7:
                code = -1  # Large negative change
        codes.append(code)
    return codes

# Function to calculate correlation between revenue, market_cap, and roic
def calculate_correlation_all(revenue, market_cap, roic):
    correlation = 0
    for r, m, ro in zip(revenue, market_cap, roic):
        if r == 1 and ro == 1 and m == 1:
            correlation += 1
        elif r == -1 and ro == -1 and m == -1:
            correlation += 1
        elif r == 0 and ro == 0 and m == 0:
            correlation += 1    
    return correlation / len(revenue) if revenue else 0

# Function to calculate correlation between revenue and roic
def calculate_correlation_rev_roic(revenue, roic):
    correlation = 0
    for r, ro in zip(revenue, roic):
        if r == 1 and ro == 1:
            correlation += 1
        elif r == -1 and ro == -1:
            correlation += 1
        elif r == 0 and ro == 0:
            correlation += 1
    return correlation / len(revenue) if revenue else 0

# Function to calculate correlation between revenue and market_cap
def calculate_correlation_rev_cap(revenue, market_cap):
    correlation = 0
    for r, m in zip(revenue, market_cap):
        if r == 1 and m == 1:
            correlation += 1
        elif r == -1 and m == -1:
            correlation += 1
        elif r == 0 and m == 0:
            correlation += 1
    return correlation / len(revenue) if revenue else 0

# Function to calculate correlation between roic and market_cap
def calculate_correlation_roic_cap(roic, market_cap):
    correlation = 0
    for ro, m in zip(roic, market_cap):
        if ro == 1 and m == 1:
            correlation += 1
        elif ro == -1 and m == -1:
            correlation += 1
        elif ro == 0 and m == 0:
            correlation += 1
    return correlation / len(roic) if roic else 0

# Function to calculate consecutive periods of code 1
def calculate_consecutive_ones(data):
    max_consecutive = 0
    current_streak = 0
    for value in data:
        if value == 1:
            current_streak += 1
            if current_streak > 2:
                max_consecutive += 1
        else:
            current_streak = 0
    return max_consecutive

# Main function
def main():
    query = """
        SELECT 
            data->>'qfs_symbol_v2' AS symbol,
            data->'financials'->'quarterly'->'revenue' AS revenue,
            data->'financials'->'quarterly'->'market_cap' AS market_cap,
            data->'financials'->'quarterly'->'roic' AS roic
        FROM companies;
    """
    
    df = fetch_data(query)
    
    # Prepare the new table data
    results = []
    for _, row in df.iterrows():
        revenue = calculate_codes(row['revenue'])
        market_cap = calculate_codes(row['market_cap'])
        roic = calculate_codes(row['roic'])
        
        correlation_all = calculate_correlation_all(revenue, market_cap, roic)
        correlation_rev_roic = calculate_correlation_rev_roic(revenue, roic)
        correlation_rev_cap = calculate_correlation_rev_cap(revenue, market_cap)
        correlation_roic_cap = calculate_correlation_roic_cap(roic, market_cap)
        consecutive_ones = calculate_consecutive_ones(market_cap)
        
        results.append({
            'symbol': row['symbol'],
            'revenue': revenue,
            'market_cap': market_cap,
            'roic': roic,
            'correlation_all': correlation_all,
            'correlation_rev_roic': correlation_rev_roic,
            'correlation_rev_cap': correlation_rev_cap,
            'correlation_roic_cap': correlation_roic_cap,
            'consecutive_ones': consecutive_ones
        })
    
    # Create a new PostgreSQL table and insert the results
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    cursor = conn.cursor()
    
    # Create the new table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS company_correlation (
            symbol TEXT PRIMARY KEY,
            revenue INTEGER[],
            market_cap INTEGER[],
            roic INTEGER[],
            correlation_all FLOAT,
            correlation_rev_roic FLOAT,
            correlation_rev_cap FLOAT,
            correlation_roic_cap FLOAT,
            consecutive_ones INT
        );
    """)
    
    # Insert the results into the table
    for result in results:
        cursor.execute("""
            INSERT INTO company_correlation (
                symbol, revenue, market_cap, roic, correlation_all, correlation_rev_roic, correlation_rev_cap, correlation_roic_cap, consecutive_ones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol) DO UPDATE
            SET revenue = EXCLUDED.revenue,
                market_cap = EXCLUDED.market_cap,
                roic = EXCLUDED.roic,
                correlation_all = EXCLUDED.correlation_all,
                correlation_rev_roic = EXCLUDED.correlation_rev_roic,
                correlation_rev_cap = EXCLUDED.correlation_rev_cap,
                correlation_roic_cap = EXCLUDED.correlation_roic_cap,
                consecutive_ones = EXCLUDED.consecutive_ones;
        """, (
            result['symbol'],
            result['revenue'],
            result['market_cap'],
            result['roic'],
            result['correlation_all'],
            result['correlation_rev_roic'],
            result['correlation_rev_cap'],
            result['correlation_roic_cap'],
            result['consecutive_ones']
        ))
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
