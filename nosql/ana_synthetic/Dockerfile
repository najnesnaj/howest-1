# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn numpy plotly

# Copy the main script into the container
COPY simple2.py .

# Ensure the shared volume directory exists
RUN mkdir -p /app/functions

# Set the Python path to include the shared volume for module imports
ENV PYTHONPATH=/app/functions

# Command to run the FastAPI application with uvicorn
CMD ["uvicorn", "simple2:app", "--host", "0.0.0.0", "--port", "8000"]
