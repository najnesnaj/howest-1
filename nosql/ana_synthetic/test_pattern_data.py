import numpy as np
from tensorflow import keras
from functions.random_data import generate_random_data

# Load the saved model
model_path = '/usr/src/howest-1/nosql/ana_synthetic/model.keras'
try:
    model = keras.models.load_model(model_path)
    print(f"Model loaded from {model_path}")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

# Generate and test 10 arrays
num_samples = 10
predictions = []

for i in range(num_samples):
    # Generate data and convert to NumPy array
    arr = np.array(generate_random_data())
    print (arr) 
    # Verify length and adjust if needed
    if len(arr) != 65:
        print(f"Warning: Sample {i+1} has length {len(arr)}, padding/truncating to 65")
        arr = np.pad(arr, (0, 65 - len(arr)), mode='constant')[:65]
    
    # Ensure data is in [0, 1]
    if arr.max() > 1 or arr.min() < 0:
        print(f"Warning: Sample {i+1} outside [0, 1], normalizing")
        arr = (arr - arr.min()) / (arr.max() - arr.min())
    
    # Reshape for model input (1 sample, 65 features)
    arr = arr.reshape(1, 65)
    
    # Make prediction
    prediction = model.predict(arr, verbose=0)
    is_pattern = prediction[0][0] > 0.5
    predictions.append((i+1, prediction[0][0], is_pattern))
    
    # Print result for this sample
    print(f"Sample {i+1}: Probability = {prediction[0][0]:.4f}, Pattern = {is_pattern}")


#same test , with random data 
for i in range(num_samples):
    # Generate random data: array of length 65 with floats in [0, 1]
    arr = np.random.uniform(low=0.0, high=1.0, size=65)
    print(f"Sample {i+1} data: {arr}")

    # Verify length (should always be 65, included for consistency)
    if len(arr) != 65:
        print(f"Warning: Sample {i+1} has length {len(arr)}, padding/truncating to 65")
        arr = np.pad(arr, (0, 65 - len(arr)), mode='constant')[:65]

    # Ensure data is in [0, 1] (should always be true with np.random.uniform)
    if arr.max() > 1 or arr.min() < 0:
        print(f"Warning: Sample {i+1} outside [0, 1], normalizing")
        arr = (arr - arr.min()) / (arr.max() - arr.min())

    # Reshape for model input (1 sample, 65 features)
    arr = arr.reshape(1, 65)

    # Make prediction
    prediction = model.predict(arr, verbose=0)
    is_pattern = prediction[0][0] > 0.5
    predictions.append((i+1, prediction[0][0], is_pattern))

    # Print result for this sample
    print(f"Sample {i+1}: Probability = {prediction[0][0]:.4f}, Pattern = {is_pattern}")


# Summary
pattern_count = sum(1 for _, _, is_pattern in predictions if is_pattern)
print(f"\nSummary: {pattern_count} out of {num_samples} samples match the pattern")
