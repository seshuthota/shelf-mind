from typing import Dict, List, Any, Optional
from enum import Enum
import json
from dataclasses import dataclass
from openai import OpenAI
from anthropic import Anthropic
import os
from dotenv import load_dotenv

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

class BaseSpecialistAgent:
    """Base class for all specialist agents"""
    
    def __init__(self, role: AgentRole, provider: str = "openai"):
        self.role = role
        self.provider = provider
        if provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-4o"
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
    """🤖 Phase 4A: Multi-Agent Coordination System
    
    Coordinates specialist agents while preserving single-agent compatibility.
    Gradual transition from monolithic Scrooge to coordinated specialists.
    """
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self.specialist_agents: Dict[AgentRole, BaseSpecialistAgent] = {}
        self.coordination_history = []
        
        # Phase 4A.1: Start with coordination system only
        # Specialist agents will be added incrementally
        
    def register_specialist(self, agent: BaseSpecialistAgent):
        """Register a specialist agent with the coordinator"""
        self.specialist_agents[agent.role] = agent
        
    def coordinate_decisions(self, store_status: Dict, context: Dict) -> AgentConsensus:
        """Coordinate decisions between all active specialist agents"""
        
        # Gather decisions from all specialists
        agent_decisions = []
        for role, agent in self.specialist_agents.items():
            try:
                decision = agent.analyze_situation(store_status, context)
                agent_decisions.append(decision)
            except Exception as e:
                print(f"Warning: {role.value} agent failed: {e}")
                
        # Resolve conflicts and build consensus
        consensus = self._build_consensus(agent_decisions, store_status, context)
        
        # Store coordination history
        self.coordination_history.append({
            'day': store_status.get('day', 0),
            'decisions': agent_decisions,
            'consensus': consensus,
            'context': context
        })
        
        return consensus
        
    def _build_consensus(self, decisions: List[AgentDecision], store_status: Dict, context: Dict) -> AgentConsensus:
        """Build consensus from multiple agent decisions"""
        
        # Phase 4A.1: Simple consensus - no conflicts yet with single agents
        # Future: Implement sophisticated conflict resolution
        
        # Sort by priority (highest first)
        sorted_decisions = sorted(decisions, key=lambda d: d.priority, reverse=True)
        
        # For now, accept all decisions (no conflicts in Phase 4A.1)
        final_decisions = sorted_decisions
        conflicts_resolved = []
        overall_confidence = sum(d.confidence for d in decisions) / len(decisions) if decisions else 0.0
        
        coordination_notes = f"Coordinated {len(decisions)} specialist decisions. Phase 4A.1: Simple coordination active."
        
        return AgentConsensus(
            final_decisions=final_decisions,
            conflicts_resolved=conflicts_resolved,
            coordination_notes=coordination_notes,
            overall_confidence=overall_confidence
        )
        
    def get_active_specialists(self) -> List[AgentRole]:
        """Get list of currently active specialist agents"""
        return list(self.specialist_agents.keys())
        
    def get_coordination_summary(self) -> Dict:
        """Get summary of recent coordination activities"""
        if not self.coordination_history:
            return {"status": "No coordination history available"}
            
        recent = self.coordination_history[-1]
        return {
            "last_coordination_day": recent.get('day', 0),
            "active_specialists": len(self.specialist_agents),
            "last_decisions_count": len(recent['decisions']),
            "last_confidence": recent['consensus'].overall_confidence,
            "specialist_roles": [role.value for role in self.specialist_agents.keys()]
        }

class HybridAgentBridge:
    """🔄 Phase 4A: Bridge between single Scrooge agent and multi-agent system
    
    Allows gradual transition while preserving all existing functionality.
    Can operate in single-agent mode OR multi-agent mode.
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
        """Make daily decisions using current mode"""
        
        if self.mode == "single":
            # Pure single-agent mode (existing functionality)
            return self.scrooge.make_daily_decision(store_status, yesterday_summary)
            
        elif self.mode == "multi":
            # Pure multi-agent mode (Phase 4B+)
            return self._make_multi_agent_decision(store_status, yesterday_summary)
            
        else:  # hybrid mode
            # Phase 4A: Hybrid mode - use single agent but analyze with specialists
            single_decision = self.scrooge.make_daily_decision(store_status, yesterday_summary)
            
            # Get specialist analysis for comparison (no interference)
            specialist_context = {
                'yesterday_summary': yesterday_summary,
                'single_agent_decision': single_decision
            }
            
            if self.coordinator.specialist_agents:
                specialist_consensus = self.coordinator.coordinate_decisions(store_status, specialist_context)
                
                # Phase 4A.1: Just observe specialists, don't override Scrooge yet
                single_decision['multi_agent_analysis'] = {
                    'specialist_count': len(specialist_consensus.final_decisions),
                    'specialist_confidence': specialist_consensus.overall_confidence,
                    'coordination_notes': specialist_consensus.coordination_notes
                }
                
            return single_decision
            
    def _make_multi_agent_decision(self, store_status: Dict, yesterday_summary: Dict = None) -> Dict:
        """Make decision using pure multi-agent system (Phase 4B+)"""
        context = {'yesterday_summary': yesterday_summary}
        consensus = self.coordinator.coordinate_decisions(store_status, context)
        
        # Convert specialist decisions to single decision format
        # This will be implemented in Phase 4B
        return {
            'status': 'Multi-agent decision making active',
            'specialist_decisions': len(consensus.final_decisions),
            'confidence': consensus.overall_confidence
        }
        
    def get_system_status(self) -> Dict:
        """Get current system operational status"""
        return {
            'mode': self.mode,
            'single_agent_active': self.scrooge is not None,
            'coordinator_active': self.coordinator is not None,
            'active_specialists': self.coordinator.get_active_specialists() if self.coordinator else [],
            'coordination_summary': self.coordinator.get_coordination_summary() if self.coordinator else {}
        } 