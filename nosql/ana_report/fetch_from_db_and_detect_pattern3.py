import os
import tensorflow as tf
import numpy as np
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
POSTGRES_USER = os.getenv('POSTGRES_USER', 'myuser')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'mypassword')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'mydatabase')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# Function to fetch data from PostgreSQL
def fetch_data(query):
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        exit(1)

# Fetch market_cap data
query = """
    SELECT 
        data->>'qfs_symbol_v2' AS symbol,
        data->'financials'->'quarterly'->'market_cap' AS market_cap
    FROM companies;
"""
df = fetch_data(query)

# Load the trained model
try:
    model = tf.keras.models.load_model('my_model.keras')
except FileNotFoundError:
    print("Error: Model file 'my_model.keras' not found. Please train and save the model first.")
    exit(1)

# Process and normalize market_cap data
def process_market_cap_data(market_cap_json):
    try:
        # Convert JSON market_cap data to a NumPy array
        market_cap_array = np.array(market_cap_json, dtype=float)
        
        # Handle different lengths
        target_length = 70
        current_length = len(market_cap_array)
        
        if current_length == target_length:
            # No adjustment needed
            pass
        elif current_length < target_length:
            # Pad with zeros (alternative: use mean or last value)
            padding = np.zeros(target_length - current_length)
            market_cap_array = np.concatenate([market_cap_array, padding])
            print(f"Warning: Padded {current_length} quarters to 70 with zeros for symbol.")
        else:
            # Truncate to the most recent 70 quarters
            market_cap_array = market_cap_array[-target_length:]
            print(f"Warning: Truncated {current_length} quarters to 70 (kept most recent) for symbol.")
        
        # Normalize by dividing by the maximum value (if non-zero)
        max_value = np.max(np.abs(market_cap_array))
        if max_value == 0:
            print(f"Warning: Maximum market cap is zero, skipping normalization for symbol.")
            return market_cap_array  # Return unnormalized array or handle differently
        market_cap_array = market_cap_array / max_value  # Normalize to [0, 1]
        return market_cap_array
    except Exception as e:
        print(f"Error processing market_cap data: {e}")
        return None

# Prepare data for prediction
results = []
for index, row in df.iterrows():
    symbol = row['symbol']
    market_cap = row['market_cap']
    
    # Process market_cap data
    market_cap_array = process_market_cap_data(market_cap)
    if market_cap_array is None:
        print(f"Skipping symbol {symbol} due to invalid market_cap data.")
        continue
    
    # Reshape for model input (1, 70)
    market_cap_input = market_cap_array.reshape(1, 70)
    
    # Make prediction
    pred_prob = model.predict(market_cap_input, verbose=0)[0][0]
    pred_label = 1 if pred_prob > 0.5 else 0
    pred_label_str = "Pattern" if pred_label == 1 else "No Pattern"
    
    # Store results
    results.append({
        'symbol': symbol,
        'market_cap': np.round(market_cap_array, 4),  # Round for readability
        'prediction': pred_label_str,
        'probability': pred_prob,
        'original_quarters': len(market_cap)  # Store original number of quarters
    })

# Print results
print("\nPredictions for Market Cap Data:\n")
for result in results:
    print(f"Company Symbol: {result['symbol']}")
    print(f"Original Quarters: {result['original_quarters']}")
    print("Market Cap (70 quarters, normalized to [0, 1]):")
    print(result['market_cap'])
    print(f"Model Prediction: {result['prediction']} (Probability: {result['probability']:.4f})")
    print("-" * 80)

# Optional: Save results to a CSV file
results_df = pd.DataFrame([
    {
        'symbol': r['symbol'],
        'original_quarters': r['original_quarters'],
        'market_cap': r['market_cap'].tolist(),
        'prediction': r['prediction'],
        'probability': r['probability']
    } for r in results
])
results_df.to_csv('market_cap_predictions.csv', index=False)
print("Results saved to 'market_cap_predictions.csv'")
