import random
from typing import Dict, List
from models import StoreState, Product, CustomerPurchase, PRODUCTS, SUPPLIERS, CustomerType, Customer, CustomerSegmentData, DeliveryOrder, PaymentTerm

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
        """🎯 Phase 1C: Customer Type Segmentation System"""
        customers = []
        base_customers = random.randint(12, 22)  # Slightly increased for segmentation
        
        # Adjust customer count based on overall pricing competitiveness  
        avg_price_ratio = sum(self.current_prices[name] / self.competitor_prices[name] 
                             for name in PRODUCTS.keys()) / len(PRODUCTS)
        
        if avg_price_ratio > 1.1:  # 10% more expensive
            num_customers = max(6, int(base_customers * 0.8))
        elif avg_price_ratio < 0.9:  # 10% cheaper  
            num_customers = min(28, int(base_customers * 1.3))
        else:
            num_customers = base_customers
        
        # 🎯 Phase 1C: Generate customer segments (60% price-sensitive, 40% brand-loyal)
        customer_segments = []
        for i in range(num_customers):
            if random.random() < 0.6:  # 60% price-sensitive
                customer_segments.append(self._create_price_sensitive_customer())
            else:  # 40% brand-loyal
                customer_segments.append(self._create_brand_loyal_customer())
        
        # Simulate each customer's shopping behavior
        for customer in customer_segments:
            purchase = self._simulate_customer_purchase(customer)
            if purchase:  # Only add if customer bought something
                customers.append(purchase)
        
        # Store daily segment analytics
        self._update_segment_analytics(customers)
        
        return customers
    
    def _create_price_sensitive_customer(self) -> Customer:
        """Create price-sensitive customer who always seeks cheapest options"""
        return Customer(
            customer_type=CustomerType.PRICE_SENSITIVE,
            price_sensitivity=random.uniform(1.2, 2.0),  # High price sensitivity
            loyalty_strength=0.0  # No brand loyalty
        )
    
    def _create_brand_loyal_customer(self) -> Customer:
        """Create brand-loyal customer with preferred products"""
        # Each brand-loyal customer has 1-2 preferred products
        num_preferred = random.randint(1, 2)
        preferred_products = random.sample(list(PRODUCTS.keys()), num_preferred)
        
        return Customer(
            customer_type=CustomerType.BRAND_LOYAL,
            preferred_products=preferred_products,
            price_sensitivity=random.uniform(0.3, 0.7),  # Lower price sensitivity
            loyalty_strength=random.uniform(0.7, 0.95)  # Strong loyalty
        )
    
    def _simulate_customer_purchase(self, customer: Customer) -> CustomerPurchase:
        """Simulate individual customer purchase based on their type"""
        purchase_items = []
        total_spent = 0.0
        num_items = random.randint(1, 3)
        
        for _ in range(num_items):
            if customer.customer_type == CustomerType.PRICE_SENSITIVE:
                product_name = self._price_sensitive_product_choice()
            else:  # BRAND_LOYAL
                product_name = self._brand_loyal_product_choice(customer)
            
            if product_name and self.state.inventory[product_name] > 0:
                # Make purchase decision based on customer type
                if self._customer_will_buy(customer, product_name):
                    purchase_items.append(product_name)
                    price = self.current_prices[product_name]
                    total_spent += price
                    
                    # Update inventory and sales
                    self.state.inventory[product_name] -= 1
                    self.state.daily_sales[product_name] += 1
        
        if purchase_items:
            return CustomerPurchase(
                products=purchase_items,
                total_spent=total_spent,
                customer_type=customer.customer_type
            )
        return None
    
    def _price_sensitive_product_choice(self) -> str:
        """Price-sensitive customers choose cheapest available products"""
        # Compare our prices to competitor for each product
        best_deals = []
        for product_name in PRODUCTS.keys():
            our_price = self.current_prices[product_name]
            competitor_price = self.competitor_prices[product_name]
            if our_price <= competitor_price * 1.05:  # Within 5% of competitor
                savings = competitor_price - our_price
                best_deals.append((product_name, savings))
        
        if best_deals:
            # Weight selection toward products with biggest savings
            best_deals.sort(key=lambda x: x[1], reverse=True)
            # 70% chance to pick top 2 deals, 30% chance random from all good deals
            if random.random() < 0.7 and len(best_deals) >= 2:
                return random.choice(best_deals[:2])[0]
            else:
                return random.choice(best_deals)[0]
        else:
            # No good deals available, pick cheapest of our products
            cheapest = min(PRODUCTS.keys(), key=lambda x: self.current_prices[x])
            return cheapest
    
    def _brand_loyal_product_choice(self, customer: Customer) -> str:
        """Brand-loyal customers stick to their preferred products"""
        available_preferred = [p for p in customer.preferred_products 
                              if self.state.inventory[p] > 0]
        
        if available_preferred:
            return random.choice(available_preferred)
        else:
            # If preferred not available, might buy substitute (low probability)
            if random.random() < 0.3:  # 30% chance to buy substitute
                return random.choice(list(PRODUCTS.keys()))
            return None  # Leave without buying
    
    def _customer_will_buy(self, customer: Customer, product_name: str) -> bool:
        """Determine if customer will buy based on their type and price"""
        our_price = self.current_prices[product_name]
        competitor_price = self.competitor_prices[product_name]
        price_ratio = our_price / competitor_price
        
        if customer.customer_type == CustomerType.PRICE_SENSITIVE:
            # Price-sensitive: very unlikely to buy if we're more expensive
            if price_ratio <= 0.95:  # 5% cheaper or more
                return random.random() < 0.95
            elif price_ratio <= 1.0:  # Equal or slightly cheaper  
                return random.random() < 0.85
            elif price_ratio <= 1.1:  # Up to 10% more expensive
                return random.random() < 0.4
            else:  # More than 10% expensive
                return random.random() < 0.1
        
        else:  # BRAND_LOYAL
            # Brand-loyal: less sensitive to price for preferred products
            if product_name in customer.preferred_products:
                loyalty_factor = customer.loyalty_strength
                # Even if expensive, loyalty keeps them buying
                if price_ratio <= 1.2:  # Up to 20% more expensive
                    return random.random() < (0.7 + loyalty_factor * 0.3)
                else:  # Very expensive
                    return random.random() < loyalty_factor * 0.5
            else:
                # Non-preferred products: similar to price-sensitive behavior
                return random.random() < max(0.1, 0.8 - price_ratio)
    
    def _update_segment_analytics(self, customers: List[CustomerPurchase]):
        """Track customer segment performance for analytics"""
        if not hasattr(self, 'segment_analytics'):
            self.segment_analytics = {}
        
        day_key = self.state.day
        self.segment_analytics[day_key] = {}
        
        for segment_type in CustomerType:
            segment_customers = [c for c in customers if c.customer_type == segment_type]
            
            self.segment_analytics[day_key][segment_type.value] = CustomerSegmentData(
                segment_type=segment_type,
                daily_customers=len(segment_customers),
                daily_revenue=sum(c.total_spent for c in segment_customers),
                daily_units=sum(len(c.products) for c in segment_customers),
                conversion_rate=len(segment_customers) / max(1, self._get_segment_visitors(segment_type))
            )
    
    def _get_segment_visitors(self, segment_type: CustomerType) -> int:
        """Estimate how many of this segment type visited (for conversion rate calculation)"""
        # Rough estimate based on segment mix (60% price-sensitive, 40% brand-loyal)
        total_visitors = random.randint(15, 25)  # Approximate visitor count
        if segment_type == CustomerType.PRICE_SENSITIVE:
            return int(total_visitors * 0.6)
        else:
            return int(total_visitors * 0.4)
    
    def process_orders(self, orders: Dict[str, int]) -> Dict[str, str]:
        """🏭 Phase 1D: SOPHISTICATED SUPPLIER WARFARE SYSTEM 🏭"""
        results = {}
        
        for product_name, quantity in orders.items():
            if product_name not in PRODUCTS:
                results[product_name] = f"ERROR: Unknown product {product_name}"
                continue
            
            if quantity <= 0:
                results[product_name] = f"ERROR: Invalid quantity {quantity} for {product_name}"
                continue
            
            # 🎯 SUPPLIER SELECTION WARFARE: Choose optimal supplier
            supplier_result = self._select_optimal_supplier(product_name, quantity)
            
            if supplier_result["success"]:
                supplier = supplier_result["supplier"]
                cost_info = supplier_result["cost_info"]
                
                # Create delivery order
                delivery_order = DeliveryOrder(
                    supplier_name=supplier.name,
                    product_name=product_name,
                    quantity=quantity,
                    cost_per_unit=cost_info["cost_per_unit"],
                    total_cost=cost_info["total_cost"],
                    order_day=self.state.day,
                    delivery_day=self.state.day + supplier.delivery_days,
                    payment_terms=supplier.payment_terms,
                    bulk_discount_applied=cost_info["bulk_discount_applied"]
                )
                
                # Process payment based on terms
                if supplier.payment_terms == PaymentTerm.UPFRONT:
                    if cost_info["total_cost"] > self.state.cash:
                        results[product_name] = f"ERROR: Not enough cash for {quantity} {product_name} from {supplier.name} (need ${cost_info['total_cost']:.2f}, have ${self.state.cash:.2f})"
                        continue
                    self.state.cash -= cost_info["total_cost"]
                    payment_info = f"PAID ${cost_info['total_cost']:.2f} upfront"
                else:  # NET_30
                    self.state.accounts_payable += cost_info["total_cost"]
                    payment_info = f"${cost_info['total_cost']:.2f} due in 30 days"
                
                # Add to pending deliveries
                self.state.pending_deliveries.append(delivery_order)
                
                # Build success message with supplier intelligence
                discount_msg = f" (BULK DISCOUNT {cost_info['discount_rate']:.1%})" if cost_info["bulk_discount_applied"] else ""
                results[product_name] = f"SUCCESS: Ordered {quantity} {product_name} from {supplier.name} - Delivery in {supplier.delivery_days} days, {payment_info}{discount_msg}"
            else:
                results[product_name] = supplier_result["error"]
        
        return results
    
    def _select_optimal_supplier(self, product_name: str, quantity: int) -> Dict:
        """🎯 SUPPLIER SELECTION WARFARE: Choose optimal supplier based on strategic factors"""
        if product_name not in SUPPLIERS:
            return {"success": False, "error": f"No suppliers available for {product_name}"}
        
        available_suppliers = SUPPLIERS[product_name]
        base_cost = PRODUCTS[product_name].cost
        
        supplier_options = []
        
        for supplier in available_suppliers:
            # Calculate actual cost with supplier pricing
            cost_per_unit = base_cost * supplier.price_multiplier
            
            # Check for bulk discount
            bulk_discount_applied = quantity >= supplier.bulk_discount_threshold
            if bulk_discount_applied:
                cost_per_unit *= (1 - supplier.bulk_discount_rate)
            
            total_cost = cost_per_unit * quantity
            
            # Strategic scoring system
            # Factors: cost, speed, reliability, cash flow impact
            cost_score = 100 - (supplier.price_multiplier * 50)  # Lower cost = higher score
            speed_score = 100 - (supplier.delivery_days * 20)    # Faster = higher score  
            reliability_score = supplier.reliability * 100       # Higher reliability = higher score
            cash_flow_score = 50 if supplier.payment_terms == PaymentTerm.NET_30 else 0  # NET_30 = cash flow advantage
            
            # Bulk discount bonus
            bulk_bonus = 25 if bulk_discount_applied else 0
            
            # Overall strategic value
            total_score = cost_score + speed_score + reliability_score + cash_flow_score + bulk_bonus
            
            supplier_options.append({
                "supplier": supplier,
                "cost_per_unit": cost_per_unit,
                "total_cost": total_cost,
                "bulk_discount_applied": bulk_discount_applied,
                "discount_rate": supplier.bulk_discount_rate if bulk_discount_applied else 0,
                "strategic_score": total_score,
                "delivery_days": supplier.delivery_days,
                "reliability": supplier.reliability
            })
        
        # Select supplier with highest strategic score
        best_supplier = max(supplier_options, key=lambda x: x["strategic_score"])
        
        return {
            "success": True,
            "supplier": best_supplier["supplier"],
            "cost_info": {
                "cost_per_unit": best_supplier["cost_per_unit"],
                "total_cost": best_supplier["total_cost"],
                "bulk_discount_applied": best_supplier["bulk_discount_applied"],
                "discount_rate": best_supplier["discount_rate"]
            }
        }
    
    def process_deliveries(self) -> List[Dict]:
        """🚚 DELIVERY PROCESSING SYSTEM: Handle incoming deliveries and supply failures"""
        delivery_results = []
        completed_deliveries = []
        
        for delivery in self.state.pending_deliveries:
            if delivery.delivery_day <= self.state.day:
                # Check if delivery succeeds (supplier reliability)
                supplier = next(s for s in SUPPLIERS[delivery.product_name] if s.name == delivery.supplier_name)
                
                if random.random() <= supplier.reliability:
                    # Successful delivery
                    self.state.inventory[delivery.product_name] += delivery.quantity
                    delivery_results.append({
                        "success": True,
                        "product": delivery.product_name,
                        "quantity": delivery.quantity,
                        "supplier": delivery.supplier_name,
                        "cost": delivery.total_cost,
                        "message": f"✅ DELIVERED: {delivery.quantity} {delivery.product_name} from {delivery.supplier_name}"
                    })
                else:
                    # Delivery failed - supplier reliability issue
                    if delivery.payment_terms == PaymentTerm.UPFRONT:
                        # Refund for failed upfront payment
                        self.state.cash += delivery.total_cost
                    else:
                        # Remove from accounts payable
                        self.state.accounts_payable -= delivery.total_cost
                    
                    delivery_results.append({
                        "success": False,
                        "product": delivery.product_name,
                        "quantity": delivery.quantity,
                        "supplier": delivery.supplier_name,
                        "cost": delivery.total_cost,
                        "message": f"❌ DELIVERY FAILED: {delivery.supplier_name} failed to deliver {delivery.quantity} {delivery.product_name} (reliability issue)"
                    })
                
                completed_deliveries.append(delivery)
        
        # Remove completed deliveries
        self.state.pending_deliveries = [d for d in self.state.pending_deliveries if d not in completed_deliveries]
        
        return delivery_results
    
    def process_payment_obligations(self) -> Dict:
        """💰 PAYMENT PROCESSING: Handle NET-30 payment obligations"""
        # For now, we'll assume all NET-30 payments are due immediately at month end
        # In a more complex system, we'd track individual payment due dates
        
        if self.state.accounts_payable > 0:
            if self.state.accounts_payable <= self.state.cash:
                # Pay all outstanding obligations
                paid_amount = self.state.accounts_payable
                self.state.cash -= paid_amount
                self.state.accounts_payable = 0
                return {
                    "success": True,
                    "message": f"💰 PAID NET-30 OBLIGATIONS: ${paid_amount:.2f}",
                    "remaining_payable": 0
                }
            else:
                # Insufficient cash - partial payment or credit issues
                return {
                    "success": False,
                    "message": f"⚠️  CASH FLOW CRISIS: Need ${self.state.accounts_payable:.2f}, only have ${self.state.cash:.2f}",
                    "remaining_payable": self.state.accounts_payable
                }
        
        return {"success": True, "message": "No outstanding obligations", "remaining_payable": 0}
        
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
        delivery_results = self.process_deliveries()
        
        # 💰 Phase 1D: Handle payment obligations (NET-30)
        payment_status = self.process_payment_obligations()
        
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
            "price_war_intensity": self.price_war_intensity,
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
        # 🏭 Phase 1D: Build supplier intelligence briefing
        supplier_info = {}
        for product_name, suppliers_list in SUPPLIERS.items():
            supplier_info[product_name] = []
            for supplier in suppliers_list:
                supplier_info[product_name].append({
                    "name": supplier.name,
                    "price_multiplier": supplier.price_multiplier,
                    "delivery_days": supplier.delivery_days,
                    "reliability": supplier.reliability,
                    "bulk_threshold": supplier.bulk_discount_threshold,
                    "bulk_discount": f"{supplier.bulk_discount_rate:.1%}",
                    "payment_terms": supplier.payment_terms.value
                })
        
        # Pending deliveries summary
        pending_summary = []
        for delivery in self.state.pending_deliveries:
            days_remaining = delivery.delivery_day - self.state.day
            pending_summary.append({
                "product": delivery.product_name,
                "quantity": delivery.quantity,
                "supplier": delivery.supplier_name,
                "days_remaining": days_remaining,
                "total_cost": delivery.total_cost
            })
        
        return {
            "day": self.state.day,
            "cash": self.state.cash,
            "inventory": dict(self.state.inventory),
            "products": {name: {"cost": p.cost, "price": self.current_prices[name]} for name, p in PRODUCTS.items()},
            "competitor_prices": dict(self.competitor_prices),
            "stockouts": [name for name, qty in self.state.inventory.items() if qty == 0],
            # Phase 1D: Supply chain intelligence
            "suppliers": supplier_info,
            "pending_deliveries": pending_summary,
            "accounts_payable": self.state.accounts_payable
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