import psycopg2
import os
import json

# Database connection parameters
POSTGRES_USER = os.getenv('POSTGRES_USER', 'myuser')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'mypassword')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'mydatabase')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# Synthetic data for symbol LLM1
data_array = [0.65, 0.75, 0.69, 0.86, 0.78, 0.73, 0.73, 0.81, 0.78, 0.83, 0.81, 0.78, 0.73, 0.68, 0.71, 0.75, 0.70, 0.60, 0.64, 0.63, 0.54, 0.57, 0.55, 0.48, 0.54, 0.54, 0.56, 0.56, 0.46, 0.49, 0.57, 0.59, 0.62, 0.80, 0.67, 0.72, 0.74, 0.75, 0.72, 0.79, 0.74, 0.77, 0.77, 0.80, 0.88, 0.70, 0.81, 0.69, 0.72, 0.77, 0.70, 0.62, 0.61, 0.65, 0.56, 0.58, 0.56, 0.51, 0.63, 0.55, 0.42, 0.52, 0.49, 0.57, 0.50, 0.55, 0.79, 0.64, 0.57, 0.64 ]



# Structure the data in JSON format
json_data = {
    "qfs_symbol_v2": "generated-by-script-by-LLM",
    "financials": {
        "quarterly": {
            "market_cap": data_array
        }
    }
}

# Function to insert data into PostgreSQL
def insert_data(json_data):
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        cursor = conn.cursor()

        # SQL query to insert data
        insert_query = """
            INSERT INTO companies (data)
            VALUES (%s);
        """
        # Convert the dictionary to a JSON string
        json_data_str = json.dumps(json_data)
        cursor.execute(insert_query, (json_data_str,))

        # Commit the transaction
        conn.commit()
        print("Data inserted successfully for symbol LLM1")

    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

# Execute the insertion
if __name__ == "__main__":
    insert_data(json_data)
