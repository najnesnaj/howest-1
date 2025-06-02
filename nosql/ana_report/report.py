"""
This script generates a PDF report with financial metrics for companies stored in a PostgreSQL database.
It includes functionalities for fetching data, categorizing companies, generating plots, and creating a PDF report.
Modules and Libraries:
- `psycopg2`: For connecting to and querying the PostgreSQL database.
- `pandas`: For data manipulation and analysis.
- `dotenv`: For loading environment variables from a `.env` file.
- `os`: For accessing environment variables."""

import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF

# Load environment variables
load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER', 'myuser')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'mypassword')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'mydatabase')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# Function to fetch data from PostgreSQL
def fetch_data(query):
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to categorize companies based on pattern
def categorize_company(data):
    avg_change = np.mean(np.diff(data))
    if avg_change > 0:
        return 'Cluster 1: Steady growth'
    elif avg_change < 0:
        return 'Cluster 3: Declining'
    else:
        return 'Cluster 2: Cyclical patterns'

# Function to get color for each value based on percentage change
def get_item_color(data):
    colors = []
    for i in range(len(data)):
        if i == 0:  # No previous value for the first item
            colors.append('blue')  # Default color for the first item
        else:
            if data[i - 1] == 0:
                change = 0
            else:
                change = (data[i] - data[i - 1]) / data[i - 1] * 100  # Percentage change
            if data[i] < 0:
                change = -100  # Negative change
#the percentage of 7 is used because a drop below is a sell signal (red = sell)
            if change > 0:
                colors.append('green')  # Positive change
            elif -7 <= change <= 0:
                colors.append('orange')  # Small negative or no change
            elif change < -7:
                colors.append('red')  # Large negative change
        
            #if data[i] < 0:  # Negative values should always be red
            #    colors.append('red')
    return colors

# Function to generate plots and save them as images
def generate_plot(data, title, filename):
    plt.figure(figsize=(6, 4))
    colors = get_item_color(data)
    plt.bar([f"Q{i+1}" for i in range(len(data))], data, color=colors)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# Function to generate PDF report
def generate_pdf(df, output_file):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for page_start in range(0, len(df), 3):  # Process 3 companies per page
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        for index, row in df.iloc[page_start:page_start + 3].iterrows():
            pdf.cell(200, 10, txt=f"Company: {row['symbol']}", ln=True, align='L')
            pdf.cell(200, 10, txt=f"Sector: {row['sector']}", ln=True, align='L')
            
            # Generate and add revenue plot
            revenue_plot = f"revenue_{index}.png"
            generate_plot(row['revenue'], f"{row['symbol']} Revenue", revenue_plot)
            
            # Generate and add market cap plot
            market_cap_plot = f"market_cap_{index}.png"
            generate_plot(row['market_cap'], f"{row['symbol']} Market Cap", market_cap_plot)
            
            # Generate and add ROIC plot
            roic_plot = f"roic_{index}.png"
            generate_plot(row['roic'], f"{row['symbol']} ROIC", roic_plot)
            
            # Add images side by side
            pdf.cell(200, 10, txt="Financial Metrics:", ln=True, align='L')
            pdf.image(revenue_plot, x=10, y=pdf.get_y(), w=60)  # Revenue plot on the left
            pdf.image(market_cap_plot, x=75, y=pdf.get_y(), w=60)  # Market cap plot in the middle
            pdf.image(roic_plot, x=140, y=pdf.get_y(), w=60)  # ROIC plot on the right
            pdf.ln(65)  # Adjust line height after adding images
            
            # Clean up plot images
            os.remove(revenue_plot)
            os.remove(market_cap_plot)
            os.remove(roic_plot)
        
        # Add spacing between groups of companies
        pdf.ln(10)
    
    pdf.output(output_file)

# Main function
def main():
    generate_report()

def generate_report(output_file="financial_report.pdf"):
    query = """
        SELECT 
            data->>'qfs_symbol_v2' AS symbol,
            data->'financials'->'quarterly'->'revenue' AS revenue,
            data->'financials'->'quarterly'->'market_cap' AS market_cap,
            data->'financials'->'quarterly'->'roic' AS roic,
            data->'metadata'->>'sector' AS sector
        FROM companies;
    """
    
    df = fetch_data(query)
    
    # Filter companies based on minimum thresholds
    min_market_cap = 500_000_000  # Example threshold
    min_roic = 0  # Example threshold
    df = df[
        df['market_cap'].apply(lambda x: np.mean(x[-5:]) > min_market_cap) &  # Last 5 values of market_cap
        df['roic'].apply(lambda x: np.mean(x[-5:]) > min_roic)  # Last 5 values of roic
    ]
    
    # Generate PDF report
    generate_pdf(df, output_file)

if __name__ == "__main__":
    main()
