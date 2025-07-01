from pydantic import BaseModel
from typing import Dict, List, Optional
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

# Phase 1D: Supplier Complexity System
class PaymentTerm(str, Enum):
    UPFRONT = "upfront"
    NET_30 = "net_30"

class Supplier(BaseModel):
    """Supplier with different terms, prices, and reliability"""
    name: str
    reliability: float  # 0.0-1.0, chance of successful delivery
    delivery_days: int  # How many days for delivery
    bulk_discount_threshold: int  # Minimum quantity for bulk discount
    bulk_discount_rate: float  # Percentage discount for bulk orders
    payment_terms: PaymentTerm
    price_multiplier: float  # Multiplier on base product cost

class DeliveryOrder(BaseModel):
    """Pending delivery order"""
    supplier_name: str
    product_name: str
    quantity: int
    cost_per_unit: float
    total_cost: float
    order_day: int
    delivery_day: int
    payment_terms: PaymentTerm
    bulk_discount_applied: bool = False

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
    # Phase 1D: Supplier tracking
    pending_deliveries: List[DeliveryOrder] = []
    accounts_payable: float = 0.0  # Outstanding NET_30 payments
    
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

# Phase 1D: Supplier selection decision
class SupplierOrder(BaseModel):
    supplier_name: str
    product_name: str
    quantity: int
    
# Phase 1A: Ultra-basic product catalog
PRODUCTS = {
    "Coke": Product(name="Coke", cost=1.0, price=2.0),
    "Chips": Product(name="Chips", cost=1.0, price=2.0), 
    "Candy": Product(name="Candy", cost=1.0, price=2.0),
    "Water": Product(name="Water", cost=1.0, price=2.0),
    "Gum": Product(name="Gum", cost=1.0, price=2.0)
}

# Phase 1D: Supplier ecosystem - 2 suppliers per product
SUPPLIERS = {
    "Coke": [
        Supplier(
            name="FastCoke Inc",
            reliability=0.95,
            delivery_days=1,
            bulk_discount_threshold=20,
            bulk_discount_rate=0.10,
            payment_terms=PaymentTerm.UPFRONT,
            price_multiplier=1.0
        ),
        Supplier(
            name="CheapCoke Co",
            reliability=0.85,
            delivery_days=3,
            bulk_discount_threshold=25,
            bulk_discount_rate=0.15,
            payment_terms=PaymentTerm.NET_30,
            price_multiplier=0.85
        )
    ],
    "Chips": [
        Supplier(
            name="CrunchyCorp",
            reliability=0.90,
            delivery_days=1,
            bulk_discount_threshold=15,
            bulk_discount_rate=0.08,
            payment_terms=PaymentTerm.UPFRONT,
            price_multiplier=1.05
        ),
        Supplier(
            name="BudgetChips Ltd",
            reliability=0.80,
            delivery_days=2,
            bulk_discount_threshold=30,
            bulk_discount_rate=0.12,
            payment_terms=PaymentTerm.NET_30,
            price_multiplier=0.90
        )
    ],
    "Candy": [
        Supplier(
            name="SweetSpeed",
            reliability=0.92,
            delivery_days=1,
            bulk_discount_threshold=25,
            bulk_discount_rate=0.10,
            payment_terms=PaymentTerm.UPFRONT,
            price_multiplier=0.98
        ),
        Supplier(
            name="CandyDiscount",
            reliability=0.88,
            delivery_days=3,
            bulk_discount_threshold=40,
            bulk_discount_rate=0.18,
            payment_terms=PaymentTerm.NET_30,
            price_multiplier=0.82
        )
    ],
    "Water": [
        Supplier(
            name="H2O Express",
            reliability=0.96,
            delivery_days=1,
            bulk_discount_threshold=30,
            bulk_discount_rate=0.12,
            payment_terms=PaymentTerm.UPFRONT,
            price_multiplier=1.02
        ),
        Supplier(
            name="AquaSaver",
            reliability=0.85,
            delivery_days=2,
            bulk_discount_threshold=50,
            bulk_discount_rate=0.20,
            payment_terms=PaymentTerm.NET_30,
            price_multiplier=0.78
        )
    ],
    "Gum": [
        Supplier(
            name="ChewFast",
            reliability=0.88,
            delivery_days=1,
            bulk_discount_threshold=20,
            bulk_discount_rate=0.09,
            payment_terms=PaymentTerm.UPFRONT,
            price_multiplier=1.08
        ),
        Supplier(
            name="GumEcon",
            reliability=0.82,
            delivery_days=3,
            bulk_discount_threshold=35,
            bulk_discount_rate=0.16,
            payment_terms=PaymentTerm.NET_30,
            price_multiplier=0.88
        )
    ]
} 