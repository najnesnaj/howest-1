"""
This script updates a PostgreSQL database with financial data for German companies
retrieved from the QuickFS API. It performs the following tasks:

1. Loads environment variables from a `.env` file to configure PostgreSQL connection details.
2. Connects to a PostgreSQL database using the `psycopg2` library.
3. Ensures the existence of a `companies` table with a JSONB column to store financial data.
4. Reads a list of German company symbols from a file named `german_companies`.
5. Fetches financial data for each company symbol using the QuickFS API.
6. Inserts the retrieved financial data into the `companies` table in the PostgreSQL database.

Dependencies:
- `dotenv` for loading environment variables.
- `psycopg2` for PostgreSQL database interaction.
- `quickfs` for accessing the QuickFS API.
- `json` for handling JSON data.

Environment Variables:
- `POSTGRES_USER`: PostgreSQL username (default: 'myuser').
- `POSTGRES_PASSWORD`: PostgreSQL password (default: 'mypassword').
- `POSTGRES_DB`: PostgreSQL database name (default: 'mydatabase').
- `POSTGRES_HOST`: PostgreSQL host (default: 'localhost').
- `POSTGRES_PORT`: PostgreSQL port (default: '5432').

Note:
- Ensure the `german_companies` file exists and contains a list of company symbols, one per line.
- Replace the QuickFS API key with a valid key before running the script.

"""
from quickfs import QuickFS
from dotenv import load_dotenv
import os
import json
import psycopg2

# Load environment variables from .env
load_dotenv()

# Retrieve the API key from the environment
QUICKFS_API_KEY = os.getenv('QUICKFS_API_KEY')

if not QUICKFS_API_KEY:
    raise ValueError("QUICKFS_API_KEY is not set in the .env file")

# Initialize the QuickFS client with the API key
client = QuickFS(QUICKFS_API_KEY)

# PostgreSQL connection details
POSTGRES_USER = os.getenv('POSTGRES_USER', 'myuser')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'mypassword')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'mydatabase')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')


def main():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            data JSONB
        )
    ''')
    conn.commit()

    # Open the file containing the list of German companies
    with open('american_companies', 'r') as file:
        german_companies = file.read().splitlines()

    for symbol in german_companies:
        euronext = client.get_data_full(symbol=symbol)
        # Insert the dictionary into the collection
        cur.execute('''
            INSERT INTO companies (data) VALUES (%s)''', [json.dumps(euronext)])
        conn.commit()
        print(f"Inserted data for {symbol}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
