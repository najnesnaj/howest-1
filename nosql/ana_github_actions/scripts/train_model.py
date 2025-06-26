# scripts/train_model.py
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split

def generate_synthetic_array(size=70):
    target_mean = 0.66
    target_std = 0.11
    min_val, max_val = 0.3, 0.9
    t = np.linspace(0, 10, size)
    base_pattern = 0.66 + 0.15 * np.sin(2 * np.pi * t / 5)
    peaks = np.random.choice([0, 0, 0, 0.2, 0.25], size=size, p=[0.8, 0.1, 0.05, 0.025, 0.025])
    noise = np.random.normal(0, 0.05, size)
    synthetic_data = base_pattern + peaks + noise
    synthetic_data = np.clip(synthetic_data, min_val, max_val)
    synthetic_data = min_val + (max_val - min_val) * (synthetic_data - synthetic_data.min()) / (
        synthetic_data.max() - synthetic_data.min()
    )
    current_mean = np.mean(synthetic_data)
    current_std = np.std(synthetic_data)
    synthetic_data = (synthetic_data - current_mean) * (target_std / current_std) + target_mean
    synthetic_data = np.clip(synthetic_data, min_val, max_val)
    synthetic_data = np.round(synthetic_data, 2)
    return synthetic_data

def create_sequences(data, window_size):
    X, y = [], []
    for sequence in data:
        for i in range(len(sequence) - window_size):
            X.append(sequence[i:i + window_size])
            y.append(sequence[i + window_size])
    return np.array(X), np.array(y)

def build_and_save_model(output_path="my_model.keras"):
    # Parameters
    n_arrays = 5000
    sequence_length = 70
    window_size = 10
    n_features = 1

    # Generate data
    print("Generating synthetic data...")
    data = np.array([generate_synthetic_array(size=sequence_length) for _ in range(n_arrays)])
    X, y = create_sequences(data, window_size)
    X = X.reshape((X.shape[0], X.shape[1], n_features))

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Build model
    model = Sequential([
        LSTM(50, activation='relu', input_shape=(window_size, n_features), return_sequences=True),
        Dropout(0.2),
        LSTM(30, activation='relu'),
        Dropout(0.2),
        Dense(10, activation='relu'),
        Dense(1)
    ])

    # Compile and train
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    print("Training model...")
    model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test), verbose=1)

    # Save model
    print(f"Saving model to {output_path}...")
    model.save(output_path)

if __name__ == "__main__":
    build_and_save_model()
