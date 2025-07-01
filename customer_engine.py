import random
from typing import Dict, List, Optional
from models import CustomerPurchase, Customer, CustomerType, CustomerSegmentData, PRODUCTS, MarketEvent


class CustomerEngine:
    """🎯 Phase 1C: Advanced Customer Psychology & Segmentation System"""
    
    def __init__(self):
        self.segment_analytics = {}
    
    def simulate_customers(self, current_prices: Dict[str, float], competitor_prices: Dict[str, float], 
                          inventory: Dict[str, int], day: int, market_event: Optional[MarketEvent] = None) -> List[CustomerPurchase]:
        """🎯 Phase 2B: Customer Type Segmentation with Seasonal Demand"""
        customers = []
        base_customers = random.randint(12, 22)  # Slightly increased for segmentation
        
        # Phase 2B: Apply market event demand multiplier
        if market_event:
            base_customers = int(base_customers * market_event.demand_multiplier)
        
        # Adjust customer count based on overall pricing competitiveness  
        avg_price_ratio = sum(current_prices[name] / competitor_prices[name] 
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
        
        # Track daily sales for updating inventory
        daily_sales = {name: 0 for name in PRODUCTS.keys()}
        
        # Simulate each customer's shopping behavior
        for customer in customer_segments:
            purchase = self._simulate_customer_purchase(customer, current_prices, competitor_prices, inventory, daily_sales, market_event)
            if purchase:  # Only add if customer bought something
                customers.append(purchase)
        
        # Store daily segment analytics
        self._update_segment_analytics(customers, day)
        
        return customers, daily_sales
    
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
    
    def _simulate_customer_purchase(self, customer: Customer, current_prices: Dict[str, float], 
                                   competitor_prices: Dict[str, float], inventory: Dict[str, int],
                                   daily_sales: Dict[str, int], market_event: Optional[MarketEvent] = None) -> CustomerPurchase:
        """Simulate individual customer purchase based on their type"""
        purchase_items = []
        total_spent = 0.0
        num_items = random.randint(1, 3)
        
        for _ in range(num_items):
            if customer.customer_type == CustomerType.PRICE_SENSITIVE:
                product_name = self._price_sensitive_product_choice(current_prices, competitor_prices, market_event)
            else:  # BRAND_LOYAL
                product_name = self._brand_loyal_product_choice(customer, inventory, market_event)
            
            if product_name and inventory[product_name] > 0:
                # Make purchase decision based on customer type and seasonal factors
                if self._customer_will_buy(customer, product_name, current_prices, competitor_prices, market_event):
                    purchase_items.append(product_name)
                    price = current_prices[product_name]
                    total_spent += price
                    
                    # Update inventory and sales
                    inventory[product_name] -= 1
                    daily_sales[product_name] += 1
        
        if purchase_items:
            return CustomerPurchase(
                products=purchase_items,
                total_spent=total_spent,
                customer_type=customer.customer_type
            )
        return None
    
    def _price_sensitive_product_choice(self, current_prices: Dict[str, float], 
                                       competitor_prices: Dict[str, float], market_event: Optional[MarketEvent] = None) -> str:
        """Price-sensitive customers choose cheapest available products with seasonal preferences"""
        # Compare our prices to competitor for each product
        best_deals = []
        for product_name in PRODUCTS.keys():
            our_price = current_prices[product_name]
            competitor_price = competitor_prices[product_name]
            if our_price <= competitor_price * 1.05:  # Within 5% of competitor
                savings = competitor_price - our_price
                
                # Phase 2B: Apply seasonal demand boost
                seasonal_boost = self._get_seasonal_demand_boost(product_name, market_event)
                adjusted_savings = savings * seasonal_boost
                
                best_deals.append((product_name, adjusted_savings))
        
        if best_deals:
            # Weight selection toward products with biggest savings (including seasonal)
            best_deals.sort(key=lambda x: x[1], reverse=True)
            # 70% chance to pick top 2 deals, 30% chance random from all good deals
            if random.random() < 0.7 and len(best_deals) >= 2:
                return random.choice(best_deals[:2])[0]
            else:
                return random.choice(best_deals)[0]
        else:
            # No good deals available, pick cheapest of our products (with seasonal preference)
            cheapest_options = list(PRODUCTS.keys())
            if market_event:
                # Apply seasonal weighting to cheapest product selection
                cheapest_options = self._apply_seasonal_weighting(cheapest_options, market_event)
            cheapest = min(cheapest_options, key=lambda x: current_prices[x])
            return cheapest
    
    def _brand_loyal_product_choice(self, customer: Customer, inventory: Dict[str, int], market_event: Optional[MarketEvent] = None) -> str:
        """Brand-loyal customers stick to their preferred products with seasonal influence"""
        available_preferred = [p for p in customer.preferred_products 
                              if inventory[p] > 0]
        
        if available_preferred:
            # Phase 2B: Weight preferred products by seasonal demand
            if market_event and len(available_preferred) > 1:
                weighted_preferred = self._apply_seasonal_weighting(available_preferred, market_event)
                return random.choice(weighted_preferred)
            else:
                return random.choice(available_preferred)
        else:
            # If preferred not available, might buy substitute (seasonal products more likely)
            substitute_probability = 0.3  # Base 30% chance
            if market_event:
                # Increase substitute buying during good market conditions
                substitute_probability *= market_event.demand_multiplier
                substitute_probability = min(0.6, substitute_probability)  # Max 60%
            
            if random.random() < substitute_probability:
                # Choose substitute with seasonal preference
                substitutes = list(PRODUCTS.keys())
                if market_event:
                    substitutes = self._apply_seasonal_weighting(substitutes, market_event)
                return random.choice(substitutes)
            return None  # Leave without buying
    
    def _customer_will_buy(self, customer: Customer, product_name: str, 
                          current_prices: Dict[str, float], competitor_prices: Dict[str, float], 
                          market_event: Optional[MarketEvent] = None) -> bool:
        """Determine if customer will buy based on their type, price, and seasonal factors"""
        our_price = current_prices[product_name]
        competitor_price = competitor_prices[product_name]
        price_ratio = our_price / competitor_price
        
        # Phase 2B: Apply seasonal demand boost
        seasonal_boost = self._get_seasonal_demand_boost(product_name, market_event)
        
        if customer.customer_type == CustomerType.PRICE_SENSITIVE:
            # Price-sensitive: very unlikely to buy if we're more expensive
            if price_ratio <= 0.95:  # 5% cheaper or more
                base_prob = 0.95
            elif price_ratio <= 1.0:  # Equal or slightly cheaper  
                base_prob = 0.85
            elif price_ratio <= 1.1:  # Up to 10% more expensive
                base_prob = 0.4
            else:  # More than 10% expensive
                base_prob = 0.1
            
            # Apply seasonal boost
            final_prob = min(0.98, base_prob * seasonal_boost)
            return random.random() < final_prob
        
        else:  # BRAND_LOYAL
            # Brand-loyal: less sensitive to price for preferred products
            if product_name in customer.preferred_products:
                loyalty_factor = customer.loyalty_strength
                # Even if expensive, loyalty keeps them buying
                if price_ratio <= 1.2:  # Up to 20% more expensive
                    base_prob = 0.7 + loyalty_factor * 0.3
                else:  # Very expensive
                    base_prob = loyalty_factor * 0.5
            else:
                # Non-preferred products: similar to price-sensitive behavior
                base_prob = max(0.1, 0.8 - price_ratio)
            
            # Apply seasonal boost
            final_prob = min(0.98, base_prob * seasonal_boost)
            return random.random() < final_prob
    
    def _update_segment_analytics(self, customers: List[CustomerPurchase], day: int):
        """Track customer segment performance for analytics"""
        self.segment_analytics[day] = {}
        
        for segment_type in CustomerType:
            segment_customers = [c for c in customers if c.customer_type == segment_type]
            
            self.segment_analytics[day][segment_type.value] = CustomerSegmentData(
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
    def _get_seasonal_demand_boost(self, product_name: str, market_event: Optional[MarketEvent]) -> float:
        """🌍 Phase 2B: Calculate seasonal demand boost for specific product"""
        if not market_event:
            return 1.0
        
        # Import here to avoid circular import
        from market_events_engine import MarketEventsEngine
        market_engine = MarketEventsEngine()
        
        return market_engine.get_product_demand_multiplier(product_name, market_event)
    
    def _apply_seasonal_weighting(self, product_list: List[str], market_event: MarketEvent) -> List[str]:
        """🌍 Phase 2B: Apply seasonal weighting to product selection"""
        if not product_list or not market_event:
            return product_list
        
        # Calculate weights for each product based on seasonal demand
        weighted_products = []
        for product_name in product_list:
            seasonal_multiplier = self._get_seasonal_demand_boost(product_name, market_event)
            # Add product multiple times based on seasonal demand (higher = more likely)
            weight = max(1, int(seasonal_multiplier * 2))  # Convert to integer weight
            weighted_products.extend([product_name] * weight)
        
        return weighted_products
