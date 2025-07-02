"""
🚨 Jack Bauer - Crisis Manager Agent
Phase 4A.2: Character-based crisis response specialist
"""

from typing import Dict, List, Any, Optional
import json
from src.core.multi_agent_engine import BaseSpecialistAgent, AgentRole, AgentDecision
from src.core.agent_prompts import AgentPrompts
from src.core.models import PRODUCTS

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
        
    def _define_specializations(self) -> List[str]:
        """Define Jack's crisis management specializations"""
        return [
            "emergency_response_planning",
            "threat_assessment_analysis",
            "business_continuity_management", 
            "rapid_decision_protocols",
            "crisis_communication_strategy"
        ]
    
    def analyze_situation(self, store_status: Dict, context: Dict) -> AgentDecision:
        """🚨 Jack Bauer analyzes crisis situation with tactical precision"""
        
        # Gather crisis intelligence with Jack's urgent approach
        threat_assessment = self._assess_immediate_threats(store_status, context)
        business_continuity = self._evaluate_business_continuity(store_status, context)
        emergency_protocols = self._identify_emergency_protocols(store_status, context)
        
        # Generate crisis response strategy
        action_plan = self._create_crisis_response(threat_assessment, business_continuity, emergency_protocols)
        
        # Calculate confidence based on crisis severity
        confidence = self._calculate_confidence(store_status, threat_assessment)
        
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
    
    def _assess_immediate_threats(self, store_status: Dict, context: Dict) -> Dict:
        """Assess immediate threats with Jack's tactical precision"""
        cash = store_status.get('cash', 0)
        inventory = store_status.get('inventory', {})
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
        
        # Assess operational crisis threats
        stockouts = [product for product, qty in inventory.items() if qty == 0]
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
    
    def _evaluate_business_continuity(self, store_status: Dict, context: Dict) -> Dict:
        """Evaluate business continuity with Jack's emergency preparedness"""
        inventory = store_status.get('inventory', {})
        
        continuity = {
            'operational_capacity': 'FULL',
            'continuity_risks': [],
            'recovery_time': 'IMMEDIATE'
        }
        
        # Assess operational capacity
        total_products = len(inventory)
        stocked_products = len([qty for qty in inventory.values() if qty > 0])
        operational_rate = stocked_products / total_products if total_products > 0 else 1.0
        
        if operational_rate < 0.3:
            continuity['operational_capacity'] = 'CRITICAL'
            continuity['continuity_risks'].append("Insufficient inventory for operations")
            continuity['recovery_time'] = '24-48 HOURS'
        elif operational_rate < 0.6:
            continuity['operational_capacity'] = 'LIMITED'
            continuity['recovery_time'] = '12-24 HOURS'
        
        return continuity
    
    def _identify_emergency_protocols(self, store_status: Dict, context: Dict) -> Dict:
        """Identify emergency protocols with Jack's rapid response training"""
        protocols = {
            'immediate_actions': [],
            'short_term_actions': [],
            'contingency_plans': []
        }
        
        cash = store_status.get('cash', 0)
        inventory = store_status.get('inventory', {})
        
        # Financial emergency protocols
        if cash <= 100:
            protocols['immediate_actions'].append("Activate cash conservation")
            protocols['short_term_actions'].append("Prioritize high-margin sales")
        
        # Operational emergency protocols  
        stockouts = [product for product, qty in inventory.items() if qty == 0]
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
    
    def _calculate_confidence(self, store_status: Dict, threats: Dict) -> float:
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