"""
This module implements a FastAPI application for visualizing and analyzing financial data 
stored in a PostgreSQL database. It provides endpoints for rendering HTML pages, fetching 
and filtering data, and generating visualizations using Plotly.
Modules and Libraries:
- fastapi: Framework for building APIs.
- psycopg2: PostgreSQL database adapter for Python.
- pandas: Data manipulation and analysis library.
- dotenv: For loading environment variables from a .env file.
- numpy: Library for numerical computations.
- plotly: Library for creating interactive visualizations.
- uvicorn: ASGI server for running FastAPI applications.
Environment Variables:
- POSTGRES_USER: PostgreSQL username.
- POSTGRES_PASSWORD: PostgreSQL password.
- POSTGRES_DB: PostgreSQL database name.
- POSTGRES_HOST: PostgreSQL host address.
- POSTGRES_PORT: PostgreSQL port.
Functions:
- fetch_data(query): Executes a SQL query on the PostgreSQL database and returns the result as a pandas DataFrame.
- categorize_company(data): Categorizes companies based on the average change in their financial data.
- get_item_color(data): Determines the color for each value in a dataset based on percentage change.
- generate_plot(data, title): Generates a Plotly bar chart for the given data and returns it as an HTML string.
Endpoints:
- GET "/": Renders the main HTML page using Jinja2 templates.
- GET "/data": Fetches and filters financial data based on market capitalization and ROIC thresholds.
- GET "/plot/{symbol}": Generates a Plotly visualization for a specific company's financial metric.
Usage:
Run the application using the command `uvicorn fastapp:app --host 0.0.0.0 --port 8001`.

"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
import numpy as np
import plotly.express as px
import uvicorn
#from report import generate_report
import re
from typing import Optional, Tuple

# Load environment variables
load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER', 'myuser')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'mypassword')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'mydatabase')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
#print (POSTGRES_HOST)
# Initialize FastAPI app
app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Function to fetch data from PostgreSQL
#def fetch_data(query):
#    conn = psycopg2.connect(
#        dbname=POSTGRES_DB,
#        user=POSTGRES_USER,
#        password=POSTGRES_PASSWORD,
#        host=POSTGRES_HOST,
#        port=POSTGRES_PORT
#    )
#    df = pd.read_sql(query, conn)
#    conn.close()
#    return df

# Updated fetch_data function to support parameterized queries
def fetch_data(query: str, params: Optional[Tuple] = None) -> pd.DataFrame:
    try:
        conn = psycopg2.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB
        )
        # Use parameterized query if params are provided
        if params:
            df = pd.read_sql(query, conn, params=params)
        else:
            df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")




# Function to categorize companies based on pattern
def categorize_company(data):
    avg_change = np.mean(np.diff(data))
    if avg_change > 0:
        return 'Cluster 1: Steady growth'
    elif avg_change < 0:
        return 'Cluster 3: Declining'
    else:
        return 'Cluster 2: Cyclical patterns'

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
            if change > 0:
                colors.append('green')  # Positive change
            elif -7 <= change <= 0:
                colors.append('orange')  # Small negative or no change
            elif change < -7:
                colors.append('red')  # Large negative change
    return colors

# Function to generate a Plotly bar chart
def generate_plot(data, title):
    colors = get_item_color(data)  # Get colors for each bar
    fig = px.bar(
        x=[f"Q{i+1}" for i in range(len(data))],  # Labels for the x-axis
        y=data,  # Data for the y-axis
        title=title
    )
    # Update the bar colors
    fig.update_traces(marker_color=colors)
    return fig.to_html(full_html=False)

# Endpoint to render the main HTML page
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint to fetch and filter data
# changed this to COALESCE because entered synthetic datan only for market_cap, rest was left empty

#@app.get("/data")
#def get_data():
#    query = """
#    SELECT 
#        data->>'qfs_symbol_v2' AS symbol,
#        COALESCE(data->'financials'->'quarterly'->'revenue', '[]'::jsonb) AS revenue,
#        COALESCE(data->'financials'->'quarterly'->'market_cap', '[]'::jsonb) AS market_cap,
#        COALESCE(data->'financials'->'quarterly'->'roic', '[]'::jsonb) AS roic,
#        data->'metadata'->>'sector' AS sector
#    FROM companies;
#    """
#    df = fetch_data(query)
#    
#    df['revenue_category'] = df['revenue'].apply(categorize_company)
#    df['market_cap_category'] = df['market_cap'].apply(categorize_company)
#    df['roic_category'] = df['roic'].apply(categorize_company)
#    
#    # Ensure the 'symbol' column is unique
#    df = df.drop_duplicates(subset='symbol')
#
#    # Convert DataFrame to a dictionary with 'symbol' as the key
#    result = df.set_index('symbol').to_dict(orient="index")
#    
#    return JSONResponse(content=result)
#

# Existing endpoint (for reference)
@app.get("/data")
def get_data():
    query = """
    SELECT 
        data->>'qfs_symbol_v2' AS symbol,
        COALESCE(data->'financials'->'quarterly'->'revenue', '[]'::jsonb) AS revenue,
        COALESCE(data->'financials'->'quarterly'->'market_cap', '[]'::jsonb) AS market_cap,
        COALESCE(data->'financials'->'quarterly'->'roic', '[]'::jsonb) AS roic,
        data->'metadata'->>'sector' AS sector
    FROM companies;
    """
    df = fetch_data(query)
    
    df['revenue_category'] = df['revenue'].apply(categorize_company)
    df['market_cap_category'] = df['market_cap'].apply(categorize_company)
    df['roic_category'] = df['roic'].apply(categorize_company)

    df = df.drop_duplicates(subset='symbol')
    result = df.set_index('symbol').to_dict(orient="index")
    
    return JSONResponse(content=result)

@app.get("/data/{symbol}")
async def get_symbol_data(symbol: str):
    # Validate the symbol input to allow alphanumeric characters and colon
    if not symbol or not re.match(r'^[A-Za-z0-9:]+$', symbol):
        raise HTTPException(status_code=400, detail="Invalid symbol format. Use alphanumeric characters and colon only.")

    if len(symbol) > 50:
        raise HTTPException(status_code=400, detail="Symbol is too long.")

    # Use parameterized query to prevent SQL injection
    query = """
    SELECT
        data->>'qfs_symbol_v2' AS symbol,
        COALESCE(data->'financials'->'quarterly'->'market_cap', '[]'::jsonb) AS market_cap
    FROM companies
    WHERE data->>'qfs_symbol_v2' = %s;
    """
    try:
        # Call fetch_data with query and parameters
        df = fetch_data(query, (symbol,))  # Expects fetch_data to handle both arguments

        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")

        # Drop duplicates and convert to dictionary
        df = df.drop_duplicates(subset='symbol')
        result = df.set_index('symbol').to_dict(orient="index")

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



# New endpoint: /data/symbol/market_cap
@app.get("/data/symbol/market_cap")
def get_symbol_market_cap():
    query = """
    SELECT 
        data->>'qfs_symbol_v2' AS symbol,
        COALESCE(data->'financials'->'quarterly'->'market_cap', '[]'::jsonb) AS market_cap
    FROM companies;
    """
    df = fetch_data(query)
    
    df['market_cap_category'] = df['market_cap'].apply(categorize_company)
    df = df.drop_duplicates(subset='symbol')
    result = df.set_index('symbol').to_dict(orient="index")
    
    return JSONResponse(content=result)



# Endpoint to generate a plot for a specific company
@app.get("/plot/{symbol}")
def get_plot(symbol: str, metric: str):
    query = f"""
        SELECT 
            data->>'qfs_symbol_v2' AS symbol,
            data->'financials'->'quarterly'->'{metric}' AS metric
        FROM companies
        WHERE data->>'qfs_symbol_v2' = '{symbol}';
    """
    print(f"Executing query: {query}")  # Debugging log
    df = fetch_data(query)
    print(f"Query result: {df}")  # Debugging log
    
    if df.empty:
        return JSONResponse(content={"error": f"Data not found for symbol '{symbol}' and metric '{metric}'"}, status_code=404)
    
    # Ensure the metric data is parsed as a list
    data = df.iloc[0]['metric']
    if isinstance(data, str):
        import json
        data = json.loads(data)  # Convert JSON string to Python list
    
    if not data:
        return JSONResponse(content={"error": f"No data available for metric '{metric}'"}, status_code=404)
    
    plot_html = generate_plot(data, f"{symbol} {metric.capitalize()}")
    return HTMLResponse(content=plot_html)

#@app.get("/generate-report", response_class=FileResponse)
#def generate_pdf_report():
#    output_file = "financial_report.pdf"
#    generate_report(output_file)
#    return FileResponse(output_file, media_type="application/pdf", filename=output_file)
#    return FileResponse(
#        path=output_file,
#        media_type="application/pdf",
#        filename=output_file,
#        as_attachment=False
#    )
# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
