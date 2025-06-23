# Use a Python base image with TensorFlow support
FROM tensorflow/tensorflow:2.17.0

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model-building script
COPY scripts/train_model.py scripts/

# Run the script to generate the model during build
RUN python scripts/train_model.py

# (Placeholder) Define the command to use the model
# Replace this with your actual application (e.g., Flask API)
CMD ["python", "-c", "import tensorflow as tf; model = tf.keras.models.load_model('my_keras.model'); print('Model loaded successfully')"]

# Expose port if serving (e.g., for a Flask API)
# EXPOSE 5000
