"""
🧪 PHASE 5A.1 TEST: True Multi-Agent Decision Making (No AI Dependencies)
Tests the decision translation and character authority system without requiring API keys
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.multi_agent_engine import (
    MultiAgentCoordinator, 
    HybridAgentBridge, 
    CHARACTER_AUTHORITY_MATRIX,
    CharacterDecisionTranslation
)
from src.core.models import AgentRole, AgentDecision
from dataclasses import dataclass
from typing import Dict, List

# Mock store status for testing
MOCK_STORE_STATUS = {
    'day': 1,
    'cash': 100.0,
    'inventory': {'Chips': 5, 'Coke': 3, 'Candy': 8, 'Water': 2, 'Sandwiches': 6},
    'products': {
        'Chips': {'price': 1.95, 'cost': 1.0},
        'Coke': {'price': 2.50, 'cost': 1.2},
        'Candy': {'price': 1.25, 'cost': 0.8},
        'Water': {'price': 1.80, 'cost': 0.9},
        'Sandwiches': {'price': 4.50, 'cost': 2.5}
    }
}

class MockSpecialistAgent:
    """Mock agent for testing without AI dependencies"""
    
    def __init__(self, role: AgentRole, mock_decisions: List[AgentDecision]):
        self.role = role
        self.mock_decisions = mock_decisions
        
    def analyze_situation(self, store_status: Dict, context: Dict) -> AgentDecision:
        # Return first available mock decision for this agent
        for decision in self.mock_decisions:
            if decision.agent_role == self.role:
                return decision
        
        # Fallback decision
        return AgentDecision(
            agent_role=self.role,
            decision_type=f"mock_{self.role.value}_decision",
            parameters={"mock": True},
            reasoning=f"Mock {self.role.value} analysis",
            priority=5,
            confidence=0.8
        )

def create_mock_character_decisions() -> List[AgentDecision]:
    """Create realistic mock character decisions for testing"""
    
    return [
        AgentDecision(
            agent_role=AgentRole.PRICING_ANALYST,
            decision_type="pricing_adjustment",
            parameters={"target_products": ["Chips", "Candy"], "pricing_strategy": "aggressive"},
            reasoning="Gekko's pricing analysis: Reduce Chips to $1.87 to undercut competitor. Increase Candy to $1.30 for better margins. Market warfare requires aggressive moves!",
            priority=8,
            confidence=0.9
        ),
        AgentDecision(
            agent_role=AgentRole.INVENTORY_MANAGER,
            decision_type="inventory_restock",
            parameters={"products_to_order": {"Water": 8, "Coke": 6}},
            reasoning="Hermione's inventory analysis: Water is critically low at 2 units - order 8 units immediately. Coke needs restock, order 6 units. Mathematics demand action!",
            priority=7,
            confidence=0.95
        ),
        AgentDecision(
            agent_role=AgentRole.CUSTOMER_SERVICE,
            decision_type="service_optimization",
            parameters={"focus_areas": ["availability", "satisfaction"]},
            reasoning="Elle's customer analysis: Current pricing seems reasonable for customer satisfaction. Focus on maintaining good service levels and avoiding stockouts.",
            priority=6,
            confidence=0.85
        ),
        AgentDecision(
            agent_role=AgentRole.STRATEGIC_PLANNER,
            decision_type="strategic_planning",
            parameters={"investment_areas": ["inventory", "competitive_positioning"]},
            reasoning="Tyrion's strategic analysis: The current cash position is strong. We can afford strategic inventory investments while maintaining competitive pricing.",
            priority=6,
            confidence=0.8
        ),
        AgentDecision(
            agent_role=AgentRole.CRISIS_MANAGER,
            decision_type="emergency_response",
            parameters={"crisis_level": "DEFCON_3", "immediate_actions": ["restock_water"]},
            reasoning="Jack's crisis assessment: Water stockout imminent! This is DEFCON 3 situation. Emergency restock required - order Water immediately!",
            priority=9,
            confidence=0.85
        )
    ]

def test_character_authority_matrix():
    """Test the character authority matrix"""
    print("🧪 Testing Character Authority Matrix...")
    
    # Test authority weights
    gekko_authority = CHARACTER_AUTHORITY_MATRIX[AgentRole.PRICING_ANALYST]
    assert gekko_authority["decision_weight"] == 2.0, "Gekko should have 2.0x pricing authority"
    assert "pricing" in gekko_authority["primary_domains"], "Gekko should control pricing"
    
    hermione_authority = CHARACTER_AUTHORITY_MATRIX[AgentRole.INVENTORY_MANAGER]
    assert hermione_authority["decision_weight"] == 2.0, "Hermione should have 2.0x inventory authority"
    assert "inventory" in hermione_authority["primary_domains"], "Hermione should control inventory"
    
    jack_authority = CHARACTER_AUTHORITY_MATRIX[AgentRole.CRISIS_MANAGER]
    assert jack_authority["decision_weight"] == 3.0, "Jack should have 3.0x crisis authority"
    assert jack_authority["override_threshold"] == 9, "Jack should have high override threshold"
    
    print("✅ Character Authority Matrix tests passed!")

def test_decision_translation():
    """Test character decision translation to business actions"""
    print("\n🧪 Testing Decision Translation...")
    
    # Create coordinator with mock decisions
    coordinator = MultiAgentCoordinator(provider="mock")
    mock_decisions = create_mock_character_decisions()
    
    # Test decision translation
    translation = coordinator._translate_consensus_to_business_decisions(
        mock_decisions, MOCK_STORE_STATUS
    )
    
    # Verify translation was created
    assert isinstance(translation, CharacterDecisionTranslation), "Translation should be CharacterDecisionTranslation"
    assert translation.primary_decision_maker is not None, "Should have identified primary decision maker"
    assert translation.decision_confidence > 0, "Should have calculated confidence"
    
    print(f"✅ Primary Decision Maker: {translation.primary_decision_maker.value}")
    print(f"✅ Decision Confidence: {translation.decision_confidence:.2f}")
    print(f"✅ Pricing Decisions: {translation.pricing_decisions}")
    print(f"✅ Ordering Decisions: {translation.ordering_decisions}")

def test_pricing_extraction():
    """Test extraction of pricing decisions from character reasoning"""
    print("\n🧪 Testing Pricing Extraction...")
    
    coordinator = MultiAgentCoordinator(provider="mock")
    
    # Test pricing extraction
    reasoning = "Reduce Chips to $1.87 to undercut competitor. Increase Candy to $1.30 for better margins."
    current_prices = {'Chips': 1.95, 'Candy': 1.25}
    
    pricing_suggestions = coordinator._extract_pricing_from_reasoning(reasoning, current_prices)
    
    print(f"✅ Extracted pricing suggestions: {pricing_suggestions}")
    
    # Test percentage-based adjustments
    reasoning2 = "Increase chips pricing for better margins. Decrease candy prices to boost sales."
    pricing_suggestions2 = coordinator._extract_pricing_from_reasoning(reasoning2, current_prices)
    
    print(f"✅ Extracted percentage adjustments: {pricing_suggestions2}")

def test_ordering_extraction():
    """Test extraction of ordering decisions from character reasoning"""
    print("\n🧪 Testing Ordering Extraction...")
    
    coordinator = MultiAgentCoordinator(provider="mock")
    
    # Test ordering extraction
    reasoning = "Water is critically low at 2 units - order 8 units immediately. Coke needs restock, order 6 units."
    current_inventory = {'Water': 2, 'Coke': 3, 'Chips': 5}
    
    ordering_suggestions = coordinator._extract_ordering_from_reasoning(reasoning, current_inventory)
    
    print(f"✅ Extracted ordering suggestions: {ordering_suggestions}")
    
    # Test stockout detection
    reasoning2 = "Chips stockout imminent! Emergency restock required."
    ordering_suggestions2 = coordinator._extract_ordering_from_reasoning(reasoning2, current_inventory)
    
    print(f"✅ Extracted stockout orders: {ordering_suggestions2}")

def test_multi_agent_decision_format():
    """Test the new multi-agent decision format with character control"""
    print("\n🧪 Testing Multi-Agent Decision Format...")
    
    # Create coordinator with mock agents
    coordinator = MultiAgentCoordinator(provider="mock")
    mock_decisions = create_mock_character_decisions()
    
    # Register mock agents
    for decision in mock_decisions:
        coordinator.register_specialist(MockSpecialistAgent(decision.agent_role, mock_decisions))
    
    # Create hybrid bridge
    class MockScroogeAgent:
        def make_daily_decision(self, store_status, yesterday_summary=None):
            return {"prices": {}, "orders": {}}
    
    scrooge = MockScroogeAgent()
    bridge = HybridAgentBridge(scrooge, coordinator)
    
    # Test character authority status
    authority_status = bridge.get_character_authority_status()
    assert authority_status["character_authority_enabled"], "Character authority should be enabled"
    assert authority_status["decision_translation_enabled"], "Decision translation should be enabled"
    
    print("✅ Character authority enabled by default")
    print(f"✅ Control capabilities: {len(authority_status['character_control_capabilities'])} types")
    
    # Test mode switching
    bridge.set_mode("multi")
    assert bridge.mode == "multi", "Should switch to multi mode"
    
    print("✅ Mode switching works correctly")

def test_executive_oversight():
    """Test executive oversight functionality"""
    print("\n🧪 Testing Executive Oversight...")
    
    class MockScroogeAgent:
        pass
    
    coordinator = MultiAgentCoordinator(provider="mock")
    scrooge = MockScroogeAgent()
    bridge = HybridAgentBridge(scrooge, coordinator)
    
    # Test oversight with risky pricing
    risky_decisions = {
        'prices': {'Chips': 0.50},  # Very low price
        'character_control_active': True
    }
    
    oversight = bridge._apply_executive_oversight(risky_decisions, MOCK_STORE_STATUS)
    assert "Large price change" in oversight, "Should detect large price changes"
    
    print(f"✅ Oversight detected risky pricing: {oversight}")
    
    # Test oversight with large orders
    large_orders = {
        'orders': {'Chips': 50, 'Coke': 30},  # Large orders
        'character_control_active': True
    }
    
    oversight2 = bridge._apply_executive_oversight(large_orders, MOCK_STORE_STATUS)
    assert "Large cash commitment" in oversight2, "Should detect large cash commitments"
    
    print(f"✅ Oversight detected large orders: {oversight2}")
    
    # Test normal decisions
    normal_decisions = {
        'prices': {'Chips': 1.90},
        'orders': {'Water': 5},
        'character_control_active': True
    }
    
    oversight3 = bridge._apply_executive_oversight(normal_decisions, MOCK_STORE_STATUS)
    assert "approved" in oversight3, "Should approve reasonable decisions"
    
    print(f"✅ Oversight approved normal decisions: {oversight3}")

def run_all_tests():
    """Run comprehensive Phase 5A.1 tests"""
    print("🚀 PHASE 5A.1 TESTING SUITE")
    print("=" * 50)
    
    try:
        test_character_authority_matrix()
        test_decision_translation()
        test_pricing_extraction()
        test_ordering_extraction()
        test_multi_agent_decision_format()
        test_executive_oversight()
        
        print("\n" + "=" * 50)
        print("🏆 ALL TESTS PASSED!")
        print("✅ Phase 5A.1 True Multi-Agent Decision Making: FUNCTIONAL")
        print("✅ Character Authority Matrix: OPERATIONAL") 
        print("✅ Decision Translation: WORKING")
        print("✅ Executive Oversight: ACTIVE")
        print("✅ Character Control System: READY FOR DEPLOYMENT")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    run_all_tests() 