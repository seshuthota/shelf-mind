"""
💰 Gekko's Market Warfare Tools - Separated from agent logic
"""
from typing import Dict
from src.core.models import PRODUCTS

class PricingTools:
    """💰 Gekko's 5 Market Warfare Tools"""
    
    def competitive_pricing_analyzer(self, store_status: Dict, context: Dict) -> Dict:
        """🎯 TOOL 1: Advanced competitive pricing analysis and market intelligence"""
        current_prices = store_status.get('current_prices', {})
        competitor_prices = store_status.get('competitor_prices', {})
        yesterday_summary = context.get('yesterday_summary', {})
        
        competitive_intelligence = {
            'price_comparison_matrix': {},
            'competitive_advantage_score': 0,
            'market_penetration_opportunities': [],
            'defensive_strategies': [],
            'aggressive_tactics': []
        }
        
        total_advantage = 0
        total_products = len(current_prices)
        
        for product, our_price in current_prices.items():
            competitor_price = competitor_prices.get(product, our_price)
            price_difference = our_price - competitor_price
            percentage_diff = (price_difference / competitor_price) * 100 if competitor_price > 0 else 0
            
            # Calculate competitive position
            if price_difference < -0.05:  # We're cheaper
                position = "DOMINATING"
                advantage_score = 10
                competitive_intelligence['aggressive_tactics'].append(f"Maintain pressure on {product} - competitor vulnerable")
            elif price_difference > 0.05:  # We're more expensive
                position = "VULNERABLE"
                advantage_score = -5
                competitive_intelligence['defensive_strategies'].append(f"Reduce {product} price to regain market share")
            else:  # Close competition
                position = "CONTESTED"
                advantage_score = 2
                competitive_intelligence['market_penetration_opportunities'].append(f"Break deadlock on {product} with aggressive pricing")
            
            competitive_intelligence['price_comparison_matrix'][product] = {
                'our_price': our_price,
                'competitor_price': competitor_price,
                'price_difference': round(price_difference, 2),
                'percentage_difference': round(percentage_diff, 1),
                'competitive_position': position,
                'advantage_score': advantage_score
            }
            
            total_advantage += advantage_score
        
        competitive_intelligence['competitive_advantage_score'] = round(total_advantage / total_products, 1) if total_products > 0 else 0
        
        return competitive_intelligence
    
    def market_positioning_optimizer(self, store_status: Dict, context: Dict) -> Dict:
        """📈 TOOL 2: Strategic market positioning and profit maximization"""
        current_prices = store_status.get('current_prices', {})
        inventory = store_status.get('inventory', {})
        yesterday_summary = context.get('yesterday_summary', {})
        
        positioning_strategy = {
            'premium_opportunities': {},
            'value_plays': {},
            'loss_leader_candidates': {},
            'margin_expansion_targets': {},
            'positioning_recommendations': []
        }
        
        for product, price in current_prices.items():
            stock_level = inventory.get(product, 0)
            units_sold = yesterday_summary.get('units_sold_by_product', {}).get(product, 0)
            
            # Premium positioning analysis
            if units_sold >= 2 and stock_level >= 5:  # High demand + good stock
                premium_potential = min(price * 0.15, 0.50)  # 15% or $0.50 max increase
                positioning_strategy['premium_opportunities'][product] = {
                    'current_price': price,
                    'premium_price': round(price + premium_potential, 2),
                    'potential_margin_gain': round(premium_potential * units_sold, 2)
                }
            
            # Value positioning for market share
            if units_sold <= 1 and price > 1.5:  # Low demand + high price
                value_price = max(price * 0.85, 1.0)  # 15% discount minimum $1
                positioning_strategy['value_plays'][product] = {
                    'current_price': price,
                    'value_price': round(value_price, 2),
                    'expected_volume_boost': round(units_sold * 1.5, 1)
                }
            
            # Loss leader identification
            if product.lower() in ['coke', 'water', 'chips'] and stock_level >= 3:
                loss_leader_price = max(price * 0.9, 0.99)
                positioning_strategy['loss_leader_candidates'][product] = {
                    'current_price': price,
                    'loss_leader_price': round(loss_leader_price, 2),
                    'traffic_generation_potential': "HIGH"
                }
            
            # Margin expansion targets
            if units_sold >= 3 and stock_level <= 5:  # High demand + limited stock
                margin_price = min(price * 1.1, price + 0.30)
                positioning_strategy['margin_expansion_targets'][product] = {
                    'current_price': price,
                    'margin_price': round(margin_price, 2),
                    'scarcity_premium': round(margin_price - price, 2)
                }
        
        # Generate positioning recommendations
        if positioning_strategy['premium_opportunities']:
            positioning_strategy['positioning_recommendations'].append("Execute premium pricing on high-demand products")
        if positioning_strategy['value_plays']:
            positioning_strategy['positioning_recommendations'].append("Implement value pricing to capture market share")
        if positioning_strategy['loss_leader_candidates']:
            positioning_strategy['positioning_recommendations'].append("Deploy loss leaders for customer acquisition")
            
        return positioning_strategy
    
    def revenue_forecasting_model(self, store_status: Dict, context: Dict) -> Dict:
        """💹 TOOL 3: Advanced revenue forecasting and profit projections"""
        current_prices = store_status.get('current_prices', {})
        inventory = store_status.get('inventory', {})
        yesterday_summary = context.get('yesterday_summary', {})
        
        revenue_forecast = {
            'current_projections': {},
            'optimized_projections': {},
            'revenue_scenarios': {},
            'profit_maximization_plan': {},
            'forecast_confidence': 0
        }
        
        total_current_revenue = 0
        total_optimized_revenue = 0
        
        for product, price in current_prices.items():
            stock_level = inventory.get(product, 0)
            units_sold_yesterday = yesterday_summary.get('units_sold_by_product', {}).get(product, 0)
            
            # Base demand forecast
            base_daily_demand = max(units_sold_yesterday, 1)
            weekly_demand = base_daily_demand * 7
            
            # Current revenue projection
            current_weekly_revenue = weekly_demand * price
            revenue_forecast['current_projections'][product] = {
                'daily_demand': base_daily_demand,
                'weekly_revenue': round(current_weekly_revenue, 2),
                'stock_constraint': stock_level < weekly_demand
            }
            total_current_revenue += current_weekly_revenue
            
            # Optimized scenario (price elasticity modeling)
            if units_sold_yesterday >= 2:  # High-demand products
                optimized_price = min(price * 1.05, price + 0.20)  # 5% or $0.20 increase
                demand_reduction = 0.95  # 5% demand reduction
            elif units_sold_yesterday <= 1:  # Low-demand products
                optimized_price = max(price * 0.95, price - 0.15)  # 5% or $0.15 decrease  
                demand_reduction = 1.15  # 15% demand increase
            else:
                optimized_price = price
                demand_reduction = 1.0
                
            optimized_demand = base_daily_demand * demand_reduction
            optimized_weekly_revenue = optimized_demand * 7 * optimized_price
            
            revenue_forecast['optimized_projections'][product] = {
                'optimized_price': round(optimized_price, 2),
                'adjusted_demand': round(optimized_demand, 1),
                'optimized_weekly_revenue': round(optimized_weekly_revenue, 2),
                'revenue_lift': round(optimized_weekly_revenue - current_weekly_revenue, 2)
            }
            total_optimized_revenue += optimized_weekly_revenue
        
        # Revenue scenarios
        revenue_forecast['revenue_scenarios'] = {
            'conservative': round(total_current_revenue * 0.9, 2),
            'realistic': round(total_current_revenue, 2),
            'aggressive': round(total_optimized_revenue, 2),
            'stretch': round(total_optimized_revenue * 1.1, 2)
        }
        
        # Profit maximization plan
        revenue_lift = total_optimized_revenue - total_current_revenue
        revenue_forecast['profit_maximization_plan'] = {
            'total_current_weekly_revenue': round(total_current_revenue, 2),
            'total_optimized_weekly_revenue': round(total_optimized_revenue, 2),
            'weekly_revenue_lift': round(revenue_lift, 2),
            'annual_revenue_impact': round(revenue_lift * 52, 2)
        }
        
        # Forecast confidence
        products_with_data = sum(1 for product in yesterday_summary.get('units_sold_by_product', {}) if yesterday_summary['units_sold_by_product'][product] > 0)
        total_products = len(current_prices)
        revenue_forecast['forecast_confidence'] = round((products_with_data / total_products) * 100, 1) if total_products > 0 else 0
        
        return revenue_forecast
    
    def profit_margin_calculator(self, store_status: Dict, context: Dict) -> Dict:
        """📊 TOOL 4: Advanced profit margin analysis and optimization"""
        current_prices = store_status.get('current_prices', {})
        inventory = store_status.get('inventory', {})
        yesterday_summary = context.get('yesterday_summary', {})
        
        margin_analysis = {
            'product_margins': {},
            'margin_optimization_opportunities': {},
            'cost_analysis': {},
            'profitability_ranking': [],
            'margin_improvement_plan': {}
        }
        
        total_revenue = 0
        total_cost = 0
        
        for product, price in current_prices.items():
            units_sold = yesterday_summary.get('units_sold_by_product', {}).get(product, 0)
            unit_cost = PRODUCTS.get(product, {}).get('cost', price * 0.6)  # Default 40% margin
            
            # Calculate margins
            gross_margin = price - unit_cost
            margin_percentage = (gross_margin / price) * 100 if price > 0 else 0
            
            # Revenue and cost calculations
            product_revenue = units_sold * price
            product_cost = units_sold * unit_cost
            
            margin_analysis['product_margins'][product] = {
                'unit_cost': round(unit_cost, 2),
                'selling_price': price,
                'gross_margin': round(gross_margin, 2),
                'margin_percentage': round(margin_percentage, 1),
                'units_sold': units_sold,
                'total_revenue': round(product_revenue, 2),
                'total_profit': round(product_revenue - product_cost, 2)
            }
            
            total_revenue += product_revenue
            total_cost += product_cost
            
            # Identify optimization opportunities
            if margin_percentage < 30:  # Low margin
                target_price = unit_cost / 0.7  # Target 30% margin
                margin_analysis['margin_optimization_opportunities'][product] = {
                    'current_margin': round(margin_percentage, 1),
                    'target_margin': 30.0,
                    'recommended_price': round(target_price, 2),
                    'price_increase_needed': round(target_price - price, 2)
                }
            elif margin_percentage > 60 and units_sold <= 1:  # High margin but low volume
                competitive_price = price * 0.9  # 10% reduction
                margin_analysis['margin_optimization_opportunities'][product] = {
                    'current_margin': round(margin_percentage, 1),
                    'strategy': 'volume_play',
                    'recommended_price': round(competitive_price, 2),
                    'expected_volume_boost': '25-50%'
                }
        
        # Profitability ranking
        profitability_data = []
        for product, data in margin_analysis['product_margins'].items():
            profit_score = data['total_profit'] + (data['margin_percentage'] * 0.1)
            profitability_data.append((product, profit_score, data['total_profit']))
        
        margin_analysis['profitability_ranking'] = [
            {'product': product, 'profit': round(profit, 2), 'score': round(score, 1)}
            for product, score, profit in sorted(profitability_data, key=lambda x: x[1], reverse=True)
        ]
        
        # Overall margin improvement plan
        overall_margin = ((total_revenue - total_cost) / total_revenue) * 100 if total_revenue > 0 else 0
        margin_analysis['margin_improvement_plan'] = {
            'current_overall_margin': round(overall_margin, 1),
            'total_revenue': round(total_revenue, 2),
            'total_cost': round(total_cost, 2),
            'total_profit': round(total_revenue - total_cost, 2),
            'optimization_opportunities_count': len(margin_analysis['margin_optimization_opportunities'])
        }
        
        return margin_analysis
    
    def aggressive_pricing_simulator(self, store_status: Dict, context: Dict) -> Dict:
        """⚔️ TOOL 5: Aggressive pricing warfare simulation and strategy generator"""
        current_prices = store_status.get('current_prices', {})
        competitor_prices = store_status.get('competitor_prices', {})
        inventory = store_status.get('inventory', {})
        yesterday_summary = context.get('yesterday_summary', {})
        
        warfare_simulation = {
            'aggressive_scenarios': {},
            'price_war_outcomes': {},
            'market_domination_plan': {},
            'risk_assessment': {},
            'warfare_recommendations': []
        }
        
        for product, our_price in current_prices.items():
            competitor_price = competitor_prices.get(product, our_price)
            units_sold = yesterday_summary.get('units_sold_by_product', {}).get(product, 0)
            stock_level = inventory.get(product, 0)
            
            # Aggressive pricing scenarios
            scenarios = {}
            
            # Scenario 1: Undercut by 10%
            undercut_price = round(competitor_price * 0.9, 2)
            scenarios['undercut_aggressive'] = {
                'price': undercut_price,
                'expected_demand_boost': 1.4,  # 40% boost
                'market_share_gain': '15-25%',
                'risk_level': 'MEDIUM'
            }
            
            # Scenario 2: Match and hold
            scenarios['match_competitor'] = {
                'price': competitor_price,
                'expected_demand_boost': 1.1,  # 10% boost
                'market_share_gain': '5-10%',
                'risk_level': 'LOW'
            }
            
            # Scenario 3: Nuclear option (20% below competitor)
            nuclear_price = round(competitor_price * 0.8, 2)
            scenarios['nuclear_warfare'] = {
                'price': nuclear_price,
                'expected_demand_boost': 1.8,  # 80% boost
                'market_share_gain': '30-50%',
                'risk_level': 'HIGH'
            }
            
            warfare_simulation['aggressive_scenarios'][product] = scenarios
            
            # Price war outcome predictions
            if competitor_price > our_price:
                warfare_outcome = "WINNING - Maintain pressure"
            elif competitor_price == our_price:
                warfare_outcome = "STALEMATE - Escalate or diversify"
            else:
                warfare_outcome = "LOSING - Immediate action required"
                
            warfare_simulation['price_war_outcomes'][product] = {
                'current_status': warfare_outcome,
                'competitive_gap': round(our_price - competitor_price, 2),
                'action_urgency': 'HIGH' if our_price > competitor_price else 'MEDIUM'
            }
            
            # Risk assessment
            unit_cost = PRODUCTS.get(product, {}).get('cost', our_price * 0.6)
            min_viable_price = unit_cost * 1.1  # 10% minimum margin
            
            warfare_simulation['risk_assessment'][product] = {
                'unit_cost': round(unit_cost, 2),
                'minimum_viable_price': round(min_viable_price, 2),
                'price_floor_risk': undercut_price < min_viable_price,
                'inventory_risk': stock_level < 3,
                'demand_surge_capacity': stock_level >= 5
            }
        
        # Market domination plan
        domination_targets = []
        for product, outcomes in warfare_simulation['price_war_outcomes'].items():
            if outcomes['action_urgency'] == 'HIGH':
                domination_targets.append(product)
        
        warfare_simulation['market_domination_plan'] = {
            'priority_targets': domination_targets,
            'coordinated_assault': len(domination_targets) >= 2,
            'resource_requirements': f"${len(domination_targets) * 50} war chest needed",
            'timeline': '1-2 weeks for market impact'
        }
        
        # Warfare recommendations
        warfare_simulation['warfare_recommendations'] = [
            "Execute coordinated price attacks on multiple fronts",
            "Monitor competitor responses and counter-attack immediately",
            "Maintain inventory buffers for demand surges",
            "Prepare psychological pricing ($X.99) for maximum impact",
            "Document all moves for pattern recognition"
        ]
        
        return warfare_simulation
