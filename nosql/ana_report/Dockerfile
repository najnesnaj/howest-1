# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .
#COPY static /app/static
#COPY templates /app/templates
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .
#COPY fastapp.py .
#COPY env .
# Expose the port that FastAPI will run on
EXPOSE 8001

# Command to run the FastAPI application
CMD ["uvicorn", "fastapp:app", "--host", "0.0.0.0", "--port", "8001"]
