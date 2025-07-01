# ML Pattern Detection with Docker and JSONB Timeseries

This project is a **showcase of using Docker containers in a Machine Learning (ML) context**, combining a PostgreSQL database with a FastAPI interface and AI pattern detection capabilities.

## 🔧 Project Overview

We use Docker to manage a set of microservices for the full ML pipeline:

- A **PostgreSQL database** (with `jsonb` fields) stores real-world time series data (revenue, ROIC, and market cap) per company.
- A **FastAPI-based API server** (Dockerized) provides access to the data and supports basic visualization and analysis.
- A **pattern detection system** where users can define interesting patterns and train a model to detect similar ones.
- Trained models are deployed in **FastAPI containers** to predict matches for individual companies.
- Batch analysis across all companies is handled using helper scripts.

---

## 🧱 Architecture

```text
┌─────────────┐    ┌────────────────────┐     ┌──────────────────────┐
│ PostgreSQL  │ ←→ │ FastAPI Interface  │ ←→  │ Visualization & Plots│
│ (jsonb TS)  │    │ (port 8001)        │     │  Pattern Insights    │
└─────────────┘    └────────────────────┘     └──────────────────────┘
                              ↓
                    ┌─────────────────┐
                    │ Train AI Model  │ ←── Synthetic Data from Pattern
                    └─────────────────┘
                              ↓
                    ┌────────────────────┐
                    │ AI FastAPI Server  │ → Prediction per company
                    └────────────────────┘
                              ↓
                    ┌───────────────────┐
                    │ Batch Matching via│
                    │   `ana_check/`    │
                    └───────────────────┘

