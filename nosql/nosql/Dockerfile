# Use an official Python runtime as a parent image
FROM python:3.12-slim as build-image

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y curl build-essential libffi-dev

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock* ./

# Install the dependencies without installing the project itself
RUN poetry install --only main --no-root

# Copy the rest of the application code to the container
COPY . .

# Expose the port the app runs on
EXPOSE 9080

# Set environment variables
ENV ENVIRONMENT=DOCKER

# Run the application
CMD ["poetry", "run", "streamlit", "run", "/app/nosql/app.py", "--server.address", "0.0.0.0", "--server.port", "9080"]
