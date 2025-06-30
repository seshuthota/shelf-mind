from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime
from enum import Enum

# Phase 1C: Customer Type System
class CustomerType(str, Enum):
    PRICE_SENSITIVE = "price_sensitive"
    BRAND_LOYAL = "brand_loyal"

class Customer(BaseModel):
    """Individual customer with behavioral traits"""
    customer_type: CustomerType
    preferred_products: List[str] = []  # For brand-loyal customers
    price_sensitivity: float = 1.0  # Multiplier for price decisions
    loyalty_strength: float = 0.5  # How strong brand loyalty is (0-1)

class Product(BaseModel):
    name: str
    cost: float
    price: float
    
class InventoryItem(BaseModel):
    product_name: str
    quantity: int
    
class StoreState(BaseModel):
    day: int
    cash: float
    inventory: Dict[str, int]  # product_name -> quantity
    daily_sales: Dict[str, int]  # product_name -> units_sold
    total_revenue: float
    total_profit: float
    
class CustomerPurchase(BaseModel):
    products: List[str]
    total_spent: float
    customer_type: CustomerType  # Track which segment made purchase
    
class StoreDecision(BaseModel):
    day: int
    orders: Dict[str, int]  # product_name -> quantity_to_order
    reasoning: str

# Customer segment analytics
class CustomerSegmentData(BaseModel):
    segment_type: CustomerType
    daily_customers: int
    daily_revenue: float
    daily_units: int
    conversion_rate: float  # % who actually bought something
    
# Phase 1A: Ultra-basic product catalog
PRODUCTS = {
    "Coke": Product(name="Coke", cost=1.0, price=2.0),
    "Chips": Product(name="Chips", cost=1.0, price=2.0), 
    "Candy": Product(name="Candy", cost=1.0, price=2.0),
    "Water": Product(name="Water", cost=1.0, price=2.0),
    "Gum": Product(name="Gum", cost=1.0, price=2.0)
} 