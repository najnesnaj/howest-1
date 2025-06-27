import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

# Load test data
X_test = np.load('X_test.npy') / 100.0  # Normalize to [0, 1]
y_test = np.load('y_test.npy')

# Ensure we have at least 20 samples
if len(X_test) < 20:
    print(f"Error: X_test contains only {len(X_test)} samples, need at least 20.")
    exit(1)

# Select 20 samples (you can change the indices if you want specific samples)
num_samples = 20
X_subset = X_test[:num_samples]
y_subset = y_test[:num_samples]

# Load the trained model (assuming it was saved as 'my_model.keras')
try:
    model = tf.keras.models.load_model('my_model.keras')
except FileNotFoundError:
    print("Error: Model file 'my_model.keras' not found. Training a new model.")
    # Train a new model if not found (using your original code)
    X_train = np.load('X_train.npy') / 100.0
    y_train = np.load('y_train.npy')
    X_val = np.load('X_val.npy') / 100.0
    y_val = np.load('y_val.npy')

    model = models.Sequential([
        layers.Input(shape=(70,)),
        layers.Dense(128, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20, batch_size=32)
    model.save('my_model.keras')  # Save for future use

# Print test data and make predictions
print("\nPrinting 20 test samples, their true labels, and model predictions:\n")
for i in range(num_samples):
    # Get the array and true label
    test_array = X_subset[i]
    true_label = y_subset[i]
    true_label_str = "Pattern" if true_label == 1 else "No Pattern"

    # Print the array and true label
    print(f"Sample #{i+1}:")
    print("Array (70 values):")
    print(np.round(test_array, 4))  # Round to 4 decimals for readability
    print(f"True Label: {true_label_str}")

    # Make prediction
    test_array_reshaped = test_array.reshape(1, 70)  # Reshape to (1, 70) for single-sample prediction
    pred_prob = model.predict(test_array_reshaped, verbose=0)[0][0]  # Get probability
    pred_label = 1 if pred_prob > 0.5 else 0  # Threshold at 0.5
    pred_label_str = "Pattern" if pred_label == 1 else "No Pattern"

    # Print model prediction
    print(f"Model Prediction: {pred_label_str} (Probability: {pred_prob:.4f})")
    print("-" * 80)

# Optional: Evaluate model on full test set for reference
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nOverall Test Accuracy: {test_accuracy:.4f}")
