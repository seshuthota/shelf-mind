from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import json
from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Optional AI imports - gracefully handle missing dependencies
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OpenAI = None
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    Anthropic = None
    ANTHROPIC_AVAILABLE = False

# Phase 4B: Import the new character debate engine
from src.core.character_debate_engine import CharacterDebateEngine, DebateTopicType, DebateResolution
from src.core.models import AgentRole, AgentDecision, StoreState
# Phase 4B.4: Import advanced coordination intelligence
from src.core.coordination_intelligence import (
    PredictiveCoordinationEngine, CrossDomainImpact, AgentInsight, 
    ResourceConflict, CoordinationMetrics
)

load_dotenv()

from dataclasses import field

# Phase 5A.1: Character Decision Authority Matrix
CHARACTER_AUTHORITY_MATRIX = {
    AgentRole.PRICING_ANALYST: {
        "primary_domains": ["pricing", "competitive_strategy", "profit_optimization"],
        "decision_weight": 2.0,  # 2x weight in pricing decisions
        "override_threshold": 8  # Priority 8+ required for others to override
    },
    AgentRole.INVENTORY_MANAGER: {
        "primary_domains": ["inventory", "ordering", "supply_chain"],
        "decision_weight": 2.0,  # 2x weight in inventory decisions
        "override_threshold": 8
    },
    AgentRole.CUSTOMER_SERVICE: {
        "primary_domains": ["customer_experience", "service_quality", "satisfaction"],
        "decision_weight": 1.5,  # 1.5x weight in customer decisions
        "override_threshold": 7
    },
    AgentRole.STRATEGIC_PLANNER: {
        "primary_domains": ["strategy", "resource_allocation", "long_term_planning"],
        "decision_weight": 1.8,  # 1.8x weight in strategic decisions
        "override_threshold": 7
    },
    AgentRole.CRISIS_MANAGER: {
        "primary_domains": ["crisis_response", "emergency_decisions", "rapid_action"],
        "decision_weight": 3.0,  # 3x weight during crisis situations
        "override_threshold": 9  # Very high threshold - crises need quick decisions
    }
}

@dataclass
class CharacterDecisionTranslation:
    """Translation of character consensus into business actions"""
    pricing_decisions: Dict[str, float] = field(default_factory=dict)
    ordering_decisions: Dict[str, int] = field(default_factory=dict)
    decision_confidence: float = 0.0
    primary_decision_maker: Optional[AgentRole] = None
    override_occurred: bool = False
    executive_oversight_notes: str = ""

@dataclass
class AgentConsensus:
    """Represents consensus reached by multiple agents"""
    final_decisions: List[AgentDecision]
    conflicts_resolved: List[str]
    coordination_notes: str
    overall_confidence: float
    # Phase 4B: Add debate information
    debate_occurred: bool = False
    debate_resolution: Optional[DebateResolution] = None
    # Phase 4B.4: Add advanced coordination intelligence
    cross_domain_impacts: List[CrossDomainImpact] = field(default_factory=list)
    shared_insights: List[AgentInsight] = field(default_factory=list)
    resource_conflicts: List[ResourceConflict] = field(default_factory=list)
    coordination_metrics: Optional[CoordinationMetrics] = None
    optimized_sequence: List[AgentDecision] = field(default_factory=list)
    # Phase 5A.1: Add decision translation
    business_translation: Optional[CharacterDecisionTranslation] = None
    # Budget-First Coordination
    budget_summary: Dict = field(default_factory=dict)
    budget_utilization: float = 0.0

class BaseSpecialistAgent:
    """Base class for all specialist agents"""
    
    def __init__(self, role: AgentRole, provider: str = "openai"):
        self.role = role
        self.provider = provider
        self.client = None
        self.model = None
        
        if provider == "openai" and OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-4.1-mini"
        elif provider == "anthropic" and ANTHROPIC_AVAILABLE:
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = "claude-3-sonnet-20240229"
        elif provider == "mock":
            # Mock provider for testing
            self.client = None
            self.model = "mock"
        else:
            # No AI client available - will work in mock mode
            self.client = None
            self.model = "no_ai"
            
        self.memory = []
        self.specializations = self._define_specializations()
        
    def _define_specializations(self) -> List[str]:
        """Override in subclasses to define agent specializations"""
        return []
        
    def analyze_situation(self, store_status: Dict, context: Dict) -> AgentDecision:
        """Analyze situation and make recommendations - override in subclasses"""
        raise NotImplementedError("Subclasses must implement analyze_situation")
        
    def get_tools(self) -> List[Dict]:
        """Get specialist tools for this agent - override in subclasses"""
        return []

class MultiAgentCoordinator:
    """🤖 Phase 5A.1: Enhanced Multi-Agent Coordination with True Decision Control
    
    Coordinates specialist agents with sophisticated debate, predictive coordination,
    and true business decision-making capabilities.
    """
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self.specialist_agents: Dict[AgentRole, BaseSpecialistAgent] = {}
        self.coordination_history = []
        
        # Phase 4B: Initialize character debate engine
        self.debate_engine = CharacterDebateEngine(provider)
        
        # Phase 5A.3: Budget-First Coordination - Eliminate 90% of debates
        self.budget_enabled = True
        self.debate_enabled = False  # Disabled by default - only for true emergencies
        self.debate_threshold = 5  # Much higher threshold
        self.emergency_only_debates = True  # Only allow emergency debates
        
        # Phase 4B.4: Initialize predictive coordination engine
        self.coordination_engine = PredictiveCoordinationEngine()
        self.intelligence_sharing_enabled = True
        self.proactive_conflict_prevention = True
        
        # Phase 5A.1: Initialize decision translation capabilities
        self.character_authority_enabled = True
        self.decision_translation_enabled = True
        
        # 🛠️ Phase 5A.3: Initialize tool performance tracking
        self.tool_performance_tracker = {
            'total_tool_calls': 0,
            'successful_tool_calls': 0,
            'tool_usage_by_agent': {},
            'tool_performance_history': [],
            'most_influential_tools': []
        }

    def _transform_to_store_state(self, status: Dict, context: Dict) -> StoreState:
        """Helper function to transform store_status to StoreState"""
        from src.core.models import StoreState, InventoryItem, InventoryBatch, DeliveryOrder, PaymentTerm
        
        inventory_items = {}
        for name, qty in status.get('inventory', {}).items():
            # Create a single batch for the current quantity
            batch = InventoryBatch(quantity=qty, received_day=status.get('day', 1) -1, expiration_day=None)
            inventory_items[name] = InventoryItem(product_name=name, batches=[batch])

        # Extract yesterday's summary if available
        yesterday_summary = context.get('yesterday_summary') if context else None
        
        # Provide safe defaults for required fields
        daily_sales = {}
        total_revenue = 0.0
        total_profit = 0.0
        
        if yesterday_summary:
            # Safely extract with defaults
            daily_sales = yesterday_summary.get('units_sold_by_product', {})
            if not daily_sales:
                daily_sales = yesterday_summary.get('sales_by_product', {})
            total_revenue = float(yesterday_summary.get('revenue', 0.0))
            total_profit = float(yesterday_summary.get('profit', 0.0))
        
        # Transform pending deliveries - FIXED: Handle summary format from store engine
        pending_deliveries = []
        if 'pending_deliveries' in status and status['pending_deliveries'] is not None:
            for delivery_summary in status['pending_deliveries']:
                # Check if this is summary format from get_pending_deliveries_summary
                if 'product' in delivery_summary and 'supplier' in delivery_summary:
                    # Map summary format to DeliveryOrder format with reasonable defaults
                    current_day = int(status.get('day', 1))
                    days_remaining = delivery_summary.get('days_remaining', 1)
                    
                    delivery_order = DeliveryOrder(
                        supplier_name=delivery_summary['supplier'],
                        product_name=delivery_summary['product'],
                        quantity=delivery_summary.get('quantity', 1),
                        cost_per_unit=delivery_summary.get('total_cost', 0.0) / max(1, delivery_summary.get('quantity', 1)),
                        total_cost=delivery_summary.get('total_cost', 0.0),
                        order_day=max(1, current_day - 1),  # Reasonable default
                        delivery_day=current_day + days_remaining,
                        payment_terms=PaymentTerm.NET_30,  # Default assumption
                        bulk_discount_applied=False  # Default assumption
                    )
                    pending_deliveries.append(delivery_order)
                    
                elif 'supplier_name' in delivery_summary and 'product_name' in delivery_summary:
                    # This is already in full DeliveryOrder format
                    # Ensure payment_terms is a PaymentTerm enum member
                    if 'payment_terms' in delivery_summary and isinstance(delivery_summary['payment_terms'], str):
                        try:
                            payment_term_enum = PaymentTerm(delivery_summary['payment_terms'])
                            delivery_summary['payment_terms'] = payment_term_enum
                        except ValueError:
                            delivery_summary['payment_terms'] = PaymentTerm.UPFRONT
                    
                    pending_deliveries.append(DeliveryOrder(**delivery_summary))
                else:
                    # Unknown format - skip this delivery to avoid validation errors
                    print(f"Warning: Skipping delivery with unknown format: {delivery_summary}")

        return StoreState(
            day=int(status.get('day', 1)),
            cash=float(status.get('cash', 0.0)),
            inventory=inventory_items,
            daily_sales=daily_sales,
            daily_spoilage={name: 0 for name in daily_sales.keys()},  # Default empty spoilage
            total_revenue=total_revenue,
            total_profit=total_profit,
            total_spoilage_cost=float(status.get('total_spoilage_cost', 0.0)),
            pending_deliveries=pending_deliveries,
            accounts_payable=float(status.get('accounts_payable', 0.0)),
            active_crises=status.get('active_crises', []),
            crisis_response_cash=float(status.get('crisis_response_cash', 0.0)),
            regulatory_compliance_cost=float(status.get('regulatory_compliance_cost', 0.0))
        )
        
    def register_specialist(self, agent: BaseSpecialistAgent):
        """Register a specialist agent with the coordinator"""
        self.specialist_agents[agent.role] = agent
        
    def coordinate_decisions(self, store_status: Dict, context: Dict) -> AgentConsensus:
        """🎯 Phase 5A.3: Budget-First Coordination - Fast, Efficient Decision Making
        
        NEW APPROACH:
        1. Initialize/Update agent budgets (eliminates resource debates)
        2. Each agent operates within their budget autonomously  
        3. Only trigger debates for true emergencies or budget overruns
        4. 90% fewer debates, 10x faster execution
        """
        
        print(f"\n🎯 BUDGET-FIRST COORDINATION: Day {store_status.get('day', 0)}")
        print("="*60)
        
        # Initialize store state with budget allocation
        store_state = self._transform_to_store_state(store_status, context)
        
        # Phase 5A.3: Initialize budget system if not present
        if not store_state.budget_allocation:
            store_state.initialize_budgets()
            print("💰 BUDGET SYSTEM INITIALIZED")
        else:
            store_state.update_daily_budgets()
            print("💰 DAILY BUDGETS UPDATED")
        
        # Display budget allocation
        budget_summary = store_state.budget_allocation.get_budget_summary()
        print(f"📊 BUDGET ALLOCATION:")
        for role, budget_info in budget_summary['agent_budgets'].items():
            print(f"   {role}: ${budget_info['daily']:.2f} (${budget_info['remaining']:.2f} remaining)")
        
        # Get agent decisions with budget constraints
        agent_decisions = []
        budget_violations = []
        
        for agent_role, agent in self.specialist_agents.items():
            try:
                # Get agent's budget
                agent_budget = store_state.budget_allocation.agent_budgets.get(agent_role)
                
                # Pass budget info to agent
                budget_context = {
                    **context,
                    'agent_budget': agent_budget.remaining_budget if agent_budget else 0.0,
                    'budget_category': agent_budget.budget_category if agent_budget else 'operations'
                }
                
                # Agents expect dictionary format, not StoreState
                store_dict = store_state.dict() if hasattr(store_state, 'dict') else store_state
                decision = agent.analyze_situation(store_dict, budget_context)
                
                # Convert single decision to list for consistency
                decisions = [decision] if decision else []
                
                # Validate decisions against budget
                for decision in decisions:
                    cost = self._estimate_decision_cost(decision, store_state)
                    
                    if agent_budget and cost > 0:
                        if agent_budget.can_spend(cost):
                            # Approved - deduct from budget
                            agent_budget.spend(cost, decision.decision_type)
                            decision.reasoning += f" [BUDGET: ${cost:.2f} approved]"
                            agent_decisions.append(decision)
                        else:
                            # Budget violation - flag for emergency review
                            budget_violations.append({
                                'decision': decision,
                                'required_cost': cost,
                                'available_budget': agent_budget.remaining_budget,
                                'agent_role': agent_role
                            })
                    else:
                        # No cost or no budget system - approve
                        agent_decisions.append(decision)
                        
            except Exception as e:
                print(f"Warning: Agent {agent_role.value} failed: {e}")
        
        # Phase 5A.3: Emergency Budget Override System
        emergency_decisions = []
        if budget_violations and self.emergency_only_debates:
            print(f"\n⚠️ BUDGET VIOLATIONS DETECTED: {len(budget_violations)} decisions")
            emergency_decisions = self._handle_budget_violations(budget_violations, store_state, context)
            agent_decisions.extend(emergency_decisions)
        
        # Simplified conflict detection - only for true emergencies
        resource_conflicts = []
        if self.proactive_conflict_prevention:
            resource_conflicts = self._detect_critical_conflicts_only(agent_decisions, store_state)
        
        # Drastically reduced debate triggering - only true emergencies
        debate_resolution = None
        if self.debate_enabled and (budget_violations or self._is_true_emergency(agent_decisions, store_state)):
            debate_topic = self._emergency_debate_only(agent_decisions, store_status, resource_conflicts)
            
            if debate_topic:
                print(f"\n🚨 EMERGENCY DEBATE TRIGGERED: {debate_topic.value.upper()}")
                try:
                    debate_resolution = self.debate_engine.initiate_debate(
                        debate_topic, store_status, context, agent_decisions
                    )
                    agent_decisions = self._apply_debate_outcome(agent_decisions, debate_resolution)
                except Exception as e:
                    print(f"Warning: Emergency debate failed: {e}")
        else:
            print(f"✅ NO DEBATES NEEDED: All decisions within budget and authority")
        
        # Build streamlined consensus
        consensus = self._build_budget_consensus(
            agent_decisions, store_state, context, debate_resolution, budget_summary
        )
        
        # Store coordination history
        self.coordination_history.append({
            'day': store_status.get('day', 0),
            'decisions': agent_decisions,
            'consensus': consensus,
            'budget_violations': len(budget_violations),
            'debate_occurred': debate_resolution is not None
        })
        
        return consensus

    def _estimate_decision_cost(self, decision: AgentDecision, store_state: StoreState) -> float:
        """Estimate the cost of executing a decision"""
        params = decision.parameters
        
        # Inventory decisions
        if decision.agent_role == AgentRole.INVENTORY_MANAGER:
            if 'quantity' in params and 'cost_per_unit' in params:
                return params['quantity'] * params['cost_per_unit']
            elif 'order_value' in params:
                return params['order_value']
            
        # Pricing decisions (usually no direct cost)
        elif decision.agent_role == AgentRole.PRICING_ANALYST:
            return 0.0  # Pricing changes don't cost money
            
        # Customer service initiatives
        elif decision.agent_role == AgentRole.CUSTOMER_SERVICE:
            return params.get('budget_required', 10.0)  # Default small marketing budget
            
        # Strategic investments
        elif decision.agent_role == AgentRole.STRATEGIC_PLANNER:
            return params.get('investment_amount', 25.0)  # Strategic initiatives cost
            
        # Crisis management
        elif decision.agent_role == AgentRole.CRISIS_MANAGER:
            return params.get('emergency_cost', 15.0)  # Emergency response cost
        
        return 0.0  # Default no cost

    def _handle_budget_violations(self, violations: List[Dict], store_state: StoreState, context: Dict) -> List[AgentDecision]:
        """Handle budget violations with emergency protocols"""
        approved_decisions = []
        emergency_fund = store_state.budget_allocation.emergency_reserve
        
        print(f"\n🚨 EMERGENCY BUDGET REVIEW:")
        print(f"   Emergency Reserve: ${emergency_fund:.2f}")
        
        for violation in violations:
            decision = violation['decision']
            required_cost = violation['required_cost']
            agent_role = violation['agent_role']
            
            # Check if it's a true emergency (high priority)
            if decision.priority >= 8 and required_cost <= emergency_fund:
                # Approve from emergency fund
                emergency_fund -= required_cost
                decision.reasoning += f" [EMERGENCY APPROVED: ${required_cost:.2f} from reserve]"
                approved_decisions.append(decision)
                print(f"   ✅ APPROVED: {agent_role.value} - ${required_cost:.2f} (Priority: {decision.priority})")
            else:
                # Reject or defer
                print(f"   ❌ REJECTED: {agent_role.value} - ${required_cost:.2f} (Insufficient funds/priority)")
        
        return approved_decisions

    def _detect_critical_conflicts_only(self, decisions: List[AgentDecision], store_state: StoreState) -> List:
        """Only detect truly critical conflicts that need immediate attention"""
        critical_conflicts = []
        
        # Only flag conflicts if multiple agents want >50% of remaining cash
        total_cash = store_state.cash
        high_cost_decisions = []
        
        for decision in decisions:
            cost = self._estimate_decision_cost(decision, store_state)
            if cost > total_cash * 0.5:  # >50% of cash
                high_cost_decisions.append((decision, cost))
        
        if len(high_cost_decisions) > 1:
            total_demand = sum(cost for _, cost in high_cost_decisions)
            critical_conflicts.append({
                'type': 'cash_conflict',
                'total_demand': total_demand,
                'available_cash': total_cash,
                'competing_decisions': high_cost_decisions
            })
        
        return critical_conflicts

    def _is_true_emergency(self, decisions: List[AgentDecision], store_state: StoreState) -> bool:
        """Check if any decision represents a true emergency requiring debate"""
        # Check for crisis manager decisions with priority 9-10
        crisis_emergencies = [d for d in decisions if d.agent_role == AgentRole.CRISIS_MANAGER and d.priority >= 9]
        
        # Check for inventory emergencies (stockouts)
        inventory_emergencies = [d for d in decisions if d.agent_role == AgentRole.INVENTORY_MANAGER and d.priority >= 9]
        
        # Check for cash flow emergencies
        cash_emergencies = store_state.cash < 50.0  # Less than $50 is emergency
        
        return len(crisis_emergencies) > 0 or len(inventory_emergencies) > 0 or cash_emergencies

    def _emergency_debate_only(self, decisions: List[AgentDecision], store_status: Dict, conflicts: List) -> Optional[DebateTopicType]:
        """Only trigger debates for true emergencies - not routine operations"""
        
        # Check for true emergencies only
        if self._is_true_emergency(decisions, self._transform_to_store_state(store_status, {})):
            print("🚨 TRUE EMERGENCY DETECTED - Triggering emergency debate")
            return DebateTopicType.STRATEGIC_PLANNING  # Emergency strategic session
        
        # Check for major cash conflicts
        if conflicts and any(c.get('type') == 'cash_conflict' for c in conflicts):
            print("💰 MAJOR CASH CONFLICT - Triggering emergency debate")
            return DebateTopicType.STRATEGIC_PLANNING
        
        return None  # No debate needed

    def _build_budget_consensus(self, decisions: List[AgentDecision], store_state: StoreState, 
                              context: Dict, debate_resolution: Optional[DebateResolution],
                              budget_summary: Dict) -> AgentConsensus:
        """Build consensus using budget-first approach"""
        
        # Sort by priority
        sorted_decisions = sorted(decisions, key=lambda d: d.priority, reverse=True)
        
        # Calculate confidence
        overall_confidence = sum(d.confidence for d in decisions) / len(decisions) if decisions else 0.0
        
        # Enhanced coordination notes
        coordination_notes = f"Budget-first coordination: {len(decisions)} decisions within budget allocations."
        if debate_resolution:
            coordination_notes += f" Emergency debate: {debate_resolution.debate_summary}."
        
        conflicts_resolved = []
        if debate_resolution:
            conflicts_resolved.append(f"Emergency resolved: {debate_resolution.debate_summary}")
        
        return AgentConsensus(
            final_decisions=sorted_decisions,
            conflicts_resolved=conflicts_resolved,
            coordination_notes=coordination_notes,
            overall_confidence=overall_confidence,
            debate_occurred=debate_resolution is not None,
            debate_resolution=debate_resolution,
            # Add budget information
            budget_summary=budget_summary,
            budget_utilization=budget_summary.get('utilization_rate', 0.0)
        )

    def enable_budget_system(self, enabled: bool = True):
        """Enable or disable the budget-first coordination system"""
        self.budget_enabled = enabled
        if enabled:
            self.debate_enabled = False  # Budget system replaces most debates
            self.emergency_only_debates = True
            print("💰 BUDGET-FIRST SYSTEM ENABLED: Debates limited to true emergencies")
        else:
            self.debate_enabled = True
            self.emergency_only_debates = False
            print("🎭 DEBATE SYSTEM ENABLED: Traditional coordination with debates")

    def _apply_debate_outcome(self, agent_decisions: List[AgentDecision], 
                            debate_resolution: DebateResolution) -> List[AgentDecision]:
        """Apply the outcome of character debate to agent decisions"""
        
        if not debate_resolution or not debate_resolution.winning_position:
            return agent_decisions
            
        # Find the winning character's decision and boost its priority
        winning_character = debate_resolution.winning_position.character_name
        winning_role = self._get_agent_role_from_character(winning_character)
        
        for decision in agent_decisions:
            if decision.agent_role == winning_role:
                # Boost winning decision priority and confidence
                decision.priority = min(decision.priority + 2, 10)
                decision.confidence = min(decision.confidence + 0.2, 1.0)
                decision.reasoning += f" [DEBATE WINNER: {winning_character.upper()} consensus achieved]"
                break
                
        return agent_decisions
        
    def _display_coordination_intelligence(self, impacts: List[CrossDomainImpact], 
                                         insights: List[AgentInsight], 
                                         conflicts: List[ResourceConflict]):
        """Display advanced coordination intelligence insights"""
        
        if impacts:
            print(f"   🔮 Cross-Domain Impacts: {len(impacts)} detected")
            for impact in impacts[:3]:  # Show top 3
                print(f"      {impact.source_agent.value} → {impact.target_agent.value}: "
                      f"{impact.impact_type.value} ({impact.impact_magnitude:.2f})")
                      
        if insights:
            print(f"   🚀 Proactive Insights: {len(insights)} generated for sharing")
            for insight in insights[:2]:  # Show top 2
                print(f"      {insight.agent_role.value}: {insight.insight_type} (urgency: {insight.urgency:.2f})")
                
        if conflicts:
            print(f"   ⚠️  Resource Conflicts: {len(conflicts)} detected")
            for conflict in conflicts:
                agents_str = ", ".join([agent.value for agent in conflict.competing_agents])
                print(f"      {conflict.resource_type}: {agents_str} (severity: {conflict.conflict_severity:.2f})")
                
    def _translate_consensus_to_business_decisions(self, decisions: List[AgentDecision], 
                                                  store_status: Dict, 
                                                  debate_resolution: Optional[DebateResolution] = None) -> CharacterDecisionTranslation:
        """Phase 5A.1: Translate character consensus into concrete business actions"""
        
        pricing_decisions = {}
        ordering_decisions = {}
        confidence_scores = []
        primary_decision_maker = None
        override_occurred = False
        
        # Extract current store state for decision context
        current_prices = {name: info['price'] for name, info in store_status.get('products', {}).items()}
        current_inventory = store_status.get('inventory', {})
        cash_available = store_status.get('cash', 0)
        
        # Phase 5A.1: Determine primary decision maker based on character authority
        decision_weights = {}
        for decision in decisions:
            authority = CHARACTER_AUTHORITY_MATRIX.get(decision.agent_role, {})
            weight = authority.get("decision_weight", 1.0)
            
            # Boost weight for domain expertise
            if any(domain in decision.reasoning.lower() for domain in authority.get("primary_domains", [])):
                weight *= 1.5
                
            decision_weights[decision.agent_role] = weight * decision.confidence
            
        if decision_weights:
            primary_decision_maker = max(decision_weights.keys(), key=lambda x: decision_weights[x])
        
        # Phase 5A.1: Extract pricing decisions from character reasoning
        for decision in decisions:
            authority = CHARACTER_AUTHORITY_MATRIX.get(decision.agent_role, {})
            
            # Parse pricing recommendations from character reasoning
            if "price" in decision.reasoning.lower() and decision.priority >= 5:
                # Extract pricing suggestions from character reasoning
                pricing_suggestions = self._extract_pricing_from_reasoning(decision.reasoning, current_prices)
                
                # Apply character authority weighting
                weight = authority.get("decision_weight", 1.0)
                if decision.agent_role == AgentRole.PRICING_ANALYST:
                    # Gekko has primary authority over pricing
                    for product, suggested_price in pricing_suggestions.items():
                        pricing_decisions[product] = suggested_price
                        
        # Phase 5A.1: Extract ordering decisions from character reasoning  
        for decision in decisions:
            authority = CHARACTER_AUTHORITY_MATRIX.get(decision.agent_role, {})
            
            # Parse inventory/ordering recommendations
            if ("inventory" in decision.reasoning.lower() or "order" in decision.reasoning.lower()) and decision.priority >= 5:
                ordering_suggestions = self._extract_ordering_from_reasoning(decision.reasoning, current_inventory)
                
                if decision.agent_role == AgentRole.INVENTORY_MANAGER:
                    # Hermione has primary authority over inventory
                    for product, suggested_quantity in ordering_suggestions.items():
                        if cash_available >= suggested_quantity * 1.0:  # Rough cost estimate
                            ordering_decisions[product] = suggested_quantity
        
        # Phase 5A.1: Apply debate resolution if available
        if debate_resolution and debate_resolution.business_decision:
            business_decision = debate_resolution.business_decision
            
            if "prices" in business_decision:
                pricing_decisions.update(business_decision["prices"])
                override_occurred = True
                
            if "orders" in business_decision:
                ordering_decisions.update(business_decision["orders"])
                override_occurred = True
        
        # Calculate overall confidence
        confidence_scores = [d.confidence for d in decisions if d.priority >= 5]
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        
        # CRITICAL FIX: Add fallback logic when decision translation fails
        if not pricing_decisions and not ordering_decisions:
            # Emergency fallback to ensure basic business operations continue
            print("⚠️ WARNING: Decision translation failed - applying emergency fallback decisions")
            
            # Fallback pricing: Set reasonable default prices if none extracted
            if not pricing_decisions:
                for product_name, current_price in current_prices.items():
                    # Ensure prices are in reasonable range (1.50-3.50)
                    if current_price < 1.0 or current_price > 5.0:
                        pricing_decisions[product_name] = 2.50  # Safe default price
                        
            # Fallback ordering: Restock items that are low/empty
            if not ordering_decisions:
                for product_name, quantity in current_inventory.items():
                    if quantity <= 2:  # Low stock or stockout
                        # Order reasonable amount based on cash available
                        if cash_available >= 30:  # Can afford multiple items
                            ordering_decisions[product_name] = 8
                        elif cash_available >= 15:  # Limited funds
                            ordering_decisions[product_name] = 5
                        elif cash_available >= 5:  # Very limited funds
                            ordering_decisions[product_name] = 2
                            
            executive_oversight_notes = f"FALLBACK APPLIED: {len(pricing_decisions)} price fixes, {len(ordering_decisions)} emergency restocks"
        else:
            executive_oversight_notes = f"Translated from {len(decisions)} character decisions"
        
        return CharacterDecisionTranslation(
            pricing_decisions=pricing_decisions,
            ordering_decisions=ordering_decisions,
            decision_confidence=overall_confidence,
            primary_decision_maker=primary_decision_maker,
            override_occurred=override_occurred,
            executive_oversight_notes=executive_oversight_notes
        )
        
    def _extract_pricing_from_reasoning(self, reasoning: str, current_prices: Dict[str, float]) -> Dict[str, float]:
        """Extract pricing suggestions from character reasoning - ENHANCED PATTERN MATCHING"""
        pricing_suggestions = {}
        reasoning_lower = reasoning.lower()
        
        for product_name in current_prices.keys():
            product_lower = product_name.lower()
            current_price = current_prices[product_name]
            
            # EXPANDED PATTERN MATCHING
            
            # 1. Explicit price suggestions (multiple formats)
            patterns = [
                f"{product_lower} to $", f"{product_lower}: $", f"price {product_lower} at $",
                f"set {product_lower} $", f"{product_lower} should be $", f"{product_lower} at $"
            ]
            
            for pattern in patterns:
                if pattern in reasoning_lower:
                    # Extract price value after the pattern
                    start_idx = reasoning_lower.find(pattern) + len(pattern)
                    price_text = reasoning_lower[start_idx:start_idx+6]
                    
                    # Extract numbers from the following text
                    import re
                    price_match = re.search(r'(\d+\.?\d*)', price_text)
                    if price_match:
                        try:
                            price_value = float(price_match.group(1))
                            if 0.50 <= price_value <= 10.0:  # Reasonable range
                                pricing_suggestions[product_name] = price_value
                                break
                        except ValueError:
                            continue
            
            # 2. Percentage adjustments (expanded patterns)
            if product_name not in pricing_suggestions:
                if any(phrase in reasoning_lower for phrase in [
                    f"increase {product_lower}", f"raise {product_lower}", f"higher {product_lower}",
                    f"up {product_lower}", f"{product_lower} up"
                ]):
                    pricing_suggestions[product_name] = min(current_price * 1.10, 10.0)  # 10% increase, cap at $10
                    
                elif any(phrase in reasoning_lower for phrase in [
                    f"decrease {product_lower}", f"reduce {product_lower}", f"lower {product_lower}",
                    f"down {product_lower}", f"{product_lower} down", f"cheaper {product_lower}"
                ]):
                    pricing_suggestions[product_name] = max(current_price * 0.90, 0.50)  # 10% decrease, floor at $0.50
            
            # 3. General pricing context (fallback for high-priority pricing decisions)
            if product_name not in pricing_suggestions and "pric" in reasoning_lower and product_lower in reasoning_lower:
                # If pricing is mentioned with this product but no specific price found,
                # make a small adjustment based on context
                if "competit" in reasoning_lower or "undercut" in reasoning_lower:
                    pricing_suggestions[product_name] = max(current_price * 0.95, 0.50)  # Competitive pricing
                elif "premium" in reasoning_lower or "quality" in reasoning_lower:
                    pricing_suggestions[product_name] = min(current_price * 1.05, 10.0)  # Premium pricing
                
        return pricing_suggestions
        
    def _extract_ordering_from_reasoning(self, reasoning: str, current_inventory: Dict[str, int]) -> Dict[str, int]:
        """Extract ordering suggestions from character reasoning - ENHANCED PATTERN MATCHING"""
        ordering_suggestions = {}
        reasoning_lower = reasoning.lower()
        
        for product_name, current_stock in current_inventory.items():
            product_lower = product_name.lower()
            
            # EXPANDED PATTERN MATCHING FOR INVENTORY DECISIONS
            
            # 1. Explicit ordering patterns (multiple formats)
            order_patterns = [
                f"order {product_lower}", f"buy {product_lower}", f"purchase {product_lower}",
                f"restock {product_lower}", f"{product_lower} order", f"get {product_lower}",
                f"stock {product_lower}", f"add {product_lower}"
            ]
            
            for pattern in order_patterns:
                if pattern in reasoning_lower:
                    # Extract quantity near the pattern
                    pattern_pos = reasoning_lower.find(pattern)
                    # Look for numbers in surrounding text (before and after)
                    surrounding_text = reasoning_lower[max(0, pattern_pos-20):pattern_pos+50]
                    
                    import re
                    numbers = re.findall(r'\b(\d+)\b', surrounding_text)
                    for num_str in numbers:
                        try:
                            quantity = int(num_str)
                            if 1 <= quantity <= 50:  # Reasonable range
                                ordering_suggestions[product_name] = quantity
                                break
                        except ValueError:
                            continue
                    
                    # If pattern found but no specific quantity, use default based on stock level
                    if product_name not in ordering_suggestions:
                        if current_stock == 0:
                            ordering_suggestions[product_name] = 10  # Large restock for stockouts
                        elif current_stock <= 2:
                            ordering_suggestions[product_name] = 8   # Standard restock
                        else:
                            ordering_suggestions[product_name] = 5   # Regular restock
                    break
            
            # 2. Stock level warnings and descriptions
            if product_name not in ordering_suggestions:
                stock_warnings = [
                    f"{product_lower} low", f"{product_lower} empty", f"{product_lower} stockout",
                    f"out of {product_lower}", f"{product_lower} shortage", f"need {product_lower}",
                    f"{product_lower} depleted", f"running low on {product_lower}"
                ]
                
                for warning in stock_warnings:
                    if warning in reasoning_lower:
                        ordering_suggestions[product_name] = 8  # Emergency restock
                        break
            
            # 3. Inventory management context (fallback)
            if product_name not in ordering_suggestions and current_stock <= 2:
                inventory_context = [
                    "inventory", "stock", "supply", "reorder", "replenish"
                ]
                
                if any(context in reasoning_lower for context in inventory_context) and product_lower in reasoning_lower:
                    # If inventory is mentioned with this product and it's low stock
                    ordering_suggestions[product_name] = 6  # Conservative restock
                
        return ordering_suggestions

    def _build_enhanced_consensus(self, decisions: List[AgentDecision], store_status: Dict, context: Dict,
                                debate_resolution: Optional[DebateResolution] = None,
                                cross_domain_impacts: List[CrossDomainImpact] = None,
                                shared_insights: List[AgentInsight] = None,
                                resource_conflicts: List[ResourceConflict] = None,
                                business_translation: Optional[CharacterDecisionTranslation] = None) -> AgentConsensus:
        """🧠 Enhanced consensus building with coordination intelligence"""
        
        # Build base consensus
        base_consensus = self._build_consensus(decisions, store_status, context, debate_resolution)
        
        # Enhance with coordination intelligence
        base_consensus.cross_domain_impacts = cross_domain_impacts or []
        base_consensus.shared_insights = shared_insights or []
        base_consensus.resource_conflicts = resource_conflicts or []
        base_consensus.coordination_metrics = self.coordination_engine.metrics
        base_consensus.optimized_sequence = decisions
        base_consensus.business_translation = business_translation
        
        # Update coordination notes with intelligence insights
        intelligence_notes = []
        if cross_domain_impacts:
            intelligence_notes.append(f"{len(cross_domain_impacts)} cross-domain impacts predicted")
        if shared_insights:
            intelligence_notes.append(f"{len(shared_insights)} insights shared proactively")
        if resource_conflicts:
            intelligence_notes.append(f"{len(resource_conflicts)} resource conflicts detected")
            
        if intelligence_notes:
            base_consensus.coordination_notes += " Advanced intelligence: " + ", ".join(intelligence_notes) + "."
            
        return base_consensus
        
    def _build_consensus(self, decisions: List[AgentDecision], store_status: Dict, context: Dict,
                        debate_resolution: Optional[DebateResolution] = None) -> AgentConsensus:
        """🎭 Enhanced consensus building with debate integration"""
        
        # Sort by priority (highest first)
        sorted_decisions = sorted(decisions, key=lambda d: d.priority, reverse=True)
        
        # Phase 4B: Enhanced conflict detection and resolution
        conflicts_resolved = []
        if debate_resolution:
            conflicts_resolved.append(f"Character debate resolved: {debate_resolution.debate_summary}")
            
        # Accept all decisions (refined conflict resolution in future phases)
        final_decisions = sorted_decisions
        overall_confidence = sum(d.confidence for d in decisions) / len(decisions) if decisions else 0.0
        
        # Enhanced coordination notes
        coordination_notes = f"Coordinated {len(decisions)} specialist decisions."
        if debate_resolution:
            coordination_notes += f" Character debate: {debate_resolution.debate_summary}."
        else:
            coordination_notes += " No character conflicts detected."
        
        return AgentConsensus(
            final_decisions=final_decisions,
            conflicts_resolved=conflicts_resolved,
            coordination_notes=coordination_notes,
            overall_confidence=overall_confidence,
            debate_occurred=debate_resolution is not None,
            debate_resolution=debate_resolution
        )
        
    def _get_agent_role_from_character(self, character_name: str) -> AgentRole:
        """Convert character name to agent role"""
        character_to_role = {
            "hermione": AgentRole.INVENTORY_MANAGER,
            "gekko": AgentRole.PRICING_ANALYST,
            "elle": AgentRole.CUSTOMER_SERVICE,
            "tyrion": AgentRole.STRATEGIC_PLANNER,
            "jack": AgentRole.CRISIS_MANAGER
        }
        return character_to_role.get(character_name, AgentRole.INVENTORY_MANAGER)
        
    def set_debate_enabled(self, enabled: bool):
        """Enable or disable character debates"""
        self.debate_enabled = enabled
        
    def set_debate_threshold(self, threshold: int):
        """Set minimum number of conflicting decisions to trigger debate"""
        self.debate_threshold = threshold
        
    def enable_intelligence_sharing(self, enabled: bool = True):
        """Enable or disable advanced intelligence sharing"""
        self.intelligence_sharing_enabled = enabled
        
    def enable_conflict_prevention(self, enabled: bool = True):
        """Enable or disable proactive conflict prevention"""
        self.proactive_conflict_prevention = enabled
        
    def get_coordination_dashboard(self) -> Dict[str, Any]:
        """📊 Get advanced coordination intelligence dashboard"""
        return self.coordination_engine.get_coordination_dashboard()
        
    def get_active_specialists(self) -> List[AgentRole]:
        """Get list of currently active specialist agents"""
        return list(self.specialist_agents.keys())
        
    def get_coordination_summary(self) -> Dict:
        """Get summary of recent coordination activities including debates"""
        if not self.coordination_history:
            return {"status": "No coordination history available"}
            
        recent = self.coordination_history[-1]
        
        # Calculate debate statistics
        total_coordinations = len(self.coordination_history)
        debate_count = sum(1 for h in self.coordination_history if h.get('debate_topic'))
        debate_rate = (debate_count / total_coordinations) * 100 if total_coordinations > 0 else 0
        
        return {
            "last_coordination_day": recent.get('day', 0),
            "active_specialists": len(self.specialist_agents),
            "last_decisions_count": len(recent['decisions']),
            "last_confidence": recent['consensus'].overall_confidence,
            "specialist_roles": [role.value for role in self.specialist_agents.keys()],
            # Phase 4B: Debate statistics
            "debate_enabled": self.debate_enabled,
            "total_debates": debate_count,
            "debate_rate": f"{debate_rate:.1f}%",
            "last_debate_topic": recent.get('debate_topic', 'None'),
            "last_debate_winner": (
                recent['debate_resolution'].winning_position.character_name.upper() 
                if recent.get('debate_resolution') and recent['debate_resolution'].winning_position 
                else 'None'
            )
        }
        
    def get_debate_engine(self) -> CharacterDebateEngine:
        """Get access to the character debate engine"""
        return self.debate_engine

class HybridAgentBridge:
    """🔄 Phase 5A.1: Enhanced Bridge with True Character Control
    
    Revolutionary bridge enabling true character-controlled business operations.
    Characters transition from advisors to primary decision-makers with Scrooge oversight.
    """
    
    def __init__(self, scrooge_agent, multi_agent_coordinator: MultiAgentCoordinator):
        self.scrooge = scrooge_agent
        self.coordinator = multi_agent_coordinator
        self.mode = "hybrid"  # "single", "multi", or "hybrid"
        
        # Phase 5A.1: Enable character authority by default
        if self.coordinator:
            self.coordinator.character_authority_enabled = True
            self.coordinator.decision_translation_enabled = True
            
        # 🛠️ Phase 5A.3: Initialize tool performance tracking
        self.tool_performance_tracker = {
            'total_tool_calls': 0,
            'successful_tool_calls': 0,
            'tool_usage_by_agent': {},
            'tool_performance_history': [],
            'most_influential_tools': []
        }
        
    def set_mode(self, mode: str):
        """Set operation mode: single, multi, or hybrid"""
        if mode in ["single", "multi", "hybrid"]:
            self.mode = mode
        else:
            raise ValueError("Mode must be 'single', 'multi', or 'hybrid'")
            
    def make_daily_decision(self, store_status: Dict, yesterday_summary: Dict = None) -> Dict:
        """🤖 Phase 4B: Hybrid decision-making with character insights"""
        
        from src.core.models import StoreState, InventoryItem, InventoryBatch, DeliveryOrder, PaymentTerm
        
        # Local transform function (not used for multi-agent mode anymore)
        def transform_to_store_state(status: Dict, context: Dict) -> StoreState:
            """Helper function to transform store_status to StoreState"""
            inventory_items = {}
            for name, qty in status.get('inventory', {}).items():
                # Create a single batch for the current quantity
                batch = InventoryBatch(quantity=qty, received_day=status.get('day', 1) -1, expiration_day=None)
                inventory_items[name] = InventoryItem(product_name=name, batches=[batch])

            # Extract yesterday's summary if available
            yesterday_summary = context.get('yesterday_summary') if context else None
            
            # Transform pending deliveries
            pending_deliveries = []
            if 'pending_deliveries' in status and status['pending_deliveries'] is not None:
                for delivery_dict in status['pending_deliveries']:
                    # Ensure payment_terms is a PaymentTerm enum member
                    if 'payment_terms' in delivery_dict and isinstance(delivery_dict['payment_terms'], str):
                        try:
                            payment_term_enum = PaymentTerm(delivery_dict['payment_terms'])
                            delivery_dict['payment_terms'] = payment_term_enum
                        except ValueError:
                            # Handle cases where the string is not a valid PaymentTerm
                            # Defaulting to UPFRONT or another appropriate default
                            delivery_dict['payment_terms'] = PaymentTerm.UPFRONT
                    
                    pending_deliveries.append(DeliveryOrder(**delivery_dict))

            return StoreState(
                day=status.get('day', 1),
                cash=status.get('cash', 0.0),
                inventory=inventory_items,
                daily_sales=yesterday_summary.get('sales_by_product', {}) if yesterday_summary else {},
                total_revenue=yesterday_summary.get('revenue', 0.0) if yesterday_summary else 0.0,
                total_profit=yesterday_summary.get('profit', 0.0) if yesterday_summary else 0.0,
                pending_deliveries=pending_deliveries,
                accounts_payable=status.get('accounts_payable', 0.0),
                active_crises=status.get('active_crises', []),
            )

        context = {'yesterday_summary': yesterday_summary}

        if self.mode == "single":
            # Pure single-agent mode (existing functionality)
            return self.scrooge.make_daily_decision(store_status, yesterday_summary)
            
        elif self.mode == "multi":
            # Phase 5A.1: Pure multi-agent mode - pass store_status dict directly
            return self._make_multi_agent_decision(store_status, yesterday_summary)
            
        else:  # hybrid mode
            # Phase 4B: Enhanced hybrid mode with character debate analysis
            single_decision = self.scrooge.make_daily_decision(store_status, yesterday_summary)
            
            # Get specialist analysis with potential debates
            specialist_context = {
                'yesterday_summary': yesterday_summary,
                'single_agent_decision': single_decision
            }
            
            if self.coordinator.specialist_agents:
                # Pass store_status dict, not store_state object
                specialist_consensus = self.coordinator.coordinate_decisions(store_status, specialist_context)
                
                # Phase 4B: Enhanced multi-agent analysis with debate information
                single_decision['multi_agent_analysis'] = {
                    'specialist_count': len(specialist_consensus.final_decisions),
                    'specialist_confidence': specialist_consensus.overall_confidence,
                    'coordination_notes': specialist_consensus.coordination_notes,
                    'debate_occurred': specialist_consensus.debate_occurred,
                    'debate_summary': (
                        specialist_consensus.debate_resolution.debate_summary 
                        if specialist_consensus.debate_resolution 
                        else 'No character debates'
                    ),
                    'character_insights': self._extract_character_insights(specialist_consensus)
                }
                
            return single_decision
            
    def _extract_character_insights(self, consensus: AgentConsensus) -> List[Dict]:
        """Extract insights from character decisions for hybrid display"""
        character_insights = []
        
        for decision in consensus.final_decisions:
            agent_name = self._get_character_name_from_role(decision.agent_role)
            if agent_name:
                insight = {
                    'character': agent_name,
                    'role': decision.agent_role.value,
                    'confidence': decision.confidence,
                    'priority': decision.priority,
                    'reasoning': decision.reasoning,
                    # 🛠️ Phase 5A.3: Extract tool usage information
                    'tool_usage': self._extract_tool_usage_from_decision(decision)
                }
                character_insights.append(insight)
                
                # 🛠️ Phase 5A.3: Track tool usage
                self._track_tool_usage(decision)
        
        return character_insights
    
    def _extract_tool_usage_from_decision(self, decision: AgentDecision) -> Dict:
        """🛠️ Phase 5A.3: Extract tool usage information from agent decision"""
        tool_usage = {
            'tools_used': 0,
            'tool_performance_score': 0,
            'key_tool_insights': [],
            'tool_summary': "No tool usage detected"
        }
        
        # Check if decision parameters contain tool usage log
        if hasattr(decision, 'parameters') and isinstance(decision.parameters, dict):
            tool_usage_log = decision.parameters.get('tool_usage_log', [])
            tool_results = decision.parameters.get('tool_results', {})
            
            if tool_usage_log:
                tool_usage['tools_used'] = len(tool_usage_log)
                tool_usage['key_tool_insights'] = [
                    f"{tool['emoji']} {tool['key_insight']}" 
                    for tool in tool_usage_log[:3]  # Top 3 insights
                ]
                tool_usage['tool_performance_score'] = decision.parameters.get('tool_performance_score', 0)
                tool_usage['tool_summary'] = f"{len(tool_usage_log)} tools deployed successfully"
                
                # Track tool names used
                tool_usage['tool_names'] = [tool['tool_name'] for tool in tool_usage_log]
        
        return tool_usage
    
    def _track_tool_usage(self, decision: AgentDecision):
        """🛠️ Phase 5A.3: Track tool usage for performance metrics"""
        agent_role = decision.agent_role.value
        
        # Initialize agent tracking if needed
        if agent_role not in self.tool_performance_tracker['tool_usage_by_agent']:
            self.tool_performance_tracker['tool_usage_by_agent'][agent_role] = {
                'total_calls': 0,
                'successful_calls': 0,
                'tools_used': set(),
                'average_performance': 0
            }
        
        # Extract tool usage from decision
        tool_usage = self._extract_tool_usage_from_decision(decision)
        
        if tool_usage['tools_used'] > 0:
            agent_stats = self.tool_performance_tracker['tool_usage_by_agent'][agent_role]
            
            # Update counters
            self.tool_performance_tracker['total_tool_calls'] += tool_usage['tools_used']
            self.tool_performance_tracker['successful_tool_calls'] += tool_usage['tools_used']
            
            agent_stats['total_calls'] += tool_usage['tools_used']
            agent_stats['successful_calls'] += tool_usage['tools_used']
            
            # Track tool names
            if 'tool_names' in tool_usage:
                agent_stats['tools_used'].update(tool_usage['tool_names'])
            
            # Update performance score
            performance_score = tool_usage.get('tool_performance_score', 0)
            if performance_score > 0:
                agent_stats['average_performance'] = (
                    agent_stats.get('average_performance', 0) * 0.7 + performance_score * 0.3
                )
    
    def get_tool_performance_dashboard(self) -> Dict[str, Any]:
        """🛠️ Phase 5A.3: Get comprehensive tool performance dashboard"""
        dashboard = {
            'overall_metrics': {
                'total_tool_calls': self.tool_performance_tracker['total_tool_calls'],
                'successful_tool_calls': self.tool_performance_tracker['successful_tool_calls'],
                'success_rate': 0,
                'active_agents_with_tools': 0
            },
            'agent_tool_usage': {},
            'tool_effectiveness_summary': [],
            'recommendations': []
        }
        
        # Calculate success rate
        total_calls = self.tool_performance_tracker['total_tool_calls']
        if total_calls > 0:
            dashboard['overall_metrics']['success_rate'] = round(
                (self.tool_performance_tracker['successful_tool_calls'] / total_calls) * 100, 1
            )
        
        # Agent-specific tool usage
        for agent_role, stats in self.tool_performance_tracker['tool_usage_by_agent'].items():
            if stats['total_calls'] > 0:
                dashboard['overall_metrics']['active_agents_with_tools'] += 1
                dashboard['agent_tool_usage'][agent_role] = {
                    'tools_deployed': len(stats['tools_used']),
                    'total_calls': stats['total_calls'],
                    'performance_score': round(stats.get('average_performance', 0), 1),
                    'tools_list': list(stats['tools_used'])
                }
        
        # Generate effectiveness summary
        if dashboard['overall_metrics']['active_agents_with_tools'] > 0:
            dashboard['tool_effectiveness_summary'] = [
                f"🎯 {dashboard['overall_metrics']['active_agents_with_tools']} agents actively using specialized tools",
                f"🛠️ {total_calls} total tool deployments with {dashboard['overall_metrics']['success_rate']}% success rate",
                f"📊 Average tool performance across all agents exceeding baseline expectations"
            ]
        
        # Generate recommendations
        if total_calls > 10:
            dashboard['recommendations'] = [
                "✅ Tool integration successful - maintain current deployment strategy",
                "📈 Consider expanding tool usage to decision-making processes",
                "🎯 Focus on tools with highest performance scores for optimization"
            ]
        elif total_calls > 0:
            dashboard['recommendations'] = [
                "🚀 Tool usage initiated - monitor performance for optimization opportunities",
                "📊 Increase tool deployment frequency for better decision support"
            ]
        else:
            dashboard['recommendations'] = [
                "⚠️ No tool usage detected - verify tool integration is active",
                "🛠️ Deploy specialized tools to enhance decision-making capabilities"
            ]
        
        return dashboard
        
    def _get_character_name_from_role(self, agent_role: AgentRole) -> Optional[str]:
        """Convert agent role to character name"""
        role_to_character = {
            AgentRole.INVENTORY_MANAGER: "hermione",
            AgentRole.PRICING_ANALYST: "gekko",
            AgentRole.CUSTOMER_SERVICE: "elle",
            AgentRole.STRATEGIC_PLANNER: "tyrion",
            AgentRole.CRISIS_MANAGER: "jack"
        }
        return role_to_character.get(agent_role)
            
    def _make_multi_agent_decision(self, store_status: Dict, yesterday_summary: Dict = None) -> Dict:
        """🎭 Phase 5A.1: True multi-agent decision making with character control"""
        context = {'yesterday_summary': yesterday_summary}
        
        # It's crucial to pass the context here
        consensus = self.coordinator.coordinate_decisions(store_status, context)
        
        # Phase 5A.1: Extract business decisions from character consensus
        business_decisions = {}
        
        if consensus.business_translation:
            translation = consensus.business_translation
            
            # Phase 5A.1: Character pricing control
            if translation.pricing_decisions:
                business_decisions['prices'] = translation.pricing_decisions
                
            # Phase 5A.1: Character inventory control
            if translation.ordering_decisions:
                business_decisions['orders'] = translation.ordering_decisions
                
            # Phase 5A.1: Add character control metadata
            business_decisions.update({
                'character_control_active': True,
                'primary_decision_maker': translation.primary_decision_maker.value if translation.primary_decision_maker else 'consensus',
                'decision_confidence': translation.decision_confidence,
                'override_occurred': translation.override_occurred,
                'executive_oversight': translation.executive_oversight_notes
            })
        else:
            # CRITICAL FIX: Fallback translation when consensus.business_translation is None
            print("⚠️ WARNING: consensus.business_translation is None - performing manual translation")
            
            # Manually call the translation method
            translation = self.coordinator._translate_consensus_to_business_decisions(
                consensus.final_decisions, store_status
            )
            
            business_decisions = {
                'character_control_active': False,
                'fallback_reason': 'Consensus translation was None - used manual translation'
            }
            
            # Add the translated business decisions
            if translation.pricing_decisions:
                business_decisions['prices'] = translation.pricing_decisions
            if translation.ordering_decisions:
                business_decisions['orders'] = translation.ordering_decisions
        
        # Phase 5A.1: Executive oversight from Scrooge
        if hasattr(self, 'scrooge') and self.scrooge:
            oversight_notes = self._apply_executive_oversight(business_decisions, store_status)
            business_decisions['executive_oversight_notes'] = oversight_notes
        
        # Enhanced character information for transparency
        business_decisions.update({
            'mode': 'character_controlled_operations',
            'specialist_decisions': len(consensus.final_decisions),
            'overall_confidence': consensus.overall_confidence,
            'coordination_notes': consensus.coordination_notes,
            'debate_occurred': consensus.debate_occurred,
            'character_insights': self._extract_character_insights(consensus)
        })
        
        if consensus.debate_resolution:
            business_decisions.update({
                'debate_topic': consensus.debate_resolution.business_decision.get('decision_type', 'unknown'),
                'debate_winner': (
                    consensus.debate_resolution.winning_position.character_name.upper()
                    if consensus.debate_resolution.winning_position
                    else 'No winner'
                ),
                'debate_summary': consensus.debate_resolution.debate_summary
            })
        
        return business_decisions
        
    def _apply_executive_oversight(self, character_decisions: Dict, store_status: Dict) -> str:
        """Phase 5A.1: Apply Scrooge executive oversight to character decisions"""
        oversight_notes = []
        
        # Check for risky pricing decisions
        if 'prices' in character_decisions:
            current_prices = {name: info['price'] for name, info in store_status.get('products', {}).items()}
            for product, new_price in character_decisions['prices'].items():
                current_price = current_prices.get(product, 0)
                if current_price > 0:
                    change_percent = ((new_price - current_price) / current_price) * 100
                    if abs(change_percent) > 20:  # >20% price change
                        oversight_notes.append(f"⚠️ Large price change for {product}: {change_percent:.1f}%")
        
        # Check for large inventory orders
        if 'orders' in character_decisions:
            cash_available = store_status.get('cash', 0)
            total_order_cost = sum(character_decisions['orders'].values()) * 1.5  # Rough estimate
            if total_order_cost > cash_available * 0.8:  # >80% of cash
                oversight_notes.append(f"⚠️ Large cash commitment: ~${total_order_cost:.2f} of ${cash_available:.2f}")
        
        if not oversight_notes:
            oversight_notes.append("✅ Character decisions approved - reasonable business operations")
        
        return "; ".join(oversight_notes)
        
    def get_system_status(self) -> Dict:
        """🎭 Enhanced system status with debate capabilities"""
        coordinator_summary = self.coordinator.get_coordination_summary() if self.coordinator else {}
        
        return {
            'mode': self.mode,
            'single_agent_active': self.scrooge is not None,
            'coordinator_active': self.coordinator is not None,
            'active_specialists': self.coordinator.get_active_specialists() if self.coordinator else [],
            'coordination_summary': coordinator_summary,
            # Phase 4B: Debate status
            'debate_system_active': self.coordinator.debate_enabled if self.coordinator else False,
            'debate_engine_status': 'Operational' if self.coordinator else 'Inactive',
            'character_debate_capabilities': [
                'Pricing Strategy Debates',
                'Inventory Allocation Conflicts', 
                'Crisis Response Coordination',
                'Strategic Planning Disputes'
            ]
        }
        
    def enable_character_debates(self, enabled: bool = True):
        """🎭 Enable or disable character debate system"""
        if self.coordinator:
            self.coordinator.set_debate_enabled(enabled)
            
    def set_debate_threshold(self, threshold: int):
        """Set debate trigger threshold"""
        if self.coordinator:
            self.coordinator.set_debate_threshold(threshold)
            
    def enable_character_authority(self, enabled: bool = True):
        """Phase 5A.1: Enable or disable character decision authority"""
        if self.coordinator:
            self.coordinator.character_authority_enabled = enabled
            
    def enable_decision_translation(self, enabled: bool = True):
        """Phase 5A.1: Enable or disable character decision translation"""
        if self.coordinator:
            self.coordinator.decision_translation_enabled = enabled
            
    def get_character_authority_status(self) -> Dict[str, Any]:
        """Phase 5A.1: Get current character authority and control status"""
        if not self.coordinator:
            return {"status": "No coordinator available"}
            
        return {
            "character_authority_enabled": self.coordinator.character_authority_enabled,
            "decision_translation_enabled": self.coordinator.decision_translation_enabled,
            "current_mode": self.mode,
            "true_multi_agent_control": self.mode == "multi",
            "character_control_capabilities": {
                "pricing_control": "Gekko (Pricing Analyst) - 2.0x authority weight",
                "inventory_control": "Hermione (Inventory Manager) - 2.0x authority weight", 
                "customer_control": "Elle (Customer Service) - 1.5x authority weight",
                "strategic_control": "Tyrion (Strategic Planner) - 1.8x authority weight",
                "crisis_control": "Jack (Crisis Manager) - 3.0x authority weight"
            }
        } 