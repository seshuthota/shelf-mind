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

# Phase 2A: Product Categories and Spoilage
class ProductCategory(str, Enum):
    BEVERAGES = "beverages"
    SNACKS = "snacks" 
    FRESH_FOOD = "fresh_food"
    FROZEN = "frozen"
    CANDY = "candy"

class Product(BaseModel):
    name: str
    cost: float
    price: float
    category: ProductCategory
    shelf_life_days: Optional[int] = None  # None = never spoils, int = days until spoilage
    seasonal_multiplier: Dict[str, float] = {}  # Season name -> demand multiplier

# Phase 2A: Inventory with spoilage tracking
class InventoryBatch(BaseModel):
    """Track inventory batches with expiration dates"""
    quantity: int
    received_day: int
    expiration_day: Optional[int] = None  # None if doesn't spoil
    
class InventoryItem(BaseModel):
    product_name: str
    batches: List[InventoryBatch] = []
    
    @property
    def total_quantity(self) -> int:
        return sum(batch.quantity for batch in self.batches)
    
    def remove_quantity(self, quantity: int, current_day: int) -> int:
        """Remove quantity using FIFO (oldest first), return actual removed"""
        remaining = quantity
        batches_to_remove = []
        
        for i, batch in enumerate(self.batches):
            if remaining <= 0:
                break
                
            # Skip expired batches (they'll be removed separately)
            if batch.expiration_day and current_day >= batch.expiration_day:
                continue
                
            if batch.quantity <= remaining:
                remaining -= batch.quantity
                batches_to_remove.append(i)
            else:
                batch.quantity -= remaining
                remaining = 0
                
        # Remove empty batches (in reverse order to maintain indices)
        for i in reversed(batches_to_remove):
            self.batches.pop(i)
            
        return quantity - remaining
    
    def remove_spoiled(self, current_day: int) -> int:
        """Remove spoiled items, return quantity spoiled"""
        spoiled_quantity = 0
        batches_to_remove = []
        
        for i, batch in enumerate(self.batches):
            if batch.expiration_day and current_day >= batch.expiration_day:
                spoiled_quantity += batch.quantity
                batches_to_remove.append(i)
                
        # Remove spoiled batches
        for i in reversed(batches_to_remove):
            self.batches.pop(i)
            
        return spoiled_quantity
    
class StoreState(BaseModel):
    day: int
    cash: float
    inventory: Dict[str, InventoryItem]  # product_name -> InventoryItem with batches
    daily_sales: Dict[str, int]  # product_name -> units_sold
    daily_spoilage: Dict[str, int] = {}  # product_name -> units_spoiled
    total_revenue: float
    total_profit: float
    total_spoilage_cost: float = 0.0  # Track cost of spoiled inventory
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

# Phase 2A: Spoilage tracking
class SpoilageReport(BaseModel):
    product_name: str
    quantity_spoiled: int
    cost_lost: float
    days_held: int
    
# Phase 2B: EXPANDED PRODUCT CATALOG with Seasonal Demand Patterns
PRODUCTS = {
    # BEVERAGES - Higher demand in summer (heat), lower in winter
    "Coke": Product(
        name="Coke", cost=1.0, price=2.0, category=ProductCategory.BEVERAGES,
        seasonal_multiplier={"spring": 1.0, "summer": 1.4, "fall": 0.9, "winter": 0.8}
    ),
    "Water": Product(
        name="Water", cost=1.0, price=2.0, category=ProductCategory.BEVERAGES,
        seasonal_multiplier={"spring": 1.1, "summer": 1.6, "fall": 0.8, "winter": 0.7}
    ),
    
    # SNACKS - Steady demand with slight spring/summer boost (outdoor activities)
    "Chips": Product(
        name="Chips", cost=1.0, price=2.0, category=ProductCategory.SNACKS,
        seasonal_multiplier={"spring": 1.1, "summer": 1.2, "fall": 1.0, "winter": 0.9}
    ),
    "Crackers": Product(
        name="Crackers", cost=0.8, price=1.75, category=ProductCategory.SNACKS,
        seasonal_multiplier={"spring": 1.0, "summer": 0.9, "fall": 1.1, "winter": 1.2}
    ),
    
    # FRESH FOOD - Sandwiches peak in spring/summer, bananas steady
    "Sandwiches": Product(
        name="Sandwiches", cost=2.5, price=4.5, category=ProductCategory.FRESH_FOOD, 
        shelf_life_days=3,
        seasonal_multiplier={"spring": 1.3, "summer": 1.4, "fall": 0.9, "winter": 0.8}
    ),
    "Bananas": Product(
        name="Bananas", cost=0.5, price=1.2, category=ProductCategory.FRESH_FOOD,
        shelf_life_days=5,
        seasonal_multiplier={"spring": 1.1, "summer": 1.0, "fall": 1.0, "winter": 1.1}
    ),
    
    # FROZEN - Ice cream MASSIVELY seasonal (summer peak!)
    "Ice Cream": Product(
        name="Ice Cream", cost=1.8, price=3.2, category=ProductCategory.FROZEN,
        shelf_life_days=7,
        seasonal_multiplier={"spring": 1.2, "summer": 2.0, "fall": 0.6, "winter": 0.3}
    ),
    
    # CANDY - Chocolate peaks in winter/valentine's, candy steady with holiday spikes
    "Candy": Product(
        name="Candy", cost=1.0, price=2.0, category=ProductCategory.CANDY,
        seasonal_multiplier={"spring": 1.0, "summer": 0.9, "fall": 1.3, "winter": 1.1}
    ),
    "Gum": Product(
        name="Gum", cost=1.0, price=2.0, category=ProductCategory.CANDY,
        seasonal_multiplier={"spring": 1.0, "summer": 1.0, "fall": 1.0, "winter": 1.0}
    ),
    "Chocolate": Product(
        name="Chocolate", cost=1.2, price=2.4, category=ProductCategory.CANDY,
        seasonal_multiplier={"spring": 1.0, "summer": 0.8, "fall": 1.1, "winter": 1.4}
    )
}

# Phase 1D: Supplier ecosystem - 2 suppliers per product (NOW 10 PRODUCTS!)
SUPPLIERS = {
    # BEVERAGES
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
    
    # SNACKS
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
    "Crackers": [
        Supplier(
            name="CrispyCrackers Co",
            reliability=0.88,
            delivery_days=1,
            bulk_discount_threshold=25,
            bulk_discount_rate=0.10,
            payment_terms=PaymentTerm.UPFRONT,
            price_multiplier=1.0
        ),
        Supplier(
            name="ValueCrunch",
            reliability=0.82,
            delivery_days=3,
            bulk_discount_threshold=40,
            bulk_discount_rate=0.18,
            payment_terms=PaymentTerm.NET_30,
            price_multiplier=0.85
        )
    ],
    
    # FRESH FOOD (Critical: Fast delivery for short shelf life!)
    "Sandwiches": [
        Supplier(
            name="FreshFast Deli",
            reliability=0.92,
            delivery_days=1,  # MUST be fast for fresh items
            bulk_discount_threshold=10,
            bulk_discount_rate=0.08,
            payment_terms=PaymentTerm.UPFRONT,
            price_multiplier=1.0
        ),
        Supplier(
            name="BudgetBites",
            reliability=0.75,  # Lower reliability for fresh is dangerous!
            delivery_days=2,
            bulk_discount_threshold=15,
            bulk_discount_rate=0.12,
            payment_terms=PaymentTerm.NET_30,
            price_multiplier=0.90
        )
    ],
    "Bananas": [
        Supplier(
            name="TropicalSpeed",
            reliability=0.90,
            delivery_days=1,
            bulk_discount_threshold=20,
            bulk_discount_rate=0.10,
            payment_terms=PaymentTerm.UPFRONT,
            price_multiplier=1.0
        ),
        Supplier(
            name="FarmDirect",
            reliability=0.85,
            delivery_days=2,
            bulk_discount_threshold=30,
            bulk_discount_rate=0.15,
            payment_terms=PaymentTerm.NET_30,
            price_multiplier=0.88
        )
    ],
    
    # FROZEN (Requires special handling)
    "Ice Cream": [
        Supplier(
            name="FrozenExpress",
            reliability=0.94,
            delivery_days=1,
            bulk_discount_threshold=12,
            bulk_discount_rate=0.09,
            payment_terms=PaymentTerm.UPFRONT,
            price_multiplier=1.05
        ),
        Supplier(
            name="ChillCheap",
            reliability=0.80,
            delivery_days=2,
            bulk_discount_threshold=20,
            bulk_discount_rate=0.14,
            payment_terms=PaymentTerm.NET_30,
            price_multiplier=0.92
        )
    ],
    
    # CANDY
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
    ],
    "Chocolate": [
        Supplier(
            name="CocoaRush",
            reliability=0.90,
            delivery_days=1,
            bulk_discount_threshold=18,
            bulk_discount_rate=0.11,
            payment_terms=PaymentTerm.UPFRONT,
            price_multiplier=1.02
        ),
        Supplier(
            name="SweetSaver",
            reliability=0.84,
            delivery_days=2,
            bulk_discount_threshold=25,
            bulk_discount_rate=0.16,
            payment_terms=PaymentTerm.NET_30,
            price_multiplier=0.89
        )
    ]
}

# Phase 2B: Seasonal Demand and Market Events
class Season(str, Enum):
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    WINTER = "winter"

class WeatherEvent(str, Enum):
    NORMAL = "normal"
    HEAT_WAVE = "heat_wave"
    COLD_SNAP = "cold_snap"
    RAINY_DAY = "rainy_day"
    PERFECT_WEATHER = "perfect_weather"

class Holiday(str, Enum):
    NONE = "none"
    VALENTINES_DAY = "valentines_day"
    SUMMER_PICNIC = "summer_picnic"
    HALLOWEEN = "halloween"
    WINTER_HOLIDAYS = "winter_holidays"
    SPRING_BREAK = "spring_break"

class EconomicCondition(str, Enum):
    NORMAL = "normal"
    BOOM = "boom"
    RECESSION = "recession"
    RECOVERY = "recovery"

class MarketEvent(BaseModel):
    """Daily market conditions affecting demand"""
    day: int
    season: Season
    weather: WeatherEvent
    holiday: Holiday
    economic_condition: EconomicCondition
    description: str
    demand_multiplier: float  # Overall market demand modifier

# Phase 2A: Product Categories and Spoilage 