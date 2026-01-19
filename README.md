# Sales Analytics System

## Overview
This is a Python-based data analytics system designed to process sales transactions, enrich them with real-time product data from an external API (DummyJSON), and generate comprehensive business reports. The system handles data cleaning, validation, analysis, API enrichment, and report generation in a structured workflow.

---

## Features
- **File Handling & Preprocessing**: Reads pipe-delimited sales data, handles encoding issues, removes invalid records, and supports user-defined filters.
- **Data Analysis**: Computes total revenue, average order value, region-wise performance, top 5 products, top 5 customers, daily sales trends, and product performance analysis.
- **API Integration**: Fetches product categories and brands from DummyJSON API to enrich local sales data.
- **Reporting**: Generates a detailed, formatted text report (`output/sales_report.txt`) including all sections: header, overall summary, region-wise performance, top products, top customers, daily sales trend, product analysis, and API enrichment summary.
- **Main Application Workflow**: Combines all modules with proper error handling and user interaction for a complete analytics experience.

---

## Project Structure
sales-analytics-system/
│
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt
│
├── output/
│   └── sales_report.txt
│
├── utils/
│   ├── file_handler.py
│   ├── data_processor.py
│   ├── api_handler.py
│   └── report_generator.py
│
├── main.py
├── README.md
├── requirements.txt
└── .gitignore

## Requirements
- Python 3.8+
- `requests` library

Install dependencies:
```bash
pip install -r requirements.txt
