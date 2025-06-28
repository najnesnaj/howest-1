import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from functions.random_data import generate_random_data  # Assumed to generate patterned data
import matplotlib.pyplot as plt

# Function to generate random data without patterns
def generate_no_pattern_data(n=70, min_val=0.01, max_val=1.0, max_diff=0.15):
    """
    Generate an array of n values in [min_val, max_val] with no clear pattern.
    Consecutive values differ by no more than max_diff.
    
    Args:
        n (int): Length of the array (default: 70).
        min_val (float): Minimum value (default: 0.01).
        max_val (float): Maximum value (default: 1.0).
        max_diff (float): Maximum difference between consecutive values (default: 0.15).
    
    Returns:
        np.array: Array of n values.
    """
    data = np.zeros(n)
    data[0] = np.random.uniform(min_val, max_val)  # Start with a random value
    for i in range(1, n):
        # Ensure consecutive values differ by no more than max_diff
        prev = data[i-1]
        lower_bound = max(min_val, prev - max_diff)
        upper_bound = min(max_val, prev + max_diff)
        data[i] = np.random.uniform(lower_bound, upper_bound)
    return np.round(data, 6)  # Round to 6 decimal places for consistency

# Function to generate synthetic dataset
def generate_dataset(num_samples=1000, n=70):
    """
    Generate synthetic dataset with patterned and non-patterned data.
    
    Args:
        num_samples (int): Total number of samples (half patterned, half non-patterned).
        n (int): Length of each array (default: 70).
    
    Returns:
        X (np.array): Input data of shape (num_samples, n).
        y (np.array): Labels (1 for patterned, 0 for non-patterned).
    """
    half_samples = num_samples // 2
    
    # Generate patterned data using generate_random_data
    X_patterned = np.array([generate_random_data(length=n) for _ in range(half_samples)])
    y_patterned = np.ones(half_samples)  # Label 1 for patterned data
    
    # Generate non-patterned data
    X_no_pattern = np.array([generate_no_pattern_data(n=n) for _ in range(half_samples)])
    y_no_pattern = np.zeros(half_samples)  # Label 0 for non-patterned data
    
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
        layers.Reshape((input_length, 1)),  # Reshape for 1D CNN
        layers.Conv1D(32, kernel_size=5, activation='relu', padding='same'),
        layers.MaxPooling1D(pool_size=2),
        layers.Conv1D(64, kernel_size=5, activation='relu', padding='same'),
        layers.MaxPooling1D(pool_size=2),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(1, activation='sigmoid')  # Binary classification
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Main script
def main():
    # Parameters
    n = 70  # Length of each sequence
    num_samples = 2000  # Total samples (1000 patterned, 1000 non-patterned)
    test_size = 0.2  # Fraction of data for testing
    
    # Generate dataset
    X, y = generate_dataset(num_samples=num_samples, n=n)
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    # Build and train model
    model = build_model(input_length=n)
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

if __name__ == "__main__":
    main()
