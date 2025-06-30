from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime

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
    
class StoreDecision(BaseModel):
    day: int
    orders: Dict[str, int]  # product_name -> quantity_to_order
    reasoning: str
    
# Phase 1A: Ultra-basic product catalog
PRODUCTS = {
    "Coke": Product(name="Coke", cost=1.0, price=2.0),
    "Chips": Product(name="Chips", cost=1.0, price=2.0), 
    "Candy": Product(name="Candy", cost=1.0, price=2.0),
    "Water": Product(name="Water", cost=1.0, price=2.0),
    "Gum": Product(name="Gum", cost=1.0, price=2.0)
} 