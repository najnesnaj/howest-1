# Use the official PostgreSQL image as the base
FROM postgres:latest

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=mydatabase

# Copy the SQL backup file into the container's initialization directory
COPY db_backup.sql /docker-entrypoint-initdb.d/

# Expose the PostgreSQL port (optional, already exposed in base image)
EXPOSE 5432
