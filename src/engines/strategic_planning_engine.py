import math
import statistics
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import defaultdict
from src.core.models import PRODUCTS, ProductCategory, StoreState
from datetime import datetime


@dataclass
class InventoryRecommendation:
    """Inventory optimization recommendation"""
    product_name: str
    current_stock: int
    optimal_stock: int
    reorder_point: int
    economic_order_quantity: int
    carrying_cost_daily: float
    stockout_risk: float
    recommended_action: str  # 'order', 'reduce', 'maintain'
    order_quantity: int
    confidence: float


@dataclass
class PromotionalOpportunity:
    """Promotional strategy recommendation"""
    product_name: str
    current_inventory: int
    days_of_inventory: float
    turnover_rate: float
    recommended_discount_pct: float
    promotional_price: float
    expected_velocity_increase: float
    estimated_roi: float
    campaign_duration_days: int
    reason: str


@dataclass
class SeasonalPreparation:
    """Seasonal preparation recommendation"""
    product_name: str
    current_season: str
    upcoming_season: str
    seasonal_demand_multiplier: float
    current_stock: int
    recommended_buildup: int
    buildup_timing_days: int
    expected_demand_spike: float
    preparation_priority: str  # 'critical', 'high', 'medium', 'low'


@dataclass
class CategoryAnalysis:
    """Category performance analysis"""
    category: str
    total_revenue: float
    total_profit: float
    profit_margin: float
    inventory_turnover: float
    space_efficiency: float
    growth_trend: str  # 'growing', 'stable', 'declining'
    optimization_opportunity: str
    recommended_actions: List[str]


class InventoryOptimizer:
    """🎯 Phase 3B: Advanced Inventory Optimization Engine"""
    
    def __init__(self):
        # Optimization parameters
        self.holding_cost_rate = 0.01  # 1% per day holding cost
        self.stockout_cost_multiplier = 3.0  # 3x profit margin for stockout cost
        self.service_level = 0.95  # 95% service level target
        self.lead_time_days = 2  # Average supplier lead time
        
    def calculate_inventory_recommendations(self, store_state: StoreState, 
                                         sales_history: List[Dict], 
                                         current_prices: Dict[str, float]) -> List[InventoryRecommendation]:
        """📊 Calculate optimal inventory levels for all products"""
        
        recommendations = []
        
        for product_name in PRODUCTS.keys():
            # Get historical data
            demand_data = self._extract_demand_data(product_name, sales_history)
            if not demand_data:
                continue
                
            # Calculate demand statistics
            avg_daily_demand = statistics.mean(demand_data)
            demand_std_dev = statistics.stdev(demand_data) if len(demand_data) > 1 else avg_daily_demand * 0.3
            
            # Current inventory
            current_stock = store_state.inventory[product_name].total_quantity
            
            # Calculate costs
            product_cost = PRODUCTS[product_name].cost
            holding_cost_per_unit = product_cost * self.holding_cost_rate
            stockout_cost_per_unit = (current_prices[product_name] - product_cost) * self.stockout_cost_multiplier
            
            # Economic Order Quantity (EOQ)
            ordering_cost = 5.0  # Fixed ordering cost per order
            if avg_daily_demand > 0 and holding_cost_per_unit > 0:
                eoq = math.sqrt(2 * avg_daily_demand * 30 * ordering_cost / (holding_cost_per_unit * 30))
            else:
                eoq = 10  # Default
                
            # Safety stock and reorder point
            z_score = 1.65  # 95% service level
            safety_stock = z_score * math.sqrt(self.lead_time_days) * demand_std_dev
            reorder_point = int(avg_daily_demand * self.lead_time_days + safety_stock)
            
            # Optimal stock level
            optimal_stock = int(reorder_point + eoq/2)
            
            # Calculate carrying cost and stockout risk
            carrying_cost_daily = current_stock * holding_cost_per_unit
            stockout_risk = max(0, min(1, (reorder_point - current_stock) / max(1, reorder_point)))
            
            # Determine recommendation
            if current_stock <= reorder_point:
                recommended_action = 'order'
                order_quantity = max(int(eoq), optimal_stock - current_stock)
            elif current_stock > optimal_stock * 1.5:
                recommended_action = 'reduce'
                order_quantity = 0
            else:
                recommended_action = 'maintain'
                order_quantity = 0
                
            # Confidence calculation
            confidence = min(1.0, len(demand_data) / 10.0)  # Higher confidence with more data
            
            recommendation = InventoryRecommendation(
                product_name=product_name,
                current_stock=current_stock,
                optimal_stock=optimal_stock,
                reorder_point=reorder_point,
                economic_order_quantity=int(eoq),
                carrying_cost_daily=carrying_cost_daily,
                stockout_risk=stockout_risk,
                recommended_action=recommended_action,
                order_quantity=order_quantity,
                confidence=confidence
            )
            
            recommendations.append(recommendation)
            
        return recommendations
    
    def _extract_demand_data(self, product_name: str, sales_history: List[Dict]) -> List[float]:
        """Extract daily demand data for a product"""
        demand_data = []
        for day_data in sales_history[-14:]:  # Last 14 days
            daily_sales = day_data.get('daily_sales', {})
            demand_data.append(daily_sales.get(product_name, 0))
        return demand_data


class PromotionalStrategy:
    """🎯 Phase 3B: Promotional Strategy Engine"""
    
    def __init__(self):
        self.slow_mover_threshold_days = 20  # 20+ days of inventory = slow mover
        self.max_discount_pct = 30  # Maximum 30% discount
        self.target_turnover_improvement = 2.0  # Target 2x turnover improvement
        
    def identify_promotional_opportunities(self, store_state: StoreState,
                                        sales_history: List[Dict],
                                        current_prices: Dict[str, float]) -> List[PromotionalOpportunity]:
        """🎯 Identify products needing promotional campaigns"""
        
        opportunities = []
        
        for product_name in PRODUCTS.keys():
            # Calculate inventory metrics
            current_inventory = store_state.inventory[product_name].total_quantity
            if current_inventory == 0:
                continue
                
            # Calculate turnover rate
            recent_sales = self._get_recent_sales(product_name, sales_history, days=7)
            avg_daily_sales = sum(recent_sales) / max(1, len(recent_sales))
            
            if avg_daily_sales == 0:
                days_of_inventory = 999  # Use large number instead of infinity
                turnover_rate = 0
            else:
                days_of_inventory = current_inventory / avg_daily_sales
                turnover_rate = 365 / days_of_inventory if days_of_inventory > 0 else 0
                
            # Identify slow movers  
            if days_of_inventory > self.slow_mover_threshold_days and current_inventory > 3:
                # Calculate promotional strategy
                target_daily_sales = current_inventory / (self.slow_mover_threshold_days / 2)  # Target halving inventory time
                sales_increase_needed = target_daily_sales / max(0.1, avg_daily_sales)
                
                # Handle extremely slow movers (no sales)
                if avg_daily_sales == 0:
                    sales_increase_needed = min(5.0, sales_increase_needed)  # Cap at 5x increase
                
                # Estimate price elasticity (simple model)
                price_elasticity = 1.5  # Assume 1.5 elasticity
                discount_needed = min(self.max_discount_pct, (sales_increase_needed - 1) * 100 / price_elasticity)
                
                promotional_price = current_prices[product_name] * (1 - discount_needed / 100)
                
                # Ensure promotional price covers cost
                product_cost = PRODUCTS[product_name].cost
                if promotional_price < product_cost * 1.1:  # Maintain 10% minimum margin
                    promotional_price = product_cost * 1.1
                    discount_needed = (1 - promotional_price / current_prices[product_name]) * 100
                
                # Calculate expected impact
                expected_velocity_increase = 1 + (discount_needed * price_elasticity / 100)
                
                # ROI calculation
                current_margin = current_prices[product_name] - product_cost
                promotional_margin = promotional_price - product_cost
                inventory_carrying_cost = current_inventory * product_cost * 0.01 * (days_of_inventory / 2)
                
                revenue_with_promo = promotional_price * current_inventory * expected_velocity_increase
                revenue_without_promo = current_prices[product_name] * current_inventory
                
                estimated_roi = ((revenue_with_promo - revenue_without_promo) - inventory_carrying_cost) / max(1, current_inventory * product_cost)
                
                # Campaign duration
                campaign_duration = min(14, max(3, int(min(days_of_inventory, 42) / 3)))  # Run for 1/3 of current inventory days, capped at 14 days
                
                # Determine reason
                if days_of_inventory > 45:
                    reason = "CRITICAL: Excessive inventory buildup"
                elif days_of_inventory > 30:
                    reason = "HIGH PRIORITY: Slow-moving inventory"
                else:
                    reason = "MODERATE: Inventory optimization"
                
                opportunity = PromotionalOpportunity(
                    product_name=product_name,
                    current_inventory=current_inventory,
                    days_of_inventory=days_of_inventory,
                    turnover_rate=turnover_rate,
                    recommended_discount_pct=discount_needed,
                    promotional_price=promotional_price,
                    expected_velocity_increase=expected_velocity_increase,
                    estimated_roi=estimated_roi,
                    campaign_duration_days=campaign_duration,
                    reason=reason
                )
                
                opportunities.append(opportunity)
        
        # Sort by priority (highest ROI and most critical first)
        opportunities.sort(key=lambda x: (x.days_of_inventory, -x.estimated_roi), reverse=True)
        
        return opportunities
    
    def _get_recent_sales(self, product_name: str, sales_history: List[Dict], days: int = 7) -> List[int]:
        """Get recent sales data for a product"""
        recent_sales = []
        for day_data in sales_history[-days:]:
            daily_sales = day_data.get('daily_sales', {})
            recent_sales.append(daily_sales.get(product_name, 0))
        return recent_sales


class SeasonalPlanner:
    """🎯 Phase 3B: Seasonal Preparation Intelligence"""
    
    def __init__(self):
        self.preparation_lead_time = 5  # Start preparing 5 days before season
        self.seasonal_multiplier_threshold = 1.3  # Focus on 30%+ seasonal increases
        
    def generate_seasonal_recommendations(self, store_state: StoreState,
                                       current_season: str,
                                       upcoming_season: str,
                                       market_events_engine) -> List[SeasonalPreparation]:
        """🌍 Generate seasonal preparation recommendations"""
        
        recommendations = []
        
        # Get seasonal demand multipliers
        from src.engines.market_events_engine import MarketEventsEngine
        from src.core.models import Season, WeatherEvent, Holiday, EconomicCondition, MarketEvent
        
        # Create upcoming season market event for analysis
        upcoming_event = MarketEvent(
            day=1,
            season=Season(upcoming_season),
            weather=WeatherEvent.NORMAL,
            holiday=Holiday.NONE,
            economic_condition=EconomicCondition.NORMAL,
            description=f"Seasonal planning for {upcoming_season}",
            demand_multiplier=1.0
        )
        
        for product_name in PRODUCTS.keys():
            # Get seasonal demand multiplier for upcoming season
            seasonal_multiplier = market_events_engine.get_product_demand_multiplier(product_name, upcoming_event)
            
            # Focus on products with significant seasonal impact
            if seasonal_multiplier >= self.seasonal_multiplier_threshold:
                current_stock = store_state.inventory[product_name].total_quantity
                
                # Estimate demand increase
                base_demand = max(1, current_stock / 10)  # Rough estimate
                expected_seasonal_demand = base_demand * seasonal_multiplier
                demand_spike = expected_seasonal_demand - base_demand
                
                # Calculate recommended buildup
                safety_factor = 1.2  # 20% safety buffer
                recommended_buildup = int(demand_spike * safety_factor)
                
                # Determine timing and priority
                if seasonal_multiplier >= 2.0:
                    priority = 'critical'
                    buildup_timing = 7  # Start 7 days early for critical items
                elif seasonal_multiplier >= 1.6:
                    priority = 'high'
                    buildup_timing = 5
                else:
                    priority = 'medium'
                    buildup_timing = 3
                    
                # Only recommend if buildup is needed
                if recommended_buildup > 0 and current_stock < expected_seasonal_demand:
                    recommendation = SeasonalPreparation(
                        product_name=product_name,
                        current_season=current_season,
                        upcoming_season=upcoming_season,
                        seasonal_demand_multiplier=seasonal_multiplier,
                        current_stock=current_stock,
                        recommended_buildup=recommended_buildup,
                        buildup_timing_days=buildup_timing,
                        expected_demand_spike=demand_spike,
                        preparation_priority=priority
                    )
                    
                    recommendations.append(recommendation)
        
        # Sort by priority and demand spike magnitude
        priority_order = {'critical': 3, 'high': 2, 'medium': 1, 'low': 0}
        recommendations.sort(key=lambda x: (priority_order[x.preparation_priority], x.expected_demand_spike), reverse=True)
        
        return recommendations


class CategoryManager:
    """🎯 Phase 3B: Category Management & Optimization"""
    
    def analyze_category_performance(self, store_state: StoreState,
                                   sales_history: List[Dict],
                                   current_prices: Dict[str, float]) -> List[CategoryAnalysis]:
        """📊 Analyze performance by product category"""
        
        category_data = defaultdict(lambda: {
            'revenue': 0,
            'profit': 0,
            'units_sold': 0,
            'inventory_value': 0,
            'products': []
        })
        
        # Aggregate data by category
        for product_name, product in PRODUCTS.items():
            category = product.category.value
            category_data[category]['products'].append(product_name)
            
            # Calculate recent performance
            recent_sales = self._get_recent_category_sales(product_name, sales_history, days=7)
            units_sold = sum(recent_sales)
            revenue = units_sold * current_prices[product_name]
            profit = units_sold * (current_prices[product_name] - product.cost)
            
            category_data[category]['revenue'] += revenue
            category_data[category]['profit'] += profit
            category_data[category]['units_sold'] += units_sold
            category_data[category]['inventory_value'] += store_state.inventory[product_name].total_quantity * product.cost
        
        # Analyze each category
        analyses = []
        for category, data in category_data.items():
            if data['revenue'] == 0:
                continue
                
            profit_margin = (data['profit'] / data['revenue']) * 100
            inventory_turnover = (data['revenue'] / max(1, data['inventory_value'])) * 52  # Annualized
            
            # Calculate space efficiency (profit per inventory slot)
            space_efficiency = data['profit'] / max(1, len(data['products']))
            
            # Determine growth trend (simplified)
            growth_trend = self._calculate_growth_trend(category, sales_history)
            
            # Generate optimization recommendations
            optimization_opportunity, recommended_actions = self._generate_category_recommendations(
                category, profit_margin, inventory_turnover, space_efficiency, growth_trend
            )
            
            analysis = CategoryAnalysis(
                category=category,
                total_revenue=data['revenue'],
                total_profit=data['profit'],
                profit_margin=profit_margin,
                inventory_turnover=inventory_turnover,
                space_efficiency=space_efficiency,
                growth_trend=growth_trend,
                optimization_opportunity=optimization_opportunity,
                recommended_actions=recommended_actions
            )
            
            analyses.append(analysis)
        
        # Sort by total profit descending
        analyses.sort(key=lambda x: x.total_profit, reverse=True)
        
        return analyses
    
    def _get_recent_category_sales(self, product_name: str, sales_history: List[Dict], days: int = 7) -> List[int]:
        """Get recent sales for category analysis"""
        sales = []
        for day_data in sales_history[-days:]:
            daily_sales = day_data.get('daily_sales', {})
            sales.append(daily_sales.get(product_name, 0))
        return sales
    
    def _calculate_growth_trend(self, category: str, sales_history: List[Dict]) -> str:
        """Calculate growth trend for category"""
        if len(sales_history) < 6:
            return 'stable'
            
        # Compare first half vs second half of recent history
        mid_point = len(sales_history) // 2
        first_half = sales_history[:mid_point]
        second_half = sales_history[mid_point:]
        
        first_half_revenue = sum(sum(day.get('daily_sales', {}).values()) for day in first_half)
        second_half_revenue = sum(sum(day.get('daily_sales', {}).values()) for day in second_half)
        
        if second_half_revenue > first_half_revenue * 1.1:
            return 'growing'
        elif second_half_revenue < first_half_revenue * 0.9:
            return 'declining'
        else:
            return 'stable'
    
    def _generate_category_recommendations(self, category: str, profit_margin: float, 
                                         inventory_turnover: float, space_efficiency: float,
                                         growth_trend: str) -> tuple[str, List[str]]:
        """Generate category-specific recommendations"""
        
        recommendations = []
        
        # Profit margin analysis
        if profit_margin < 20:
            opportunity = "Low profitability"
            recommendations.append("Increase prices or reduce costs")
        elif profit_margin > 50:
            opportunity = "High margin opportunity"
            recommendations.append("Consider volume expansion")
        else:
            opportunity = "Balanced performance"
            
        # Inventory turnover analysis
        if inventory_turnover < 10:
            recommendations.append("Improve inventory turnover through promotions")
        elif inventory_turnover > 30:
            recommendations.append("Consider increasing stock levels for this high-velocity category")
            
        # Growth trend analysis
        if growth_trend == 'growing':
            recommendations.append("Expand this growing category with more variety")
        elif growth_trend == 'declining':
            recommendations.append("Investigate declining performance and consider category review")
            
        # Space efficiency
        if space_efficiency < 5:
            recommendations.append("Optimize space allocation for better profitability")
            
        return opportunity, recommendations


class StrategicPlanningEngine:
    """🧠 Phase 3B: Master Strategic Planning & Optimization Engine"""
    
    def __init__(self):
        self.inventory_optimizer = InventoryOptimizer()
        self.promotional_strategy = PromotionalStrategy()
        self.seasonal_planner = SeasonalPlanner()
        self.category_manager = CategoryManager()
        
    def generate_comprehensive_strategy(self, store_state: StoreState,
                                      sales_history: List[Dict],
                                      current_prices: Dict[str, float],
                                      current_season: str,
                                      market_events_engine) -> Dict[str, Any]:
        """🎯 Generate comprehensive strategic planning recommendations"""
        
        strategy = {
            'inventory_optimization': self.inventory_optimizer.calculate_inventory_recommendations(
                store_state, sales_history, current_prices
            ),
            'promotional_opportunities': self.promotional_strategy.identify_promotional_opportunities(
                store_state, sales_history, current_prices
            ),
            'seasonal_preparation': self.seasonal_planner.generate_seasonal_recommendations(
                store_state, current_season, self._get_next_season(current_season), market_events_engine
            ),
            'category_analysis': self.category_manager.analyze_category_performance(
                store_state, sales_history, current_prices
            ),
            'strategic_priorities': self._identify_strategic_priorities(store_state, sales_history),
            'execution_plan': self._create_execution_plan(store_state)
        }
        
        return strategy
    
    def _get_next_season(self, current_season: str) -> str:
        """Get the next season for planning"""
        seasons = ['spring', 'summer', 'fall', 'winter']
        current_index = seasons.index(current_season.lower())
        next_index = (current_index + 1) % len(seasons)
        return seasons[next_index]
    
    def _identify_strategic_priorities(self, store_state: StoreState, sales_history: List[Dict]) -> List[str]:
        """Identify top strategic priorities"""
        priorities = []
        
        # Cash flow priority
        if store_state.cash < 100:
            priorities.append("🚨 CRITICAL: Cash flow optimization required")
            
        # Inventory management priority
        stockouts = [name for name, item in store_state.inventory.items() if item.total_quantity == 0]
        if len(stockouts) > 2:
            priorities.append("📦 HIGH: Multiple stockouts - improve inventory management")
            
        # Profitability priority
        if len(sales_history) >= 3:
            recent_profits = [day.get('profit', 0) for day in sales_history[-3:]]
            if sum(recent_profits) < 0:
                priorities.append("💰 URGENT: Profitability issues - review pricing strategy")
                
        return priorities
    
    def _create_execution_plan(self, store_state: StoreState) -> List[str]:
        """Create actionable execution plan"""
        plan = [
            "1. Review inventory optimization recommendations and place strategic orders",
            "2. Implement promotional campaigns for slow-moving items",
            "3. Prepare for seasonal demand changes with inventory buildup",
            "4. Monitor category performance and adjust space allocation",
            "5. Execute strategic priorities in order of importance"
        ]
        return plan 