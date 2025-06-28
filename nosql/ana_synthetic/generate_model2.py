import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Function to generate patterned data mimicking the provided dataset
def generate_random_data(length=70, period1=8, period2=16, noise_level=0.15):
    """
    Generate synthetic data with periodicity similar to the provided dataset.
    
    Args:
        length (int): Number of data points (default: 70).
        period1 (float): Primary period of sinusoidal component (default: 8).
        period2 (float): Secondary period for added complexity (default: 16).
        noise_level (float): Magnitude of random noise (default: 0.15).
    
    Returns:
        np.array: Array of length values in [0, 1] with periodic pattern.
    """
    t = np.arange(length)
    # Combine two sinusoids for quasi-periodic pattern
    base_pattern = 0.5 * np.sin(2 * np.pi * t / period1) + 0.3 * np.sin(2 * np.pi * t / period2)
    
    # Add controlled noise
    noise = np.random.normal(0, noise_level, length)
    synthetic_data = base_pattern + noise
    
    # Normalize to [0.01, 1]
    synthetic_data = (synthetic_data - np.min(synthetic_data)) / (np.max(synthetic_data) - np.min(synthetic_data))
    synthetic_data = 0.01 + synthetic_data * (1.0 - 0.01)  # Scale to [0.01, 1]
    
    return np.round(synthetic_data, 6)

# Function to generate random data without patterns
def generate_no_pattern_data(length=70, min_val=0.01, max_val=1.0, max_diff=0.15):
    """
    Generate random data without periodicity, with consecutive values differing by <= 15%.
    
    Args:
        length (int): Number of data points (default: 70).
        min_val (float): Minimum value (default: 0.01).
        max_val (float): Maximum value (default: 1.0).
        max_diff (float): Maximum difference between consecutive values (default: 0.15).
    
    Returns:
        np.array: Array of length values in [min_val, max_val].
    """
    data = np.zeros(length)
    data[0] = np.random.uniform(min_val, max_val)
    for i in range(1, length):
        prev = data[i-1]
        lower_bound = max(min_val, prev - max_diff)
        upper_bound = min(max_val, prev + max_diff)
        data[i] = np.random.uniform(lower_bound, upper_bound)
    return np.round(data, 6)

# Generate synthetic dataset
def generate_dataset(num_samples=2000, length=70):
    """
    Generate dataset with patterned and non-patterned data.
    
    Args:
        num_samples (int): Total number of samples (half patterned, half non-patterned).
        length (int): Length of each array (default: 70).
    
    Returns:
        X (np.array): Input data of shape (num_samples, length).
        y (np.array): Labels (1 for patterned, 0 for non-patterned).
    """
    half_samples = num_samples // 2
    
    # Generate patterned data
    X_patterned = np.array([generate_random_data(length=length) for _ in range(half_samples)])
    y_patterned = np.ones(half_samples)
    
    # Generate non-patterned data
    X_no_pattern = np.array([generate_no_pattern_data(length=length) for _ in range(half_samples)])
    y_no_pattern = np.zeros(half_samples)
    
    # Combine datasets
    X = np.vstack((X_patterned, X_no_pattern))
    y = np.hstack((y_patterned, y_no_pattern))
    
    return X, y

# Build Keras model
def build_model(input_length=70):
    """
    Build a Keras model for binary classification of sequences.
    
    Args:
        input_length (int): Length of input sequences (default: 70).
    
    Returns:
        keras.Model: Compiled Keras model.
    """
    model = keras.Sequential([
        layers.Input(shape=(input_length,)),
        layers.Reshape((input_length, 1)),
        layers.Conv1D(32, kernel_size=5, activation='relu', padding='same'),
        layers.MaxPooling1D(pool_size=2),
        layers.Conv1D(64, kernel_size=5, activation='relu', padding='same'),
        layers.MaxPooling1D(pool_size=2),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Main script
def main():
    # Parameters
    length = 70
    num_samples = 2000
    test_size = 0.2
    
    # Generate dataset
    print("Generating synthetic dataset...")
    X, y = generate_dataset(num_samples=num_samples, length=length)
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    # Build and train model
    print("Building and training model...")
    model = build_model(input_length=length)
    model.summary()
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=20,
        batch_size=32,
        verbose=1
    )
    
    # Evaluate model
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"\nTest Accuracy: {test_accuracy:.4f}")
    
    # Plot training history
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Save the model
    model.save('pattern_classifier.keras')
    print("Model saved to 'pattern_classifier.keras'")
    
    # Test the model on a sample patterned array
    print("\nTesting model on a sample patterned array:")
    sample_array = generate_random_data(length=length)
    sample_array = sample_array.reshape(1, length)
    prediction = model.predict(sample_array, verbose=0)[0][0]
    label = "has pattern" if prediction >= 0.5 else "no pattern"
    print(f"Sample array: {np.round(sample_array[0], 6)}")
    print(f"Prediction: The sample array {label}.")
    print(f"Probability of having a pattern: {prediction:.6f}")

if __name__ == "__main__":
    main()
