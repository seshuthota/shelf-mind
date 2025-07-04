from typing import Dict, List
from src.core.models import (
    StoreState, Product, CustomerPurchase, PRODUCTS, SUPPLIERS, CustomerType, Customer, 
    CustomerSegmentData, DeliveryOrder, PaymentTerm, InventoryItem, InventoryBatch, 
    SpoilageReport, ProductCategory, MarketEvent
)
from src.engines.customer_engine import CustomerEngine
from src.engines.competitor_engine import CompetitorEngine
from src.engines.supplier_engine import SupplierEngine
from src.engines.market_events_engine import MarketEventsEngine
from src.engines.crisis_engine import CrisisEngine
from src.engines.analytics_engine import AnalyticsEngine
from src.engines.strategic_planning_engine import StrategicPlanningEngine
from src.engines.learning_adaptation_engine import LearningAdaptationEngine
from src.engines.growth_expansion_engine import GrowthExpansionEngine


class StoreEngine:
    """🏆 Phase 2A Enhanced Store Engine - Spoilage Mechanics & 10-Product Catalog
    
    NEW FEATURES:
    - 10 products across 5 categories (beverages, snacks, fresh food, frozen, candy)
    - Batch-based inventory tracking with expiration dates
    - Spoilage mechanics for fresh and frozen items
    - FIFO inventory management (first in, first out)
    - Spoilage cost tracking and reporting
    """
    
    def __init__(self, starting_cash: float = 150.0):  # Increased starting cash for more complexity
        # Core store state with Phase 2A inventory system
        self.state = StoreState(
            day=1,
            cash=starting_cash,
            inventory={name: InventoryItem(
                product_name=name,
                batches=[InventoryBatch(
                    quantity=8,  # Smaller starting quantities for 10 products
                    received_day=0,
                    expiration_day=product.shelf_life_days if product.shelf_life_days else None
                )]
            ) for name, product in PRODUCTS.items()},
            daily_sales={name: 0 for name in PRODUCTS.keys()},
            daily_spoilage={name: 0 for name in PRODUCTS.keys()},
            total_revenue=0.0,
            total_profit=0.0,
            total_spoilage_cost=0.0
        )
        self.sales_history = []
        self.spoilage_history = []  # Track spoilage over time
        self.current_prices = {name: product.price for name, product in PRODUCTS.items()}
        
        # Initialize specialized engines
        self.customer_engine = CustomerEngine()
        self.competitor_engine = CompetitorEngine()
        self.supplier_engine = SupplierEngine()
        self.market_events_engine = MarketEventsEngine()  # Phase 2B: Seasonal demand & market events
        self.crisis_engine = CrisisEngine()  # Phase 2C: Crisis management & supply chain disruptions
        self.analytics_engine = AnalyticsEngine()  # Phase 3A: Performance analysis & strategic intelligence
        self.strategic_planning_engine = StrategicPlanningEngine()  # Phase 3B: Strategic planning & optimization
        self.learning_engine = LearningAdaptationEngine()  # Phase 3C: Learning & adaptation systems
        self.growth_engine = GrowthExpansionEngine()  # Phase 3D: Growth & expansion intelligence
        
    def process_spoilage(self) -> List[SpoilageReport]:
        """🍌 Phase 2A: Process daily spoilage for fresh and frozen items"""
        spoilage_reports = []
        total_spoilage_cost = 0.0
        
        for product_name, inventory_item in self.state.inventory.items():
            spoiled_quantity = inventory_item.remove_spoiled(self.state.day)
            
            if spoiled_quantity > 0:
                product = PRODUCTS[product_name]
                spoilage_cost = spoiled_quantity * product.cost
                total_spoilage_cost += spoilage_cost
                
                self.state.daily_spoilage[product_name] = spoiled_quantity
                
                spoilage_report = SpoilageReport(
                    product_name=product_name,
                    quantity_spoiled=spoiled_quantity,
                    cost_lost=spoilage_cost,
                    days_held=product.shelf_life_days or 0
                )
                spoilage_reports.append(spoilage_report)
                
        self.state.total_spoilage_cost += total_spoilage_cost
        return spoilage_reports
        
    def simulate_customers(self) -> List[CustomerPurchase]:
        """🎯 Phase 2B: Customer simulation with seasonal demand patterns"""
        # Generate market conditions for today
        market_event = self.market_events_engine.get_market_conditions(self.state.day)
        
        # Convert inventory to simple format for customer engine
        inventory_quantities = {
            name: item.total_quantity 
            for name, item in self.state.inventory.items()
        }
        
        customers, daily_sales = self.customer_engine.simulate_customers(
            current_prices=self.current_prices,
            competitor_prices=self.competitor_engine.competitor_prices,
            inventory=inventory_quantities,
            day=self.state.day,
            market_event=market_event  # Phase 2B: Pass market conditions
        )
        
        # Update inventory using FIFO and track sales
        for product_name, quantity_sold in daily_sales.items():
            if quantity_sold > 0:
                actual_sold = self.state.inventory[product_name].remove_quantity(quantity_sold, self.state.day)
                self.state.daily_sales[product_name] = actual_sold
        
        # 🧠 Phase 3C: Store customer data for learning
        self._yesterday_customers = customers
                
        return customers
    
    def process_orders(self, orders: Dict[str, int]) -> Dict[str, str]:
        """🏭 Phase 2C: Enhanced supplier ordering with crisis management"""
        return self.supplier_engine.process_orders(orders, self.state, self.crisis_engine)
        
    def add_inventory_batch(self, product_name: str, quantity: int, delivery_day: int):
        """🚚 Phase 2A: Add new inventory batch with expiration tracking"""
        product = PRODUCTS[product_name]
        expiration_day = None
        
        if product.shelf_life_days:
            expiration_day = delivery_day + product.shelf_life_days
            
        new_batch = InventoryBatch(
            quantity=quantity,
            received_day=delivery_day,
            expiration_day=expiration_day
        )
        
        if product_name not in self.state.inventory:
            self.state.inventory[product_name] = InventoryItem(product_name=product_name, batches=[])
            
        self.state.inventory[product_name].batches.append(new_batch)
    
    def set_prices(self, new_prices: Dict[str, float]) -> Dict[str, str]:
        """Phase 2A: Set new prices with category awareness"""
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
            
            # Add category context to feedback
            category = PRODUCTS[product_name].category.value
            results[product_name] = f"SUCCESS: {product_name} ({category}) price changed from ${old_price:.2f} to ${new_price:.2f}"
        
        return results
    
    def execute_emergency_action(self, action_type: str, parameters: Dict = None) -> Dict:
        """🚨 Phase 2C: Execute emergency response actions during crises"""
        if parameters is None:
            parameters = {}
            
        return self.crisis_engine.execute_emergency_action(action_type, parameters, self.state)
    
    def end_day(self) -> Dict:
        """🌅 Phase 3A: Enhanced end-of-day processing with analytics tracking"""
        # Process spoilage BEFORE calculating profits
        spoilage_reports = self.process_spoilage()
        
        # Calculate daily financials
        daily_revenue = sum(
            self.state.daily_sales[name] * self.current_prices[name] 
            for name in PRODUCTS.keys()
        )
        daily_cost = sum(
            self.state.daily_sales[name] * PRODUCTS[name].cost 
            for name in PRODUCTS.keys()
        )
        daily_spoilage_cost = sum(
            self.state.daily_spoilage[name] * PRODUCTS[name].cost
            for name in PRODUCTS.keys()
        )
        daily_profit = daily_revenue - daily_cost - daily_spoilage_cost
        
        self.state.cash += daily_revenue
        self.state.total_revenue += daily_revenue
        self.state.total_profit += daily_profit
        
        # 📊 Phase 3A: Record decision outcomes for analysis
        outcome_data = {
            'daily_sales': self.state.daily_sales.copy(),
            'daily_profit': daily_profit,
            'daily_revenue': daily_revenue,
            'cash_after': self.state.cash,
            'total_spoilage_cost': daily_spoilage_cost,
            'stockouts': [name for name, item in self.state.inventory.items() if item.total_quantity == 0],
            'price_war_intensity': self.competitor_engine.price_war_intensity,
            'business_continued': True
        }
        self.analytics_engine.update_decision_outcome(self.state.day, outcome_data)
        
        # 🚚 Phase 2C: Process incoming deliveries with crisis effects
        delivery_results = self.supplier_engine.process_deliveries(self.state, self.crisis_engine)
        
        # Add delivered items as new batches
        for delivery in delivery_results.get('successful_deliveries', []):
            self.add_inventory_batch(
                delivery['product_name'], 
                delivery['quantity'], 
                self.state.day
            )
        
        # 💰 Phase 1D: Handle payment obligations (NET-30)
        payment_status = self.supplier_engine.process_payment_obligations(self.state)
        
        # Update competitor prices based on our moves
        competitor_reactions = self.competitor_engine.update_competitor_prices(self.current_prices, self.state.day)
        
        # Store spoilage history
        if spoilage_reports:
            self.spoilage_history.extend(spoilage_reports)
        
        # 🧠 Phase 3C: Process daily learning and adaptation
        # Get yesterday's customer purchases (stored from simulate_customers)
        yesterday_customers = getattr(self, '_yesterday_customers', [])
        
        # Detect price changes from yesterday (if any)
        yesterday_prices = getattr(self, '_yesterday_prices', self.current_prices.copy())
        pricing_changes = {
            product: price for product, price in self.current_prices.items()
            if abs(price - yesterday_prices.get(product, price)) > 0.01
        }
        
        # Get market conditions for this day (needed for market context)
        market_event = self.market_events_engine.get_market_conditions(self.state.day)
        
        # Get market context
        market_context = {
            'season': market_event.season.value,
            'weather': market_event.weather.value,
            'holiday': market_event.holiday.value,
            'economic_condition': market_event.economic_condition.value,
            'demand_multiplier': market_event.demand_multiplier,
            'profit': daily_profit,
            'cash': self.state.cash
        }
        
        # Process learning for all dimensions
        learning_results = self.learning_engine.process_daily_learning(
            store_state=self.state,
            customer_purchases=yesterday_customers,
            yesterday_sales=self.state.daily_sales,
            market_context=market_context,
            pricing_changes=pricing_changes if pricing_changes else None,
            current_prices=self.current_prices  # Pass current prices to learning engine
        )
        
        # Store data for next day's learning
        self._yesterday_customers = []  # Will be updated by simulate_customers
        self._yesterday_prices = self.current_prices.copy()
        
        # 🚨 Phase 2C: Process crisis events and emergency responses
        # Generate new crisis events based on market conditions
        new_crises = self.crisis_engine.generate_crisis_events(self.state.day, self.state, market_event)
        self.state.active_crises.extend(new_crises)
        
        # Update existing crises and apply costs
        crisis_updates = self.crisis_engine.update_active_crises(self.state)
        self.state.cash -= crisis_updates["crisis_costs"]  # Apply daily crisis costs
        
        day_summary = {
            "day": self.state.day,
            "revenue": daily_revenue,
            "profit": daily_profit,
            "spoilage_cost": daily_spoilage_cost,
            "units_sold": sum(self.state.daily_sales.values()),
            "units_spoiled": sum(self.state.daily_spoilage.values()),
            "cash_balance": self.state.cash,
            "inventory_status": {name: item.total_quantity for name, item in self.state.inventory.items()},
            "spoilage_reports": [
                {
                    "product": report.product_name,
                    "quantity": report.quantity_spoiled,
                    "cost_lost": report.cost_lost
                } for report in spoilage_reports
            ],
            "competitor_reactions": competitor_reactions,
            "price_war_intensity": self.competitor_engine.price_war_intensity,
            # Phase 2B: Market conditions
            "market_event": {
                "season": market_event.season.value,
                "weather": market_event.weather.value,
                "holiday": market_event.holiday.value,
                "economic_condition": market_event.economic_condition.value,
                "description": market_event.description,
                "demand_multiplier": market_event.demand_multiplier
            },
            # Phase 1D: Supply chain intelligence
            "deliveries": delivery_results,
            "pending_deliveries": len(self.state.pending_deliveries),
            "accounts_payable": self.state.accounts_payable,
            "payment_status": payment_status,
            # Phase 2C: Crisis management
            "crisis_events": {
                "new_crises": [
                    {
                        "crisis_type": crisis.crisis_type.value,
                        "severity": crisis.severity,
                        "remaining_days": crisis.remaining_days,
                        "description": crisis.description,
                        "affected_products": crisis.affected_products,
                        "affected_suppliers": crisis.affected_suppliers
                    } for crisis in new_crises
                ],
                "resolved_crises": [
                    {
                        "crisis_type": crisis.crisis_type.value,
                        "description": crisis.description
                    } for crisis in crisis_updates["resolved_crises"]
                ],
                "daily_crisis_costs": crisis_updates["crisis_costs"],
                "active_crisis_count": len(self.state.active_crises)
            },
            # Phase 3C: Learning & adaptation results
            "learning_results": {
                "customer_learning": {
                    "actual_segments": f"{getattr(learning_results.get('customer_learning'), 'actual_price_sensitive_ratio', 0.6):.0%} price-sensitive",
                    "segment_shift": getattr(learning_results.get('customer_learning'), 'segment_shift', 0.0),
                    "lost_sales_value": learning_results.get('lost_sales', {}).get('total_lost_value', 0.0),
                    "market_shift_warning": getattr(learning_results.get('customer_learning'), 'market_shift_warning', None)
                },
                "trend_analysis": {
                    product: f"{trend.trend_direction} ({trend.days_in_trend} days)"
                    for product, trend in learning_results.get('trend_analysis', {}).items()
                    if hasattr(trend, 'trend_direction') and trend.trend_direction != 'stable'
                },
                "price_elasticity": {
                    product: f"{elasticity.price_sensitivity} elasticity"
                    for product, elasticity in learning_results.get('price_elasticity', {}).items()
                    if hasattr(elasticity, 'confidence_level') and elasticity.confidence_level > 0.6
                },
                "adaptive_strategies": len(learning_results.get('strategy_updates', {})),
                "learning_insights": [
                    insight.message for insight in learning_results.get('insights', [])
                    if hasattr(insight, 'priority') and insight.priority in ['critical', 'high']
                ][:3]  # Top 3 insights
            }
        }
        
        # Reset for next day
        self.state.daily_sales = {name: 0 for name in PRODUCTS.keys()}
        self.state.daily_spoilage = {name: 0 for name in PRODUCTS.keys()}
        self.state.day += 1
        
        return day_summary
    
    def get_status(self) -> Dict:
        """📊 Phase 2A: Enhanced status with spoilage intelligence"""
        # Calculate spoilage warnings
        spoilage_warnings = []
        for product_name, inventory_item in self.state.inventory.items():
            for batch in inventory_item.batches:
                if batch.expiration_day:
                    days_until_expiry = batch.expiration_day - self.state.day
                    if days_until_expiry <= 1:  # Expires tomorrow or today
                        spoilage_warnings.append({
                            "product": product_name,
                            "quantity": batch.quantity,
                            "days_until_expiry": days_until_expiry
                        })
        
        return {
            "day": self.state.day,
            "cash": self.state.cash,
            "inventory": {name: item.total_quantity for name, item in self.state.inventory.items()},
            "products": {
                name: {
                    "cost": p.cost, 
                    "price": self.current_prices[name],
                    "category": p.category.value,
                    "shelf_life": p.shelf_life_days
                } for name, p in PRODUCTS.items()
            },
            "competitor_prices": dict(self.competitor_engine.competitor_prices),
            "stockouts": [name for name, item in self.state.inventory.items() if item.total_quantity == 0],
            "spoilage_warnings": spoilage_warnings,
            "total_spoilage_cost": self.state.total_spoilage_cost,
            # Phase 1D: Supply chain intelligence
            "suppliers": self.supplier_engine.get_supplier_info(),
            "pending_deliveries": self.supplier_engine.get_pending_deliveries_summary(self.state),
            "accounts_payable": self.state.accounts_payable,
            # Phase 2C: Crisis management status
            "crisis_status": {
                "active_crises": [
                    {
                        "crisis_type": crisis.crisis_type.value,
                        "severity": crisis.severity,
                        "remaining_days": crisis.remaining_days,
                        "description": crisis.description,
                        "affected_products": crisis.affected_products,
                        "affected_suppliers": crisis.affected_suppliers
                    } for crisis in self.state.active_crises
                ],
                "emergency_actions": self.crisis_engine.get_emergency_actions(self.state),
                "daily_crisis_costs": sum(
                    self.crisis_engine._calculate_daily_crisis_cost(crisis, self.state) 
                    for crisis in self.state.active_crises
                ),
                "crisis_response_cash": self.state.crisis_response_cash
            }
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
    
    # 🧠 Phase 3A: Analytics & Strategic Intelligence Methods
    
    def record_pricing_decision(self, prices: Dict[str, float], market_context: Dict) -> None:
        """📊 Record pricing decision for analytics"""
        self.analytics_engine.record_decision(
            'pricing', 
            {'prices': prices}, 
            self.state, 
            market_context
        )
    
    def record_inventory_decision(self, orders: Dict[str, int], market_context: Dict) -> None:
        """📦 Record inventory decision for analytics"""
        self.analytics_engine.record_decision(
            'inventory', 
            {'orders': orders}, 
            self.state, 
            market_context
        )
    
    def record_crisis_decision(self, action_type: str, parameters: Dict, market_context: Dict) -> None:
        """🚨 Record crisis response decision for analytics"""
        self.analytics_engine.record_decision(
            'crisis', 
            {'action_type': action_type, 'parameters': parameters}, 
            self.state, 
            market_context
        )
    
    def get_performance_analysis(self, days_back: int = 7) -> Dict:
        """📈 Get comprehensive performance analysis"""
        return self.analytics_engine.get_performance_analysis(days_back)
    
    def get_strategic_insights(self) -> Dict:
        """💡 Get strategic insights and optimization recommendations"""
        market_context = self.market_events_engine.get_market_conditions(self.state.day).__dict__
        competitor_info = {
            'war_intensity': self.competitor_engine.price_war_intensity,
            'strategy': self.competitor_engine.competitor_strategy,
            'price_advantage_score': self._calculate_price_advantage()
        }
        return self.analytics_engine.generate_strategic_insights(
            self.state, 
            market_context, 
            competitor_info
        )
    
    def get_strategy_patterns(self) -> List:
        """🎯 Get identified successful strategy patterns"""
        return self.analytics_engine.identify_strategy_patterns()
    
    # 🎯 Phase 3B: Strategic Planning & Optimization Methods
    
    def get_inventory_optimization(self) -> Dict:
        """📦 Get inventory optimization recommendations"""
        recommendations = self.strategic_planning_engine.inventory_optimizer.calculate_inventory_recommendations(
            self.state, self.sales_history, self.current_prices
        )
        return {
            'recommendations': [rec.__dict__ for rec in recommendations],
            'summary': {
                'critical_reorders': len([r for r in recommendations if r.recommended_action == 'order' and r.stockout_risk > 0.7]),
                'overstock_items': len([r for r in recommendations if r.recommended_action == 'reduce']),
                'total_carrying_cost': sum(r.carrying_cost_daily for r in recommendations),
                'avg_confidence': sum(r.confidence for r in recommendations) / max(1, len(recommendations))
            }
        }
    
    def get_promotional_opportunities(self) -> Dict:
        """🎯 Get promotional strategy recommendations"""
        opportunities = self.strategic_planning_engine.promotional_strategy.identify_promotional_opportunities(
            self.state, self.sales_history, self.current_prices
        )
        return {
            'opportunities': [opp.__dict__ for opp in opportunities],
            'summary': {
                'slow_movers': len(opportunities),
                'total_potential_roi': sum(max(0, opp.estimated_roi) for opp in opportunities),
                'avg_discount_needed': sum(opp.recommended_discount_pct for opp in opportunities) / max(1, len(opportunities)),
                'priority_items': [opp.product_name for opp in opportunities[:3]]
            }
        }
    
    def get_seasonal_preparation(self) -> Dict:
        """🌍 Get seasonal preparation recommendations"""
        current_season = self.market_events_engine.get_market_conditions(self.state.day).season.value
        preparations = self.strategic_planning_engine.seasonal_planner.generate_seasonal_recommendations(
            self.state, current_season, self.strategic_planning_engine._get_next_season(current_season),
            self.market_events_engine
        )
        return {
            'preparations': [prep.__dict__ for prep in preparations],
            'summary': {
                'critical_preparations': len([p for p in preparations if p.preparation_priority == 'critical']),
                'total_buildup_needed': sum(p.recommended_buildup for p in preparations),
                'next_season': self.strategic_planning_engine._get_next_season(current_season),
                'priority_products': [p.product_name for p in preparations[:3]]
            }
        }
    
    def get_category_analysis(self) -> Dict:
        """📊 Get category performance analysis"""
        analyses = self.strategic_planning_engine.category_manager.analyze_category_performance(
            self.state, self.sales_history, self.current_prices
        )
        return {
            'analyses': [analysis.__dict__ for analysis in analyses],
            'summary': {
                'best_category': analyses[0].category if analyses else 'none',
                'avg_profit_margin': sum(a.profit_margin for a in analyses) / max(1, len(analyses)),
                'growing_categories': [a.category for a in analyses if a.growth_trend == 'growing'],
                'declining_categories': [a.category for a in analyses if a.growth_trend == 'declining']
            }
        }
    
    def get_comprehensive_strategy(self) -> Dict:
        """🧠 Get comprehensive strategic planning recommendations"""
        current_season = self.market_events_engine.get_market_conditions(self.state.day).season.value
        strategy = self.strategic_planning_engine.generate_comprehensive_strategy(
            self.state, self.sales_history, self.current_prices, current_season, self.market_events_engine
        )
        
        # Convert dataclasses to dicts for JSON serialization
        strategy_dict = {
            'inventory_optimization': [rec.__dict__ for rec in strategy['inventory_optimization']],
            'promotional_opportunities': [opp.__dict__ for opp in strategy['promotional_opportunities']],
            'seasonal_preparation': [prep.__dict__ for prep in strategy['seasonal_preparation']],
            'category_analysis': [analysis.__dict__ for analysis in strategy['category_analysis']],
            'strategic_priorities': strategy['strategic_priorities'],
            'execution_plan': strategy['execution_plan']
        }
        
        return strategy_dict
    
    def calculate_current_performance(self) -> Dict:
        """📊 Calculate current day performance metrics"""
        competitor_info = {
            'war_intensity': self.competitor_engine.price_war_intensity,
            'strategy': self.competitor_engine.competitor_strategy,
            'price_advantage_score': self._calculate_price_advantage()
        }
        
        # Get yesterday's data if available
        yesterday_data = None
        if len(self.sales_history) > 0:
            yesterday_data = self.sales_history[-1]
        
        metrics = self.analytics_engine.calculate_daily_performance(
            self.state, 
            competitor_info, 
            yesterday_data
        )
        return metrics.__dict__
    
    def _calculate_price_advantage(self) -> float:
        """Calculate our price advantage vs competitor (0-100)"""
        our_prices = list(self.current_prices.values())
        competitor_prices = list(self.competitor_engine.competitor_prices.values())
        
        if not our_prices or not competitor_prices:
            return 50
        
        avg_our_price = sum(our_prices) / len(our_prices)
        avg_competitor_price = sum(competitor_prices) / len(competitor_prices)
        
        # Score based on how competitive our pricing is
        if avg_our_price < avg_competitor_price:
            advantage = min(100, 60 + ((avg_competitor_price - avg_our_price) / avg_competitor_price) * 100)
        else:
            advantage = max(0, 60 - ((avg_our_price - avg_competitor_price) / avg_competitor_price) * 100)
        
        return advantage 
    
    # 🧠 Phase 3C: Learning & Adaptation Methods
    
    def get_learning_insights(self) -> Dict:
        """🧠 Get learning insights and adaptive intelligence"""
        return {
            'adaptive_prompts': self.learning_engine.get_adaptive_agent_prompts(),
            'learning_summary': self.learning_engine.get_learning_summary(),
            'customer_evolution': len(self.learning_engine.segment_evolution),
            'product_trends': len(self.learning_engine.product_trends),
            'adaptive_strategies': len(self.learning_engine.adaptive_strategies),
            'high_priority_insights': [
                insight.message for insight in self.learning_engine.learning_insights
                if insight.priority in ['critical', 'high']
            ][-5:]  # Last 5 high priority insights
        }
    
    def get_strategy_playbook(self) -> List[str]:
        """📚 Get relevant proven strategies from learned pattern library"""
        market_event = self.market_events_engine.get_market_conditions(self.state.day)
        current_conditions = {
            'season': market_event.season.value,
            'weather': market_event.weather.value,
            'profit': self.state.total_profit,
            'cash': self.state.cash
        }
        return self.learning_engine.get_strategy_playbook(current_conditions)
    
    def get_adaptive_customer_analysis(self) -> Dict:
        """🎯 Get dynamic customer segment analysis based on learning"""
        if not self.learning_engine.segment_evolution:
            return {
                'segments': 'No data yet - need more customer interactions',
                'recommendations': ['Continue monitoring customer behavior']
            }
        
        latest_analysis = self.learning_engine.segment_evolution[-1]
        recommendations = []
        
        if latest_analysis.segment_shift > 0.15:
            recommendations.append("Market shifted toward price-sensitive customers - consider competitive pricing")
        elif latest_analysis.segment_shift < -0.15:
            recommendations.append("Market shifted toward brand-loyal customers - premium pricing opportunity")
        
        if latest_analysis.lost_sales_value > 20:
            recommendations.append(f"Lost ${latest_analysis.lost_sales_value:.2f} to stockouts - improve inventory management")
        
        return {
            'current_segments': f"{latest_analysis.actual_price_sensitive_ratio:.0%} price-sensitive, {latest_analysis.actual_brand_loyal_ratio:.0%} brand-loyal",
            'baseline_shift': f"{latest_analysis.segment_shift:+.1%} from 60/40 baseline",
            'lost_sales_warning': f"${latest_analysis.lost_sales_value:.2f} lost to stockouts" if latest_analysis.lost_sales_value > 0 else "No lost sales",
            'market_alert': latest_analysis.market_shift_warning,
            'recommendations': recommendations
        }
    
    def get_product_lifecycle_analysis(self) -> Dict:
        """📈 Get product trend and lifecycle analysis"""
        if not self.learning_engine.product_trends:
            return {
                'trends': 'No trend data yet - need 7+ days of sales history',
                'recommendations': ['Continue tracking sales patterns']
            }
        
        trends = {}
        recommendations = []
        
        for product, trend in self.learning_engine.product_trends.items():
            trends[product] = {
                'direction': trend.trend_direction,
                'strength': f"{trend.trend_strength:+.1%}",
                'days_in_trend': trend.days_in_trend,
                'lifecycle_stage': trend.lifecycle_stage,
                'sales_velocity': f"{trend.sales_velocity:.1f} units/day",
                'recommendation': trend.recommendation
            }
            
            if trend.trend_direction == 'rising' and trend.days_in_trend >= 3:
                recommendations.append(f"🚀 {product}: Rising star - increase inventory and consider premium pricing")
            elif trend.trend_direction == 'falling' and trend.days_in_trend >= 3:
                recommendations.append(f"📉 {product}: Declining trend - consider promotion or reduce inventory")
        
        return {
            'product_trends': trends,
            'lifecycle_recommendations': recommendations
        }
    
    def get_price_elasticity_intelligence(self) -> Dict:
        """💰 Get price elasticity learning from experiments"""
        if not self.learning_engine.price_elasticity:
            return {
                'elasticity_data': 'No elasticity data yet - need price change experiments',
                'recommendations': ['Try adjusting prices to learn customer price sensitivity']
            }
        
        elasticity_data = {}
        recommendations = []
        
        for product, elasticity in self.learning_engine.price_elasticity.items():
            if elasticity.confidence_level > 0.5:  # Only show confident measurements
                elasticity_data[product] = {
                    'sensitivity': elasticity.price_sensitivity,
                    'coefficient': elasticity.elasticity_coefficient,
                    'confidence': f"{elasticity.confidence_level:.0%}",
                    'insight': elasticity.last_test_result
                }
                
                if elasticity.price_sensitivity == 'high':
                    recommendations.append(f"⚠️ {product}: Highly price elastic - small price changes cause big demand changes")
                elif elasticity.price_sensitivity == 'low':
                    recommendations.append(f"💎 {product}: Price inelastic - can adjust prices with less demand impact")
        
        return {
            'price_elasticity': elasticity_data,
            'pricing_recommendations': recommendations,
            'experiments_conducted': len(self.learning_engine.price_change_experiments)
        }
    
    # 🚀 Phase 3D: Growth & Expansion Intelligence Methods
    
    def evaluate_new_products(self) -> Dict:
        """🧪 Phase 3D: Evaluate new product opportunities with market analysis"""
        store_data = {
            'cash': self.state.cash,
            'daily_customers': sum(self.state.daily_sales.values()),
            'daily_revenue': sum(self.state.daily_sales[name] * self.current_prices[name] for name in PRODUCTS.keys()),
            'daily_profit': self.state.total_profit / max(1, self.state.day)
        }
        
        return self.growth_engine.evaluate_new_products(store_data, self.state.day)
    
    def analyze_service_opportunities(self) -> Dict:
        """💼 Phase 3D: Analyze service expansion opportunities"""
        store_data = {
            'cash': self.state.cash,
            'daily_customers': sum(self.state.daily_sales.values()),
            'daily_revenue': sum(self.state.daily_sales[name] * self.current_prices[name] for name in PRODUCTS.keys()),
            'daily_profit': self.state.total_profit / max(1, self.state.day)
        }
        
        customer_data = {
            'price_sensitive_ratio': 0.6,  # Default segment ratios
            'brand_loyal_ratio': 0.4
        }
        
        return self.growth_engine.analyze_service_opportunities(store_data, customer_data)
    
    def optimize_customer_retention(self) -> Dict:
        """❤️ Phase 3D: Optimize customer retention and loyalty programs"""
        store_data = {
            'cash': self.state.cash,
            'daily_customers': sum(self.state.daily_sales.values()),
            'daily_revenue': sum(self.state.daily_sales[name] * self.current_prices[name] for name in PRODUCTS.keys()),
            'daily_profit': self.state.total_profit / max(1, self.state.day)
        }
        
        customer_data = {
            'price_sensitive_ratio': 0.6,
            'brand_loyal_ratio': 0.4
        }
        
        return self.growth_engine.optimize_customer_retention(store_data, customer_data)
    
    def analyze_expansion_opportunities(self) -> Dict:
        """🏢 Phase 3D: Analyze multi-location expansion opportunities"""
        store_data = {
            'cash': self.state.cash,
            'daily_revenue': sum(self.state.daily_sales[name] * self.current_prices[name] for name in PRODUCTS.keys()),
            'daily_profit': self.state.total_profit / max(1, self.state.day)
        }
        
        return self.growth_engine.analyze_expansion_opportunities(store_data)
    
    def get_comprehensive_growth_analysis(self) -> Dict:
        """🚀 Phase 3D: Get comprehensive growth and expansion analysis"""
        store_data = {
            'cash': self.state.cash,
            'daily_customers': sum(self.state.daily_sales.values()),
            'daily_revenue': sum(self.state.daily_sales[name] * self.current_prices[name] for name in PRODUCTS.keys()),
            'daily_profit': self.state.total_profit / max(1, self.state.day)
        }
        
        customer_data = {
            'price_sensitive_ratio': 0.6,
            'brand_loyal_ratio': 0.4
        }
        
        return self.growth_engine.get_comprehensive_growth_analysis(store_data, customer_data, self.state.day)