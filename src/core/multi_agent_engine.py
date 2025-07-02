from typing import Dict, List, Any, Optional
from enum import Enum
import json
from dataclasses import dataclass
from openai import OpenAI
from anthropic import Anthropic
import os
from dotenv import load_dotenv

# Phase 4B: Import the new character debate engine
from src.core.character_debate_engine import CharacterDebateEngine, DebateTopicType, DebateResolution

load_dotenv()

class AgentRole(Enum):
    """Specialist agent roles for business management"""
    INVENTORY_MANAGER = "inventory_manager"
    PRICING_ANALYST = "pricing_analyst" 
    CUSTOMER_SERVICE = "customer_service"
    STRATEGIC_PLANNER = "strategic_planner"
    CRISIS_MANAGER = "crisis_manager"

@dataclass
class AgentDecision:
    """Represents a decision made by a specialist agent"""
    agent_role: AgentRole
    decision_type: str
    parameters: Dict[str, Any]
    confidence: float
    reasoning: str
    priority: int  # 1-10, higher = more urgent

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

class BaseSpecialistAgent:
    """Base class for all specialist agents"""
    
    def __init__(self, role: AgentRole, provider: str = "openai"):
        self.role = role
        self.provider = provider
        if provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-4.1-mini"
        else:
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = "claude-3-sonnet-20240229"
            
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
    """🤖 Phase 4B: Enhanced Multi-Agent Coordination System with Character Debates
    
    Coordinates specialist agents with sophisticated debate and consensus building.
    Features revolutionary character interaction dynamics and conflict resolution.
    """
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self.specialist_agents: Dict[AgentRole, BaseSpecialistAgent] = {}
        self.coordination_history = []
        
        # Phase 4B: Initialize character debate engine
        self.debate_engine = CharacterDebateEngine(provider)
        self.debate_enabled = True
        self.debate_threshold = 2  # Minimum conflicting decisions to trigger debate
        
    def register_specialist(self, agent: BaseSpecialistAgent):
        """Register a specialist agent with the coordinator"""
        self.specialist_agents[agent.role] = agent
        
    def coordinate_decisions(self, store_status: Dict, context: Dict) -> AgentConsensus:
        """🎭 Phase 4B: Coordinate decisions with character debates when conflicts arise"""
        
        # Gather decisions from all specialists
        agent_decisions = []
        for role, agent in self.specialist_agents.items():
            try:
                decision = agent.analyze_situation(store_status, context)
                agent_decisions.append(decision)
            except Exception as e:
                print(f"Warning: {role.value} agent failed: {e}")
                
        # Phase 4B: Check if situation should trigger character debate
        debate_topic = None
        debate_resolution = None
        
        if self.debate_enabled and len(agent_decisions) >= self.debate_threshold:
            debate_topic = self.debate_engine.should_trigger_debate(agent_decisions, store_status)
            
            if debate_topic:
                print(f"\n🎭 DEBATE TRIGGERED: {debate_topic.value.upper()}")
                try:
                    debate_resolution = self.debate_engine.initiate_debate(
                        debate_topic, store_status, context, agent_decisions
                    )
                    
                    # Apply debate outcome to agent decisions
                    agent_decisions = self._apply_debate_outcome(agent_decisions, debate_resolution)
                    
                except Exception as e:
                    print(f"Warning: Character debate failed: {e}")
                    debate_resolution = None
        
        # Build consensus (enhanced with debate results)
        consensus = self._build_consensus(agent_decisions, store_status, context, debate_resolution)
        
        # Store coordination history
        self.coordination_history.append({
            'day': store_status.get('day', 0),
            'decisions': agent_decisions,
            'consensus': consensus,
            'context': context,
            'debate_topic': debate_topic.value if debate_topic else None,
            'debate_resolution': debate_resolution
        })
        
        return consensus
        
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
    """🔄 Phase 4B: Enhanced Bridge with Character Debate Integration
    
    Seamlessly integrates character debates with existing single-agent functionality.
    Provides smooth transition between tactical and strategic decision-making modes.
    """
    
    def __init__(self, scrooge_agent, multi_agent_coordinator: MultiAgentCoordinator):
        self.scrooge = scrooge_agent
        self.coordinator = multi_agent_coordinator
        self.mode = "hybrid"  # "single", "multi", or "hybrid"
        
    def set_mode(self, mode: str):
        """Set operation mode: single, multi, or hybrid"""
        if mode in ["single", "multi", "hybrid"]:
            self.mode = mode
        else:
            raise ValueError("Mode must be 'single', 'multi', or 'hybrid'")
            
    def make_daily_decision(self, store_status: Dict, yesterday_summary: Dict = None) -> Dict:
        """🎭 Enhanced daily decisions with character debate integration"""
        
        if self.mode == "single":
            # Pure single-agent mode (existing functionality)
            return self.scrooge.make_daily_decision(store_status, yesterday_summary)
            
        elif self.mode == "multi":
            # Phase 4B: Pure multi-agent mode with character debates
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
        """Extract character insights from specialist consensus"""
        insights = []
        
        for decision in consensus.final_decisions:
            character_name = self._get_character_name_from_role(decision.agent_role)
            insights.append({
                'character': character_name.upper() if character_name else 'UNKNOWN',
                'expertise': decision.agent_role.value,
                'priority': decision.priority,
                'confidence': decision.confidence,
                'reasoning': decision.reasoning[:100] + "..." if len(decision.reasoning) > 100 else decision.reasoning
            })
            
        return insights
        
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
        """🎭 Phase 4B: Multi-agent decision making with character debates"""
        context = {'yesterday_summary': yesterday_summary}
        consensus = self.coordinator.coordinate_decisions(store_status, context)
        
        # Phase 4B: Enhanced multi-agent decision format
        decision_result = {
            'status': 'Multi-agent decision making with character debates active',
            'mode': 'character_ensemble',
            'specialist_decisions': len(consensus.final_decisions),
            'overall_confidence': consensus.overall_confidence,
            'coordination_notes': consensus.coordination_notes,
            'debate_occurred': consensus.debate_occurred
        }
        
        if consensus.debate_resolution:
            decision_result.update({
                'debate_topic': consensus.debate_resolution.business_decision['decision_type'],
                'debate_winner': (
                    consensus.debate_resolution.winning_position.character_name.upper()
                    if consensus.debate_resolution.winning_position
                    else 'No winner'
                ),
                'debate_summary': consensus.debate_resolution.debate_summary,
                'business_decision': consensus.debate_resolution.business_decision
            })
            
        # Character insights
        decision_result['character_insights'] = self._extract_character_insights(consensus)
        
        return decision_result
        
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