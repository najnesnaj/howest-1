import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np 


# Load data
X_train = np.load('X_train.npy') / 100.0  # Normalize to [0, 1]
y_train = np.load('y_train.npy')
X_val = np.load('X_val.npy') / 100.0
y_val = np.load('y_val.npy')

# Define a simple neural network
model = models.Sequential([
    layers.Input(shape=(70,)),
    layers.Dense(128, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Compile and train
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20, batch_size=32)

# Evaluate on test set
X_test = np.load('X_test.npy') / 100.0
y_test = np.load('y_test.npy')
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_accuracy:.4f}")

#save the model
model.save('my_model.keras')
