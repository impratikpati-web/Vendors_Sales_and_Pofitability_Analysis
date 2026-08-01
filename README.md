# Vendor_Sales_and_Pofitability_Analysis

![Python](https://img.shields.io/badge/Python-EDA%20%7C%20Analysis-blue?logo=python&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboarding-yellow?logo=powerbi&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Portfolio%20Project-black?logo=github)
![EDA](https://img.shields.io/badge/EDA-Exploratory%20Data%20Analysis-green)
![Data Analytics](https://img.shields.io/badge/Data%20Analytics-Insights%20%26%20Visualization-brightgreen)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Future%20Scope-orange)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)


## Project Overview
This project is an end-to-end Data Analytics solution designed to analyze vendor performance by evaluating sales, purchases, profitability, inventory turnover, and operational efficiency. The project demonstrates the complete analytics workflow, beginning with raw CSV data ingestion, data transformation using SQL and Python, exploratory data analysis (EDA), and culminating in an interactive Power BI dashboard for business decision-making.

The objective is to help stakeholders identify high-performing vendors, improve procurement strategies, optimize inventory management, and maximize profitability through data-driven insights.


## Business Problems
Organizations often purchase products from multiple vendors but lack a centralized view of vendor performance. Without meaningful analytics, it becomes difficult to answer questions such as:

- Which vendors generate the highest revenue and profit?
- Which vendors contribute the most to total purchases?
- Are there vendors with high purchase costs but low sales?
- Which products have poor inventory turnover?
- How efficiently is inventory being converted into sales?

This project addresses these challenges by integrating purchasing, sales, pricing, and freight data into a unified analytical model.


## Project Workflow
### 1. Data Ingestion
- Imported multiple CSV datasets into a SQLite database using Python.
- Implemented chunk-based ingestion for efficient processing of large datasets.
- Added logging for monitoring the ingestion process and error handling.

### 2. Data Processing & Feature Engineering
- Combined purchase, sales, and freight information using SQL queries.
- Generated a consolidated vendor summary table.
- Performed data cleaning by handling missing values, correcting data types, and standardizing vendor names.
- Engineered business metrics including:
    - Gross Profit = Total Sales − Total Purchase Dollars
    - Profit Margin = Gross Profit / Total Sales Dollars
    - Sales-to-Purchase Ratio = Total Sales Dollars / Total Purchase Dollars
    - Stock Turnover = Total Sales Quantity / Total Purchase Quantity

### 3. Exploratory Data Analysis (EDA)
Performed statistical and visual analysis to uncover business insights, including:

- Vendor-wise sales and purchase analysis.
- Gross profit analysis.
- Profit margin distribution.
- Purchase contribution (Pareto Analysis).
- Inventory turnover analysis.
- Correlation between purchase cost and sales.
- Detection of high-performing and underperforming vendors.

### 4. Interactive Power BI Dashboard
Developed a dynamic dashboard featuring:

- KPI Cards.
- Scatter Plot for Sales vs. Profit.
- Vendor-wise Profitability Analysis.
- Purchase Contribution Analysis.
- Performance Comparison Visualizations.

<img width="1283" height="722" alt="image" src="https://github.com/user-attachments/assets/78668159-0f89-4842-9286-4c0855478f97" />



## Key Insights
- A small number of top vendors account for a disproportionate share of total procurement spend.
- Bulk purchasing meaningfully lowers unit price, but the benefit plateaus past an optimal order size.
- Some vendors carry high unsold inventory value, tying up capital in slow-moving stock.
- Low-performing vendors show a higher average profit margin range than top-performing vendors — a hypothesis test confirms this difference is statistically significant, suggesting top vendors may be competing on volume/price rather than margin.
