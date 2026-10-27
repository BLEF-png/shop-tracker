import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Category, Product, Sale

# Connect to SQLite source
source_conn = sqlite3.connect('shop.db')
source_cursor = source_conn.cursor()

# Connect to target DB (can be changed to Postgres)
# Replace with: DATABASE_URL = "postgresql://user:password@host/dbname"
DATABASE_URL = "sqlite:///./shop.db" 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Create tables
Base.metadata.create_all(bind=engine)

# Migrate Categories
source_cursor.execute("SELECT * FROM categories")
for row in source_cursor.fetchall():
    db.merge(Category(id=row[0], type=row[1], brand=row[2], strength=row[3], price=row[4], profit=row[5]))

# Migrate Products
source_cursor.execute("SELECT * FROM products")
for row in source_cursor.fetchall():
    db.merge(Product(id=row[0], category_id=row[1], name=row[2], quantity=row[3]))

db.commit()
print("Migration completed!")
source_conn.close()
db.close()
