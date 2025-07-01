# Use the official PostgreSQL image as the base
FROM postgres:latest

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=postgres
# Copy the SQL backup file into the container's initialization directory
ADD companies.sql /docker-entrypoint-initdb.d/

# Expose the PostgreSQL port (optional, already exposed in base image)
EXPOSE 5432
