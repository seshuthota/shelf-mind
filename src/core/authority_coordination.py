#!/usr/bin/env python3
"""
🎯 Authority-Based Coordination System

CORRECTED APPROACH: Domain Authority instead of Artificial Budgets

PROBLEM: Multi-agent debates on every decision
WRONG SOLUTION: Fake budgets for agents who don't spend money  
RIGHT SOLUTION: Clear domain authority + real inventory budget only

AUTHORITY MATRIX:
- Hermione: Full inventory authority + actual purchase budget
- Gekko: Full pricing authority (no money needed)
- Elle: Full customer service authority (no money needed)  
- Tyrion: Full strategic authority (no money needed)
- Jack: Emergency override authority + emergency fund access

DEBATES ONLY WHEN: 
- True cross-domain conflicts (rare)
- Emergency overrides normal authority
- Multiple agents claiming same domain
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from src.core.models import AgentRole, AgentDecision, StoreState

class AuthorityLevel(Enum):
    """Authority levels for agent decisions"""
    FULL_AUTHORITY = "full_authority"          # Agent has complete control
    SHARED_AUTHORITY = "shared_authority"      # Requires coordination
    EMERGENCY_OVERRIDE = "emergency_override"  # Can override other agents
    NO_AUTHORITY = "no_authority"              # Cannot make this decision

@dataclass
class DomainAuthority:
    """Authority definition for agent domains"""
    agent_role: AgentRole
    domain_areas: List[str]
    authority_level: AuthorityLevel
    budget_required: bool = False  # Only True for inventory/emergency
    override_conditions: List[str] = None

@dataclass 
class AuthorityDecision:
    """Decision with authority validation"""
    decision: AgentDecision
    authority_level: AuthorityLevel
    requires_budget: bool
    requires_coordination: bool
    can_proceed: bool

class AuthorityCoordinator:
    """🎯 Authority-Based Coordination - Eliminates artificial budget constraints"""
    
    def __init__(self):
        self.authority_matrix = self._build_authority_matrix()
        self.inventory_budget = 0.0
        self.emergency_fund = 0.0
        
    def _build_authority_matrix(self) -> Dict[AgentRole, DomainAuthority]:
        """Define clear authority for each agent domain"""
        return {
            # 📦 HERMIONE: Inventory Domain + Real Budget
            AgentRole.INVENTORY_MANAGER: DomainAuthority(
                agent_role=AgentRole.INVENTORY_MANAGER,
                domain_areas=[
                    "inventory_management", "supplier_orders", "stock_levels",
                    "spoilage_management", "reorder_decisions", "inventory_optimization"
                ],
                authority_level=AuthorityLevel.FULL_AUTHORITY,
                budget_required=True  # ONLY agent that actually spends money!
            ),
            
            # 💰 GEKKO: Pricing Domain + No Budget Needed
            AgentRole.PRICING_ANALYST: DomainAuthority(
                agent_role=AgentRole.PRICING_ANALYST,
                domain_areas=[
                    "pricing_strategy", "price_changes", "competitive_pricing",
                    "price_wars", "margin_optimization", "market_positioning"
                ],
                authority_level=AuthorityLevel.FULL_AUTHORITY,
                budget_required=False  # Price changes don't cost money!
            ),
            
            # 💕 ELLE: Customer Domain + No Budget Needed  
            AgentRole.CUSTOMER_SERVICE: DomainAuthority(
                agent_role=AgentRole.CUSTOMER_SERVICE,
                domain_areas=[
                    "customer_satisfaction", "service_quality", "customer_experience",
                    "loyalty_programs", "customer_relationships", "brand_sentiment"
                ],
                authority_level=AuthorityLevel.FULL_AUTHORITY,
                budget_required=False  # Service improvements don't cost money!
            ),
            
            # 🏰 TYRION: Strategic Domain + No Budget Needed
            AgentRole.STRATEGIC_PLANNER: DomainAuthority(
                agent_role=AgentRole.STRATEGIC_PLANNER,
                domain_areas=[
                    "strategic_planning", "business_intelligence", "market_analysis",
                    "growth_strategy", "competitive_analysis", "long_term_planning"
                ],
                authority_level=AuthorityLevel.FULL_AUTHORITY,
                budget_required=False  # Planning doesn't cost money!
            ),
            
            # ⚡ JACK: Emergency Domain + Emergency Fund Access
            AgentRole.CRISIS_MANAGER: DomainAuthority(
                agent_role=AgentRole.CRISIS_MANAGER,
                domain_areas=[
                    "crisis_management", "emergency_response", "business_continuity",
                    "risk_mitigation", "emergency_overrides"
                ],
                authority_level=AuthorityLevel.EMERGENCY_OVERRIDE,
                budget_required=True,  # Emergency responses may cost money
                override_conditions=["crisis_priority_9+", "stockout_emergency", "cash_crisis"]
            )
        }
    
    def allocate_real_budgets(self, store_state: StoreState):
        """Allocate actual budgets only where money is spent"""
        total_cash = store_state.cash
        
        # 80% for inventory (actual purchases)
        self.inventory_budget = total_cash * 0.8
        
        # 20% emergency fund (for Jack's real emergencies)
        self.emergency_fund = total_cash * 0.2
        
        print(f"💰 REAL BUDGET ALLOCATION:")
        print(f"   📦 Inventory Budget (Hermione): ${self.inventory_budget:.2f}")
        print(f"   🚨 Emergency Fund (Jack): ${self.emergency_fund:.2f}")
        print(f"   🎯 Authority-Based Decisions: No budget needed")
    
    def validate_decision_authority(self, decision: AgentDecision) -> AuthorityDecision:
        """Validate if agent has authority to make this decision"""
        
        agent_authority = self.authority_matrix.get(decision.agent_role)
        if not agent_authority:
            return AuthorityDecision(
                decision=decision,
                authority_level=AuthorityLevel.NO_AUTHORITY,
                requires_budget=False,
                requires_coordination=True,
                can_proceed=False
            )
        
        # Check if decision falls within agent's domain
        decision_domain = self._classify_decision_domain(decision)
        has_domain_authority = any(
            domain in decision_domain.lower() 
            for domain in agent_authority.domain_areas
        )
        
        if has_domain_authority:
            # Agent has authority in this domain
            requires_budget = agent_authority.budget_required and self._decision_needs_money(decision)
            
            can_proceed = True
            if requires_budget:
                # Check if sufficient budget available
                cost = self._estimate_decision_cost(decision)
                if decision.agent_role == AgentRole.INVENTORY_MANAGER:
                    can_proceed = cost <= self.inventory_budget
                elif decision.agent_role == AgentRole.CRISIS_MANAGER:
                    can_proceed = cost <= self.emergency_fund
            
            return AuthorityDecision(
                decision=decision,
                authority_level=agent_authority.authority_level,
                requires_budget=requires_budget,
                requires_coordination=False,
                can_proceed=can_proceed
            )
        else:
            # Decision outside agent's domain - requires coordination
            return AuthorityDecision(
                decision=decision,
                authority_level=AuthorityLevel.NO_AUTHORITY,
                requires_budget=False,
                requires_coordination=True,
                can_proceed=False
            )
    
    def _classify_decision_domain(self, decision: AgentDecision) -> str:
        """Classify decision into domain category"""
        decision_type = decision.decision_type.lower()
        
        # Inventory domain keywords
        if any(keyword in decision_type for keyword in ['inventory', 'stock', 'order', 'supplier', 'spoilage']):
            return "inventory_management"
        
        # Pricing domain keywords  
        if any(keyword in decision_type for keyword in ['pricing', 'price', 'margin', 'competitive']):
            return "pricing_strategy"
        
        # Customer domain keywords
        if any(keyword in decision_type for keyword in ['customer', 'service', 'satisfaction', 'loyalty']):
            return "customer_service"
        
        # Strategic domain keywords
        if any(keyword in decision_type for keyword in ['strategic', 'planning', 'analysis', 'growth']):
            return "strategic_planning"
        
        # Crisis domain keywords
        if any(keyword in decision_type for keyword in ['crisis', 'emergency', 'risk']):
            return "crisis_management"
        
        return "unknown_domain"
    
    def _decision_needs_money(self, decision: AgentDecision) -> bool:
        """Check if decision requires actual money spending"""
        money_keywords = [
            'order', 'purchase', 'buy', 'emergency_cost', 
            'supplier', 'restock', 'investment'
        ]
        
        decision_text = f"{decision.decision_type} {str(decision.parameters)}".lower()
        return any(keyword in decision_text for keyword in money_keywords)
    
    def _estimate_decision_cost(self, decision: AgentDecision) -> float:
        """Estimate cost only for decisions that actually spend money"""
        params = decision.parameters
        
        # Inventory costs
        if 'quantity' in params and 'cost_per_unit' in params:
            return params['quantity'] * params['cost_per_unit']
        elif 'order_value' in params:
            return params['order_value']
        elif 'emergency_cost' in params:
            return params['emergency_cost']
        
        return 0.0  # Most decisions don't cost money
    
    def coordinate_decisions(self, decisions: List[AgentDecision], store_state: StoreState) -> Dict:
        """Coordinate decisions using authority-based approach"""
        
        # Allocate real budgets
        self.allocate_real_budgets(store_state)
        
        approved_decisions = []
        authority_conflicts = []
        budget_violations = []
        
        print(f"\n🎯 AUTHORITY-BASED COORDINATION:")
        
        for decision in decisions:
            authority_decision = self.validate_decision_authority(decision)
            
            if authority_decision.can_proceed:
                # Agent has authority and budget (if needed) - APPROVE
                if authority_decision.requires_budget:
                    cost = self._estimate_decision_cost(decision)
                    if decision.agent_role == AgentRole.INVENTORY_MANAGER:
                        self.inventory_budget -= cost
                    elif decision.agent_role == AgentRole.CRISIS_MANAGER:
                        self.emergency_fund -= cost
                    
                    decision.reasoning += f" [APPROVED: ${cost:.2f} from budget]"
                else:
                    decision.reasoning += " [APPROVED: Domain authority]"
                
                approved_decisions.append(decision)
                print(f"   ✅ {decision.agent_role.value}: {decision.decision_type}")
                
            elif authority_decision.requires_coordination:
                # Outside domain - potential conflict
                authority_conflicts.append(decision)
                print(f"   ⚠️ {decision.agent_role.value}: {decision.decision_type} (DOMAIN CONFLICT)")
                
            else:
                # Budget violation
                budget_violations.append(decision)
                print(f"   ❌ {decision.agent_role.value}: {decision.decision_type} (BUDGET EXCEEDED)")
        
        return {
            'approved_decisions': approved_decisions,
            'authority_conflicts': authority_conflicts,
            'budget_violations': budget_violations,
            'debate_needed': len(authority_conflicts) > 0,
            'inventory_budget_remaining': self.inventory_budget,
            'emergency_fund_remaining': self.emergency_fund
        }
    
    def get_authority_summary(self) -> Dict:
        """Get summary of authority assignments"""
        return {
            'authority_matrix': {
                role.value: {
                    'domains': authority.domain_areas,
                    'authority_level': authority.authority_level.value,
                    'needs_budget': authority.budget_required
                }
                for role, authority in self.authority_matrix.items()
            },
            'budget_allocations': {
                'inventory_budget': self.inventory_budget,
                'emergency_fund': self.emergency_fund,
                'total_allocated': self.inventory_budget + self.emergency_fund
            }
        } 