# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for psycopg2 and TensorFlow
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and model
COPY pattern_app.py .
COPY my_model.keras .

# Expose the port for the pattern detection service
EXPOSE 8002

# Command to run the FastAPI application
CMD ["uvicorn", "pattern_app:app", "--host", "0.0.0.0", "--port", "8002"]
