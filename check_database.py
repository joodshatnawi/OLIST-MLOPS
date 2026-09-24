from sqlalchemy import create_engine, text
import pandas as pd

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://olist:olist123@localhost:5432/olist"
)

print("=" * 60)
print("DATABASE INTEGRITY CHECK")
print("=" * 60)

# Test connection
try:
    with engine.connect() as conn:
        print("\n✅ Database connection successful!")
except Exception as e:
    print("\n❌ Database connection failed!")
    print(e)
    exit()

# --------------------------------------------------
# 1. Check tables and row counts
# --------------------------------------------------

tables = [
    "customers",
    "geolocation",
    "orders",
    "order_items",
    "order_payments",
    "products",
    "sellers",
    "orders_reviews",
    "product_category_name_translation"
]

print("\n" + "=" * 60)
print("1. TABLE ROW COUNTS")
print("=" * 60)

for table in tables:
    query = text(f'SELECT COUNT(*) FROM "{table}"')

    with engine.connect() as conn:
        count = conn.execute(query).scalar()

    print(f"{table}: {count:,} rows")


# --------------------------------------------------
# 2. Check duplicate primary IDs
# --------------------------------------------------

print("\n" + "=" * 60)
print("2. DUPLICATE KEY CHECK")
print("=" * 60)

primary_keys = {
    "customers": "customer_id",
    "orders": "order_id",
    "products": "product_id",
    "sellers": "seller_id",
}

for table, column in primary_keys.items():

    query = text(f'''
        SELECT "{column}", COUNT(*)
        FROM "{table}"
        GROUP BY "{column}"
        HAVING COUNT(*) > 1
    ''')

    with engine.connect() as conn:
        result = conn.execute(query).fetchall()

    if len(result) == 0:
        print(f"✅ {table}.{column}: No duplicates")
    else:
        print(f"❌ {table}.{column}: {len(result)} duplicate values")


# --------------------------------------------------
# 3. Check NULL values in important columns
# --------------------------------------------------

print("\n" + "=" * 60)
print("3. NULL CHECK")
print("=" * 60)

important_columns = {
    "customers": ["customer_id", "customer_unique_id"],
    "orders": ["order_id", "customer_id"],
    "products": ["product_id"],
    "sellers": ["seller_id"],
    "order_items": ["order_id", "product_id", "seller_id"],
    "order_payments": ["order_id"],
    "orders_reviews": ["review_id", "order_id"],
}

for table, columns in important_columns.items():

    for column in columns:

        query = text(f'''
            SELECT COUNT(*)
            FROM "{table}"
            WHERE "{column}" IS NULL
        ''')

        with engine.connect() as conn:
            null_count = conn.execute(query).scalar()

        if null_count == 0:
            print(f"✅ {table}.{column}: No NULLs")
        else:
            print(f"⚠️ {table}.{column}: {null_count:,} NULL values")


# --------------------------------------------------
# 4. Foreign Key consistency checks
# --------------------------------------------------

print("\n" + "=" * 60)
print("4. FOREIGN KEY CHECK")
print("=" * 60)

foreign_keys = [
    ("orders", "customer_id", "customers", "customer_id"),
    ("order_items", "order_id", "orders", "order_id"),
    ("order_items", "product_id", "products", "product_id"),
    ("order_items", "seller_id", "sellers", "seller_id"),
    ("order_payments", "order_id", "orders", "order_id"),
    ("orders_reviews", "order_id", "orders", "order_id"),
]

for child_table, child_column, parent_table, parent_column in foreign_keys:

    query = text(f'''
        SELECT COUNT(*)
        FROM "{child_table}" c
        LEFT JOIN "{parent_table}" p
        ON c."{child_column}" = p."{parent_column}"
        WHERE p."{parent_column}" IS NULL
    ''')

    with engine.connect() as conn:
        orphan_count = conn.execute(query).scalar()

    if orphan_count == 0:
        print(
            f"✅ {child_table}.{child_column} → "
            f"{parent_table}.{parent_column}: OK"
        )
    else:
        print(
            f"❌ {child_table}.{child_column} → "
            f"{parent_table}.{parent_column}: "
            f"{orphan_count:,} unmatched rows"
        )


# --------------------------------------------------
# 5. Database tables list
# --------------------------------------------------

print("\n" + "=" * 60)
print("5. DATABASE TABLES")
print("=" * 60)

query = text("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    ORDER BY table_name;
""")

with engine.connect() as conn:
    db_tables = [row[0] for row in conn.execute(query)]

for table in db_tables:
    print(f"✅ {table}")

print("\n" + "=" * 60)
print("CHECK COMPLETED")
print("=" * 60)