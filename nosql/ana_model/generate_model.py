import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# Your provided function (unchanged)
def generate_synthetic_array(size=70):
    # Target statistical properties
    target_mean = 0.66
    target_std = 0.11
    min_val, max_val = 0.3, 0.9

    # Create a base pattern with periodic fluctuations
    t = np.linspace(0, 10, size)  # Time-like index for smooth transitions
    base_pattern = 0.66 + 0.15 * np.sin(2 * np.pi * t / 5)  # Periodic component (period ~5)
    peaks = np.random.choice([0, 0, 0, 0.2, 0.25], size=size, p=[0.8, 0.1, 0.05, 0.025, 0.025])  # Occasional peaks
    noise = np.random.normal(0, 0.05, size)  # Small noise for variability

    # Combine components
    synthetic_data = base_pattern + peaks + noise

    # Apply slight right skew using a transformation
    synthetic_data = np.clip(synthetic_data, min_val, max_val)
    synthetic_data = min_val + (max_val - min_val) * (synthetic_data - synthetic_data.min()) / (
        synthetic_data.max() - synthetic_data.min()
    )

    # Adjust mean and standard deviation
    current_mean = np.mean(synthetic_data)
    current_std = np.std(synthetic_data)
    synthetic_data = (synthetic_data - current_mean) * (target_std / current_std) + target_mean

    # Clip to ensure values stay within [0.3, 0.9]
    synthetic_data = np.clip(synthetic_data, min_val, max_val)

    # Round to two decimal places
    synthetic_data = np.round(synthetic_data, 2)

    return synthetic_data

# Function to create supervised learning data (sliding window)
def create_sequences(data, window_size):
    X, y = [], []
    for sequence in data:
        for i in range(len(sequence) - window_size):
            X.append(sequence[i:i + window_size])
            y.append(sequence[i + window_size])
    return np.array(X), np.array(y)

# Parameters
n_arrays = 5000
sequence_length = 70
window_size = 10  # Number of past values to use for prediction
n_features = 1    # Univariate time series

# Generate 5000 synthetic arrays
print("Generating synthetic data...")
data = np.array([generate_synthetic_array(size=sequence_length) for _ in range(n_arrays)])

# Create supervised learning dataset
X, y = create_sequences(data, window_size)

# Reshape X for LSTM [samples, timesteps, features]
X = X.reshape((X.shape[0], X.shape[1], n_features))

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build Keras LSTM model
model = Sequential([
    LSTM(50, activation='relu', input_shape=(window_size, n_features), return_sequences=True),
    Dropout(0.2),
    LSTM(30, activation='relu'),
    Dropout(0.2),
    Dense(10, activation='relu'),
    Dense(1)  # Output layer for predicting the next value
])

# Compile the model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Model summary
model.summary()

# Train the model
print("Training model...")
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=32,
    validation_data=(X_test, y_test),
    verbose=1
)

# Evaluate the model
print("Evaluating model...")
test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Loss (MSE): {test_loss:.6f}")
print(f"Test MAE: {test_mae:.6f}")

# Optional: Plot training history
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 4))

# Plot loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss (MSE)')
plt.legend()

# Plot MAE
plt.subplot(1, 2, 2)
plt.plot(history.history['mae'], label='Training MAE')
plt.plot(history.history['val_mae'], label='Validation MAE')
plt.title('Model MAE')
plt.xlabel('Epoch')
plt.ylabel('MAE')
plt.legend()

plt.tight_layout()
plt.show()

# Example prediction
sample_sequence = data[0][:window_size].reshape(1, window_size, n_features)
predicted_value = model.predict(sample_sequence, verbose=0)
print(f"Sample prediction: {predicted_value[0][0]:.2f}")


# After training the model
print("Saving model to model.keras...")
model.save('my_model.keras')

# Optional: Demonstrate loading the model for inference
print("Loading model from model.keras...")
loaded_model = tf.keras.models.load_model('model.keras')

# Verify loaded model with a sample prediction
sample_sequence = data[0][:window_size].reshape(1, window_size, n_features)
predicted_value = loaded_model.predict(sample_sequence, verbose=0)
print(f"Prediction from loaded model: {predicted_value[0][0]:.2f}")
