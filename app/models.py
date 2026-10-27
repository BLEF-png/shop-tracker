from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    brand = Column(String)
    strength = Column(String)
    price = Column(Float)
    profit = Column(Float)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String)
    quantity = Column(Integer)
    category = relationship("Category", back_populates="products")

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    product_name = Column(String)
    category_brand = Column(String)
    price = Column(Float)
    profit = Column(Float)
    sold_at = Column(DateTime, default=datetime.datetime.utcnow)
