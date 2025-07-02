from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
from dataclasses import dataclass

# Phase 4B: Multi-Agent System Core Models
class AgentRole(Enum):
    """Specialist agent roles for business management"""
    INVENTORY_MANAGER = "inventory_manager"
    PRICING_ANALYST = "pricing_analyst" 
    CUSTOMER_SERVICE = "customer_service"
    STRATEGIC_PLANNER = "strategic_planner"
    CRISIS_MANAGER = "crisis_manager"

@dataclass
class AgentDecision:
    """Represents a decision made by a specialist agent"""
    agent_role: AgentRole
    decision_type: str
    parameters: Dict[str, Any]
    confidence: float
    reasoning: str
    priority: int  # 1-10, higher = more urgent

# Phase 2C: Crisis Management & Supply Chain Disruptions
class CrisisType(str, Enum):
    NONE = "none"
    SUPPLIER_BANKRUPTCY = "supplier_bankruptcy"
    SUPPLY_SHORTAGE = "supply_shortage"
    DELIVERY_DISRUPTION = "delivery_disruption"
    REGULATORY_CRISIS = "regulatory_crisis"
    ECONOMIC_SHOCK = "economic_shock"
    RAW_MATERIAL_SPIKE = "raw_material_spike"
    COMPETITIVE_DISRUPTION = "competitive_disruption"

class EmergencyAction(str, Enum):
    EMERGENCY_RESTOCK = "emergency_restock"  # Pay premium for immediate delivery
    SWITCH_SUPPLIER = "switch_supplier"      # Emergency supplier change
    RAISE_PRICES = "raise_prices"           # Emergency price increases
    LIQUIDATE_INVENTORY = "liquidate_inventory"  # Emergency clearance sale
    TAKE_LOAN = "take_loan"                 # Emergency cash injection
    COMPETITOR_INTELLIGENCE = "competitor_intelligence"  # Spy on competitor vulnerabilities

class CrisisEvent(BaseModel):
    """Crisis event affecting store operations"""
    crisis_type: CrisisType
    affected_products: List[str] = []  # Products affected by this crisis
    affected_suppliers: List[str] = []  # Suppliers affected by this crisis
    severity: float  # 0.0-1.0, how severe the crisis is
    duration_days: int  # How many days the crisis lasts
    remaining_days: int  # Days remaining
    cost_multiplier: float = 1.0  # Cost increase multiplier
    delivery_delay_multiplier: float = 1.0  # Delivery delay multiplier
    reliability_penalty: float = 0.0  # Reliability reduction (0.0-1.0)
    description: str
    emergency_actions_available: List[str] = []  # Available emergency responses

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
    # Phase 2C: Crisis Management
    active_crises: List[CrisisEvent] = []  # Current active crisis events
    crisis_response_cash: float = 0.0  # Emergency funds from loans/responses
    regulatory_compliance_cost: float = 0.0  # Daily compliance costs from regulatory crises

    # Phase 5A.3: Add budget allocation system
    budget_allocation: Optional['BudgetAllocation'] = None
    
    def initialize_budgets(self, total_daily_budget: float = None):
        """Initialize the budget allocation system"""
        if total_daily_budget is None:
            # Default to 30% of current cash as daily operational budget
            total_daily_budget = self.cash * 0.3
            
        self.budget_allocation = BudgetAllocation(
            total_daily_budget=total_daily_budget,
            agent_budgets={},
            emergency_reserve=self.cash * 0.2  # 20% emergency reserve
        )
        
        # Allocate initial budgets
        self.budget_allocation.allocate_daily_budgets(self.day, self.cash)
    
    def update_daily_budgets(self):
        """Update daily budgets if needed"""
        if self.budget_allocation:
            self.budget_allocation.allocate_daily_budgets(self.day, self.cash)

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

# Crisis-related models are now defined above before StoreState 

@dataclass
class AgentBudget:
    """Fixed budget allocation for each agent domain"""
    agent_role: AgentRole
    daily_budget: float
    remaining_budget: float
    budget_category: str  # "inventory", "pricing", "marketing", "operations"
    auto_replenish: bool = True
    emergency_override_threshold: float = 0.95  # When to allow budget overrides
    
    def can_spend(self, amount: float) -> bool:
        """Check if agent can spend the requested amount"""
        return self.remaining_budget >= amount
    
    def spend(self, amount: float, description: str = "") -> bool:
        """Attempt to spend from budget, returns success"""
        if self.can_spend(amount):
            self.remaining_budget -= amount
            return True
        return False
    
    def get_utilization_rate(self) -> float:
        """Get budget utilization rate (0.0 to 1.0)"""
        if self.daily_budget <= 0:
            return 0.0
        return (self.daily_budget - self.remaining_budget) / self.daily_budget

@dataclass
class BudgetAllocation:
    """Store-wide budget allocation system"""
    total_daily_budget: float
    agent_budgets: Dict[AgentRole, AgentBudget]
    emergency_reserve: float
    last_allocation_day: int = 0
    
    def allocate_daily_budgets(self, current_day: int, store_cash: float):
        """Allocate daily budgets to agents based on store performance"""
        if current_day <= self.last_allocation_day:
            return  # Already allocated today
            
        # Calculate total available for allocation (80% of cash, keep 20% reserve)
        available_budget = min(store_cash * 0.8, self.total_daily_budget)
        
        # Fixed allocation percentages - no more debates!
        allocations = {
            AgentRole.INVENTORY_MANAGER: 0.40,  # 40% - biggest operational need
            AgentRole.PRICING_ANALYST: 0.20,   # 20% - price adjustments
            AgentRole.CUSTOMER_SERVICE: 0.15,  # 15% - customer initiatives  
            AgentRole.STRATEGIC_PLANNER: 0.15,  # 15% - strategic investments
            AgentRole.CRISIS_MANAGER: 0.10     # 10% - emergency response
        }
        
        # Allocate budgets
        for role, percentage in allocations.items():
            budget_amount = available_budget * percentage
            if role in self.agent_budgets:
                self.agent_budgets[role].remaining_budget = budget_amount
                self.agent_budgets[role].daily_budget = budget_amount
            else:
                self.agent_budgets[role] = AgentBudget(
                    agent_role=role,
                    daily_budget=budget_amount,
                    remaining_budget=budget_amount,
                    budget_category=self._get_budget_category(role)
                )
        
        self.last_allocation_day = current_day
        print(f"💰 DAILY BUDGETS ALLOCATED (Day {current_day}): ${available_budget:.2f} total")
        for role, budget in self.agent_budgets.items():
            print(f"   {role.value}: ${budget.daily_budget:.2f}")
    
    def _get_budget_category(self, role: AgentRole) -> str:
        """Get budget category for agent role"""
        categories = {
            AgentRole.INVENTORY_MANAGER: "inventory",
            AgentRole.PRICING_ANALYST: "pricing",
            AgentRole.CUSTOMER_SERVICE: "marketing",
            AgentRole.STRATEGIC_PLANNER: "operations",
            AgentRole.CRISIS_MANAGER: "emergency"
        }
        return categories.get(role, "operations")
    
    def get_budget_summary(self) -> Dict:
        """Get summary of all agent budgets"""
        return {
            "total_allocated": sum(b.daily_budget for b in self.agent_budgets.values()),
            "total_remaining": sum(b.remaining_budget for b in self.agent_budgets.values()),
            "utilization_rate": sum(b.get_utilization_rate() for b in self.agent_budgets.values()) / len(self.agent_budgets),
            "agent_budgets": {
                role.value: {
                    "daily": budget.daily_budget,
                    "remaining": budget.remaining_budget,
                    "utilization": budget.get_utilization_rate()
                }
                for role, budget in self.agent_budgets.items()
            }
        } 