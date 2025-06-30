import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from functions.random_data import generate_random_data

# Generate training data
X_train = []
y_train = []
for _ in range(5000):
    arr = np.array(generate_random_data())  # Convert to NumPy array
    if len(arr) != 65:
        print(f"Warning: generate_random_data returned {len(arr)} values, padding to 65")
        arr = np.pad(arr, (0, 65 - len(arr)), mode='constant')[:67]
    # Ensure range [0, 1]
#    if arr.max() > 1 or arr.min() < 0:
#        arr = (arr - arr.min()) / (arr.max() - arr.min())
    X_train.append(arr)
    # Example pattern: first 10 values ascending (replace with actual pattern)
#    is_pattern = all(arr[i] < arr[i + 1] for i in range(min(9, len(arr) - 1)))
#    y_train.append(1 if is_pattern else 0)  # Label based on pattern
    y_train.append(1)  # Label based on pattern

for _ in range(5000):
    arr = np.random.rand(65)  # Random data in [0, 1)
    X_train.append(arr)
    y_train.append(0)  # No pattern

X_train = np.array(X_train)
y_train = np.array(y_train)

# Verify shapes
print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")  # Should be (2000, 65), (2000,)

# Split into train and test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Build model
model = keras.Sequential([
    layers.Input(shape=(65,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(32, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Compile model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Model summary
model.summary()

# Train model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, verbose=1)

# Evaluate on test set
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test accuracy: {test_accuracy:.4f}")

# Save model
model.save('/usr/src/howest-1/nosql/ana_synthetic/model.keras')
print("Model saved to /usr/src/howest-1/nosql/ana_synthetic/model.keras")
