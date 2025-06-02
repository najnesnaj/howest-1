
"""
This script provides a Streamlit web application for querying JSON data stored in a PostgreSQL database.
It allows users to dynamically select fields from the JSON schema and execute queries to retrieve the data.
Modules:
    - streamlit: For creating the web application interface.
    - psycopg2: For connecting to and querying the PostgreSQL database.
    - pandas: For handling and displaying query results in a DataFrame.
    - dotenv: For loading environment variables from a .env file.
    - os: For accessing environment variables.
Functions:
    - get_json_schema(): Fetches the JSON schema from the PostgreSQL database and caches it to avoid repeated queries.
    - run_query(selected_fields): Executes a query based on user-selected fields and returns the results as a DataFrame.
    - main(): The main function that sets up the Streamlit interface, allowing users to select fields and run queries.
Environment Variables:
    - POSTGRES_USER: The PostgreSQL username.
    - POSTGRES_PASSWORD: The PostgreSQL password.
    - POSTGRES_DB: The PostgreSQL database name.
    - POSTGRES_HOST: The PostgreSQL host.
    - POSTGRES_PORT: The PostgreSQL port.
Usage:
    Run the script to start the Streamlit web application. Users can select fields from the JSON schema and execute queries to view the results.
"""
import streamlit as st
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os


load_dotenv() # Make sure we have our .env values

POSTGRES_USER = os.getenv('POSTGRES_USER', 'myuser')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'mypassword')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'mydatabase')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)

# Fetch JSON schema from PostgreSQL
@st.cache_data  # Cache the schema to avoid repeated queries
def get_json_schema():
    with conn.cursor() as cur:
        cur.execute("""
            WITH RECURSIVE json_keys AS (
                SELECT key, data->key AS value, jsonb_typeof(data->key) AS value_type, key AS path
                FROM companies, jsonb_object_keys(data) AS key
                UNION ALL
                SELECT k.key, v.value->k.key, jsonb_typeof(v.value->k.key), v.path || '->' || k.key
                FROM json_keys v, jsonb_object_keys(v.value) AS k(key)
                WHERE jsonb_typeof(v.value) = 'object'
            )
            SELECT DISTINCT path, value_type
            FROM json_keys
            WHERE value_type IN ('string', 'number', 'boolean', 'array')
            ORDER BY path;
        """)
        schema = [{"path": row[0], "type": row[1]} for row in cur.fetchall()]
    conn.close()
    return schema

# Execute user-selected query
def run_query(selected_fields):
    if not selected_fields:
        return None
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    select_clause = ", ".join([f"data->{'->'.join([f'\'{part}\'' for part in field.split('->')])} AS {field.replace('->', '_')}" for field in selected_fields])
    query = f"SELECT {select_clause} FROM companies;"
    print(query)

    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
        colnames = [field.replace('->', '_') for field in selected_fields]
        df = pd.DataFrame(results, columns=colnames)
    conn.close()
    return df

# Streamlit UI
def main():
    st.title("JSON Query Builder")

    # Get schema
    schema = get_json_schema()
    
    # Display schema and let user select fields
    st.subheader("Select Fields to Query")
    selected_fields = []
    for index, field in enumerate(schema):
        if st.checkbox(f"{field['path']} ({field['type']})", key=f"{field['path']}_{index}"):
            selected_fields.append(field['path'])

    # Run query button
    if st.button("Run Query"):
        if selected_fields:
            with st.spinner("Running query..."):
                results = run_query(selected_fields)
                if results is not None:
                    st.subheader("Query Results")
                    st.dataframe(results)
        else:
            st.warning("Please select at least one field.")

if __name__ == "__main__":
    main()