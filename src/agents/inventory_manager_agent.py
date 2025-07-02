from typing import Dict, List, Any, Optional
import json
from src.core.multi_agent_engine import BaseSpecialistAgent, AgentRole, AgentDecision
from src.core.agent_prompts import AgentPrompts
from src.core.models import PRODUCTS

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
            # If we're low on high-volume products, consider bulk ordering
            if quantity <= 5 and product_name in ['Coke', 'Chips', 'Candy']:
                bulk_candidates.append(product_name)
                
        return bulk_candidates
        
    def _forecast_demand(self, store_status: Dict, context: Dict) -> Dict:
        """Forecast demand based on historical data and context"""
        yesterday_summary = context.get('yesterday_summary', {})
        
        # Simple demand forecast based on yesterday's sales
        demand_forecast = {}
        if yesterday_summary and 'units_sold_by_product' in yesterday_summary:
            for product_name, units_sold in yesterday_summary['units_sold_by_product'].items():
                # Forecast tomorrow's demand as yesterday's sales + buffer
                forecasted_demand = max(units_sold + 2, 3)  # Minimum 3 units expected
                demand_forecast[product_name] = forecasted_demand
        else:
            # Default forecast if no historical data
            for product_name in PRODUCTS.keys():
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
            current_stock = 0  # Will be filled from store_status in real implementation
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
        """Get inventory management tools"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "optimize_inventory_specialist",
                    "description": "Inventory Manager: Get detailed inventory optimization recommendations with reorder calculations",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "analyze_supplier_options",
                    "description": "Inventory Manager: Analyze supplier options for optimal ordering strategy",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "forecast_demand_specialist",
                    "description": "Inventory Manager: Generate demand forecasts for inventory planning",
                    "parameters": {"type": "object", "properties": {}}
                }
            }
        ] 