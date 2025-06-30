import random
from typing import Dict, List
from models import StoreState, Product, CustomerPurchase, PRODUCTS

class StoreEngine:
    def __init__(self, starting_cash: float = 100.0):
        self.state = StoreState(
            day=1,
            cash=starting_cash,
            inventory={name: 10 for name in PRODUCTS.keys()},  # Start with 10 of each
            daily_sales={name: 0 for name in PRODUCTS.keys()},
            total_revenue=0.0,
            total_profit=0.0
        )
        self.sales_history = []
        
        # Phase 1B Enhanced: Dynamic Competition System
        self.competitor_prices = {
            "Coke": 2.10,
            "Chips": 1.95, 
            "Candy": 2.20,
            "Water": 1.80,
            "Gum": 2.05
        }
        self.current_prices = {name: product.price for name, product in PRODUCTS.items()}
        
        # Dynamic competitor state tracking
        self.competitor_last_prices = self.competitor_prices.copy()
        self.price_war_intensity = 0  # 0-10 scale of how aggressive competition is
        self.competitor_reactions = []  # Track competitor moves for analysis
        
    def simulate_customers(self) -> List[CustomerPurchase]:
        """Phase 1B: Price-sensitive customer simulation"""
        customers = []
        base_customers = random.randint(10, 20)  # Base customer count
        
        # Adjust customer count based on overall pricing competitiveness
        avg_price_ratio = sum(self.current_prices[name] / self.competitor_prices[name] 
                             for name in PRODUCTS.keys()) / len(PRODUCTS)
        
        # If we're more expensive overall, fewer customers visit
        if avg_price_ratio > 1.1:  # 10% more expensive
            num_customers = max(5, int(base_customers * 0.8))
        elif avg_price_ratio < 0.9:  # 10% cheaper  
            num_customers = min(25, int(base_customers * 1.2))
        else:
            num_customers = base_customers
        
        for _ in range(num_customers):
            # Each customer buys 1-3 items based on price attractiveness
            num_items = random.randint(1, 3)
            purchase_items = []
            total_spent = 0.0
            
            for _ in range(num_items):
                # Pick random product
                product_name = random.choice(list(PRODUCTS.keys()))
                
                # Check if in stock
                if self.state.inventory[product_name] > 0:
                    # Price sensitivity: compare our price to competitor
                    our_price = self.current_prices[product_name]
                    competitor_price = self.competitor_prices[product_name]
                    price_ratio = our_price / competitor_price
                    
                    # Customer decision based on price competitiveness
                    if price_ratio <= 0.95:  # 5% cheaper or more
                        buy_probability = 0.9  # Very likely to buy
                    elif price_ratio <= 1.0:  # Equal or slightly cheaper
                        buy_probability = 0.8
                    elif price_ratio <= 1.1:  # Up to 10% more expensive
                        buy_probability = 0.6
                    elif price_ratio <= 1.2:  # Up to 20% more expensive
                        buy_probability = 0.3
                    else:  # More than 20% expensive
                        buy_probability = 0.1  # Very unlikely
                    
                    if random.random() < buy_probability:
                        purchase_items.append(product_name)
                        total_spent += our_price
                        
                        # Update inventory and sales
                        self.state.inventory[product_name] -= 1
                        self.state.daily_sales[product_name] += 1
            
            if purchase_items:  # Only add if customer bought something
                customers.append(CustomerPurchase(
                    products=purchase_items,
                    total_spent=total_spent
                ))
        
        return customers
    
    def process_orders(self, orders: Dict[str, int]) -> Dict[str, str]:
        """Process LLM's ordering decisions"""
        results = {}
        total_cost = 0.0
        
        for product_name, quantity in orders.items():
            if product_name not in PRODUCTS:
                results[product_name] = f"ERROR: Unknown product {product_name}"
                continue
                
            cost = PRODUCTS[product_name].cost * quantity
            
            if total_cost + cost > self.state.cash:
                results[product_name] = f"ERROR: Not enough cash for {quantity} {product_name} (need ${cost:.2f})"
                continue
            
            # Process order
            self.state.inventory[product_name] += quantity
            self.state.cash -= cost
            total_cost += cost
            results[product_name] = f"SUCCESS: Ordered {quantity} {product_name} for ${cost:.2f}"
        
        return results
        
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
        """Process end of day - calculate profits, reset daily sales, update competition"""
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
        
        # Update competitor prices based on our moves (price war logic)
        competitor_reactions = self.update_competitor_prices()
        
        day_summary = {
            "day": self.state.day,
            "revenue": daily_revenue,
            "profit": daily_profit,
            "units_sold": sum(self.state.daily_sales.values()),
            "cash_balance": self.state.cash,
            "inventory_status": dict(self.state.inventory),
            "competitor_reactions": competitor_reactions,
            "price_war_intensity": self.price_war_intensity
        }
        
        # Reset for next day
        self.state.daily_sales = {name: 0 for name in PRODUCTS.keys()}
        self.state.day += 1
        
        return day_summary
    
    def get_status(self) -> Dict:
        """Get current store status for LLM"""
        return {
            "day": self.state.day,
            "cash": self.state.cash,
            "inventory": dict(self.state.inventory),
            "products": {name: {"cost": p.cost, "price": self.current_prices[name]} for name, p in PRODUCTS.items()},
            "competitor_prices": dict(self.competitor_prices),
            "stockouts": [name for name, qty in self.state.inventory.items() if qty == 0]
        }
    
    def update_competitor_prices(self):
        """Dynamic competitor reacts to our pricing moves - the heart of price war logic"""
        reactions = []
        
        for product_name in PRODUCTS.keys():
            our_price = self.current_prices[product_name]
            competitor_price = self.competitor_prices[product_name]
            product_cost = PRODUCTS[product_name].cost
            
            # Calculate how much we're undercutting
            price_difference = competitor_price - our_price
            
            # Competitor reaction probability based on how much we undercut
            if price_difference > 0.15:  # We're significantly cheaper
                reaction_chance = 0.8  # 80% chance they'll respond aggressively
                potential_cut = min(0.15, price_difference * 0.7)  # Cut up to 70% of difference
            elif price_difference > 0.10:  # Moderate undercut
                reaction_chance = 0.6  # 60% chance they'll respond
                potential_cut = min(0.10, price_difference * 0.5)  # Cut up to 50% of difference
            elif price_difference > 0.05:  # Small undercut
                reaction_chance = 0.3  # 30% chance they'll respond
                potential_cut = min(0.07, price_difference * 0.4)  # Small response
            else:
                reaction_chance = 0.1  # 10% chance of random adjustment
                potential_cut = random.uniform(-0.05, 0.05)  # Random small change
            
            # Increase reaction chance based on price war intensity
            reaction_chance += (self.price_war_intensity * 0.05)  # +5% per intensity level
            reaction_chance = min(0.95, reaction_chance)  # Cap at 95%
            
            # Roll for reaction
            if random.random() < reaction_chance:
                # Calculate new competitor price
                new_competitor_price = competitor_price - potential_cut
                
                # Competitor minimum price (cost + 40% margin minimum)
                min_competitor_price = product_cost * 1.4
                new_competitor_price = max(min_competitor_price, new_competitor_price)
                
                # Apply the price change
                old_price = self.competitor_prices[product_name]
                self.competitor_prices[product_name] = round(new_competitor_price, 2)
                
                # Track the reaction
                if abs(new_competitor_price - old_price) > 0.01:  # Meaningful change
                    reaction_type = "AGGRESSIVE CUT" if potential_cut > 0.10 else "DEFENSIVE CUT" if potential_cut > 0.05 else "MINOR ADJUSTMENT"
                    reactions.append(f"{product_name}: ${old_price:.2f} → ${new_competitor_price:.2f} ({reaction_type})")
                    
                    # Increase price war intensity when competitor cuts prices
                    if new_competitor_price < old_price:
                        self.price_war_intensity = min(10, self.price_war_intensity + 1)
        
        # Store reactions for analysis
        if reactions:
            self.competitor_reactions.append({
                "day": self.state.day,
                "reactions": reactions,
                "intensity": self.price_war_intensity
            })
        
        # Gradual cooling of price war intensity
        if not reactions and self.price_war_intensity > 0:
            self.price_war_intensity = max(0, self.price_war_intensity - 0.5)
        
        return reactions 