from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import psycopg2
import os
import re
from typing import Optional, Tuple
import numpy as np
import tensorflow as tf

app = FastAPI()

# Read environment variables for database connection
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# Load the Keras model at startup for efficiency
MODEL = tf.keras.models.load_model('my_model.keras')

# Database query function
def fetch_data(query: str, params: Optional[Tuple] = None) -> pd.DataFrame:
    try:
        conn = psycopg2.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB
        )
        if params:
            df = pd.read_sql(query, conn, params=params)
        else:
            df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

# Endpoint: /pattern/{symbol}
@app.get("/pattern/{symbol}")
async def check_pattern(symbol: str):
    # Validate the symbol input
    if not symbol or not re.match(r'^[A-Za-z0-9:]+$', symbol):
        raise HTTPException(status_code=400, detail="Invalid symbol format. Use alphanumeric characters and colon only.")
    if len(symbol) > 50:
        raise HTTPException(status_code=400, detail="Symbol is too long.")

    # Query market_cap data
    query = """
    SELECT
        data->>'qfs_symbol_v2' AS symbol,
        COALESCE(data->'financials'->'quarterly'->'market_cap', '[]'::jsonb) AS market_cap
    FROM companies
    WHERE data->>'qfs_symbol_v2' = %s;
    """
    try:
        df = fetch_data(query, params=(symbol,))
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")

        # Extract market_cap data
        market_cap = df['market_cap'].iloc[0]
        if not isinstance(market_cap, list) or len(market_cap) != 70:
            raise HTTPException(status_code=400, detail=f"Invalid market_cap data for {symbol}. Expected 70 quarters.")

        # Preprocess data for the model
        input_data = np.array(market_cap, dtype=np.float32)
        input_data = input_data.reshape(1, -1)  # Reshape to (1, 70)

        # Run prediction
        prediction = MODEL.predict(input_data)
        # Assuming binary classification
        pattern_detected = bool(np.argmax(prediction[0]) if prediction.shape[-1] > 1 else prediction[0] > 0.5)

        return JSONResponse(content={
            "symbol": symbol,
            "pattern_detected": pattern_detected
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
