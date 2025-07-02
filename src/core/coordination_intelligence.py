from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime

from src.core.models import AgentRole, AgentDecision, StoreState


class CoordinationEventType(Enum):
    """Types of coordination events between agents"""
    INSIGHT_SHARING = "insight_sharing"
    RESOURCE_CONFLICT = "resource_conflict"
    IMPACT_PREDICTION = "impact_prediction"
    PRIORITY_ESCALATION = "priority_escalation"
    STRATEGIC_ALIGNMENT = "strategic_alignment"


class ImpactType(Enum):
    """Types of cross-domain impacts"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    CRITICAL = "critical"


@dataclass
class CrossDomainImpact:
    """Represents impact of one agent's decision on another domain"""
    source_agent: AgentRole
    target_agent: AgentRole
    impact_type: ImpactType
    impact_magnitude: float  # 0.0-1.0
    impact_description: str
    decision_parameters: Dict[str, Any]
    confidence: float


@dataclass
class AgentInsight:
    """Enhanced insight with sharing metadata"""
    agent_role: AgentRole
    insight_type: str
    content: Dict[str, Any]
    relevance_scores: Dict[AgentRole, float]  # How relevant to each other agent
    urgency: float  # 0.0-1.0
    timestamp: datetime = field(default_factory=datetime.now)
    shared_with: List[AgentRole] = field(default_factory=list)


@dataclass
class ResourceConflict:
    """Represents a resource allocation conflict"""
    competing_agents: List[AgentRole]
    resource_type: str  # "cash", "inventory", "supplier_capacity"
    total_demand: float
    available_supply: float
    conflict_severity: float  # 0.0-1.0
    resolution_strategy: Optional[str] = None


@dataclass
class CoordinationMetrics:
    """Metrics for coordination effectiveness"""
    information_sharing_rate: float
    conflict_resolution_time: float
    cross_domain_accuracy: float
    resource_utilization_efficiency: float
    strategic_alignment_score: float


class PredictiveCoordinationEngine:
    """🧠 Phase 4B.4: Advanced Predictive Coordination Intelligence
    
    Implements smart information sharing, impact prediction, and proactive coordination
    to prevent conflicts and optimize multi-agent collaboration.
    """
    
    def __init__(self):
        self.coordination_history: List[Dict] = []
        self.shared_insights: List[AgentInsight] = []
        self.active_conflicts: List[ResourceConflict] = []
        self.impact_prediction_models: Dict[str, Any] = {}
        self.coordination_patterns: Dict[str, float] = {}
        self.metrics = CoordinationMetrics(0.0, 0.0, 0.0, 0.0, 0.0)
        
    def analyze_cross_domain_impacts(self, decisions: List[AgentDecision], 
                                   store_state: StoreState) -> List[CrossDomainImpact]:
        """🔮 Predict how each agent's decisions will impact other domains"""
        impacts = []
        
        for decision in decisions:
            for other_agent in AgentRole:
                if other_agent == decision.agent_role:
                    continue
                    
                impact = self._predict_decision_impact(decision, other_agent, store_state)
                if impact.impact_magnitude > 0.1:  # Only significant impacts
                    impacts.append(impact)
                    
        return impacts
        
    def _predict_decision_impact(self, decision: AgentDecision, target_agent: AgentRole, 
                               store_state: StoreState) -> CrossDomainImpact:
        """Predict impact of one agent's decision on another agent's domain"""
        
        # Inventory → Pricing impacts
        if decision.agent_role == AgentRole.INVENTORY_MANAGER and target_agent == AgentRole.PRICING_ANALYST:
            return self._predict_inventory_to_pricing_impact(decision, store_state)
            
        # Pricing → Customer Service impacts  
        elif decision.agent_role == AgentRole.PRICING_ANALYST and target_agent == AgentRole.CUSTOMER_SERVICE:
            return self._predict_pricing_to_customer_impact(decision, store_state)
            
        # Crisis → All other agents impacts
        elif decision.agent_role == AgentRole.CRISIS_MANAGER:
            return self._predict_crisis_to_domain_impact(decision, target_agent, store_state)
            
        # Strategic → All other agents impacts
        elif decision.agent_role == AgentRole.STRATEGIC_PLANNER:
            return self._predict_strategic_to_domain_impact(decision, target_agent, store_state)
            
        # Default minimal impact
        return CrossDomainImpact(
            source_agent=decision.agent_role,
            target_agent=target_agent,
            impact_type=ImpactType.NEUTRAL,
            impact_magnitude=0.05,
            impact_description="Minimal cross-domain impact",
            decision_parameters=decision.parameters,
            confidence=0.3
        )
        
    def _predict_inventory_to_pricing_impact(self, decision: AgentDecision, 
                                           store_state: StoreState) -> CrossDomainImpact:
        """Predict how inventory decisions affect pricing strategy"""
        params = decision.parameters
        
        # Stockout risk increases pricing pressure
        if "emergency_reorder" in params or decision.priority >= 7:
            return CrossDomainImpact(
                source_agent=AgentRole.INVENTORY_MANAGER,
                target_agent=AgentRole.PRICING_ANALYST,
                impact_type=ImpactType.CRITICAL,
                impact_magnitude=0.8,
                impact_description="Stockout situation requires pricing strategy adjustment",
                decision_parameters=params,
                confidence=0.9
            )
            
        # Large inventory orders affect cash flow for pricing flexibility
        elif params.get("order_value", 0) > store_state.cash * 0.3:
            return CrossDomainImpact(
                source_agent=AgentRole.INVENTORY_MANAGER,
                target_agent=AgentRole.PRICING_ANALYST,
                impact_type=ImpactType.NEGATIVE,
                impact_magnitude=0.6,
                impact_description="Large inventory investment reduces pricing flexibility",
                decision_parameters=params,
                confidence=0.7
            )
            
        return CrossDomainImpact(
            source_agent=AgentRole.INVENTORY_MANAGER,
            target_agent=AgentRole.PRICING_ANALYST,
            impact_type=ImpactType.NEUTRAL,
            impact_magnitude=0.2,
            impact_description="Standard inventory management impact",
            decision_parameters=params,
            confidence=0.5
        )
        
    def _predict_pricing_to_customer_impact(self, decision: AgentDecision, 
                                          store_state: StoreState) -> CrossDomainImpact:
        """Predict how pricing decisions affect customer experience"""
        params = decision.parameters
        
        # Aggressive price increases hurt customer satisfaction
        if "price_increase" in params and params.get("aggressive", False):
            return CrossDomainImpact(
                source_agent=AgentRole.PRICING_ANALYST,
                target_agent=AgentRole.CUSTOMER_SERVICE,
                impact_type=ImpactType.NEGATIVE,
                impact_magnitude=0.7,
                impact_description="Aggressive pricing may damage customer relationships",
                decision_parameters=params,
                confidence=0.8
            )
            
        # Competitive pricing helps customer satisfaction
        elif "competitive_pricing" in params:
            return CrossDomainImpact(
                source_agent=AgentRole.PRICING_ANALYST,
                target_agent=AgentRole.CUSTOMER_SERVICE,
                impact_type=ImpactType.POSITIVE,
                impact_magnitude=0.5,
                impact_description="Competitive pricing improves customer value perception",
                decision_parameters=params,
                confidence=0.7
            )
            
        return CrossDomainImpact(
            source_agent=AgentRole.PRICING_ANALYST,
            target_agent=AgentRole.CUSTOMER_SERVICE,
            impact_type=ImpactType.NEUTRAL,
            impact_magnitude=0.3,
            impact_description="Standard pricing impact on customer experience",
            decision_parameters=params,
            confidence=0.6
        )
        
    def _predict_crisis_to_domain_impact(self, decision: AgentDecision, target_agent: AgentRole,
                                       store_state: StoreState) -> CrossDomainImpact:
        """Predict how crisis decisions affect other domains"""
        params = decision.parameters
        
        if decision.priority >= 8:  # High severity crisis
            impact_type = ImpactType.CRITICAL
            magnitude = 0.9
            description = f"Crisis response critically affects {target_agent.value} operations"
            confidence = 0.95
        elif decision.priority >= 6:  # Medium severity crisis
            impact_type = ImpactType.NEGATIVE
            magnitude = 0.6
            description = f"Crisis response significantly impacts {target_agent.value} domain"
            confidence = 0.8
        else:
            impact_type = ImpactType.NEUTRAL
            magnitude = 0.3
            description = f"Minor crisis impact on {target_agent.value} operations"
            confidence = 0.6
            
        return CrossDomainImpact(
            source_agent=AgentRole.CRISIS_MANAGER,
            target_agent=target_agent,
            impact_type=impact_type,
            impact_magnitude=magnitude,
            impact_description=description,
            decision_parameters=params,
            confidence=confidence
        )
        
    def _predict_strategic_to_domain_impact(self, decision: AgentDecision, target_agent: AgentRole,
                                          store_state: StoreState) -> CrossDomainImpact:
        """Predict how strategic decisions affect operational domains"""
        params = decision.parameters
        
        # Strategic resource allocation affects all domains
        if "resource_allocation" in params:
            return CrossDomainImpact(
                source_agent=AgentRole.STRATEGIC_PLANNER,
                target_agent=target_agent,
                impact_type=ImpactType.POSITIVE,
                impact_magnitude=0.6,
                impact_description=f"Strategic resource allocation benefits {target_agent.value}",
                decision_parameters=params,
                confidence=0.7
            )
            
        return CrossDomainImpact(
            source_agent=AgentRole.STRATEGIC_PLANNER,
            target_agent=target_agent,
            impact_type=ImpactType.NEUTRAL,
            impact_magnitude=0.4,
            impact_description=f"Strategic decision affects {target_agent.value} planning",
            decision_parameters=params,
            confidence=0.6
        )
        
    def generate_proactive_insights(self, decisions: List[AgentDecision], 
                                  store_state: StoreState) -> List[AgentInsight]:
        """🚀 Generate insights that should be proactively shared between agents"""
        insights = []
        
        # Analyze each decision for shareable insights
        for decision in decisions:
            insight = self._extract_shareable_insight(decision, store_state)
            if insight:
                # Calculate relevance to other agents
                insight.relevance_scores = self._calculate_insight_relevance(insight, decisions)
                insights.append(insight)
                
        return insights
        
    def _extract_shareable_insight(self, decision: AgentDecision, 
                                 store_state: StoreState) -> Optional[AgentInsight]:
        """Extract insights from a decision that other agents should know about"""
        
        # High priority decisions are always worth sharing
        if decision.priority >= 7:
            return AgentInsight(
                agent_role=decision.agent_role,
                insight_type="high_priority_alert",
                content={
                    "decision_type": decision.decision_type,
                    "priority": decision.priority,
                    "reasoning": decision.reasoning,
                    "parameters": decision.parameters
                },
                relevance_scores={},
                urgency=decision.priority / 10.0
            )
            
        # Crisis-related decisions
        if decision.agent_role == AgentRole.CRISIS_MANAGER:
            return AgentInsight(
                agent_role=decision.agent_role,
                insight_type="crisis_intelligence",
                content={
                    "crisis_level": decision.priority,
                    "response_strategy": decision.parameters.get("strategy", "unknown"),
                    "affected_domains": decision.parameters.get("affected_domains", []),
                    "timeline": decision.parameters.get("timeline", "immediate")
                },
                relevance_scores={},
                urgency=0.8
            )
            
        # Strategic insights affect long-term planning
        elif decision.agent_role == AgentRole.STRATEGIC_PLANNER and decision.priority >= 5:
            return AgentInsight(
                agent_role=decision.agent_role,
                insight_type="strategic_intelligence",
                content={
                    "strategic_focus": decision.parameters.get("focus_area", "general"),
                    "resource_implications": decision.parameters.get("resources", {}),
                    "timeline": decision.parameters.get("planning_horizon", "medium_term"),
                    "expected_outcomes": decision.parameters.get("outcomes", [])
                },
                relevance_scores={},
                urgency=0.6
            )
            
        return None
        
    def _calculate_insight_relevance(self, insight: AgentInsight, 
                                   all_decisions: List[AgentDecision]) -> Dict[AgentRole, float]:
        """Calculate how relevant an insight is to each other agent"""
        relevance = {}
        
        for agent_role in AgentRole:
            if agent_role == insight.agent_role:
                continue
                
            # Base relevance on agent relationships and insight type
            if insight.insight_type == "high_priority_alert":
                relevance[agent_role] = 0.8  # High priority affects everyone
            elif insight.insight_type == "crisis_intelligence":
                # Crisis affects all agents differently
                if agent_role == AgentRole.STRATEGIC_PLANNER:
                    relevance[agent_role] = 0.9  # Strategic needs crisis intel
                elif agent_role == AgentRole.INVENTORY_MANAGER:
                    relevance[agent_role] = 0.7  # Inventory affected by crisis
                else:
                    relevance[agent_role] = 0.6
            elif insight.insight_type == "strategic_intelligence":
                # Strategic insights most relevant to operational agents
                if agent_role in [AgentRole.INVENTORY_MANAGER, AgentRole.PRICING_ANALYST]:
                    relevance[agent_role] = 0.8
                else:
                    relevance[agent_role] = 0.5
            else:
                relevance[agent_role] = 0.3  # Default low relevance
                
        return relevance
        
    def detect_resource_conflicts(self, decisions: List[AgentDecision], 
                                store_state: StoreState) -> List[ResourceConflict]:
        """🔍 Proactively detect potential resource allocation conflicts"""
        conflicts = []
        
        # Cash flow conflicts
        cash_conflict = self._detect_cash_conflicts(decisions, store_state)
        if cash_conflict:
            conflicts.append(cash_conflict)
            
        # Supplier capacity conflicts
        supplier_conflicts = self._detect_supplier_conflicts(decisions, store_state)
        conflicts.extend(supplier_conflicts)
        
        # Priority conflicts (multiple high-priority competing demands)
        priority_conflict = self._detect_priority_conflicts(decisions)
        if priority_conflict:
            conflicts.append(priority_conflict)
            
        return conflicts
        
    def _detect_cash_conflicts(self, decisions: List[AgentDecision], 
                             store_state: StoreState) -> Optional[ResourceConflict]:
        """Detect when multiple agents want to spend more cash than available"""
        total_cash_demand = 0
        demanding_agents = []
        
        for decision in decisions:
            cash_need = decision.parameters.get("cash_required", 0)
            if cash_need > 0:
                total_cash_demand += cash_need
                demanding_agents.append(decision.agent_role)
                
        if total_cash_demand > store_state.cash and len(demanding_agents) > 1:
            return ResourceConflict(
                competing_agents=demanding_agents,
                resource_type="cash",
                total_demand=total_cash_demand,
                available_supply=store_state.cash,
                conflict_severity=(total_cash_demand - store_state.cash) / store_state.cash
            )
            
        return None
        
    def _detect_supplier_conflicts(self, decisions: List[AgentDecision], 
                                 store_state: StoreState) -> List[ResourceConflict]:
        """Detect when multiple agents compete for supplier capacity"""
        supplier_demand = {}
        conflicts = []
        
        for decision in decisions:
            supplier_orders = decision.parameters.get("supplier_orders", {})
            for supplier, demand in supplier_orders.items():
                if supplier not in supplier_demand:
                    supplier_demand[supplier] = {"total": 0, "agents": []}
                supplier_demand[supplier]["total"] += demand
                supplier_demand[supplier]["agents"].append(decision.agent_role)
                
        # Check if any supplier is over-demanded (simplified check)
        for supplier, data in supplier_demand.items():
            if data["total"] > 1000 and len(data["agents"]) > 1:  # Arbitrary threshold
                conflicts.append(ResourceConflict(
                    competing_agents=data["agents"],
                    resource_type=f"supplier_capacity_{supplier}",
                    total_demand=data["total"],
                    available_supply=1000,  # Simplified
                    conflict_severity=min((data["total"] - 1000) / 1000, 1.0)
                ))
                
        return conflicts
        
    def _detect_priority_conflicts(self, decisions: List[AgentDecision]) -> Optional[ResourceConflict]:
        """Detect when multiple agents have competing high-priority demands"""
        high_priority_agents = []
        
        for decision in decisions:
            if decision.priority >= 8:  # Very high priority
                high_priority_agents.append(decision.agent_role)
                
        if len(high_priority_agents) > 2:  # Multiple agents with critical priorities
            return ResourceConflict(
                competing_agents=high_priority_agents,
                resource_type="executive_attention",
                total_demand=len(high_priority_agents),
                available_supply=2,  # Can only handle 2 critical issues at once
                conflict_severity=0.8
            )
            
        return None
        
    def optimize_coordination_sequence(self, decisions: List[AgentDecision], 
                                     impacts: List[CrossDomainImpact]) -> List[AgentDecision]:
        """🎯 Optimize the sequence of agent decisions to minimize conflicts and maximize synergies"""
        
        # Sort decisions by dependency and impact
        dependency_graph = self._build_dependency_graph(decisions, impacts)
        optimized_sequence = self._topological_sort_decisions(decisions, dependency_graph)
        
        return optimized_sequence
        
    def _build_dependency_graph(self, decisions: List[AgentDecision], 
                              impacts: List[CrossDomainImpact]) -> Dict[AgentRole, List[AgentRole]]:
        """Build dependency graph showing which agents should go before others"""
        dependencies = {role: [] for role in AgentRole}
        
        for impact in impacts:
            if impact.impact_magnitude > 0.6:  # Significant impact
                # Source agent should execute before target agent if impact is critical
                if impact.impact_type in [ImpactType.CRITICAL, ImpactType.NEGATIVE]:
                    dependencies[impact.target_agent].append(impact.source_agent)
                    
        return dependencies
        
    def _topological_sort_decisions(self, decisions: List[AgentDecision], 
                                   dependencies: Dict[AgentRole, List[AgentRole]]) -> List[AgentDecision]:
        """Sort decisions based on dependencies (simplified topological sort)"""
        
        # Create decision lookup
        decision_map = {decision.agent_role: decision for decision in decisions}
        
        # Sort by priority first, then apply dependency ordering
        sorted_decisions = sorted(decisions, key=lambda d: d.priority, reverse=True)
        
        # Apply basic dependency reordering (simplified)
        optimized = []
        remaining = sorted_decisions.copy()
        
        while remaining:
            # Find decisions with no unmet dependencies
            ready = []
            for decision in remaining:
                deps = dependencies.get(decision.agent_role, [])
                unmet_deps = [dep for dep in deps if dep in [d.agent_role for d in remaining]]
                if not unmet_deps:
                    ready.append(decision)
                    
            if not ready:  # Circular dependency or other issue, just take highest priority
                ready = [max(remaining, key=lambda d: d.priority)]
                
            # Add ready decisions to optimized sequence
            for decision in ready:
                optimized.append(decision)
                remaining.remove(decision)
                
        return optimized
        
    def update_coordination_metrics(self, coordination_session: Dict):
        """📊 Update coordination effectiveness metrics"""
        
        # Update information sharing rate
        insights_shared = len(coordination_session.get("shared_insights", []))
        total_decisions = len(coordination_session.get("decisions", []))
        if total_decisions > 0:
            sharing_rate = insights_shared / total_decisions
            self.metrics.information_sharing_rate = (self.metrics.information_sharing_rate * 0.8 + 
                                                    sharing_rate * 0.2)
            
        # Update conflict resolution time (simplified)
        conflicts_resolved = len(coordination_session.get("resolved_conflicts", []))
        if conflicts_resolved > 0:
            avg_resolution_time = coordination_session.get("resolution_time", 1.0)
            self.metrics.conflict_resolution_time = (self.metrics.conflict_resolution_time * 0.8 + 
                                                    avg_resolution_time * 0.2)
            
        # Update strategic alignment score
        alignment_score = coordination_session.get("alignment_score", 0.5)
        self.metrics.strategic_alignment_score = (self.metrics.strategic_alignment_score * 0.8 + 
                                                 alignment_score * 0.2)
                                                 
    def get_coordination_dashboard(self) -> Dict[str, Any]:
        """📊 Generate coordination intelligence dashboard"""
        return {
            "metrics": {
                "information_sharing_rate": round(self.metrics.information_sharing_rate, 3),
                "conflict_resolution_time": round(self.metrics.conflict_resolution_time, 3),
                "strategic_alignment_score": round(self.metrics.strategic_alignment_score, 3),
                "active_conflicts": len(self.active_conflicts)
            },
            "active_insights": len(self.shared_insights),
            "coordination_patterns": self.coordination_patterns,
            "recent_conflicts": [
                {
                    "type": conflict.resource_type,
                    "severity": round(conflict.conflict_severity, 3),
                    "agents": [agent.value for agent in conflict.competing_agents]
                }
                for conflict in self.active_conflicts[-3:]  # Last 3 conflicts
            ],
            "coordination_recommendations": self._generate_coordination_recommendations()
        }
        
    def _generate_coordination_recommendations(self) -> List[str]:
        """Generate actionable coordination improvement recommendations"""
        recommendations = []
        
        if self.metrics.information_sharing_rate < 0.5:
            recommendations.append("Increase proactive insight sharing between agents")
            
        if self.metrics.conflict_resolution_time > 2.0:
            recommendations.append("Implement faster conflict resolution protocols")
            
        if len(self.active_conflicts) > 2:
            recommendations.append("Focus on preventing resource conflicts through better planning")
            
        if self.metrics.strategic_alignment_score < 0.6:
            recommendations.append("Improve strategic coordination between long-term and operational planning")
            
        return recommendations if recommendations else ["Coordination system operating optimally"] 