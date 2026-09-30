import csv
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "part1_sql" / "output"
DATABASE = BASE_DIR / "part1_sql" / "meesho_reseller.db"

QUERIES = {
    "monthly_category_revenue.csv": """
        SELECT month, category,
               ROUND(SUM(quantity * unit_price), 2) AS revenue,
               COUNT(*) AS n_orders
        FROM orders
        GROUP BY month, category
        ORDER BY month, category
    """,
    "region_revenue.csv": """
        SELECT r.region,
               ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
               COUNT(*) AS n_orders
        FROM orders AS o
        JOIN resellers AS r ON r.reseller_id = o.reseller_id
        GROUP BY r.region
        ORDER BY r.region
    """,
    "top_resellers.csv": """
        SELECT o.reseller_id, r.reseller_name,
               ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
        FROM orders AS o
        JOIN resellers AS r ON r.reseller_id = o.reseller_id
        GROUP BY o.reseller_id, r.reseller_name
        HAVING total_spend > 50000
        ORDER BY total_spend DESC
        LIMIT 5
    """,
    "zero_order_resellers.csv": """
        SELECT r.reseller_id, r.reseller_name, r.city, r.region
        FROM resellers AS r
        LEFT JOIN orders AS o ON o.reseller_id = r.reseller_id
        WHERE o.order_id IS NULL
        ORDER BY r.reseller_id
    """,
    "left_join_count_demo.csv": """
        SELECT r.reseller_id,
               COUNT(*) AS row_count,
               COUNT(o.order_id) AS order_id_count
        FROM resellers AS r
        LEFT JOIN orders AS o ON o.reseller_id = r.reseller_id
        WHERE r.reseller_id = 'RS024'
        GROUP BY r.reseller_id
    """,
    "june_delivered_aov.csv": """
        SELECT ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS aov
        FROM orders
        WHERE month = 'June' AND status = 'Delivered'
    """,
    "grand_total_revenue.csv": """
        SELECT ROUND(SUM(quantity * unit_price), 2) AS grand_total_revenue
        FROM orders
    """,
}


def export_query(connection, query, output_path):
    cursor = connection.execute(query)
    columns = [description[0] for description in cursor.description]
    with output_path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(columns)
        writer.writerows(cursor.fetchall())


OUTPUT_DIR.mkdir(exist_ok=True)
with sqlite3.connect(DATABASE) as connection:
    for filename, query in QUERIES.items():
        export_query(connection, query, OUTPUT_DIR / filename)
        print(f"Wrote {OUTPUT_DIR / filename}")