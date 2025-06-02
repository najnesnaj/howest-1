---
title: Modules
date: 2025-05-18T09:13:55
draft: false
categories: ["Blog"]
tags: ["sphinx", "hugo"]
---
# Module Documentation

## correlation.py

This script calculates financial correlations and stores the results in a PostgreSQL database.

Modules:
: - psycopg2: For connecting to and interacting with a PostgreSQL database.
  - pandas: For handling and processing tabular data.
  - dotenv: For loading environment variables from a .env file.
  - os: For accessing environment variables.
  - numpy: For numerical operations.

Environment Variables:
: - POSTGRES_USER: PostgreSQL username (default: ‘myuser’).
  - POSTGRES_PASSWORD: PostgreSQL password (default: ‘mypassword’).
  - POSTGRES_DB: PostgreSQL database name (default: ‘mydatabase’).
  - POSTGRES_HOST: PostgreSQL host (default: ‘localhost’).
  - POSTGRES_PORT: PostgreSQL port (default: ‘5432’).

Functions:
: - fetch_data(query): Fetches data from the PostgreSQL database based on the provided SQL query.
  - calculate_codes(data): Calculates codes based on percentage changes in the data.
    : - Code 1: Positive change.
      - Code 0: Small negative or no change (-7% to 0%).
      - Code -1: Large negative change (less than -7%).
  - calculate_correlation(revenue, market_cap, roic): Calculates the correlation between revenue, market cap, and ROIC codes.
    : - Correlation is incremented when all three codes are either 1 or -1.
  - calculate_consecutive_ones(data): Calculates the number of periods with more than two consecutive code 1 values.
  - main(): Main function that fetches data, processes it, and stores the results in a PostgreSQL table.

Database Schema:
: - Table: company_correlation
    : - symbol (TEXT): Primary key representing the company symbol.
      - revenue (INTEGER[]): Array of calculated revenue codes.
      - market_cap (INTEGER[]): Array of calculated market cap codes.
      - roic (INTEGER[]): Array of calculated ROIC codes.
      - correlation (FLOAT): Correlation value between revenue, market cap, and ROIC.
      - consecutive_ones (INT): Number of periods with more than two consecutive code 1 values.

Usage:
: - Ensure the required environment variables are set in a .env file.
  - Run the script to calculate financial correlations and store the results in the database.

### advisor.correlation.calculate_codes(data)

### advisor.correlation.calculate_consecutive_ones(data)

### advisor.correlation.calculate_correlation_all(revenue, market_cap, roic)

### advisor.correlation.calculate_correlation_rev_cap(revenue, market_cap)

### advisor.correlation.calculate_correlation_rev_roic(revenue, roic)

### advisor.correlation.calculate_correlation_roic_cap(roic, market_cap)

### advisor.correlation.fetch_data(query)

### advisor.correlation.main()

## fastapp.py

## report.py

This script generates a PDF report with financial metrics for companies stored in a PostgreSQL database.
It includes functionalities for fetching data, categorizing companies, generating plots, and creating a PDF report.
Modules and Libraries:
- psycopg2: For connecting to and querying the PostgreSQL database.
- pandas: For data manipulation and analysis.
- dotenv: For loading environment variables from a .env file.
- os: For accessing environment variables.

### ana_report.report.categorize_company(data)

### ana_report.report.fetch_data(query)

### ana_report.report.generate_pdf(df, output_file)

### ana_report.report.generate_plot(data, title, filename)

### ana_report.report.generate_report(output_file='financial_report.pdf')

### ana_report.report.get_item_color(data)

### ana_report.report.main()

## update_postgres.py

This script updates a PostgreSQL database with financial data for German companies
retrieved from the QuickFS API. It performs the following tasks:

1. Loads environment variables from a .env file to configure PostgreSQL connection details.
2. Connects to a PostgreSQL database using the psycopg2 library.
3. Ensures the existence of a companies table with a JSONB column to store financial data.
4. Reads a list of German company symbols from a file named german_companies.
5. Fetches financial data for each company symbol using the QuickFS API.
6. Inserts the retrieved financial data into the companies table in the PostgreSQL database.

Dependencies:
- dotenv for loading environment variables.
- psycopg2 for PostgreSQL database interaction.
- quickfs for accessing the QuickFS API.
- json for handling JSON data.

Environment Variables:
- POSTGRES_USER: PostgreSQL username (default: ‘myuser’).
- POSTGRES_PASSWORD: PostgreSQL password (default: ‘mypassword’).
- POSTGRES_DB: PostgreSQL database name (default: ‘mydatabase’).
- POSTGRES_HOST: PostgreSQL host (default: ‘localhost’).
- POSTGRES_PORT: PostgreSQL port (default: ‘5432’).

Note:
- Ensure the german_companies file exists and contains a list of company symbols, one per line.
- Replace the QuickFS API key with a valid key before running the script.

### nosql.update_postgres.main()

<!-- app.py -->
<!-- ------ -->
<!-- .. automodule:: app -->
<!-- :members: -->
<!-- :undoc-members: -->
<!-- :show-inheritance: -->

## show-json.py
