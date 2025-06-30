from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd
import numpy as np
import tensorflow as tf
import re
from typing import Optional, Tuple

# Load environment variables
load_dotenv()

# Initialize FastAPI app
#app = FastAPI()

# Read environment variables for database connection
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# Load the Keras model at startup
MODEL = tf.keras.models.load_model('model.keras')

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
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Process market cap data to ensure correct shape
def process_market_cap_data(market_cap: list, symbol: str) -> Optional[np.ndarray]:
    try:
        # Convert market cap data to numpy array
        data = np.array([float(x) for x in market_cap if x is not None], dtype=np.float32)
        
        # Handle cases where data length is not 65
        target_length = 65
        if len(data) == 0:
            return None
        elif len(data) < target_length:
            # Pad with zeros if too short
            data = np.pad(data, (0, target_length - len(data)), mode='constant')
        elif len(data) > target_length:
            # Truncate if too long
            data = data[:target_length]
        
        # Normalize data (assuming model expects normalized input)
        data = (np.max(data)-data) / (np.max(data) )
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing market cap data for {symbol}: {str(e)}")

# Endpoint to check pattern
def check_pattern(symbol: str):
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
        print ("market_cap", market_cap)
        # Process market_cap to ensure it fits model input (65 values)
        processed_data = process_market_cap_data(market_cap, symbol)
        print ("processed_data", processed_data)
        if processed_data is None:
            raise HTTPException(status_code=400, detail=f"Failed to process market_cap data for {symbol}")

        # Preprocess data for the model
        input_data = processed_data.reshape(1, -1)  # Reshape to (1, 65)

        # Run prediction
        prediction = MODEL.predict(input_data)
        # Assuming binary classification
        pattern_detected = bool(np.argmax(prediction[0]) if prediction.shape[-1] > 1 else prediction[0] > 0.5)

        return (pattern_detected)

#JSONResponse(content={
#            "symbol": symbol,
#            "pattern_detected": pattern_detected
#        })

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Run the application (optional, for development)
if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=8000)
  print(check_pattern("MSFT:US"))
