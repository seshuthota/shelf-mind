import random
from typing import Dict, List
from models import CustomerPurchase, Customer, CustomerType, CustomerSegmentData, PRODUCTS


class CustomerEngine:
    """🎯 Phase 1C: Advanced Customer Psychology & Segmentation System"""
    
    def __init__(self):
        self.segment_analytics = {}
    
    def simulate_customers(self, current_prices: Dict[str, float], competitor_prices: Dict[str, float], 
                          inventory: Dict[str, int], day: int) -> List[CustomerPurchase]:
        """🎯 Phase 1C: Customer Type Segmentation System"""
        customers = []
        base_customers = random.randint(12, 22)  # Slightly increased for segmentation
        
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
            purchase = self._simulate_customer_purchase(customer, current_prices, competitor_prices, inventory, daily_sales)
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
                                   daily_sales: Dict[str, int]) -> CustomerPurchase:
        """Simulate individual customer purchase based on their type"""
        purchase_items = []
        total_spent = 0.0
        num_items = random.randint(1, 3)
        
        for _ in range(num_items):
            if customer.customer_type == CustomerType.PRICE_SENSITIVE:
                product_name = self._price_sensitive_product_choice(current_prices, competitor_prices)
            else:  # BRAND_LOYAL
                product_name = self._brand_loyal_product_choice(customer, inventory)
            
            if product_name and inventory[product_name] > 0:
                # Make purchase decision based on customer type
                if self._customer_will_buy(customer, product_name, current_prices, competitor_prices):
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
                                       competitor_prices: Dict[str, float]) -> str:
        """Price-sensitive customers choose cheapest available products"""
        # Compare our prices to competitor for each product
        best_deals = []
        for product_name in PRODUCTS.keys():
            our_price = current_prices[product_name]
            competitor_price = competitor_prices[product_name]
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
            cheapest = min(PRODUCTS.keys(), key=lambda x: current_prices[x])
            return cheapest
    
    def _brand_loyal_product_choice(self, customer: Customer, inventory: Dict[str, int]) -> str:
        """Brand-loyal customers stick to their preferred products"""
        available_preferred = [p for p in customer.preferred_products 
                              if inventory[p] > 0]
        
        if available_preferred:
            return random.choice(available_preferred)
        else:
            # If preferred not available, might buy substitute (low probability)
            if random.random() < 0.3:  # 30% chance to buy substitute
                return random.choice(list(PRODUCTS.keys()))
            return None  # Leave without buying
    
    def _customer_will_buy(self, customer: Customer, product_name: str, 
                          current_prices: Dict[str, float], competitor_prices: Dict[str, float]) -> bool:
        """Determine if customer will buy based on their type and price"""
        our_price = current_prices[product_name]
        competitor_price = competitor_prices[product_name]
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