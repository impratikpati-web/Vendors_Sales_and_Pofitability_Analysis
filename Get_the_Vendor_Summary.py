import sqlite3
import pandas as pd
import logging
import os

os.makedirs("logs", exist_ok=True)

# ✅ Named logger — isolated from ingestion_db.py's basicConfig
logger = logging.getLogger("VendorSummary")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/Get_Vendor_Summary.log", mode="a")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logger.addHandler(file_handler)

from ingestion_db import ingest_db  # import AFTER logger setup
from sqlalchemy import create_engine


def create_vendor_summary(conn):
    '''This function will merge the different tables to get the overall summary and adding new columns in the resultant data'''
    vendor_sales_summary = pd.read_sql_query("""WITH FreightSummary as (
    SELECT
        VendorNumber,
        SUM(Freight) as FreightCost
    FROM vendor_invoice
    GROUP BY VendorNumber
),
PurchaseSummary as (
    SELECT
        p.VendorNumber,
        p.VendorName,
        p.Brand,
        p.Description,
        p.PurchasePrice,
        pp.Price as ActualPrice,
        pp.Volume,
        SUM(p.Quantity) as TotalPurchaseQuantity,
        SUM(p.Dollars) as TotalPurchaseDollars
    FROM purchases p
    JOIN purchase_prices pp
        ON p.Brand = pp.Brand
    WHERE p.PurchasePrice > 0
    GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
),
SalesSummary as (
    SELECT
        VendorNo,
        Brand,
        SUM(SalesQuantity) as TotalSalesQuantity,
        SUM(SalesDollars) as TotalSalesDollars,
        SUM(SalesPrice) as TotalSalesPrice,
        SUM(ExciseTax) as TotalExciseTax
    FROM Sales
    GROUP BY VendorNo, Brand
)
SELECT
    ps.VendorNumber,
    ps.VendorName,
    ps.Brand,
    ps.Description,
    ps.PurchasePrice,
    ps.ActualPrice,
    ps.Volume,
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ss.TotalSalesQuantity,
    ss.TotalSalesDollars,
    ss.TotalSalesPrice,
    ss.TotalExciseTax,
    fs.FreightCost
FROM PurchaseSummary ps
LEFT JOIN SalesSummary ss
    ON ps.VendorNumber = ss.VendorNo
    AND ps.Brand = ss.Brand
LEFT JOIN FreightSummary fs
    ON ps.VendorNumber = fs.VendorNumber
ORDER BY ps.TotalPurchaseDollars DESC""", conn)
    return vendor_sales_summary


def clean_data(df):
    '''This function will clean the data'''
    # Changing data type to float
    df['Volume'] = df['Volume'].astype('float64')
    # Filling missing values with zero
    df.fillna(0, inplace=True)
    # Removing space from Categorical column
    df['VendorName'] = df['VendorName'].str.strip()
    # Creating new columns for better analysis
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars']) * 100
    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    df['SalestoPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']
    return df


if __name__ == '__main__':
    conn = sqlite3.connect('inventory.db')
    engine = create_engine('sqlite:///inventory.db')

    logger.info('Creating Vendor Summary Table..')
    summary_df = create_vendor_summary(conn)
    logger.info(f"\n{summary_df.head()}")

    logger.info('Cleaning data....')
    clean_df = clean_data(summary_df)
    logger.info(f"\n{clean_df.head()}")

    logger.info('Ingesting data...')
    ingest_db(clean_df, 'Vendor_Sales_Summary', engine, first_chunk=True)
    logger.info('Completed')