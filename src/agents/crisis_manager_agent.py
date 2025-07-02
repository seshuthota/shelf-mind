"""
🚨 Jack Bauer - Crisis Manager Agent
Phase 4A.2: Character-based crisis response specialist
"""

from typing import Dict, List, Any, Optional
import json
from src.core.multi_agent_engine import BaseSpecialistAgent, AgentRole, AgentDecision
from src.core.agent_prompts import AgentPrompts
from src.core.models import PRODUCTS
from src.tools.crisis_tools import CrisisTools

class CrisisManagerAgent(BaseSpecialistAgent):
    """🚨 Phase 4A.2: Jack Bauer - Crisis Response Specialist
    
    "We have a situation. I need action NOW!"
    
    Responsible for:
    - Emergency response and crisis management
    - Risk assessment and threat detection
    - Business continuity planning
    - Rapid decision-making under pressure
    """
    
    def __init__(self, provider: str = "openai"):
        super().__init__(AgentRole.CRISIS_MANAGER, provider)
        self.tools = CrisisTools()
        
    def _define_specializations(self) -> List[str]:
        """Define Jack's crisis management specializations"""
        return [
            "emergency_response_planning",
            "threat_assessment_analysis",
            "business_continuity_management", 
            "rapid_decision_protocols",
            "crisis_communication_strategy"
        ]
    
    def analyze_situation(self, store_state: Dict, context: Dict) -> AgentDecision:
        """🚨 Jack Bauer analyzes crisis situation with tactical precision"""
        
        # Gather crisis intelligence with Jack's urgent approach
        threat_assessment = self._assess_immediate_threats(store_state, context)
        business_continuity = self._evaluate_business_continuity(store_state, context)
        emergency_protocols = self._identify_emergency_protocols(store_state, context)
        
        # Generate crisis response strategy
        action_plan = self._create_crisis_response(threat_assessment, business_continuity, emergency_protocols)
        
        # Calculate confidence based on crisis severity
        confidence = self._calculate_confidence(store_state, threat_assessment)
        
        # Determine priority (crises are ALWAYS urgent for Jack)
        priority = self._determine_priority(threat_assessment, business_continuity)
        
        # 🎭 Generate Jack's reasoning with character personality
        bauer_reasoning = self._generate_bauer_reasoning(threat_assessment, business_continuity, action_plan)
        
        return AgentDecision(
            agent_role=self.role,
            decision_type="crisis_management",
            parameters=action_plan,
            confidence=confidence,
            reasoning=bauer_reasoning,
            priority=priority
        )
    
    def _assess_immediate_threats(self, store_state: Dict, context: Dict) -> Dict:
        """Assess immediate threats with Jack's tactical precision"""
        cash = store_state.get('cash', 0)
        inventory = store_state.get('inventory', {})
        yesterday_summary = context.get('yesterday_summary', {})
        
        threats = {
            'financial_crisis': 'stable',
            'operational_crisis': 'stable',
            'immediate_threats': [],
            'escalating_risks': [],
            'threat_level': 'GREEN',
            'crisis_probability': 0.1
        }
        
        # Assess financial crisis threats
        if cash <= 50:
            threats['financial_crisis'] = 'CRITICAL'
            threats['immediate_threats'].append("FINANCIAL EMERGENCY: Cash critically low")
            threats['threat_level'] = 'RED'
            threats['crisis_probability'] += 0.6
        elif cash <= 100:
            threats['financial_crisis'] = 'HIGH'
            threats['escalating_risks'].append("Financial pressure increasing")
            threats['threat_level'] = 'ORANGE'
            threats['crisis_probability'] += 0.3
        
        # Assess operational crisis threats - handle both dict and int inventory values
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
        
        if len(stockouts) >= 5:
            threats['operational_crisis'] = 'CRITICAL'
            threats['immediate_threats'].append(f"OPERATIONAL EMERGENCY: {len(stockouts)} products out of stock")
            threats['threat_level'] = 'RED'
            threats['crisis_probability'] += 0.4
        elif len(stockouts) >= 3:
            threats['operational_crisis'] = 'HIGH'
            threats['escalating_risks'].append(f"Multiple stockouts affecting operations")
            if threats['threat_level'] != 'RED':
                threats['threat_level'] = 'ORANGE'
            threats['crisis_probability'] += 0.2
        
        return threats
    
    def _evaluate_business_continuity(self, store_state: Dict, context: Dict) -> Dict:
        """Evaluate business continuity with Jack's emergency preparedness"""
        inventory = store_state.get('inventory', {})
        
        continuity = {
            'operational_capacity': 'FULL',
            'continuity_risks': [],
            'recovery_time': 'IMMEDIATE'
        }
        
        # Assess operational capacity - handle both dict and int inventory values
        total_products = len(inventory)
        stocked_products = 0
        
        for product, qty in inventory.items():
            if isinstance(qty, dict):
                actual_qty = qty.get('total_quantity', 0)
            elif hasattr(qty, 'total_quantity'):
                actual_qty = qty.total_quantity
            else:
                actual_qty = qty
                
            if actual_qty > 0:
                stocked_products += 1
        
        operational_rate = stocked_products / total_products if total_products > 0 else 1.0
        
        if operational_rate < 0.3:
            continuity['operational_capacity'] = 'CRITICAL'
            continuity['continuity_risks'].append("Insufficient inventory for operations")
            continuity['recovery_time'] = '24-48 HOURS'
        elif operational_rate < 0.6:
            continuity['operational_capacity'] = 'LIMITED'
            continuity['recovery_time'] = '12-24 HOURS'
        
        return continuity
    
    def _identify_emergency_protocols(self, store_state: Dict, context: Dict) -> Dict:
        """Identify emergency protocols with Jack's rapid response training"""
        protocols = {
            'immediate_actions': [],
            'short_term_actions': [],
            'contingency_plans': []
        }
        
        cash = store_state.get('cash', 0)
        inventory = store_state.get('inventory', {})
        
        # Financial emergency protocols
        if cash <= 100:
            protocols['immediate_actions'].append("Activate cash conservation")
            protocols['short_term_actions'].append("Prioritize high-margin sales")
        
        # Operational emergency protocols - handle both dict and int inventory values
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
        
        if stockouts:
            protocols['immediate_actions'].append("Emergency restock critical products")
            protocols['contingency_plans'].append("Alternative product recommendations")
        
        return protocols
    
    def _create_crisis_response(self, threats: Dict, continuity: Dict, protocols: Dict) -> Dict:
        """Create Jack's crisis response strategy"""
        response = {
            'threat_mitigation': [],
            'emergency_actions': [],
            'recovery_procedures': []
        }
        
        # Address immediate threats
        for threat in threats['immediate_threats']:
            if "FINANCIAL" in threat:
                response['emergency_actions'].append("Emergency cash conservation")
            elif "OPERATIONAL" in threat:
                response['emergency_actions'].append("Emergency restocking protocol")
        
        # Execute protocols
        response['emergency_actions'].extend(protocols['immediate_actions'])
        response['recovery_procedures'].extend(protocols['short_term_actions'])
        
        return response
    
    def _calculate_confidence(self, store_state: Dict, threats: Dict) -> float:
        """Calculate Jack's confidence in crisis assessment"""
        base_confidence = 0.90
        
        if threats['threat_level'] == 'RED':
            return min(0.95, base_confidence + 0.05)
        elif threats['threat_level'] == 'GREEN':
            return max(0.85, base_confidence - 0.05)
            
        return base_confidence
    
    def _determine_priority(self, threats: Dict, continuity: Dict) -> int:
        """Determine priority - crises are ALWAYS urgent for Jack"""
        if threats['threat_level'] == 'RED':
            return 5  # Maximum priority - active crisis
        elif threats['threat_level'] == 'ORANGE':
            return 4  # High priority - crisis developing
        else:
            return 2  # Low priority - monitoring mode
    
    def _generate_bauer_reasoning(self, threats: Dict, continuity: Dict, action_plan: Dict) -> str:
        """🚨 Generate Jack Bauer's character-based reasoning"""
        reasoning_parts = []
        
        threat_level = threats['threat_level']
        crisis_probability = threats['crisis_probability']
        reasoning_parts.append(f"🚨 BAUER'S THREAT ASSESSMENT: 'Threat level {threat_level}. Crisis probability {crisis_probability:.0%}. We need to act fast!'")
        
        if threats['immediate_threats']:
            threat_count = len(threats['immediate_threats'])
            reasoning_parts.append(f"⚡ BAUER'S CRISIS ALERT: '{threat_count} immediate threats detected. This is not a drill!'")
        
        if action_plan['emergency_actions']:
            action_count = len(action_plan['emergency_actions'])
            reasoning_parts.append(f"🎯 BAUER'S RESPONSE: '{action_count} emergency protocols activated. Every second counts!'")
        
        if not reasoning_parts:
            reasoning_parts.append("✅ BAUER'S STATUS: 'Situation stable. Maintaining vigilant monitoring.'")
        
        # Add Jack's characteristic sign-off
        bauer_conclusion = f"\n🚨 BAUER'S CONCLUSION: 'We WILL protect this business - whatever it takes!' (Threat Level: {threat_level})"
        
        return " | ".join(reasoning_parts) + bauer_conclusion 

    # 🚨 PHASE 4B.2: JACK'S SPECIALIZED CRISIS MANAGEMENT TOOLS 🚨
    
    def emergency_response_protocols(self, store_status: Dict, context: Dict) -> Dict:
        """⚡ TOOL 1: Advanced emergency response protocols and rapid deployment systems"""
        return self.tools.emergency_response_protocols(store_status, context)
    
    def rapid_decision_frameworks(self, store_status: Dict, context: Dict) -> Dict:
        """⚡ TOOL 2: High-speed decision-making frameworks for time-critical situations"""
        return self.tools.rapid_decision_frameworks(store_status, context)
    
    def crisis_severity_assessments(self, store_status: Dict, context: Dict) -> Dict:
        """🎯 TOOL 3: Advanced crisis severity assessment and impact analysis"""
        return self.tools.crisis_severity_assessments(store_status, context)
    
    def action_priority_matrices(self, store_status: Dict, context: Dict) -> Dict:
        """🎯 TOOL 4: Dynamic action prioritization and resource allocation matrices"""
        return self.tools.action_priority_matrices(store_status, context)
    
    def time_critical_optimizers(self, store_status: Dict, context: Dict) -> Dict:
        """⏰ TOOL 5: Time-critical optimization and rapid execution systems"""
        return self.tools.time_critical_optimizers(store_status, context) 