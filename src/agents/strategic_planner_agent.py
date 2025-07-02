"""
🎯 Tyrion Lannister - Strategic Planner Agent
Phase 4A.2: Character-based strategic planning specialist
"""

from typing import Dict, List, Any, Optional
import json
from src.core.multi_agent_engine import BaseSpecialistAgent, AgentRole, AgentDecision
from src.core.agent_prompts import AgentPrompts
from src.core.models import PRODUCTS
from src.tools.strategic_tools import StrategicTools

class StrategicPlannerAgent(BaseSpecialistAgent):
    """🎯 Phase 4A.2: Tyrion Lannister - Master Strategic Planner
    
    "A business needs strategy like a kingdom needs allies!"
    
    Responsible for:
    - Long-term strategic planning and resource allocation
    - Multi-dimensional business optimization
    - Risk assessment and contingency planning
    - Growth opportunities and expansion strategies
    """
    
    def __init__(self, provider: str = "openai"):
        super().__init__(AgentRole.STRATEGIC_PLANNER, provider)
        self.tools = StrategicTools()
        
    def _define_specializations(self) -> List[str]:
        """Define Tyrion's strategic planning specializations"""
        return [
            "long_term_strategic_planning",
            "resource_allocation_optimization",
            "risk_assessment_analysis", 
            "growth_opportunity_identification",
            "multi_dimensional_coordination"
        ]
    
    def analyze_situation(self, store_status: Dict, context: Dict) -> AgentDecision:
        """🎯 Tyrion Lannister analyzes strategic situation with masterful wisdom"""
        
        # Gather strategic intelligence with Tyrion's comprehensive approach
        strategic_position = self._assess_strategic_position(store_status, context)
        resource_analysis = self._analyze_resource_allocation(store_status, context)
        growth_opportunities = self._identify_growth_opportunities(store_status, context)
        
        # Generate comprehensive strategic plan
        action_plan = self._create_strategic_plan(strategic_position, resource_analysis, growth_opportunities)
        
        # Calculate confidence based on strategic clarity
        confidence = self._calculate_confidence(store_status, strategic_position)
        
        # Determine priority (strategic thinking is always important to Tyrion)
        priority = self._determine_priority(strategic_position, resource_analysis)
        
        # 🎭 Generate Tyrion's reasoning with character personality
        tyrion_reasoning = self._generate_tyrion_reasoning(strategic_position, resource_analysis, action_plan)
        
        return AgentDecision(
            agent_role=self.role,
            decision_type="strategic_planning",
            parameters=action_plan,
            confidence=confidence,
            reasoning=tyrion_reasoning,
            priority=priority
        )
    
    def _assess_strategic_position(self, store_status: Dict, context: Dict) -> Dict:
        """Assess overall strategic position with Tyrion's analytical mind"""
        cash = store_status.get('cash', 0)
        inventory = store_status.get('inventory', {})
        yesterday_summary = context.get('yesterday_summary', {})
        
        position = {
            'financial_strength': 'moderate',    # Cash position assessment
            'market_position': 'competitive',    # Competitive standing
            'operational_efficiency': 'good',    # How well we're operating
            'strategic_risks': [],               # Major risks to address
            'competitive_advantages': [],        # Our strengths
        }
        
        # Assess financial strength
        if cash >= 300:
            position['financial_strength'] = 'strong'
            position['competitive_advantages'].append("Strong cash position")
        elif cash >= 200:
            position['financial_strength'] = 'moderate'
        else:
            position['financial_strength'] = 'weak'
            position['strategic_risks'].append("Low cash limits options")
        
        # Assess operational efficiency - handle both dict and int inventory values
        stockouts = []
        for product, qty in inventory.items():
            if isinstance(qty, dict):
                actual_qty = qty.get('total_quantity', 0)
            elif hasattr(qty, 'total_quantity'):
                actual_qty = qty.total_quantity
            else:
                actual_qty = qty
                
            if actual_qty == 0:
                stockouts.append(product)
        
        if len(stockouts) == 0:
            position['operational_efficiency'] = 'excellent'
        elif len(stockouts) <= 2:
            position['operational_efficiency'] = 'good'
        else:
            position['operational_efficiency'] = 'poor'
            position['strategic_risks'].append("Multiple stockouts")
        
        return position
    
    def _analyze_resource_allocation(self, store_status: Dict, context: Dict) -> Dict:
        """Analyze resource allocation with Tyrion's efficiency focus"""
        cash = store_status.get('cash', 0)
        inventory = store_status.get('inventory', {})
        
        allocation = {
            'cash_utilization': 'moderate',
            'inventory_efficiency': 'good',
            'optimization_opportunities': []
        }
        
        # Analyze inventory balance - handle both dict and int inventory values
        high_stock = []
        low_stock = []
        
        for product, qty in inventory.items():
            if isinstance(qty, dict):
                actual_qty = qty.get('total_quantity', 0)
            elif hasattr(qty, 'total_quantity'):
                actual_qty = qty.total_quantity
            else:
                actual_qty = qty
                
            if actual_qty >= 7:
                high_stock.append(product)
            elif actual_qty <= 2:
                low_stock.append(product)
        
        if len(high_stock) > len(low_stock):
            allocation['optimization_opportunities'].append("Rebalance inventory")
        
        return allocation
    
    def _identify_growth_opportunities(self, store_status: Dict, context: Dict) -> Dict:
        """Identify growth opportunities with Tyrion's strategic vision"""
        cash = store_status.get('cash', 0)
        yesterday_summary = context.get('yesterday_summary', {})
        
        opportunities = {
            'expansion_readiness': 'evaluating',
            'growth_initiatives': []
        }
        
        if cash >= 300:
            opportunities['expansion_readiness'] = 'ready'
            opportunities['growth_initiatives'] = ["Product expansion", "Service diversification"]
        
        return opportunities
    
    def _create_strategic_plan(self, position: Dict, allocation: Dict, opportunities: Dict) -> Dict:
        """Create Tyrion's comprehensive strategic plan"""
        plan = {
            'strategic_objectives': [],
            'risk_mitigation': [],
            'growth_initiatives': [],
            'tactical_recommendations': []
        }
        
        # Set objectives based on position
        if position['financial_strength'] == 'strong':
            plan['strategic_objectives'].append("Capitalize on strong position")
        else:
            plan['strategic_objectives'].append("Strengthen foundation")
        
        # Address risks
        for risk in position['strategic_risks']:
            plan['risk_mitigation'].append(f"Address: {risk}")
        
        return plan
    
    def _calculate_confidence(self, store_status: Dict, position: Dict) -> float:
        """Calculate Tyrion's confidence in strategic analysis"""
        base_confidence = 0.85
        
        if position['financial_strength'] == 'strong':
            return min(0.95, base_confidence + 0.10)
        elif position['financial_strength'] == 'weak':
            return max(0.70, base_confidence - 0.15)
            
        return base_confidence
    
    def _determine_priority(self, position: Dict, allocation: Dict) -> int:
        """Determine priority - strategic planning is always important to Tyrion"""
        if position['financial_strength'] == 'weak':
            return 5  # High priority - financial crisis
        elif len(position['strategic_risks']) > 2:
            return 4  # Medium-high priority - multiple risks
        else:
            return 3  # Medium priority - strategic optimization
    
    def _generate_tyrion_reasoning(self, position: Dict, allocation: Dict, action_plan: Dict) -> str:
        """🎯 Generate Tyrion Lannister's character-based reasoning"""
        reasoning_parts = []
        
        financial_strength = position['financial_strength']
        reasoning_parts.append(f"🏰 TYRION'S ASSESSMENT: 'Our strategic position shows {financial_strength} finances. A wise ruler knows his true position!'")
        
        if position['strategic_risks']:
            risks_count = len(position['strategic_risks'])
            reasoning_parts.append(f"⚔️ TYRION'S WARNINGS: '{risks_count} strategic risks identified. We must prepare for these challenges!'")
        
        if action_plan['strategic_objectives']:
            objectives_count = len(action_plan['strategic_objectives'])
            reasoning_parts.append(f"🎯 TYRION'S STRATEGY: '{objectives_count} strategic objectives defined. A mind needs books like a sword needs a whetstone!'")
        
        # Add Tyrion's characteristic sign-off
        tyrion_conclusion = f"\n🎯 TYRION'S CONCLUSION: 'A business needs strategy like a kingdom needs allies! Every decision shapes our position tomorrow!'"
        
        return " | ".join(reasoning_parts) + tyrion_conclusion 

    # 🏰 PHASE 4B.2: TYRION'S SPECIALIZED STRATEGIC PLANNING TOOLS 🏰
    # Tools extracted to src/tools/strategic_tools.py
    
    def long_term_planning_framework(self, store_status: Dict, context: Dict) -> Dict:
        """📜 TOOL 1: Advanced long-term strategic planning and scenario modeling"""
        return self.tools.long_term_planning_framework(store_status, context)
    
    def risk_assessment_matrix(self, store_status: Dict, context: Dict) -> Dict:
        """⚖️ TOOL 2: Comprehensive risk assessment and mitigation planning"""
        return self.tools.risk_assessment_matrix(store_status, context)
    
    def resource_allocation_optimizer(self, store_status: Dict, context: Dict) -> Dict:
        """💰 TOOL 3: Strategic resource allocation and investment optimization"""
        return self.tools.resource_allocation_optimizer(store_status, context)
    
    def strategic_scenario_planner(self, store_status: Dict, context: Dict) -> Dict:
        """🎲 TOOL 4: Advanced scenario planning and strategic contingency modeling"""
        return self.tools.strategic_scenario_planner(store_status, context)
    
    def diplomatic_negotiation_tools(self, store_status: Dict, context: Dict) -> Dict:
        """🤝 TOOL 5: Strategic negotiation and relationship optimization frameworks"""
        return self.tools.diplomatic_negotiation_tools(store_status, context) 