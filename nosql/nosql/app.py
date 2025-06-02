"""
This script is a Streamlit application that visualizes financial data of companies 
retrieved from a PostgreSQL database. It includes functionalities for data fetching, 
categorization, filtering, and visualization.
Modules and Libraries:
- `streamlit`: Used for creating the web-based user interface.
- `psycopg2`: For connecting to and querying the PostgreSQL database.
- `pandas`: For data manipulation and analysis.
- `dotenv`: For loading environment variables from a `.env` file.
- `os`: For accessing environment variables.
- `json`: For handling JSON data.
- `plotly.express`: For creating interactive visualizations.
- `multiprocessing`: For parallel processing of data.
- `numpy`: For numerical operations.
Features:
1. **Environment Variable Loading**:
    - Loads database credentials and configurations from a `.env` file.
2. **Database Querying**:
    - Fetches financial data (revenue, market cap, ROIC, and sector) from a PostgreSQL database.
3. **Data Categorization**:
    - Categorizes companies into clusters based on patterns in their financial data:
      - Cluster 1: Steady growth
      - Cluster 2: Cyclical patterns
      - Cluster 3: Declining
4. **Data Filtering**:
    - Filters companies based on user-defined thresholds for market cap and ROIC.
5. **Visualization**:
    - Displays bar charts for revenue, market cap, and ROIC using Plotly.
    - Colors individual bars based on percentage changes:
      - Green: Positive change
      - Orange: Small negative or no change
      - Red: Large negative change
6. **Parallel Processing**:
    - Utilizes multiprocessing to improve performance when fetching data.
7. **Streamlit UI**:
    - Provides an interactive interface for users to input thresholds and view visualizations.
Functions:
- `fetch_data(query)`: Executes a SQL query and returns the result as a Pandas DataFrame.
- `categorize_company(data)`: Categorizes companies based on patterns in their financial data.
- `get_color(category)`: Returns a color based on the company category.
- `get_item_color(data)`: Determines bar colors based on percentage changes in data.
- `get_data()`: Fetches, processes, and filters data from the database.

"""

import streamlit as st
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
import json
import plotly.express as px  # Import plotly.express
from multiprocessing import Pool, cpu_count  # Import multiprocessing
import numpy as np  # Import numpy for numerical operations

# Minimum market cap threshold
# only companies with a market cap above this value will be considered
min_market_cap = 500_000_000  # 500 million


    
#this is a github vscode test
# Load environment variables
load_dotenv() # Make sure we have our .env values

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

# Function to categorize companies based on pattern
def categorize_company(data):
    avg_change = np.mean(np.diff(data))
    if avg_change > 0:
        return 'Cluster 1: Steady growth'
    elif avg_change < 0:
        return 'Cluster 3: Declining'
    else:
        return 'Cluster 2: Cyclical patterns'

# Function to get color based on category
def get_color(category):
    if category == 'Cluster 1: Steady growth':
        return 'green'
    elif category == 'Cluster 2: Cyclical patterns':
        return 'orange'
    elif category == 'Cluster 3: Declining':
        return 'red'
    else:
        return 'blue'

# Function to get color for each value based on percentage change
def get_item_color(data):
    colors = []
    for i in range(len(data)):
        if i == 0:  # No previous value for the first item
            colors.append('blue')  # Default color for the first item
        else:
            if data[i - 1] == 0:
                change = 0
            else:
                change = (data[i] - data[i - 1]) / data[i - 1] * 100  # Percentage change
            if data[i] < 0:
                change = -100  # Negative change
#the percentage of 7 is used because a drop below is a sell signal (red = sell)
            if change > 0:
                colors.append('green')  # Positive change
            elif -7 <= change <= 0:
                colors.append('orange')  # Small negative or no change
            elif change < -7:
                colors.append('red')  # Large negative change
        
            #if data[i] < 0:  # Negative values should always be red
            #    colors.append('red')
    return colors

def get_data():
    query = """
        SELECT 
            data->>'qfs_symbol_v2' AS symbol,
            data->'financials'->'quarterly'->'revenue' AS revenue,
            data->'financials'->'quarterly'->'market_cap' AS market_cap,
            data->'financials'->'quarterly'->'roic' AS roic,
            data->'metadata'->>'sector' AS sector
        FROM companies;
    """
    #TODO REMOVE BMW.DE
    # Split the query into chunks for parallel processing
    queries = [query] * cpu_count()  # This is a simplified example, you may need to split the query based on your data
    
    with Pool(cpu_count()) as pool:
        results = pool.map(fetch_data, queries)
    
    df = pd.concat(results, ignore_index=True)
    
    # Filter companies based on minimum market cap
    df = df[df['market_cap'].apply(lambda x: np.mean(x) > min_market_cap)]
    
    # Add category columns based on patterns
    df['revenue_category'] = df['revenue'].apply(categorize_company)
    df['market_cap_category'] = df['market_cap'].apply(categorize_company)
    df['roic_category'] = df['roic'].apply(categorize_company)
    
    print(df.head())
    return df[['symbol', 'revenue', 'market_cap', 'roic', 'sector', 'revenue_category', 'market_cap_category', 'roic_category']]

# Streamlit UI
st.title("Company Financial Data")
st.write("Displaying data from PostgreSQL")

# Add input widgets for minimum thresholds
min_market_cap = st.number_input("Minimum Market Cap (in millions)", value=500.0, step=10.0) * 1_000_000
min_roic = st.number_input("Minimum ROIC (in percentage)", value=0.0, step=1.0)

df = get_data()

# Filter companies based on user-defined thresholds
df = df[
    df['market_cap'].apply(lambda x: np.mean(x[-5:]) > min_market_cap) &  # Last 5 values of market_cap
    df['roic'].apply(lambda x: np.mean(x[-5:]) > min_roic)  # Last 5 values of roic
]

# Add category columns based on patterns
df['revenue_category'] = df['revenue'].apply(categorize_company)
df['market_cap_category'] = df['market_cap'].apply(categorize_company)
df['roic_category'] = df['roic'].apply(categorize_company)

# Create a column layout with specified widths
col1, col2, col3 = st.columns([1, 1, 1])

# Display the plots
for index, row in df.iterrows():
    with col1:
        revenue_colors = get_item_color(row['revenue'])
        fig_revenue = px.bar(
            x=[f"Q{i+1}" for i in range(len(row['revenue']))],
            y=row['revenue'],
            title=f"{row['symbol']} Revenue"
        )
        fig_revenue.update_traces(marker_color=revenue_colors)  # Use marker_color for individual bar colors
        fig_revenue.update_layout(height=140, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_revenue, use_container_width=True, key=f"plot_revenue_{index}")
    
    with col2:
        market_cap_colors = get_item_color(row['market_cap'])
        fig_market_cap = px.bar(
            x=[f"Q{i+1}" for i in range(len(row['market_cap']))],
            y=row['market_cap'],
            title=f"{row['symbol']} Market Cap"
        )
        fig_market_cap.update_traces(marker_color=market_cap_colors)  # Use marker_color for individual bar colors
        fig_market_cap.update_layout(height=140, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_market_cap, use_container_width=True, key=f"plot_market_cap_{index}")
    
    with col3:
        roic_colors = get_item_color(row['roic'])
        fig_roic = px.bar(
            x=[f"Q{i+1}" for i in range(len(row['roic']))],
            y=row['roic'],
            title=f"{row['symbol']} ROIC"
        )
        fig_roic.update_traces(marker_color=roic_colors)  # Use marker_color for individual bar colors
        fig_roic.update_layout(height=140, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_roic, use_container_width=True, key=f"plot_roic_{index}")



