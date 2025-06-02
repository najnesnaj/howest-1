# Financial Data Storage and Analysis for Stock-Exchange Companies

## Overview
This project is designed to store and analyze financial data for companies listed on the stock exchange, using Germany as an example. The financial data is stored in a PostgreSQL database in JSONB format, enabling efficient querying and storage of structured data. The project includes microservices for data visualization, analysis, and further treatment, all containerized using Docker and orchestrated with Kubernetes for cloud deployment.

The primary goal is to generate decision-supporting reports based on quarterly financial data, focusing on **revenue**, **market capitalization (marketcap)**, and **return on invested capital (ROIC)**. The project also incorporates a machine learning (ML) component for **deep reinforcement learning (DRL)** to identify patterns in financial data and classify companies based on their performance.

---

## Key Features
1. **Data Storage**:
   - Financial data is retrieved in JSON format and stored in PostgreSQL as JSONB.
   - Example data includes quarterly revenue, marketcap, and ROIC.

2. **Microservices**:
   - Microservices are implemented for:
     - Visualizing financial data.
     - Calculating correlations between revenue, marketcap, and ROIC.
     - Generating decision-supporting reports.

3. **Data Visualization**:
   - Financial data is presented in color-coded formats:
     - **Red**: Negative performance.
     - **Green**: Positive performance.
     - **Blue**: Neutral performance.
   - This allows users to easily detect patterns in the data.

4. **Correlation Analysis**:
   - The project assumes a strong correlation between ROIC, revenue, and marketcap.
   - Correlation values are calculated and stored in the database for further analysis.

5. **Trend Analysis**:
   - Quarterly upward or downward trends are stored as integer arrays (`-1`, `0`, `1`).
   - These trends are used for pattern detection and classification.

6. **Machine Learning (ML) Component**:
   - A **deep reinforcement learning (DRL)** model is trained on historical data to identify patterns.
   - The model generates probabilities for future price movements based on backward-looking data.
   - Example: A company reporting an increase in revenue for three consecutive quarters multiple times might exhibit similar behavior in the future.

7. **Classification of Companies**:
   - Companies are classified into categories such as:
     - **Cyclical**: Companies with fluctuating performance.
     - **Growth**: Companies with consistent upward trends.
     - **Value**: Companies with stable but undervalued performance.

8. **Cloud Deployment**:
   - The project uses Docker containers and Kubernetes pods for scalable deployment in the cloud.

9. **Extensive Documentation**:
   - The project is fully documented using Sphinx and GitHub Copilot.
   - Documentation includes detailed descriptions of Python scripts, APIs, and workflows.

---

## Project Workflow
1. **Data Retrieval**:
   - Financial data is retrieved using the `QuickFS` API.
   - Example: German companies listed on the stock exchange.

2. **Data Storage**:
   - The retrieved data is stored in a PostgreSQL database as JSONB.

3. **Data Processing**:
   - Microservices process the data to calculate correlations and generate reports.
   - Trends are stored as integer arrays for further analysis.

4. **Visualization**:
   - Data is visualized in a user-friendly, color-coded format.

5. **Machine Learning**:
   - Historical data is used to train a DRL model to identify patterns and classify companies.

---

## Assumptions
1. **Investor Behavior**:
   - Investors sell when losses exceed 7%.
   - This assumption is used to classify trends and patterns.

2. **Correlation**:
   - A strong correlation exists between ROIC, revenue, and marketcap.

3. **Pattern Detection**:
   - Companies with consistent trends (e.g., three consecutive quarters of revenue growth) are likely to exhibit similar behavior in the future.

---

## Technologies Used
- **Python**:
  - Data processing and analysis.
  - Microservices implementation.
- **PostgreSQL**:
  - JSONB storage for financial data.
  - Efficient querying and analysis.
- **Docker**:
  - Containerization of microservices.
- **Kubernetes**:
  - Orchestration of containers for cloud deployment.
- **Sphinx**:
  - Documentation generation.
- **Deep Reinforcement Learning (DRL)**:
  - Machine learning for pattern detection and classification.

---

## Installation and Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/financial-data-analysis.git
   cd financial-data-analysis
   ```

2. Set up the environment:
   - Create a `.env` file with the following variables:
     ```env
     POSTGRES_USER=myuser
     POSTGRES_PASSWORD=mypassword
     POSTGRES_DB=mydatabase
     POSTGRES_HOST=localhost
     POSTGRES_PORT=5432
     ```

3. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

4. Deploy to Kubernetes (optional):
   ```bash
   kubectl apply -f k8s/
   ```

5. Generate documentation:
   ```bash
   cd docs
   make html
   ```

---

## Example Usage
1. **Store Financial Data**:
   - Use `update_postgres.py` to retrieve and store financial data in the PostgreSQL database.

2. **Visualize Data**:
   - Access the visualization microservice to view color-coded trends.

3. **Analyze Correlations**:
   - Use `correlation.py` to calculate correlations and store the results in the database.

4. **Train Machine Learning Model**:
   - Use the stored trends to train a DRL model for pattern detection.

---

## Limitations
- The project does not predict future price movements but identifies patterns in historical data.
- Assumptions about investor behavior and correlations may not hold true in all cases.

---

## Future Work
- Extend the project to include companies from other stock exchanges.
- Improve the ML model to handle more complex patterns.
- Add real-time data processing capabilities.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments
- **QuickFS API**: For providing financial data.
- **PostgreSQL**: For efficient data storage and querying.
- **Sphinx**: For generating project documentation.
- **GitHub Copilot**: For assisting with code and documentation generation.
