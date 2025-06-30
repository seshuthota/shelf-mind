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
        
        # Phase 1B Enhanced: ULTRA-AGGRESSIVE Competition System
        self.competitor_prices = {
            "Coke": 2.10,
            "Chips": 1.95, 
            "Candy": 2.20,
            "Water": 1.80,
            "Gum": 2.05
        }
        self.current_prices = {name: product.price for name, product in PRODUCTS.items()}
        
        # Enhanced competitor intelligence and aggression tracking
        self.competitor_last_prices = self.competitor_prices.copy()
        self.price_war_intensity = 0  # 0-10 scale of how vicious the war is
        self.competitor_reactions = []
        self.competitor_strategy = "BALANCED"  # Changes daily: AGGRESSIVE, DEFENSIVE, PREDATORY, PSYCHOLOGICAL
        self.competitor_cash_reserves = 500.0  # Competitor has deep pockets
        self.days_since_last_attack = 0  # Tracks when competitor last initiated
        self.our_total_undercuts = 0  # Tracks how much we've been undercutting
        self.competitor_revenge_mode = False  # Special mode when competitor gets really pissed
        
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
        """🔥 ULTRA-AGGRESSIVE competitor that will make Scrooge sweat bullets! 🔥"""
        reactions = []
        
        # Update competitor's daily strategy - they adapt and get nastier
        self._update_competitor_strategy()
        
        # Track our aggressive behavior
        self._track_our_undercuts()
        
        # Phase 1: Reactive responses to our moves
        reactive_moves = self._execute_reactive_strategy()
        reactions.extend(reactive_moves)
        
        # Phase 2: Proactive attacks (competitor initiates fights!)
        proactive_moves = self._execute_proactive_strategy()
        reactions.extend(proactive_moves)
        
        # Phase 3: Psychological warfare and dirty tactics
        psychological_moves = self._execute_psychological_warfare()
        reactions.extend(psychological_moves)
        
        # Update war intensity and revenge mode
        self._update_war_dynamics(reactions)
        
        # Store reactions for Scrooge's analysis
        if reactions:
            self.competitor_reactions.append({
                "day": self.state.day,
                "reactions": reactions,
                "intensity": self.price_war_intensity,
                "strategy": self.competitor_strategy,
                "revenge_mode": self.competitor_revenge_mode
            })
        
        self.days_since_last_attack += 1
        return reactions
    
    def _update_competitor_strategy(self):
        """Competitor adapts their strategy based on market conditions"""
        strategies = ["AGGRESSIVE", "DEFENSIVE", "PREDATORY", "PSYCHOLOGICAL", "BALANCED"]
        
        # Higher war intensity = more aggressive strategies
        if self.price_war_intensity >= 8:
            self.competitor_strategy = random.choice(["PREDATORY", "PSYCHOLOGICAL", "AGGRESSIVE"])
        elif self.price_war_intensity >= 5:
            self.competitor_strategy = random.choice(["AGGRESSIVE", "PREDATORY", "PSYCHOLOGICAL"])
        elif self.price_war_intensity >= 3:
            self.competitor_strategy = random.choice(["AGGRESSIVE", "BALANCED", "DEFENSIVE"])
        else:
            # Sometimes they randomly get aggressive even when things are calm
            if random.random() < 0.15:  # 15% chance of random aggression
                self.competitor_strategy = "AGGRESSIVE"
            else:
                self.competitor_strategy = random.choice(["BALANCED", "DEFENSIVE"])
    
    def _track_our_undercuts(self):
        """Track how much we've been undercutting - builds competitor anger"""
        total_undercuts = 0
        for product_name in PRODUCTS.keys():
            our_price = self.current_prices[product_name]
            competitor_price = self.competitor_prices[product_name]
            if our_price < competitor_price:
                total_undercuts += (competitor_price - our_price)
        
        self.our_total_undercuts += total_undercuts
        
        # Trigger revenge mode if we've been too aggressive
        if self.our_total_undercuts > 1.0 and not self.competitor_revenge_mode:
            self.competitor_revenge_mode = True
            
    def _execute_reactive_strategy(self):
        """Competitor reacts to our pricing moves"""
        reactions = []
        
        for product_name in PRODUCTS.keys():
            our_price = self.current_prices[product_name]
            competitor_price = self.competitor_prices[product_name]
            product_cost = PRODUCTS[product_name].cost
            
            price_difference = competitor_price - our_price
            
            if price_difference <= 0:  # We're not cheaper, skip
                continue
                
            # Calculate reaction intensity based on strategy
            reaction_multiplier = {
                "AGGRESSIVE": 1.2,
                "PREDATORY": 1.5,
                "PSYCHOLOGICAL": 1.0,
                "DEFENSIVE": 0.7,
                "BALANCED": 1.0
            }.get(self.competitor_strategy, 1.0)
            
            # Base reaction chance
            if price_difference > 0.20:
                reaction_chance = 0.95 * reaction_multiplier
                cut_percentage = 0.8  # Cut 80% of difference
            elif price_difference > 0.15:
                reaction_chance = 0.85 * reaction_multiplier
                cut_percentage = 0.7
            elif price_difference > 0.10:
                reaction_chance = 0.70 * reaction_multiplier
                cut_percentage = 0.6
            elif price_difference > 0.05:
                reaction_chance = 0.50 * reaction_multiplier
                cut_percentage = 0.5
            else:
                reaction_chance = 0.25 * reaction_multiplier
                cut_percentage = 0.4
            
            # Revenge mode makes them MUCH more aggressive
            if self.competitor_revenge_mode:
                reaction_chance = min(0.98, reaction_chance * 1.5)
                cut_percentage = min(0.95, cut_percentage * 1.3)
            
            # War intensity boosts reaction chance
            reaction_chance += (self.price_war_intensity * 0.08)
            reaction_chance = min(0.98, reaction_chance)
            
            if random.random() < reaction_chance:
                # Calculate the cut
                potential_cut = price_difference * cut_percentage
                
                # In PREDATORY mode, they sometimes cut BELOW our price!
                if self.competitor_strategy == "PREDATORY" and random.random() < 0.4:
                    potential_cut += random.uniform(0.01, 0.08)  # Undercut us!
                
                new_price = competitor_price - potential_cut
                
                # Competitor minimum price (they'll go as low as cost + 25% in war)
                min_price = product_cost * (1.25 if self.price_war_intensity >= 7 else 1.4)
                new_price = max(min_price, new_price)
                
                old_price = self.competitor_prices[product_name]
                self.competitor_prices[product_name] = round(new_price, 2)
                
                if abs(new_price - old_price) > 0.01:
                    # Determine reaction type
                    if potential_cut > 0.15:
                        reaction_type = "💀 NUCLEAR STRIKE"
                    elif potential_cut > 0.10:
                        reaction_type = "⚔️ AGGRESSIVE ASSAULT"
                    elif potential_cut > 0.05:
                        reaction_type = "🔥 FIERCE COUNTER"
                    else:
                        reaction_type = "⚡ QUICK STRIKE"
                        
                    reactions.append(f"{product_name}: ${old_price:.2f} → ${new_price:.2f} ({reaction_type})")
        
        return reactions
    
    def _execute_proactive_strategy(self):
        """Competitor initiates price cuts to start fights!"""
        reactions = []
        
        # Don't attack every day - make it strategic
        attack_chance = {
            "AGGRESSIVE": 0.35,
            "PREDATORY": 0.45,
            "PSYCHOLOGICAL": 0.25,
            "DEFENSIVE": 0.05,
            "BALANCED": 0.15
        }.get(self.competitor_strategy, 0.15)
        
        # More likely to attack if it's been a while
        attack_chance += (self.days_since_last_attack * 0.05)
        
        # Revenge mode makes them attack more often
        if self.competitor_revenge_mode:
            attack_chance *= 1.8
            
        if random.random() < attack_chance:
            # Pick 1-3 products to attack
            num_attacks = random.randint(1, 3)
            products_to_attack = random.sample(list(PRODUCTS.keys()), num_attacks)
            
            for product_name in products_to_attack:
                old_price = self.competitor_prices[product_name]
                product_cost = PRODUCTS[product_name].cost
                our_price = self.current_prices[product_name]
                
                # Different attack strategies
                if self.competitor_strategy == "PREDATORY":
                    # Cut to just above cost to crush margins
                    new_price = max(product_cost * 1.25, old_price * 0.85)
                elif self.competitor_strategy == "AGGRESSIVE":
                    # Standard aggressive cut
                    new_price = max(product_cost * 1.3, old_price * 0.9)
                else:
                    # Moderate cut to test our response
                    new_price = max(product_cost * 1.4, old_price * 0.95)
                
                # Sometimes aim to just undercut us
                if our_price < old_price and random.random() < 0.6:
                    new_price = max(new_price, our_price - random.uniform(0.01, 0.05))
                
                self.competitor_prices[product_name] = round(new_price, 2)
                
                if abs(new_price - old_price) > 0.01:
                    attack_type = "🚀 SURPRISE ATTACK" if self.competitor_strategy == "PREDATORY" else "⚡ PROACTIVE STRIKE"
                    reactions.append(f"{product_name}: ${old_price:.2f} → ${new_price:.2f} ({attack_type})")
                    
            if reactions:
                self.days_since_last_attack = 0
        
        return reactions
    
    def _execute_psychological_warfare(self):
        """Dirty tactics to mess with Scrooge's head"""
        reactions = []
        
        if self.competitor_strategy != "PSYCHOLOGICAL":
            return reactions
            
        # Psychological tactics
        if random.random() < 0.3:  # 30% chance of psychological move
            tactic = random.choice([
                "FAKE_RETREAT",  # Raise prices to make us think we won, then attack
                "LOSS_LEADER",   # Cut one product to loss to steal customers
                "RANDOM_CHAOS"   # Make unpredictable moves to confuse
            ])
            
            if tactic == "FAKE_RETREAT":
                # Raise prices on 1-2 products to fake weakness
                products = random.sample(list(PRODUCTS.keys()), random.randint(1, 2))
                for product_name in products:
                    old_price = self.competitor_prices[product_name]
                    new_price = min(old_price * 1.1, PRODUCTS[product_name].cost * 2.0)
                    self.competitor_prices[product_name] = round(new_price, 2)
                    reactions.append(f"{product_name}: ${old_price:.2f} → ${new_price:.2f} (🎭 FAKE RETREAT)")
                    
            elif tactic == "LOSS_LEADER":
                # Cut one product to barely above cost
                product_name = random.choice(list(PRODUCTS.keys()))
                old_price = self.competitor_prices[product_name]
                cost = PRODUCTS[product_name].cost
                new_price = cost * 1.15  # Very low margin
                self.competitor_prices[product_name] = round(new_price, 2)
                reactions.append(f"{product_name}: ${old_price:.2f} → ${new_price:.2f} (🎯 LOSS LEADER)")
                
            elif tactic == "RANDOM_CHAOS":
                # Make seemingly random moves to confuse
                for product_name in PRODUCTS.keys():
                    if random.random() < 0.4:  # 40% chance per product
                        old_price = self.competitor_prices[product_name]
                        change = random.uniform(-0.08, 0.08)
                        new_price = max(PRODUCTS[product_name].cost * 1.2, old_price + change)
                        self.competitor_prices[product_name] = round(new_price, 2)
                        if abs(new_price - old_price) > 0.01:
                            reactions.append(f"{product_name}: ${old_price:.2f} → ${new_price:.2f} (🌀 CHAOS THEORY)")
        
        return reactions
    
    def _update_war_dynamics(self, reactions):
        """Update war intensity and competitor state"""
        if reactions:
            # War escalates with each move
            escalation = len(reactions) * 0.5
            
            # Different strategies escalate differently
            if self.competitor_strategy == "PREDATORY":
                escalation *= 1.5
            elif self.competitor_strategy == "PSYCHOLOGICAL":
                escalation *= 0.8
                
            self.price_war_intensity = min(10, self.price_war_intensity + escalation)
        else:
            # War cools down slowly if no moves
            self.price_war_intensity = max(0, self.price_war_intensity - 0.3)
            
        # Exit revenge mode occasionally
        if self.competitor_revenge_mode and random.random() < 0.1:
            self.competitor_revenge_mode = False
            self.our_total_undercuts *= 0.7  # Reduce anger 