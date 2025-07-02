from typing import Dict, List, Any, Optional
import json
from src.core.multi_agent_engine import BaseSpecialistAgent, AgentRole, AgentDecision
from src.core.agent_prompts import AgentPrompts
from src.core.models import PRODUCTS
from src.tools.inventory_tools import InventoryTools

class InventoryManagerAgent(BaseSpecialistAgent):
    """🏭 Phase 4A.1: Inventory Manager Specialist Agent
    
    Responsible for:
    - Inventory optimization and reorder decisions
    - Stock level monitoring and alerts
    - Supplier selection and ordering strategy
    - Spoilage prevention and inventory turnover
    """
    
    def __init__(self, provider: str = "openai"):
        super().__init__(AgentRole.INVENTORY_MANAGER, provider)
        # 🔬 Phase 4B.2: Initialize separated analytics tools
        self.tools = InventoryTools()
        
    def _define_specializations(self) -> List[str]:
        """Define inventory management specializations"""
        return [
            "Stock level optimization",
            "Reorder point calculations", 
            "Supplier selection and negotiations",
            "Spoilage prevention and FIFO management",
            "Seasonal inventory planning",
            "Emergency restocking procedures"
        ]
        
    def analyze_situation(self, store_status: Dict, context: Dict) -> AgentDecision:
        """🏭 Hermione Granger analyzes inventory situation with methodical precision"""
        
        # Gather inventory intelligence with Hermione's systematic approach
        inventory_analysis = self._analyze_inventory_levels(store_status)
        supplier_intelligence = self._analyze_supplier_situation(store_status)
        demand_forecast = self._forecast_demand(store_status, context)
        
        # Generate inventory action plan
        action_plan = self._create_action_plan(inventory_analysis, supplier_intelligence, demand_forecast)
        
        # Calculate confidence based on data quality and certainty
        confidence = self._calculate_confidence(store_status, inventory_analysis)
        
        # Determine priority (inventory issues are urgent)
        priority = self._determine_priority(inventory_analysis)
        
        # 🎭 Generate Hermione's reasoning with character personality
        hermione_reasoning = self._generate_hermione_reasoning(inventory_analysis, supplier_intelligence, action_plan)
        
        # Store decision info for UI display
        self.last_decision_summary = f"Inventory optimization"
        self.last_confidence = confidence
        
        return AgentDecision(
            agent_role=self.role,
            decision_type="inventory_optimization",
            parameters=action_plan,
            confidence=confidence,
            reasoning=hermione_reasoning,
            priority=priority
        )
        
    def _analyze_inventory_levels(self, store_status: Dict) -> Dict:
        """Analyze current inventory levels and identify issues"""
        inventory = store_status.get('inventory', {})
        
        analysis = {
            'stockouts': [],
            'low_stock': [],
            'overstocked': [],
            'optimal': [],
            'total_items': len(inventory),
            'stockout_risk_score': 0
        }
        
        for product_name, quantity in inventory.items():
            # Ensure quantity is a number (not a dict or InventoryItem object)
            if isinstance(quantity, dict):
                quantity = quantity.get('total_quantity', 0)
            elif hasattr(quantity, 'total_quantity'):
                quantity = quantity.total_quantity
            elif not isinstance(quantity, (int, float)):
                quantity = 0
                
            if quantity == 0:
                analysis['stockouts'].append(product_name)
                analysis['stockout_risk_score'] += 10  # High penalty for stockouts
            elif quantity <= 2:
                analysis['low_stock'].append(product_name)
                analysis['stockout_risk_score'] += 5  # Medium penalty for low stock
            elif quantity >= 15:  # High inventory level
                analysis['overstocked'].append(product_name)
            else:
                analysis['optimal'].append(product_name)
                
        return analysis
        
    def _analyze_supplier_situation(self, store_status: Dict) -> Dict:
        """Analyze supplier conditions and pending deliveries"""
        return {
            'pending_deliveries': store_status.get('pending_deliveries', []),
            'supplier_available': True,  # Assume suppliers available for Phase 4A.1
            'bulk_opportunities': self._identify_bulk_opportunities(store_status),
            'payment_terms_optimal': True  # Simplified for Phase 4A.1
        }
        
    def _identify_bulk_opportunities(self, store_status: Dict) -> List[str]:
        """Identify products that could benefit from bulk ordering"""
        inventory = store_status.get('inventory', {})
        bulk_candidates = []
        
        for product_name, quantity in inventory.items():
            # Ensure quantity is a number (not a dict or InventoryItem object)
            if isinstance(quantity, dict):
                quantity = quantity.get('total_quantity', 0)
            elif hasattr(quantity, 'total_quantity'):
                quantity = quantity.total_quantity
            elif not isinstance(quantity, (int, float)):
                quantity = 0
                
            # If we're low on high-volume products, consider bulk ordering
            if quantity <= 5 and product_name in ['Coke', 'Chips', 'Candy']:
                bulk_candidates.append(product_name)
                
        return bulk_candidates
        
    def _forecast_demand(self, store_status: Dict, context: Dict) -> Dict:
        """Forecast demand based on historical data and context"""
        yesterday_summary = context.get('yesterday_summary', {})
        
        # Simple demand forecast based on yesterday's sales
        demand_forecast = {}
        if yesterday_summary:
            # Try different possible keys for sales data
            sales_data = (
                yesterday_summary.get('units_sold_by_product') or
                yesterday_summary.get('sales_by_product') or
                yesterday_summary.get('daily_sales') or
                {}
            )
            
            if sales_data:
                for product_name, units_sold in sales_data.items():
                    # Ensure units_sold is a number
                    if isinstance(units_sold, (int, float)):
                        # Forecast tomorrow's demand as yesterday's sales + buffer
                        forecasted_demand = max(int(units_sold) + 2, 3)  # Minimum 3 units expected
                        demand_forecast[product_name] = forecasted_demand
        
        # Fill in defaults for any missing products
        for product_name in PRODUCTS.keys():
            if product_name not in demand_forecast:
                demand_forecast[product_name] = 5  # Conservative default
                
        return demand_forecast
        
    def _create_action_plan(self, inventory_analysis: Dict, supplier_intelligence: Dict, demand_forecast: Dict) -> Dict:
        """Create specific inventory action plan"""
        action_plan = {
            'recommended_orders': {},
            'priority_restocks': inventory_analysis['stockouts'],
            'bulk_order_opportunities': supplier_intelligence['bulk_opportunities'],
            'inventory_adjustments': [],
            'spoilage_prevention_actions': []
        }
        
        # Calculate recommended orders for each product
        for product_name in PRODUCTS.keys():
            # Check current stock level properly
            current_stock = 0
            if product_name in inventory_analysis.get('stockouts', []):
                current_stock = 0
            elif product_name in inventory_analysis.get('low_stock', []):
                current_stock = 1  # Assume low stock means 1-2 units
            elif product_name in inventory_analysis.get('optimal', []):
                current_stock = 5  # Assume optimal means around 5 units
            elif product_name in inventory_analysis.get('overstocked', []):
                current_stock = 15  # Assume overstocked means 15+ units
                
            forecasted_demand = demand_forecast.get(product_name, 5)
            
            # Simple reorder logic: order if below forecasted demand + safety buffer
            if product_name in inventory_analysis['stockouts']:
                # Emergency restock
                recommended_order = max(forecasted_demand * 2, 8)
                action_plan['recommended_orders'][product_name] = recommended_order
            elif product_name in inventory_analysis['low_stock']:
                # Regular restock
                recommended_order = max(forecasted_demand + 3, 6)
                action_plan['recommended_orders'][product_name] = recommended_order
                
        return action_plan
        
    def _calculate_confidence(self, store_status: Dict, inventory_analysis: Dict) -> float:
        """Calculate confidence in recommendations"""
        base_confidence = 0.8  # High confidence in inventory management
        
        # Reduce confidence if too many unknowns
        if inventory_analysis['stockout_risk_score'] > 20:
            base_confidence -= 0.2  # Lower confidence in crisis situations
            
        # Increase confidence if situation is stable
        if len(inventory_analysis['optimal']) > len(inventory_analysis['stockouts'] + inventory_analysis['low_stock']):
            base_confidence += 0.1
            
        return min(base_confidence, 1.0)
        
    def _determine_priority(self, inventory_analysis: Dict) -> int:
        """Determine priority level for inventory decisions"""
        stockout_count = len(inventory_analysis['stockouts'])
        low_stock_count = len(inventory_analysis['low_stock'])
        
        if stockout_count > 2:
            return 9  # Critical priority - multiple stockouts
        elif stockout_count > 0:
            return 7  # High priority - some stockouts
        elif low_stock_count > 3:
            return 6  # Medium-high priority - many low stock items
        elif low_stock_count > 0:
            return 4  # Medium priority - some low stock
        else:
            return 2  # Low priority - stable inventory
            
    def _generate_hermione_reasoning(self, inventory_analysis: Dict, supplier_intelligence: Dict, action_plan: Dict) -> str:
        """🏭 Generate Hermione's character-based reasoning for decisions"""
        personality = AgentPrompts.get_agent_personality(AgentRole.INVENTORY_MANAGER)
        
        reasoning_parts = []
        
        # Hermione's systematic analysis approach
        if inventory_analysis['stockouts']:
            stockout_list = ', '.join(inventory_analysis['stockouts'])
            reasoning_parts.append(f"📚 HERMIONE'S ANALYSIS: 'Honestly! We have {len(inventory_analysis['stockouts'])} products completely out of stock ({stockout_list}). This is mathematically unacceptable!'")
            
        if inventory_analysis['low_stock']:
            low_stock_list = ', '.join(inventory_analysis['low_stock'])
            reasoning_parts.append(f"⚠️ HERMIONE'S WARNING: 'I've calculated that {len(inventory_analysis['low_stock'])} products are dangerously low ({low_stock_list}). We must act before they become stockouts!'")
            
        # Hermione's action recommendations
        if action_plan['recommended_orders']:
            order_count = len(action_plan['recommended_orders'])
            reasoning_parts.append(f"📋 HERMIONE'S PLAN: 'I've prepared a systematic restocking strategy for {order_count} products. Every quantity has been calculated with precision!'")
            
        if action_plan['bulk_order_opportunities']:
            bulk_products = ', '.join(action_plan['bulk_order_opportunities'])
            reasoning_parts.append(f"💡 HERMIONE'S OPTIMIZATION: 'Clever! I've identified bulk ordering opportunities for {bulk_products}. We'll save money and ensure adequate stock levels!'")
            
        if not reasoning_parts:
            reasoning_parts.append("✅ HERMIONE'S ASSESSMENT: 'Excellent! Our inventory levels are mathematically optimal. I'll continue monitoring for any inefficiencies.'")
            
        # Add Hermione's characteristic sign-off
        hermione_conclusion = f"\n🎓 HERMIONE'S CONCLUSION: 'Remember, it's our choices that show what we truly are - and I choose perfect inventory management!' (Confidence: {personality['thinking_style']})"
        
        return " | ".join(reasoning_parts) + hermione_conclusion
    
    def _generate_reasoning(self, inventory_analysis: Dict, supplier_intelligence: Dict, action_plan: Dict) -> str:
        """Generate human-readable reasoning for decisions (legacy method)"""
        reasoning_parts = []
        
        # Inventory status reasoning
        if inventory_analysis['stockouts']:
            reasoning_parts.append(f"CRITICAL: {len(inventory_analysis['stockouts'])} products out of stock: {', '.join(inventory_analysis['stockouts'])}")
            
        if inventory_analysis['low_stock']:
            reasoning_parts.append(f"WARNING: {len(inventory_analysis['low_stock'])} products low on stock: {', '.join(inventory_analysis['low_stock'])}")
            
        # Action reasoning
        if action_plan['recommended_orders']:
            order_count = len(action_plan['recommended_orders'])
            reasoning_parts.append(f"Recommending restocking {order_count} products to prevent stockouts")
            
        if action_plan['bulk_order_opportunities']:
            bulk_products = ', '.join(action_plan['bulk_order_opportunities'])
            reasoning_parts.append(f"Bulk order opportunities identified for: {bulk_products}")
            
        if not reasoning_parts:
            reasoning_parts.append("Inventory levels stable - monitoring for optimization opportunities")
            
        return " | ".join(reasoning_parts)
        
    def get_tools(self) -> List[Dict]:
        """Get Hermione's available tools"""
        return [
            {
                'name': 'analyze_situation',
                'description': 'Analyze current inventory situation and provide recommendations',
                'parameters': ['store_status', 'context']
            }
        ]

    # 🔬 PHASE 4B.2: HERMIONE'S SPECIALIZED ANALYTICS TOOLS 🔬
    # Tools separated into src/tools/inventory_tools.py for better organization
    
    def advanced_inventory_optimization(self, store_status: Dict, context: Dict) -> Dict:
        """🧮 TOOL 1: Advanced EOQ and multi-variable inventory optimization"""
        return self.tools.advanced_inventory_optimization(store_status, context)
    
    def predictive_stock_modeling(self, store_status: Dict, context: Dict) -> Dict:
        """📈 TOOL 2: ML-inspired predictive stock level modeling"""
        return self.tools.predictive_stock_modeling(store_status, context)
    
    def supply_chain_efficiency_analyzer(self, store_status: Dict, context: Dict) -> Dict:
        """🚚 TOOL 3: Supply chain efficiency and bottleneck analysis"""
        pending_deliveries = store_status.get('pending_deliveries', [])
        inventory = store_status.get('inventory', {})
        suppliers_status = store_status.get('suppliers_status', {})
        
        efficiency_analysis = {
            'delivery_performance': {},
            'supplier_reliability': {},
            'bottleneck_analysis': [],
            'efficiency_score': 0,
            'optimization_recommendations': []
        }
        
        # Analyze pending deliveries
        delivery_urgency = {}
        for delivery in pending_deliveries:
            product = delivery.get('product', 'Unknown')
            quantity = delivery.get('quantity', 0)
            supplier = delivery.get('supplier', 'Unknown')
            
            current_stock = inventory.get(product, 0)
            urgency_score = 10 - current_stock if current_stock < 10 else 1
            
            delivery_urgency[product] = {
                'urgency_score': urgency_score,
                'supplier': supplier,
                'quantity': quantity
            }
        
        efficiency_analysis['delivery_performance'] = delivery_urgency
        
        # Supplier reliability analysis
        for supplier_name, status in suppliers_status.items():
            reliability_score = 85  # Base score
            if status.get('bankrupt', False):
                reliability_score = 0
            elif status.get('delayed', False):
                reliability_score = 60
            elif status.get('limited_stock', False):
                reliability_score = 75
                
            efficiency_analysis['supplier_reliability'][supplier_name] = reliability_score
        
        # Bottleneck identification
        stockout_products = [p for p, qty in inventory.items() if qty == 0]
        if stockout_products:
            efficiency_analysis['bottleneck_analysis'].append(f"CRITICAL: {len(stockout_products)} stockouts detected")
        
        low_stock_products = [p for p, qty in inventory.items() if 0 < qty <= 2]
        if low_stock_products:
            efficiency_analysis['bottleneck_analysis'].append(f"WARNING: {len(low_stock_products)} low-stock situations")
        
        # Calculate efficiency score
        total_products = len(inventory)
        well_stocked = sum(1 for qty in inventory.values() if qty >= 5)
        efficiency_score = (well_stocked / total_products) * 100 if total_products > 0 else 0
        efficiency_analysis['efficiency_score'] = round(efficiency_score, 1)
        
        # Optimization recommendations
        if efficiency_score < 70:
            efficiency_analysis['optimization_recommendations'].append("Implement emergency restocking protocol")
        if len(stockout_products) > 0:
            efficiency_analysis['optimization_recommendations'].append("Establish alternative supplier relationships")
        if efficiency_score > 90:
            efficiency_analysis['optimization_recommendations'].append("Consider just-in-time inventory to reduce carrying costs")
        
        return efficiency_analysis
    
    def inventory_performance_calculator(self, store_status: Dict, context: Dict) -> Dict:
        """📊 TOOL 4: Comprehensive inventory performance metrics"""
        inventory = store_status.get('inventory', {})
        yesterday_summary = context.get('yesterday_summary', {})
        
        performance_metrics = {
            'turnover_ratios': {},
            'days_of_supply': {},
            'fill_rates': {},
            'inventory_value': {},
            'performance_score': 0
        }
        
        total_inventory_value = 0
        total_performance_score = 0
        
        for product_name, current_stock in inventory.items():
            units_sold = yesterday_summary.get('units_sold_by_product', {}).get(product_name, 0)
            unit_cost = PRODUCTS.get(product_name, {}).get('cost', 1.0)
            
            # Inventory turnover ratio (annualized)
            if current_stock > 0:
                turnover = (units_sold * 365) / current_stock
                days_supply = current_stock / units_sold if units_sold > 0 else 999
            else:
                turnover = 0
                days_supply = 0
            
            performance_metrics['turnover_ratios'][product_name] = round(turnover, 2)
            performance_metrics['days_of_supply'][product_name] = round(days_supply, 1)
            
            # Fill rate (ability to fulfill demand)
            if units_sold == 0:
                fill_rate = 100.0  # No demand = perfect fill
            elif current_stock >= units_sold:
                fill_rate = 100.0
            else:
                fill_rate = (current_stock / units_sold) * 100
                
            performance_metrics['fill_rates'][product_name] = round(fill_rate, 1)
            
            # Inventory value
            inventory_value = current_stock * unit_cost
            performance_metrics['inventory_value'][product_name] = round(inventory_value, 2)
            total_inventory_value += inventory_value
            
            # Individual product performance score
            product_score = (min(turnover, 10) * 2) + (min(fill_rate, 100) * 0.3) + (10 if days_supply <= 7 else 0)
            total_performance_score += product_score
        
        # Overall performance score
        num_products = len(inventory)
        performance_metrics['performance_score'] = round(total_performance_score / num_products, 1) if num_products > 0 else 0
        performance_metrics['total_inventory_value'] = round(total_inventory_value, 2)
        
        return performance_metrics
    
    def inventory_visualization_dashboard(self, store_status: Dict, context: Dict) -> Dict:
        """📈 TOOL 5: Data visualization dashboard for inventory insights"""
        inventory = store_status.get('inventory', {})
        yesterday_summary = context.get('yesterday_summary', {})
        
        dashboard_data = {
            'stock_level_chart': {},
            'turnover_analysis': {},
            'alert_summary': {},
            'trend_indicators': {},
            'visual_recommendations': []
        }
        
        # Stock level visualization data
        total_stock = sum(inventory.values())
        for product_name, quantity in inventory.items():
            percentage = (quantity / total_stock) * 100 if total_stock > 0 else 0
            
            # Visual status
            if quantity == 0:
                status = "🔴 STOCKOUT"
            elif quantity <= 2:
                status = "🟡 LOW"
            elif quantity >= 10:
                status = "🟢 HIGH"
            else:
                status = "🔵 NORMAL"
            
            dashboard_data['stock_level_chart'][product_name] = {
                'quantity': quantity,
                'percentage': round(percentage, 1),
                'status': status
            }
        
        # Turnover analysis for visual representation
        for product_name, quantity in inventory.items():
            units_sold = yesterday_summary.get('units_sold_by_product', {}).get(product_name, 0)
            
            if quantity > 0 and units_sold > 0:
                velocity = "🚀 FAST" if units_sold >= 3 else "🐢 SLOW" if units_sold <= 1 else "⚡ MEDIUM"
            else:
                velocity = "⏸️ STALLED"
                
            dashboard_data['turnover_analysis'][product_name] = {
                'units_sold': units_sold,
                'current_stock': quantity,
                'velocity': velocity
            }
        
        # Alert summary for dashboard
        stockouts = len([q for q in inventory.values() if q == 0])
        low_stock = len([q for q in inventory.values() if 0 < q <= 2])
        
        dashboard_data['alert_summary'] = {
            'stockouts': stockouts,
            'low_stock': low_stock,
            'total_alerts': stockouts + low_stock,
            'alert_level': "🚨 CRITICAL" if stockouts > 0 else "⚠️ WARNING" if low_stock > 0 else "✅ GOOD"
        }
        
        # Trend indicators
        dashboard_data['trend_indicators'] = {
            'inventory_health': "📉 DECLINING" if stockouts + low_stock > 3 else "📈 IMPROVING" if stockouts + low_stock == 0 else "📊 STABLE",
            'action_required': stockouts > 0 or low_stock > 2,
            'priority_focus': "Emergency restocking" if stockouts > 0 else "Preventive ordering" if low_stock > 0 else "Optimization"
        }
        
        # Visual recommendations
        dashboard_data['visual_recommendations'] = [
            f"📊 Display stock levels as bar chart with color coding",
            f"🎯 Highlight {stockouts + low_stock} products needing attention",
            f"📈 Show turnover velocity with animated indicators",
            f"⚡ Create alert dashboard with priority ranking"
        ]
        
        return dashboard_data 