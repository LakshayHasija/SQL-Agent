from sqlalchemy import create_engine, text
import pandas as pd

DB_PATH = "ecommerce.db"
ENGINE = create_engine(f"sqlite:///{DB_PATH}")

def init_db():
    with ENGINE.connect() as conn:

        conn.execute(text("DROP TABLE IF EXISTS customers"))
        conn.execute(text("DROP TABLE IF EXISTS products"))
        conn.execute(text("DROP TABLE IF EXISTS orders"))
        conn.execute(text("DROP TABLE IF EXISTS order_items"))

        conn.execute(text("""
            CREATE TABLE customers (
                customer_id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                city TEXT,
                signup_date TEXT
            )
        """))

        conn.execute(text("""
            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                price REAL,
                stock INTEGER
            )
        """))

        conn.execute(text("""
            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                order_date TEXT,
                status TEXT,
                total_amount REAL
            )
        """))

        conn.execute(text("""
            CREATE TABLE order_items (
                item_id INTEGER PRIMARY KEY,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                unit_price REAL
            )
        """))

        # --- Sample Data ---
        conn.execute(text("""
            INSERT INTO customers VALUES
            (1, 'Rahul Sharma', 'rahul@gmail.com', 'Delhi', '2023-01-15'),
            (2, 'Priya Singh', 'priya@gmail.com', 'Mumbai', '2023-03-22'),
            (3, 'Amit Verma', 'amit@gmail.com', 'Bangalore', '2023-05-10'),
            (4, 'Sneha Patel', 'sneha@gmail.com', 'Ahmedabad', '2023-07-18'),
            (5, 'Karan Mehta', 'karan@gmail.com', 'Delhi', '2023-09-05'),
            (6, 'Neha Gupta', 'neha@gmail.com', 'Pune', '2024-01-12'),
            (7, 'Rohit Joshi', 'rohit@gmail.com', 'Hyderabad', '2024-02-28'),
            (8, 'Ananya Das', 'ananya@gmail.com', 'Kolkata', '2024-03-15')
        """))

        conn.execute(text("""
            INSERT INTO products VALUES
            (1, 'iPhone 15', 'Electronics', 79999, 50),
            (2, 'Samsung TV 55inch', 'Electronics', 54999, 30),
            (3, 'Nike Air Max', 'Footwear', 8999, 100),
            (4, 'Levi Jeans', 'Clothing', 3499, 200),
            (5, 'Laptop Dell XPS', 'Electronics', 120000, 20),
            (6, 'Whirlpool Washing Machine', 'Appliances', 35000, 15),
            (7, 'Boat Headphones', 'Electronics', 2999, 150),
            (8, 'Yoga Mat', 'Fitness', 999, 300)
        """))

        conn.execute(text("""
            INSERT INTO orders VALUES
            (1, 1, '2024-01-10', 'Delivered', 79999),
            (2, 2, '2024-01-15', 'Delivered', 54999),
            (3, 3, '2024-02-01', 'Shipped', 8999),
            (4, 1, '2024-02-14', 'Delivered', 3499),
            (5, 4, '2024-03-05', 'Cancelled', 120000),
            (6, 5, '2024-03-18', 'Delivered', 35000),
            (7, 6, '2024-04-02', 'Shipped', 2999),
            (8, 7, '2024-04-20', 'Pending', 999),
            (9, 2, '2024-05-01', 'Delivered', 8999),
            (10, 8, '2024-05-15', 'Delivered', 120000)
        """))

        conn.execute(text("""
            INSERT INTO order_items VALUES
            (1, 1, 1, 1, 79999),
            (2, 2, 2, 1, 54999),
            (3, 3, 3, 1, 8999),
            (4, 4, 4, 1, 3499),
            (5, 5, 5, 1, 120000),
            (6, 6, 6, 1, 35000),
            (7, 7, 7, 1, 2999),
            (8, 8, 8, 1, 999),
            (9, 9, 3, 1, 8999),
            (10, 10, 5, 1, 120000)
        """))

        conn.commit()
        print("✅ Database initialized successfully!")

def get_schema() -> str:
    schema = ""
    with ENGINE.connect() as conn:
        tables = ["customers", "products", "orders", "order_items"]
        for table in tables:
            result = conn.execute(text(f"PRAGMA table_info({table})"))
            cols = result.fetchall()
            col_str = ", ".join([f"{c[1]} ({c[2]})" for c in cols])
            schema += f"Table: {table}\nColumns: {col_str}\n\n"
    return schema

def run_query(sql: str) -> pd.DataFrame:
    with ENGINE.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        cols = result.keys()
        return pd.DataFrame(rows, columns=cols)

if __name__ == "__main__":
    init_db()