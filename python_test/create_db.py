import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "sales.db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "test.csv")

def create_and_populate():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS sales;
        CREATE TABLE sales (
            id        INTEGER PRIMARY KEY,
            region    TEXT,
            product   TEXT,
            quantity  INTEGER,
            unit_price REAL,
            sale_date TEXT
        );
        INSERT INTO sales VALUES
            (1,  'North', 'Widget A', 120, 9.99,  '2024-01-05'),
            (2,  'South', 'Widget B',  85, 14.99, '2024-01-08'),
            (3,  'East',  'Widget A',  60, 9.99,  '2024-01-12'),
            (4,  'West',  'Widget C', 200, 4.99,  '2024-01-15'),
            (5,  'North', 'Widget B',  45, 14.99, '2024-02-03'),
            (6,  'South', 'Widget C', 310, 4.99,  '2024-02-10'),
            (7,  'East',  'Widget B',  70, 14.99, '2024-02-18'),
            (8,  'West',  'Widget A',  95, 9.99,  '2024-02-22'),
            (9,  'North', 'Widget C', 150, 4.99,  '2024-03-01'),
            (10, 'South', 'Widget A',  80, 9.99,  '2024-03-14'),
            (11, 'East',  'Widget C', 240, 4.99,  '2024-03-20'),
            (12, 'West',  'Widget B',  55, 14.99, '2024-03-28');
    """)
    conn.commit()
    conn.close()

SQL = """
SELECT
    region,
    product,
    SUM(quantity)              AS total_units,
    ROUND(SUM(quantity * unit_price), 2) AS total_revenue,
    COUNT(*)                   AS num_transactions
FROM sales
GROUP BY region, product
ORDER BY total_revenue DESC;
"""

def export_to_csv():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(SQL, conn)
    conn.close()
    df.to_csv(CSV_PATH, index=False)
    print(f"Saved {len(df)} rows to {CSV_PATH}")
    print(df.to_string(index=False))

if __name__ == "__main__":
    create_and_populate()
    export_to_csv()
