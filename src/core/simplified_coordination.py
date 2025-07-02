#!/usr/bin/env python3
"""
🎯 Simplified Business Coordination System

REALISTIC DAILY WORKFLOW:
- Daily: Hermione (Inventory) + Gekko (Pricing) only
- Every 3 Days: Tyrion provides strategic guidance to others
- Crisis Triggered: Jack advises when performance declines
- Elle: Removed for now (no direct customer interaction yet)

This matches how real small businesses operate day-to-day.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from src.core.models import AgentRole, AgentDecision, StoreState

class OperationMode(Enum):
    """Different operational modes based on situation"""
    DAILY_OPERATIONS = "daily_operations"     # Hermione + Gekko only
    STRATEGIC_REVIEW = "strategic_review"     # + Tyrion guidance  
    CRISIS_MANAGEMENT = "crisis_management"   # + Jack crisis response

@dataclass
class BusinessMetrics:
    """Key metrics that determine operation mode"""
    current_day: int
    daily_profit: float
    daily_revenue: float
    inventory_stockouts: int
    cash_available: float
    
    # Performance trends (last 3 days)
    profit_trend: float  # % change
    revenue_trend: float  # % change
    stockout_trend: int  # count change
    
    def is_crisis_triggered(self) -> bool:
        """Determine if Jack should be activated for crisis management"""
        crisis_conditions = [
            self.daily_profit < 5.0,              # Very low profit
            self.profit_trend < -20.0,             # 20%+ profit decline
            self.revenue_trend < -15.0,            # 15%+ revenue decline  
            self.inventory_stockouts >= 3,         # Multiple stockouts
            self.cash_available < 50.0,            # Cash crisis
            self.stockout_trend >= 2               # Increasing stockouts
        ]
        
        return any(crisis_conditions)
    
    def needs_strategic_review(self) -> bool:
        """Determine if Tyrion should provide strategic guidance"""
        return self.current_day % 3 == 0  # Every 3 days

@dataclass
class OperationalDecision:
    """Decision with operational context"""
    agent_role: AgentRole
    decision: AgentDecision
    operation_mode: OperationMode
    strategic_guidance: Optional[str] = None
    crisis_context: Optional[str] = None

class SimplifiedCoordinator:
    """🎯 Simplified coordination matching real business operations"""
    
    def __init__(self):
        self.operation_history: List[Dict] = []
        self.strategic_guidance_history: List[Dict] = []
        self.crisis_interventions: List[Dict] = []
        
        # Core daily agents
        self.daily_agents = [AgentRole.INVENTORY_MANAGER, AgentRole.PRICING_ANALYST]
        
        # Periodic agents
        self.strategic_agent = AgentRole.STRATEGIC_PLANNER
        self.crisis_agent = AgentRole.CRISIS_MANAGER
        
        # Removed agent (for future)
        self.future_agents = [AgentRole.CUSTOMER_SERVICE]  # Add back when needed
    
    def coordinate_daily_business(self, store_state: StoreState, context: Dict,
                                recent_performance: List[Dict]) -> Dict:
        """Main coordination method - determines mode and coordinates accordingly"""
        
        mode, metrics = self.determine_operation_mode(store_state, recent_performance)
        
        if mode == OperationMode.CRISIS_MANAGEMENT:
            result = self.coordinate_crisis_management(store_state, context, metrics)
        elif mode == OperationMode.STRATEGIC_REVIEW:
            result = self.coordinate_strategic_review(store_state, context, recent_performance)
        else:
            result = self.coordinate_daily_operations(store_state, context)
        
        # Record operation
        self.operation_history.append({
            'day': store_state.day,
            'mode': mode,
            'metrics': metrics,
            'result': result
        })
        
        return result
    
    def determine_operation_mode(self, store_state: StoreState, 
                                recent_performance: List[Dict]) -> Tuple[OperationMode, BusinessMetrics]:
        """Determine what type of coordination is needed today"""
        
        # Calculate business metrics
        metrics = self._calculate_business_metrics(store_state, recent_performance)
        
        # Determine operation mode
        if metrics.is_crisis_triggered():
            mode = OperationMode.CRISIS_MANAGEMENT
            print(f"🚨 CRISIS MODE ACTIVATED: Performance declining")
        elif metrics.needs_strategic_review():
            mode = OperationMode.STRATEGIC_REVIEW  
            print(f"📊 STRATEGIC REVIEW: Day {metrics.current_day} (every 3 days)")
        else:
            mode = OperationMode.DAILY_OPERATIONS
            print(f"🏪 DAILY OPERATIONS: Standard business day")
        
        return mode, metrics
    
    def coordinate_daily_operations(self, store_state: StoreState, context: Dict) -> Dict:
        """Core daily coordination: Hermione + Gekko only"""
        
        print(f"\n🎯 DAILY OPERATIONS COORDINATION:")
        print(f"   📦 Hermione: Inventory management (80% budget)")
        print(f"   💰 Gekko: Pricing optimization (no budget needed)")
        
        decisions = []
        
        # Hermione handles all inventory decisions with 80% budget
        inventory_budget = store_state.cash * 0.8  # 80% for inventory
        context['inventory_budget'] = inventory_budget
        context['focus'] = 'inventory_optimization'
        
        hermione_decision = self._get_agent_decision(
            AgentRole.INVENTORY_MANAGER, store_state, context
        )
        if hermione_decision:
            decisions.append(hermione_decision)
        
        # Gekko handles all pricing decisions (no budget needed)
        context['focus'] = 'pricing_optimization'
        context['competitive_analysis'] = True
        
        gekko_decision = self._get_agent_decision(
            AgentRole.PRICING_ANALYST, store_state, context
        )
        if gekko_decision:
            decisions.append(gekko_decision)
        
        return {
            'mode': OperationMode.DAILY_OPERATIONS,
            'decisions': decisions,
            'active_agents': ['hermione', 'gekko'],
            'budget_allocation': {'hermione': inventory_budget, 'gekko': 0},
            'guidance_provided': None,
            'crisis_response': None
        }
    
    def coordinate_strategic_review(self, store_state: StoreState, context: Dict,
                                   recent_performance: List[Dict]) -> Dict:
        """Every 3 days: Tyrion provides strategic guidance"""
        
        print(f"\n📊 STRATEGIC REVIEW COORDINATION:")
        print(f"   🏰 Tyrion: Analyzing performance and providing guidance")
        print(f"   📦 Hermione: Inventory with strategic input")  
        print(f"   💰 Gekko: Pricing with strategic input")
        
        # First, get Tyrion's strategic analysis
        context['operation_mode'] = 'strategic_review'
        context['recent_performance'] = recent_performance
        context['guidance_target'] = ['inventory_manager', 'pricing_analyst']
        
        tyrion_guidance = self._get_strategic_guidance(store_state, context)
        
        # Then get daily decisions with strategic context
        decisions = []
        inventory_budget = store_state.cash * 0.8
        
        # Hermione with strategic guidance
        context['strategic_guidance'] = tyrion_guidance.get('inventory_guidance', '')
        context['inventory_budget'] = inventory_budget
        context['focus'] = 'strategic_inventory'
        
        hermione_decision = self._get_agent_decision(
            AgentRole.INVENTORY_MANAGER, store_state, context
        )
        if hermione_decision:
            hermione_decision.reasoning += f" [STRATEGIC: {context['strategic_guidance'][:40]}...]"
            decisions.append(hermione_decision)
        
        # Gekko with strategic guidance
        context['strategic_guidance'] = tyrion_guidance.get('pricing_guidance', '')
        context['focus'] = 'strategic_pricing'
        
        gekko_decision = self._get_agent_decision(
            AgentRole.PRICING_ANALYST, store_state, context
        )
        if gekko_decision:
            gekko_decision.reasoning += f" [STRATEGIC: {context['strategic_guidance'][:40]}...]"
            decisions.append(gekko_decision)
        
        # Store strategic guidance
        self.strategic_guidance_history.append({
            'day': store_state.day,
            'guidance': tyrion_guidance,
            'performance_analysis': recent_performance[-3:] if len(recent_performance) >= 3 else recent_performance
        })
        
        return {
            'mode': OperationMode.STRATEGIC_REVIEW,
            'decisions': decisions,
            'active_agents': ['tyrion', 'hermione', 'gekko'],
            'budget_allocation': {'hermione': inventory_budget, 'gekko': 0, 'tyrion': 0},
            'guidance_provided': tyrion_guidance,
            'crisis_response': None
        }
    
    def coordinate_crisis_management(self, store_state: StoreState, context: Dict,
                                   metrics: BusinessMetrics) -> Dict:
        """Crisis mode: Jack provides emergency guidance to core team"""
        
        print(f"\n🚨 CRISIS MANAGEMENT COORDINATION:")
        print(f"   ⚡ Jack: Crisis analysis and emergency guidance")
        print(f"   📦 Hermione: Emergency inventory response") 
        print(f"   💰 Gekko: Crisis pricing strategy")
        
        # Calculate emergency budget allocation
        emergency_inventory_budget = store_state.cash * 0.6  # 60% for emergency inventory
        emergency_reserve = store_state.cash * 0.2           # 20% kept as reserve
        
        # First, get Jack's crisis analysis
        context['operation_mode'] = 'crisis_management'
        context['crisis_metrics'] = {
            'profit_decline': metrics.profit_trend,
            'revenue_decline': metrics.revenue_trend,
            'stockouts': metrics.inventory_stockouts,
            'cash_crisis': metrics.cash_available < 50.0
        }
        
        jack_crisis_response = self._get_crisis_response(store_state, context, metrics)
        
        # Emergency decisions with crisis guidance
        decisions = []
        
        # Hermione with crisis guidance and emergency budget
        context['crisis_guidance'] = jack_crisis_response.get('inventory_response', '')
        context['inventory_budget'] = emergency_inventory_budget
        context['emergency_reserve'] = emergency_reserve
        context['focus'] = 'crisis_inventory'
        
        hermione_decision = self._get_agent_decision(
            AgentRole.INVENTORY_MANAGER, store_state, context
        )
        if hermione_decision:
            hermione_decision.reasoning += f" [CRISIS: {context['crisis_guidance'][:40]}...]"
            hermione_decision.priority = min(hermione_decision.priority + 2, 10)  # Boost priority
            decisions.append(hermione_decision)
        
        # Gekko with crisis guidance
        context['crisis_guidance'] = jack_crisis_response.get('pricing_response', '')
        context['focus'] = 'crisis_pricing'
        
        gekko_decision = self._get_agent_decision(
            AgentRole.PRICING_ANALYST, store_state, context
        )
        if gekko_decision:
            gekko_decision.reasoning += f" [CRISIS: {context['crisis_guidance'][:40]}...]"
            gekko_decision.priority = min(gekko_decision.priority + 2, 10)  # Boost priority
            decisions.append(gekko_decision)
        
        # Store crisis intervention
        self.crisis_interventions.append({
            'day': store_state.day,
            'crisis_type': self._identify_crisis_type(metrics),
            'response': jack_crisis_response,
            'metrics': metrics
        })
        
        return {
            'mode': OperationMode.CRISIS_MANAGEMENT,
            'decisions': decisions,
            'active_agents': ['jack', 'hermione', 'gekko'],
            'budget_allocation': {
                'hermione': emergency_inventory_budget,
                'gekko': 0,
                'jack': 0,
                'emergency_reserve': emergency_reserve
            },
            'guidance_provided': None,
            'crisis_response': jack_crisis_response
        }
    
    def _calculate_business_metrics(self, store_state: StoreState, 
                                  recent_performance: List[Dict]) -> BusinessMetrics:
        """Calculate key business metrics to determine operation mode"""
        
        current_profit = recent_performance[-1].get('profit', 0) if recent_performance else store_state.total_profit
        current_revenue = recent_performance[-1].get('revenue', 0) if recent_performance else store_state.total_revenue
        stockouts = len([name for name, item in store_state.inventory.items() if item.total_quantity == 0])
        
        # Calculate trends
        profit_trend = 0.0
        revenue_trend = 0.0
        stockout_trend = 0
        
        if len(recent_performance) >= 2:
            old_profit = recent_performance[-2].get('profit', 0)
            old_revenue = recent_performance[-2].get('revenue', 0)
            
            if old_profit > 0:
                profit_trend = ((current_profit - old_profit) / old_profit) * 100
            if old_revenue > 0:
                revenue_trend = ((current_revenue - old_revenue) / old_revenue) * 100
        
        if len(recent_performance) >= 3:
            # Compare stockouts over last 3 days
            recent_stockouts = []
            for day_data in recent_performance[-3:]:
                day_stockouts = day_data.get('stockouts', 0)
                if isinstance(day_stockouts, int):
                    recent_stockouts.append(day_stockouts)
                else:
                    recent_stockouts.append(0)
            
            if len(recent_stockouts) >= 2:
                stockout_trend = recent_stockouts[-1] - recent_stockouts[0]
        
        return BusinessMetrics(
            current_day=store_state.day,
            daily_profit=current_profit,
            daily_revenue=current_revenue,
            inventory_stockouts=stockouts,
            cash_available=store_state.cash,
            profit_trend=profit_trend,
            revenue_trend=revenue_trend,
            stockout_trend=stockout_trend
        )
    
    def _get_agent_decision(self, agent_role: AgentRole, store_state: StoreState, 
                          context: Dict) -> Optional[AgentDecision]:
        """Get a decision from an agent (placeholder for actual agent calls)"""
        
        # This would call the actual agent in implementation
        # For now, return a mock decision based on role and context
        
        if agent_role == AgentRole.INVENTORY_MANAGER:
            # Hermione's inventory decision
            low_stock_items = [name for name, item in store_state.inventory.items() if item.total_quantity <= 2]
            if low_stock_items:
                budget = context.get('inventory_budget', 100)
                return AgentDecision(
                    agent_role=agent_role,
                    decision_type="inventory_reorder",
                    parameters={
                        "products": low_stock_items,
                        "quantities": {item: min(10, int(budget / (len(low_stock_items) * 2))) for item in low_stock_items},
                        "budget_used": min(budget * 0.8, len(low_stock_items) * 20)
                    },
                    confidence=0.8,
                    priority=7,
                    reasoning=f"Hermione: Restocking {len(low_stock_items)} low inventory items"
                )
                
        elif agent_role == AgentRole.PRICING_ANALYST:
            # Gekko's pricing decision
            return AgentDecision(
                agent_role=agent_role,
                decision_type="pricing_optimization",
                parameters={
                    "price_changes": {"chips": 2.25, "soda": 2.10},
                    "strategy": context.get('focus', 'margin_optimization')
                },
                confidence=0.9,
                priority=6,
                reasoning=f"Gekko: {context.get('focus', 'Standard')} pricing optimization"
            )
        
        return None
    
    def _get_strategic_guidance(self, store_state: StoreState, context: Dict) -> Dict:
        """Get strategic guidance from Tyrion (placeholder)"""
        
        performance = context.get('recent_performance', [])
        
        # Analyze performance trends
        if len(performance) >= 3:
            recent_profits = [day.get('profit', 0) for day in performance[-3:]]
            trend = "improving" if recent_profits[-1] > recent_profits[0] else "declining"
        else:
            trend = "insufficient_data"
        
        guidance = {
            'inventory_guidance': f"Based on {trend} trend: Focus on high-margin items, reduce spoilage risk",
            'pricing_guidance': f"Market analysis suggests: Test 5% price increases on top performers",
            'overall_strategy': "Consolidate around profitable core products",
            'performance_analysis': f"Analyzed {len(performance)} days of performance data",
            'trend_assessment': trend
        }
        
        return guidance
    
    def _get_crisis_response(self, store_state: StoreState, context: Dict, 
                           metrics: BusinessMetrics) -> Dict:
        """Get crisis response from Jack (placeholder)"""
        
        crisis_type = self._identify_crisis_type(metrics)
        
        response = {
            'crisis_type': crisis_type,
            'inventory_response': "Emergency restock of critical items, minimize risk",
            'pricing_response': "Implement competitive pricing to boost sales volume",
            'emergency_actions': ["increase_inventory_budget", "aggressive_pricing"],
            'timeline': "Immediate action required",
            'severity': "high" if metrics.cash_available < 30.0 else "medium"
        }
        
        return response
    
    def _identify_crisis_type(self, metrics: BusinessMetrics) -> str:
        """Identify the type of crisis occurring"""
        
        if metrics.cash_available < 50.0:
            return "cash_crisis"
        elif metrics.inventory_stockouts >= 3:
            return "inventory_crisis"
        elif metrics.profit_trend < -20.0:
            return "profit_decline"
        elif metrics.revenue_trend < -15.0:
            return "revenue_decline"
        else:
            return "performance_decline"
    
    def get_coordination_summary(self) -> Dict:
        """Get summary of coordination activities"""
        
        total_operations = len(self.operation_history)
        strategic_reviews = len(self.strategic_guidance_history)
        crisis_interventions = len(self.crisis_interventions)
        
        return {
            'total_days': total_operations,
            'daily_operations': total_operations - strategic_reviews - crisis_interventions,
            'strategic_reviews': strategic_reviews,
            'crisis_interventions': crisis_interventions,
            'active_agents': ['hermione_inventory', 'gekko_pricing'],
            'periodic_agents': ['tyrion_strategy'],
            'crisis_agents': ['jack_crisis'],
            'removed_agents': ['elle_customer_service'],
            'coordination_efficiency': f"{((total_operations - crisis_interventions) / max(total_operations, 1)) * 100:.1f}%",
            'average_agents_per_day': round((total_operations * 2 + strategic_reviews + crisis_interventions) / max(total_operations, 1), 1)
        } 