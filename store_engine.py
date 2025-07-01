from typing import Dict, List
from models import StoreState, Product, CustomerPurchase, PRODUCTS, SUPPLIERS, CustomerType, Customer, CustomerSegmentData, DeliveryOrder, PaymentTerm
from customer_engine import CustomerEngine
from competitor_engine import CompetitorEngine
from supplier_engine import SupplierEngine


class StoreEngine:
    """🏆 Refactored Store Engine - Clean Architecture with Specialized Engines
    
    Previously 788 lines of bloated code - now clean and focused!
    Delegates to specialized engines for:
    - CustomerEngine: Customer simulation & segmentation
    - CompetitorEngine: Ultra-aggressive competitor AI
    - SupplierEngine: Supplier management & delivery system
    """
    
    def __init__(self, starting_cash: float = 100.0):
        # Core store state
        self.state = StoreState(
            day=1,
            cash=starting_cash,
            inventory={name: 10 for name in PRODUCTS.keys()},  # Start with 10 of each
            daily_sales={name: 0 for name in PRODUCTS.keys()},
            total_revenue=0.0,
            total_profit=0.0
        )
        self.sales_history = []
        self.current_prices = {name: product.price for name, product in PRODUCTS.items()}
        
        # Initialize specialized engines
        self.customer_engine = CustomerEngine()
        self.competitor_engine = CompetitorEngine()
        self.supplier_engine = SupplierEngine()
        
    def simulate_customers(self) -> List[CustomerPurchase]:
        """🎯 Phase 1C: Customer Type Segmentation System - Delegated to CustomerEngine"""
        customers, daily_sales = self.customer_engine.simulate_customers(
            current_prices=self.current_prices,
            competitor_prices=self.competitor_engine.competitor_prices,
            inventory=self.state.inventory,
            day=self.state.day
        )
        
        # Update daily sales
        for product_name, quantity in daily_sales.items():
            self.state.daily_sales[product_name] += quantity
            
        return customers
    
    def process_orders(self, orders: Dict[str, int]) -> Dict[str, str]:
        """🏭 Phase 1D: SOPHISTICATED SUPPLIER WARFARE SYSTEM - Delegated to SupplierEngine"""
        return self.supplier_engine.process_orders(orders, self.state)
    
    def set_prices(self, new_prices: Dict[str, float]) -> Dict[str, str]:
        """Phase 1B: Set new prices for products"""
        results = {}
        
        for product_name, new_price in new_prices.items():
            if product_name not in PRODUCTS:
                results[product_name] = f"ERROR: Unknown product {product_name}"
                continue
                
            min_price = PRODUCTS[product_name].cost * 1.01  # Must be profitable
            if new_price < min_price:
                results[product_name] = f"ERROR: Price ${new_price:.2f} too low for {product_name} (min ${min_price:.2f})"
                continue
                
            old_price = self.current_prices[product_name]
            self.current_prices[product_name] = new_price
            results[product_name] = f"SUCCESS: {product_name} price changed from ${old_price:.2f} to ${new_price:.2f}"
        
        return results
    
    def end_day(self) -> Dict:
        """Process end of day - calculate profits, reset daily sales, update competition, process deliveries"""
        daily_revenue = sum(
            self.state.daily_sales[name] * self.current_prices[name] 
            for name in PRODUCTS.keys()
        )
        daily_cost = sum(
            self.state.daily_sales[name] * PRODUCTS[name].cost 
            for name in PRODUCTS.keys()
        )
        daily_profit = daily_revenue - daily_cost
        
        self.state.cash += daily_revenue
        self.state.total_revenue += daily_revenue
        self.state.total_profit += daily_profit
        
        # 🚚 Phase 1D: Process incoming deliveries
        delivery_results = self.supplier_engine.process_deliveries(self.state)
        
        # 💰 Phase 1D: Handle payment obligations (NET-30)
        payment_status = self.supplier_engine.process_payment_obligations(self.state)
        
        # Update competitor prices based on our moves (price war logic)
        competitor_reactions = self.competitor_engine.update_competitor_prices(self.current_prices, self.state.day)
        
        day_summary = {
            "day": self.state.day,
            "revenue": daily_revenue,
            "profit": daily_profit,
            "units_sold": sum(self.state.daily_sales.values()),
            "cash_balance": self.state.cash,
            "inventory_status": dict(self.state.inventory),
            "competitor_reactions": competitor_reactions,
            "price_war_intensity": self.competitor_engine.price_war_intensity,
            # Phase 1D: Supply chain intelligence
            "deliveries": delivery_results,
            "pending_deliveries": len(self.state.pending_deliveries),
            "accounts_payable": self.state.accounts_payable,
            "payment_status": payment_status
        }
        
        # Reset for next day
        self.state.daily_sales = {name: 0 for name in PRODUCTS.keys()}
        self.state.day += 1
        
        return day_summary
    
    def get_status(self) -> Dict:
        """Get current store status for LLM with Phase 1D supplier intelligence"""
        return {
            "day": self.state.day,
            "cash": self.state.cash,
            "inventory": dict(self.state.inventory),
            "products": {name: {"cost": p.cost, "price": self.current_prices[name]} for name, p in PRODUCTS.items()},
            "competitor_prices": dict(self.competitor_engine.competitor_prices),
            "stockouts": [name for name, qty in self.state.inventory.items() if qty == 0],
            # Phase 1D: Supply chain intelligence
            "suppliers": self.supplier_engine.get_supplier_info(),
            "pending_deliveries": self.supplier_engine.get_pending_deliveries_summary(self.state),
            "accounts_payable": self.state.accounts_payable
        }
    
    # Convenience properties to maintain compatibility with existing code
    @property
    def competitor_prices(self) -> Dict[str, float]:
        """Access competitor prices through the engine"""
        return self.competitor_engine.competitor_prices
    
    @property
    def price_war_intensity(self) -> float:
        """Access price war intensity through the engine"""
        return self.competitor_engine.price_war_intensity
    
    @property
    def competitor_strategy(self) -> str:
        """Access competitor strategy through the engine"""
        return self.competitor_engine.competitor_strategy
    
    @property
    def competitor_revenge_mode(self) -> bool:
        """Access competitor revenge mode through the engine"""
        return self.competitor_engine.competitor_revenge_mode
    
    @property
    def competitor_reactions(self) -> List:
        """Access competitor reactions through the engine"""
        return self.competitor_engine.competitor_reactions
    
    @property
    def segment_analytics(self) -> Dict:
        """Access customer segment analytics through the engine"""
        return self.customer_engine.segment_analytics 