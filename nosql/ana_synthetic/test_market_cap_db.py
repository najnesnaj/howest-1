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


def process_market_cap_data(market_cap_json, symbol):
    """
    Process market_cap data to ensure it fits the model input size (65).
    Args:
        market_cap_json: List or array-like market cap data
        symbol: str, for logging purposes
    Returns:
        np.ndarray: Processed array of length 65, or None if processing fails
    """
    try:
        # Convert JSON market_cap data to a NumPy array
        market_cap_array = np.array(market_cap_json, dtype=float)

        # Handle different lengths
        target_length = 65
        current_length = len(market_cap_array)

        if current_length == target_length:
            # No adjustment needed
            pass
        elif current_length < target_length:
            # Pad with zeros (alternative: use mean or last value)
            padding = np.zeros(target_length - current_length)
            market_cap_array = np.concatenate([market_cap_array, padding])
            print(f"Warning: Padded {current_length} quarters to {target_length} with zeros for {symbol}.")
        else:
            # Truncate to the most recent 65 quarters
            market_cap_array = market_cap_array[-target_length:]
            print(f"Warning: Truncated {current_length} quarters to {target_length} (kept most recent) for {symbol}.")

        # Normalize by dividing by the maximum value (if non-zero)
        max_value = np.max(np.abs(market_cap_array))
        print ("max_value in array = ", max_value)
        if max_value == 0:
            print(f"Warning: Maximum market cap is zero, skipping normalization for {symbol}.")
            return market_cap_array  # Return unnormalized array or handle differently
        market_cap_array = market_cap_array / max_value  # Normalize to [0, 1]
        formatted_array = np.array2string(market_cap_array, separator=', ', formatter={'float': '{:.3f}'.format})
        print(f"Normalized market cap array for {symbol}: {formatted_array}")
        #np.set_printoptions(formatter={'float': '{:.3f}'.format}, separator=', ')
        print (market_cap_array)
        return market_cap_array
    except Exception as e:
        print(f"Error processing market_cap data for {symbol}: {e}")
        return None




# Process market cap data to ensure correct shape
#def process_market_cap_data(market_cap: list, symbol: str) -> Optional[np.ndarray]:
#    try:
#        # Convert market cap data to numpy array
#        data = np.array([float(x) for x in market_cap if x is not None], dtype=np.float32)
#        
#        # Handle cases where data length is not 65
#        target_length = 65
#        if len(data) == 0:
#            return None
#        elif len(data) < target_length:
#            # Pad with zeros if too short
#            data = np.pad(data, (0, target_length - len(data)), mode='constant')
#        elif len(data) > target_length:
#            # Truncate if too long
#            data = data[:target_length]
#        
#        # Normalize data (assuming model expects normalized input)
#        data = (data) / (np.max(data) )
#        return data
#    except Exception as e:
#        raise HTTPException(status_code=400, detail=f"Error processing market cap data for {symbol}: {str(e)}")
#
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
        #print ("market_cap", market_cap)
        # Process market_cap to ensure it fits model input (65 values)
        processed_data = process_market_cap_data(market_cap, symbol)
        print ("processed_data", processed_data)
        if processed_data is None:
            raise HTTPException(status_code=400, detail=f"Failed to process market_cap data for {symbol}")

        # Preprocess data for the model
        input_data = processed_data.reshape(1, -1)  # Reshape to (1, 65)

        # Run prediction
        prediction = MODEL.predict(input_data)
        print ("prediction", prediction)
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
  print(check_pattern("BMW:DE"))
  print(check_pattern("DEZ:DE"))
  print(check_pattern("MSFT:US"))
