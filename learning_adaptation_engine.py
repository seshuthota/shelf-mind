from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, deque
import statistics
import json
from models import StoreState, CustomerType, PRODUCTS, MarketEvent

@dataclass
class CustomerLearning:
    """Dynamic customer segment analysis results"""
    actual_price_sensitive_ratio: float
    actual_brand_loyal_ratio: float
    segment_shift: float  # How much segments changed from baseline
    lost_sales_value: float
    lost_sales_products: Dict[str, int]
    market_shift_warning: Optional[str] = None

@dataclass
class ProductTrend:
    """Product lifecycle and trend analysis"""
    product_name: str
    trend_direction: str  # 'rising', 'falling', 'stable'
    trend_strength: float  # -1.0 to 1.0
    days_in_trend: int
    sales_velocity: float  # Units per day
    lifecycle_stage: str  # 'star', 'cash_cow', 'dog', 'question_mark'
    recommendation: str

@dataclass
class PriceElasticity:
    """Price elasticity learning for products"""
    product_name: str
    elasticity_coefficient: float  # How responsive demand is to price changes
    confidence_level: float  # How confident we are in this measurement
    price_sensitivity: str  # 'high', 'medium', 'low'
    last_test_result: Optional[str] = None

@dataclass
class AdaptiveStrategy:
    """Dynamic strategy adjustment"""
    strategy_name: str
    original_rule: str
    adapted_rule: str
    success_rate: float
    adaptation_reason: str
    last_updated: int

@dataclass
class LearningInsight:
    """Generated learning insights for agent"""
    insight_type: str  # 'customer', 'trend', 'elasticity', 'strategy'
    priority: str  # 'critical', 'high', 'medium', 'low'
    message: str
    data: Dict[str, Any]
    actionable: bool

class LearningAdaptationEngine:
    """🧠 Phase 3C: Learning & Adaptation Systems Engine
    
    Transform Scrooge into a truly self-improving AI that:
    - Learns from customer behavior patterns dynamically
    - Recognizes market trends and adapts strategies
    - Builds a library of successful patterns
    - Rewrites its own heuristics based on experience
    """
    
    def __init__(self):
        # Customer Learning Systems
        self.daily_customer_data = deque(maxlen=30)  # 30 days of customer data
        self.lost_sales_history = []
        self.segment_evolution = []
        
        # Market Trend Analysis
        self.product_sales_history = defaultdict(lambda: deque(maxlen=14))  # 14-day sliding window
        self.price_change_experiments = []
        self.product_trends = {}
        self.price_elasticity = {}
        
        # Adaptive Strategy System
        self.adaptive_strategies = {}
        self.strategy_library = []
        self.dynamic_heuristics = self._initialize_base_heuristics()
        
        # Learning Insights
        self.learning_insights = []
        self.pattern_confidence_threshold = 0.7
        
    def process_daily_learning(self, store_state: StoreState, customer_purchases: List, 
                             yesterday_sales: Dict[str, int], market_context: Dict,
                             pricing_changes: Dict[str, float] = None, current_prices: Dict[str, float] = None) -> Dict[str, Any]:
        """🧠 Main daily learning processing - analyze all learning dimensions"""
        
        learning_results = {}
        
        # 1. Customer Feedback Integration
        customer_learning = self._analyze_customer_behavior(customer_purchases, store_state)
        lost_sales_analysis = self._analyze_lost_sales(store_state, yesterday_sales, current_prices)
        learning_results['customer_learning'] = customer_learning
        learning_results['lost_sales'] = lost_sales_analysis
        
        # 2. Market Trend Recognition  
        trend_analysis = self._analyze_product_trends(yesterday_sales, store_state.day)
        elasticity_learning = self._analyze_price_elasticity(pricing_changes, yesterday_sales, store_state.day)
        learning_results['trend_analysis'] = trend_analysis
        learning_results['price_elasticity'] = elasticity_learning
        
        # 3. Adaptive Strategy Refinement
        strategy_updates = self._update_adaptive_strategies(store_state, customer_learning, trend_analysis)
        pattern_library = self._update_strategy_library(store_state, market_context)
        learning_results['strategy_updates'] = strategy_updates
        learning_results['pattern_library'] = pattern_library
        
        # Generate actionable insights
        insights = self._generate_learning_insights(learning_results)
        learning_results['insights'] = insights
        
        return learning_results
    
    def get_adaptive_agent_prompts(self) -> Dict[str, str]:
        """🎯 Generate dynamic prompts that adapt based on learning"""
        
        prompts = {}
        
        # Dynamic customer segmentation insights
        if self.segment_evolution:
            latest_segments = self.segment_evolution[-1]
            prompts['customer_intelligence'] = f"""
🎯 DYNAMIC CUSTOMER INTELLIGENCE (LEARNED FROM EXPERIENCE):
- Current market is {latest_segments.actual_price_sensitive_ratio:.0%} price-sensitive, {latest_segments.actual_brand_loyal_ratio:.0%} brand-loyal
- Segment shift: {latest_segments.segment_shift:+.1%} from baseline (60/40 split)
{latest_segments.market_shift_warning if latest_segments.market_shift_warning else ''}
- Lost sales value: ${latest_segments.lost_sales_value:.2f} (learn from these mistakes!)
"""
        
        # Product trend intelligence
        if self.product_trends:
            trend_insights = []
            for product, trend in self.product_trends.items():
                if trend.trend_direction != 'stable':
                    trend_insights.append(f"• {product}: {trend.trend_direction.upper()} {trend.days_in_trend} days ({trend.lifecycle_stage}) - {trend.recommendation}")
            
            if trend_insights:
                prompts['trend_intelligence'] = f"""
📈 PRODUCT LIFECYCLE INTELLIGENCE (LEARNED FROM SALES PATTERNS):
{chr(10).join(trend_insights)}
"""
        
        # Price elasticity wisdom
        if self.price_elasticity:
            elasticity_insights = []
            for product, elasticity in self.price_elasticity.items():
                if elasticity.confidence_level > 0.6:
                    elasticity_insights.append(f"• {product}: {elasticity.price_sensitivity.upper()} elasticity ({elasticity.elasticity_coefficient:.2f}) - {elasticity.last_test_result}")
            
            if elasticity_insights:
                prompts['elasticity_intelligence'] = f"""
💰 PRICE ELASTICITY WISDOM (LEARNED FROM PRICING EXPERIMENTS):
{chr(10).join(elasticity_insights)}
"""
        
        # Adaptive strategy heuristics
        if self.adaptive_strategies:
            strategy_updates = []
            for name, strategy in self.adaptive_strategies.items():
                if strategy.success_rate != 1.0:  # Only show adapted strategies
                    strategy_updates.append(f"• {name}: {strategy.adapted_rule} (Success: {strategy.success_rate:.0%}) - {strategy.adaptation_reason}")
            
            if strategy_updates:
                prompts['adaptive_strategies'] = f"""
🧠 ADAPTIVE STRATEGY EVOLUTION (LEARNED FROM EXPERIENCE):
{chr(10).join(strategy_updates)}
"""
        
        return prompts
    
    def get_strategy_playbook(self, current_conditions: Dict[str, Any]) -> List[str]:
        """📚 Get relevant strategies from learned pattern library"""
        
        relevant_strategies = []
        
        for pattern in self.strategy_library:
            # Check if current conditions match pattern conditions
            match_score = self._calculate_pattern_match(pattern['conditions'], current_conditions)
            
            if match_score > self.pattern_confidence_threshold:
                confidence = pattern['confidence_score']
                profit_impact = pattern['avg_profit_impact']
                relevant_strategies.append(
                    f"PROVEN STRATEGY (Match: {match_score:.0%}, Success: {confidence:.0%}, Profit: +${profit_impact:.2f}): {pattern['description']}"
                )
        
        return relevant_strategies[:3]  # Top 3 most relevant strategies
    
    def _analyze_customer_behavior(self, customer_purchases: List, store_state: StoreState) -> CustomerLearning:
        """🎯 Dynamic customer segment analysis"""
        
        if not customer_purchases:
            return CustomerLearning(0.6, 0.4, 0.0, 0.0, {})
        
        # Count actual customer segments from purchases
        price_sensitive_count = sum(1 for p in customer_purchases if p.customer_type == CustomerType.PRICE_SENSITIVE)
        brand_loyal_count = sum(1 for p in customer_purchases if p.customer_type == CustomerType.BRAND_LOYAL)
        total_customers = len(customer_purchases)
        
        actual_price_sensitive = price_sensitive_count / total_customers if total_customers > 0 else 0.6
        actual_brand_loyal = brand_loyal_count / total_customers if total_customers > 0 else 0.4
        
        # Calculate shift from baseline (60/40)
        baseline_price_sensitive = 0.6
        segment_shift = actual_price_sensitive - baseline_price_sensitive
        
        # Generate market shift warning
        warning = None
        if abs(segment_shift) > 0.15:  # 15% shift threshold
            if segment_shift > 0:
                warning = "⚠️ MARKET ALERT: Aggressive price wars are attracting more price-sensitive customers!"
            else:
                warning = "⚠️ MARKET ALERT: Premium pricing is shifting market toward brand-loyal customers!"
        
        customer_learning = CustomerLearning(
            actual_price_sensitive_ratio=actual_price_sensitive,
            actual_brand_loyal_ratio=actual_brand_loyal,
            segment_shift=segment_shift,
            lost_sales_value=0.0,  # Will be updated by lost sales analysis
            lost_sales_products={},
            market_shift_warning=warning
        )
        
        self.segment_evolution.append(customer_learning)
        return customer_learning
    
    def _analyze_lost_sales(self, store_state: StoreState, yesterday_sales: Dict[str, int], current_prices: Dict[str, float] = None) -> Dict[str, Any]:
        """💸 Analyze lost sales due to stockouts"""
        
        lost_sales_value = 0.0
        lost_products = {}
        
        for product_name, quantity in store_state.inventory.items():
            if quantity.total_quantity == 0:  # Stockout
                # Estimate lost sales based on average daily sales
                if len(self.product_sales_history[product_name]) > 0:
                    avg_daily_sales = statistics.mean(self.product_sales_history[product_name])
                    estimated_lost_units = max(1, int(avg_daily_sales * 0.5))  # Conservative estimate
                    
                    lost_value = estimated_lost_units * current_prices.get(product_name, 0) if current_prices else 0
                    lost_sales_value += lost_value
                    lost_products[product_name] = estimated_lost_units
        
        lost_sales_analysis = {
            'total_lost_value': lost_sales_value,
            'lost_products': lost_products,
            'stockout_count': len(lost_products)
        }
        
        # Update customer learning with lost sales
        if self.segment_evolution:
            self.segment_evolution[-1].lost_sales_value = lost_sales_value
            self.segment_evolution[-1].lost_sales_products = lost_products
        
        self.lost_sales_history.append(lost_sales_analysis)
        return lost_sales_analysis
    
    def _analyze_product_trends(self, yesterday_sales: Dict[str, int], current_day: int) -> Dict[str, ProductTrend]:
        """📈 Product lifecycle and trend analysis"""
        
        trends = {}
        
        for product_name, sales in yesterday_sales.items():
            # Update sales history
            self.product_sales_history[product_name].append(sales)
            
            # Need at least 7 days for trend analysis
            if len(self.product_sales_history[product_name]) >= 7:
                trend = self._calculate_product_trend(product_name, current_day)
                trends[product_name] = trend
                self.product_trends[product_name] = trend
        
        return trends
    
    def _calculate_product_trend(self, product_name: str, current_day: int) -> ProductTrend:
        """Calculate individual product trend"""
        
        sales_data = list(self.product_sales_history[product_name])
        
        # Calculate trend using linear regression approximation
        if len(sales_data) >= 7:
            recent_avg = statistics.mean(sales_data[-3:])  # Last 3 days
            older_avg = statistics.mean(sales_data[-7:-4])  # 4-7 days ago
            
            trend_strength = (recent_avg - older_avg) / max(older_avg, 1)  # Avoid division by zero
            
            # Determine trend direction
            if trend_strength > 0.2:  # 20% increase
                direction = 'rising'
                days_in_trend = self._count_consecutive_trend_days(sales_data, 'rising')
            elif trend_strength < -0.2:  # 20% decrease
                direction = 'falling'  
                days_in_trend = self._count_consecutive_trend_days(sales_data, 'falling')
            else:
                direction = 'stable'
                days_in_trend = 0
            
            # Determine lifecycle stage
            avg_sales = statistics.mean(sales_data)
            if avg_sales > 8 and direction == 'rising':
                lifecycle_stage = 'star'
                recommendation = "Increase inventory and consider premium pricing"
            elif avg_sales > 6 and direction == 'stable':
                lifecycle_stage = 'cash_cow'
                recommendation = "Maintain current strategy, reliable performer"
            elif avg_sales < 3 and direction == 'falling':
                lifecycle_stage = 'dog'
                recommendation = "Consider promotional pricing or reduced inventory"
            else:
                lifecycle_stage = 'question_mark'
                recommendation = "Monitor closely and test pricing strategies"
            
            return ProductTrend(
                product_name=product_name,
                trend_direction=direction,
                trend_strength=trend_strength,
                days_in_trend=days_in_trend,
                sales_velocity=avg_sales,
                lifecycle_stage=lifecycle_stage,
                recommendation=recommendation
            )
        
        # Not enough data
        return ProductTrend(
            product_name=product_name,
            trend_direction='unknown',
            trend_strength=0.0,
            days_in_trend=0,
            sales_velocity=0.0,
            lifecycle_stage='unknown',
            recommendation="Collect more sales data"
        )
    
    def _count_consecutive_trend_days(self, sales_data: List[int], trend_type: str) -> int:
        """Count consecutive days in current trend"""
        if len(sales_data) < 3:
            return 0
        
        consecutive_days = 0
        for i in range(len(sales_data) - 1, 0, -1):
            if trend_type == 'rising' and sales_data[i] > sales_data[i-1]:
                consecutive_days += 1
            elif trend_type == 'falling' and sales_data[i] < sales_data[i-1]:
                consecutive_days += 1
            else:
                break
        
        return consecutive_days
    
    def _analyze_price_elasticity(self, pricing_changes: Dict[str, float], yesterday_sales: Dict[str, int], current_day: int) -> Dict[str, PriceElasticity]:
        """💰 Learn price elasticity from pricing experiments"""
        
        elasticity_results = {}
        
        if pricing_changes:
            # Record price change experiments
            for product, new_price in pricing_changes.items():
                experiment = {
                    'day': current_day,
                    'product': product,
                    'price_change': new_price,
                    'sales_result': yesterday_sales.get(product, 0)
                }
                self.price_change_experiments.append(experiment)
        
        # Analyze existing experiments for elasticity learning
        for product_name in PRODUCTS.keys():
            elasticity = self._calculate_price_elasticity(product_name)
            if elasticity:
                elasticity_results[product_name] = elasticity
                self.price_elasticity[product_name] = elasticity
        
        return elasticity_results
    
    def _calculate_price_elasticity(self, product_name: str) -> Optional[PriceElasticity]:
        """Calculate price elasticity for a specific product"""
        
        # Find price change experiments for this product
        product_experiments = [e for e in self.price_change_experiments if e['product'] == product_name]
        
        if len(product_experiments) < 2:
            return None
        
        # Analyze most recent experiments
        recent_experiments = product_experiments[-3:]  # Last 3 experiments
        
        # Simple elasticity calculation
        price_changes = []
        sales_changes = []
        
        for i in range(1, len(recent_experiments)):
            prev_exp = recent_experiments[i-1]
            curr_exp = recent_experiments[i]
            
            price_change_pct = (curr_exp['price_change'] - prev_exp['price_change']) / prev_exp['price_change']
            sales_change_pct = (curr_exp['sales_result'] - prev_exp['sales_result']) / max(prev_exp['sales_result'], 1)
            
            if abs(price_change_pct) > 0.01:  # Meaningful price change
                elasticity_coeff = sales_change_pct / price_change_pct
                price_changes.append(price_change_pct)
                sales_changes.append(elasticity_coeff)
        
        if not sales_changes:
            return None
        
        # Average elasticity coefficient
        avg_elasticity = statistics.mean(sales_changes)
        confidence = min(len(sales_changes) / 5.0, 1.0)  # Higher confidence with more data
        
        # Classify price sensitivity
        if abs(avg_elasticity) > 1.5:
            sensitivity = 'high'
            test_result = "Highly price elastic - small price changes cause large demand changes"
        elif abs(avg_elasticity) > 0.5:
            sensitivity = 'medium'
            test_result = "Moderately price elastic - typical price sensitivity"
        else:
            sensitivity = 'low'
            test_result = "Price inelastic - demand relatively stable despite price changes"
        
        return PriceElasticity(
            product_name=product_name,
            elasticity_coefficient=avg_elasticity,
            confidence_level=confidence,
            price_sensitivity=sensitivity,
            last_test_result=test_result
        )
    
    def _update_adaptive_strategies(self, store_state: StoreState, customer_learning: CustomerLearning, trend_analysis: Dict[str, ProductTrend]) -> Dict[str, AdaptiveStrategy]:
        """🧠 Update agent's strategies based on learning"""
        
        strategy_updates = {}
        
        # Adapt inventory ordering strategy based on spoilage and stockouts
        inventory_strategy = self._adapt_inventory_strategy(store_state)
        if inventory_strategy:
            strategy_updates['inventory_ordering'] = inventory_strategy
            self.adaptive_strategies['inventory_ordering'] = inventory_strategy
        
        # Adapt pricing strategy based on customer segments
        pricing_strategy = self._adapt_pricing_strategy(customer_learning)
        if pricing_strategy:
            strategy_updates['pricing_strategy'] = pricing_strategy
            self.adaptive_strategies['pricing_strategy'] = pricing_strategy
        
        # Adapt product focus based on trends
        product_strategy = self._adapt_product_strategy(trend_analysis)
        if product_strategy:
            strategy_updates['product_focus'] = product_strategy
            self.adaptive_strategies['product_focus'] = product_strategy
        
        return strategy_updates
    
    def _adapt_inventory_strategy(self, store_state: StoreState) -> Optional[AdaptiveStrategy]:
        """Adapt inventory ordering rules based on performance"""
        
        # Analyze recent inventory performance
        spoilage_rate = 0.0  # Could calculate from spoilage data
        stockout_rate = len([1 for item in store_state.inventory.values() if item.total_quantity == 0]) / len(store_state.inventory)
        
        original_rule = "Order high-selling items (8-12 units), medium-selling (5-8 units), low-selling (3-5 units)"
        
        if stockout_rate > 0.3:  # 30% stockout rate
            adapted_rule = "ADAPTED: Increase safety stock - High-selling (10-15 units), medium-selling (7-10 units), low-selling (4-6 units)"
            reason = f"High stockout rate ({stockout_rate:.0%}) causing lost sales"
            success_rate = 0.6  # Lower success rate due to stockouts
        elif spoilage_rate > 0.2:  # 20% spoilage rate
            adapted_rule = "ADAPTED: Reduce ordering to prevent spoilage - High-selling (6-9 units), medium-selling (4-6 units), low-selling (2-4 units)"
            reason = f"High spoilage rate ({spoilage_rate:.0%}) wasting money"
            success_rate = 0.7
        else:
            return None  # No adaptation needed
        
        return AdaptiveStrategy(
            strategy_name="Inventory Ordering",
            original_rule=original_rule,
            adapted_rule=adapted_rule,
            success_rate=success_rate,
            adaptation_reason=reason,
            last_updated=store_state.day
        )
    
    def _adapt_pricing_strategy(self, customer_learning: CustomerLearning) -> Optional[AdaptiveStrategy]:
        """Adapt pricing strategy based on customer segment shifts"""
        
        original_rule = "Balance competitive prices with profitability (60% price-sensitive customers)"
        
        if customer_learning.segment_shift > 0.15:  # Market shifted toward price-sensitive
            adapted_rule = f"ADAPTED: Focus on competitive pricing - Market is {customer_learning.actual_price_sensitive_ratio:.0%} price-sensitive"
            reason = f"Market shifted +{customer_learning.segment_shift:.0%} toward price-sensitive customers"
            success_rate = 0.8
        elif customer_learning.segment_shift < -0.15:  # Market shifted toward brand-loyal
            adapted_rule = f"ADAPTED: Premium pricing opportunity - Market is {customer_learning.actual_brand_loyal_ratio:.0%} brand-loyal"
            reason = f"Market shifted {customer_learning.segment_shift:.0%} toward brand-loyal customers"
            success_rate = 0.8
        else:
            return None  # No adaptation needed
        
        return AdaptiveStrategy(
            strategy_name="Pricing Strategy",
            original_rule=original_rule,
            adapted_rule=adapted_rule,
            success_rate=success_rate,
            adaptation_reason=reason,
            last_updated=0  # Will be set by caller
        )
    
    def _adapt_product_strategy(self, trend_analysis: Dict[str, ProductTrend]) -> Optional[AdaptiveStrategy]:
        """Adapt product focus based on trend analysis"""
        
        rising_products = [name for name, trend in trend_analysis.items() if trend.trend_direction == 'rising']
        falling_products = [name for name, trend in trend_analysis.items() if trend.trend_direction == 'falling']
        
        if len(rising_products) >= 2 or len(falling_products) >= 2:
            original_rule = "Focus equally on all products"
            
            focus_items = rising_products[:2] if rising_products else []
            reduce_items = falling_products[:2] if falling_products else []
            
            adapted_rule = f"ADAPTED: Focus on trending products - Prioritize: {', '.join(focus_items)} | Reduce: {', '.join(reduce_items)}"
            reason = f"Trends detected: {len(rising_products)} rising, {len(falling_products)} falling"
            success_rate = 0.75
            
            return AdaptiveStrategy(
                strategy_name="Product Focus",
                original_rule=original_rule,
                adapted_rule=adapted_rule,
                success_rate=success_rate,
                adaptation_reason=reason,
                last_updated=0
            )
        
        return None
    
    def _update_strategy_library(self, store_state: StoreState, market_context: Dict) -> List[Dict[str, Any]]:
        """📚 Build library of successful strategy patterns"""
        
        # Analyze recent successful decisions for patterns
        if store_state.total_profit > 50:  # Only analyze when profitable
            
            # Create pattern from current successful state
            pattern = {
                'conditions': {
                    'season': market_context.get('season', 'unknown'),
                    'weather': market_context.get('weather', 'unknown'),
                    'profit_level': 'high' if store_state.total_profit > 100 else 'medium',
                    'cash_level': 'high' if store_state.cash > 200 else 'medium',
                    'day_range': f"{(store_state.day - 1) // 7 * 7 + 1}-{(store_state.day - 1) // 7 * 7 + 7}"
                },
                'description': f"Successful strategy on day {store_state.day} - ${store_state.total_profit:.2f} profit",
                'avg_profit_impact': store_state.total_profit / store_state.day,  # Profit per day
                'confidence_score': 0.8,  # Could be calculated based on repetition
                'pattern_id': f"success_{store_state.day}"
            }
            
            # Add to library if not duplicate
            existing_patterns = [p['pattern_id'] for p in self.strategy_library]
            if pattern['pattern_id'] not in existing_patterns:
                self.strategy_library.append(pattern)
        
        return self.strategy_library
    
    def _calculate_pattern_match(self, pattern_conditions: Dict[str, Any], current_conditions: Dict[str, Any]) -> float:
        """Calculate how well current conditions match a pattern"""
        
        matches = 0
        total_conditions = len(pattern_conditions)
        
        for key, value in pattern_conditions.items():
            if key in current_conditions and current_conditions[key] == value:
                matches += 1
            elif key == 'profit_level':
                # Special handling for profit levels
                current_profit = current_conditions.get('profit', 0)
                if (value == 'high' and current_profit > 100) or (value == 'medium' and 50 <= current_profit <= 100):
                    matches += 1
        
        return matches / total_conditions if total_conditions > 0 else 0.0
    
    def _generate_learning_insights(self, learning_results: Dict[str, Any]) -> List[LearningInsight]:
        """Generate actionable learning insights for the agent"""
        
        insights = []
        
        # Customer learning insights
        customer_learning = learning_results.get('customer_learning')
        if customer_learning and customer_learning.market_shift_warning:
            insights.append(LearningInsight(
                insight_type='customer',
                priority='critical',
                message=customer_learning.market_shift_warning,
                data={'segment_shift': customer_learning.segment_shift},
                actionable=True
            ))
        
        # Lost sales insights
        lost_sales = learning_results.get('lost_sales', {})
        if lost_sales.get('total_lost_value', 0) > 20:
            insights.append(LearningInsight(
                insight_type='customer',
                priority='high',
                message=f"CRITICAL LEARNING: Lost ${lost_sales['total_lost_value']:.2f} in sales due to stockouts on {', '.join(lost_sales['lost_products'].keys())}",
                data=lost_sales,
                actionable=True
            ))
        
        # Trend insights
        trend_analysis = learning_results.get('trend_analysis', {})
        for product, trend in trend_analysis.items():
            if trend.trend_direction in ['rising', 'falling'] and trend.days_in_trend >= 3:
                priority = 'high' if trend.days_in_trend >= 5 else 'medium'
                insights.append(LearningInsight(
                    insight_type='trend',
                    priority=priority,
                    message=f"TREND ALERT: {product} sales {trend.trend_direction} for {trend.days_in_trend} days - {trend.recommendation}",
                    data={'product': product, 'trend': trend.trend_direction, 'days': trend.days_in_trend},
                    actionable=True
                ))
        
        # Price elasticity insights
        price_elasticity = learning_results.get('price_elasticity', {})
        for product, elasticity in price_elasticity.items():
            if elasticity.confidence_level > 0.7:
                insights.append(LearningInsight(
                    insight_type='elasticity',
                    priority='medium',
                    message=f"ELASTICITY LEARNING: {product} is {elasticity.price_sensitivity} price elastic - {elasticity.last_test_result}",
                    data={'product': product, 'sensitivity': elasticity.price_sensitivity, 'coefficient': elasticity.elasticity_coefficient},
                    actionable=True
                ))
        
        self.learning_insights.extend(insights)
        return insights
    
    def _initialize_base_heuristics(self) -> Dict[str, str]:
        """Initialize base heuristics that can be adapted"""
        return {
            'inventory_ordering': "Order high-selling items (8-12 units), medium-selling (5-8 units), low-selling (3-5 units)",
            'pricing_strategy': "Balance competitive prices with profitability (60% price-sensitive customers)",
            'product_focus': "Focus equally on all products",
            'crisis_response': "React quickly to supply chain disruptions",
            'seasonal_planning': "Increase inventory before seasonal demand spikes"
        }
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """📊 Generate comprehensive learning summary for dashboard"""
        
        summary = {
            'customer_evolution': len(self.segment_evolution),
            'trend_products_tracked': len(self.product_trends),
            'price_experiments': len(self.price_change_experiments),
            'adaptive_strategies': len(self.adaptive_strategies),
            'strategy_patterns': len(self.strategy_library),
            'learning_insights': len([i for i in self.learning_insights if i.priority in ['critical', 'high']]),
            'recent_insights': [i.message for i in self.learning_insights[-3:]]  # Last 3 insights
        }
        
        return summary 