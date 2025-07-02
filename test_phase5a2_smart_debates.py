#!/usr/bin/env python3
"""
🧠 Phase 5A.2: Smart Debate Triggering System Test

Tests the revolutionary domain authority respect and smart debate triggering logic.
Demonstrates how the system eliminates unnecessary debates while catching real conflicts.
"""

import sys
sys.path.append('.')

from src.core.multi_agent_engine import MultiAgentCoordinator, AgentDecision, AgentRole, CHARACTER_AUTHORITY_MATRIX
from src.core.character_debate_engine import CharacterDebateEngine, DebateTopicType
from src.agents.inventory_manager_agent import InventoryManagerAgent
from src.agents.pricing_analyst_agent import PricingAnalystAgent
from src.agents.customer_service_agent import CustomerServiceAgent
from src.agents.strategic_planner_agent import StrategyPlannerAgent
from src.agents.crisis_manager_agent import CrisisManagerAgent

def test_domain_authority_respect():
    """🏛️ Test that domain-specific decisions proceed without debate"""
    
    print("\n" + "="*80)
    print("🏛️ PHASE 5A.2 TEST: DOMAIN AUTHORITY RESPECT")
    print("Testing that domain-specific decisions proceed automatically")
    print("="*80)
    
    # Initialize coordinator
    coordinator = MultiAgentCoordinator(provider="mock")
    
    # Register all specialists
    coordinator.register_specialist(InventoryManagerAgent(provider="mock"))
    coordinator.register_specialist(PricingAnalystAgent(provider="mock"))
    coordinator.register_specialist(CustomerServiceAgent(provider="mock"))
    coordinator.register_specialist(StrategyPlannerAgent(provider="mock"))
    coordinator.register_specialist(CrisisManagerAgent(provider="mock"))
    
    print(f"✅ Registered {len(coordinator.get_active_specialists())} character specialists")
    
    # Test scenario 1: Domain-specific decisions (should NOT trigger debate)
    print(f"\n📋 SCENARIO 1: DOMAIN-SPECIFIC DECISIONS")
    print("-" * 50)
    
    domain_specific_decisions = [
        AgentDecision(
            agent_role=AgentRole.INVENTORY_MANAGER,
            decision_type="inventory_reorder",
            parameters={"product": "chips", "quantity": 20},
            confidence=0.8,
            priority=6,  # Below override threshold
            reasoning="Hermione: Standard inventory replenishment based on demand analysis"
        ),
        AgentDecision(
            agent_role=AgentRole.PRICING_ANALYST,
            decision_type="pricing_optimization",
            parameters={"product": "soda", "new_price": 1.25},
            confidence=0.9,
            priority=7,  # Within Gekko's authority
            reasoning="Gekko: Price adjustment for optimal profit margin"
        ),
        AgentDecision(
            agent_role=AgentRole.CUSTOMER_SERVICE,
            decision_type="customer_experience_enhancement",
            parameters={"service_focus": "satisfaction"},
            confidence=0.7,
            priority=5,
            reasoning="Elle: Improve customer service protocols"
        )
    ]
    
    store_status = {
        "day": 15,
        "cash": 200.0,
        "inventory": {"chips": 5, "soda": 8, "candy": 10}
    }
    
    # Test debate triggering
    debate_engine = CharacterDebateEngine(provider="mock")
    debate_topic = debate_engine.should_trigger_debate(domain_specific_decisions, store_status)
    
    print(f"🔍 RESULT: Debate Topic = {debate_topic}")
    
    if debate_topic is None:
        print(f"✅ SUCCESS: No debate triggered - all decisions within domain authority")
        print(f"📊 ANALYSIS:")
        for decision in domain_specific_decisions:
            domains = CHARACTER_AUTHORITY_MATRIX.get(decision.agent_role, {}).get("primary_domains", [])
            print(f"   - {decision.agent_role.value}: '{decision.decision_type}' → Domains: {domains}")
    else:
        print(f"❌ FAILED: Unexpected debate triggered for domain-specific decisions")
        
    return debate_topic is None

def test_cross_domain_conflict_detection():
    """⚔️ Test detection of genuine cross-domain conflicts"""
    
    print(f"\n" + "="*80)
    print("⚔️ PHASE 5A.2 TEST: CROSS-DOMAIN CONFLICT DETECTION")
    print("Testing detection of genuine conflicts between character domains")
    print("="*80)
    
    # Create conflicting decisions across domains
    print(f"\n📋 SCENARIO 2: CROSS-DOMAIN CONFLICTS")
    print("-" * 50)
    
    conflicting_decisions = [
        AgentDecision(
            agent_role=AgentRole.PRICING_ANALYST,
            decision_type="aggressive_pricing",
            parameters={"strategy": "maximize_profit", "price_increase": True},
            confidence=0.9,
            priority=8,
            reasoning="Gekko: Maximize profit with aggressive pricing strategy to beat competition"
        ),
        AgentDecision(
            agent_role=AgentRole.CUSTOMER_SERVICE,
            decision_type="customer_retention_focus",
            parameters={"strategy": "customer_satisfaction", "price_sensitivity": "high"},
            confidence=0.8,
            priority=7,
            reasoning="Elle: Conservative pricing needed to maintain customer satisfaction and loyalty"
        ),
        AgentDecision(
            agent_role=AgentRole.INVENTORY_MANAGER,
            decision_type="conservative_inventory",
            parameters={"strategy": "minimize_risk", "cash_conservation": True},
            confidence=0.7,
            priority=6,
            reasoning="Hermione: Safe inventory approach to minimize financial risk"
        )
    ]
    
    store_status = {
        "day": 20,
        "cash": 150.0,
        "inventory": {"chips": 2, "soda": 1, "candy": 0}
    }
    
    # Test debate triggering
    debate_engine = CharacterDebateEngine(provider="mock") 
    debate_topic = debate_engine.should_trigger_debate(conflicting_decisions, store_status)
    
    print(f"🔍 RESULT: Debate Topic = {debate_topic}")
    
    if debate_topic is not None:
        print(f"✅ SUCCESS: Cross-domain conflict detected → {debate_topic.value.upper()}")
        print(f"📊 CONFLICT ANALYSIS:")
        print(f"   - Gekko (Pricing): Aggressive profit maximization")
        print(f"   - Elle (Customer): Conservative customer satisfaction focus")
        print(f"   - Hermione (Inventory): Risk-minimizing approach")
        print(f"   → Strategic conflict detected: aggressive vs conservative approaches")
    else:
        print(f"❌ FAILED: No debate triggered despite clear cross-domain conflicts")
        
    return debate_topic is not None

def test_resource_conflict_triggering():
    """💰 Test resource allocation conflict detection"""
    
    print(f"\n" + "="*80)
    print("💰 PHASE 5A.2 TEST: RESOURCE CONFLICT DETECTION")
    print("Testing detection of resource allocation conflicts")
    print("="*80)
    
    # Create resource-competing decisions
    print(f"\n📋 SCENARIO 3: RESOURCE ALLOCATION CONFLICTS")
    print("-" * 50)
    
    resource_competing_decisions = [
        AgentDecision(
            agent_role=AgentRole.INVENTORY_MANAGER,
            decision_type="emergency_restock",
            parameters={"products": ["chips", "soda", "candy"], "total_cost": 120},
            confidence=0.9,
            priority=8,
            reasoning="Hermione: Emergency restock needed - invest $120 in inventory"
        ),
        AgentDecision(
            agent_role=AgentRole.STRATEGIC_PLANNER,
            decision_type="strategic_expansion",
            parameters={"expansion_cost": 100, "marketing_budget": 50},
            confidence=0.8,
            priority=7,
            reasoning="Tyrion: Strategic expansion requires $150 investment in growth"
        ),
        AgentDecision(
            agent_role=AgentRole.CRISIS_MANAGER,
            decision_type="crisis_response_fund",
            parameters={"emergency_reserve": 80},
            confidence=0.9,
            priority=9,
            reasoning="Jack: Set aside $80 emergency fund for crisis response"
        )
    ]
    
    # Limited cash scenario
    store_status = {
        "day": 25,
        "cash": 180.0,  # Not enough for all demands ($120 + $150 + $80 = $350)
        "inventory": {"chips": 0, "soda": 0, "candy": 1}
    }
    
    # Create mock resource conflicts
    from src.core.coordination_intelligence import ResourceConflict
    resource_conflicts = [
        ResourceConflict(
            competing_agents=[AgentRole.INVENTORY_MANAGER, AgentRole.STRATEGIC_PLANNER, AgentRole.CRISIS_MANAGER],
            resource_type="cash",
            total_demand=350.0,
            available_supply=180.0,
            conflict_severity=0.8
        )
    ]
    
    # Test debate triggering with resource conflicts
    debate_engine = CharacterDebateEngine(provider="mock")
    debate_topic = debate_engine.should_trigger_debate(
        resource_competing_decisions, store_status, resource_conflicts
    )
    
    print(f"🔍 RESULT: Debate Topic = {debate_topic}")
    print(f"💰 RESOURCE ANALYSIS:")
    print(f"   - Total Demand: $350 (Hermione: $120, Tyrion: $150, Jack: $80)")
    print(f"   - Available Cash: $180")
    print(f"   - Conflict Severity: 0.8 (High)")
    
    if debate_topic is not None:
        print(f"✅ SUCCESS: Resource conflict triggered debate → {debate_topic.value.upper()}")
    else:
        print(f"❌ FAILED: No debate triggered despite severe resource conflict")
        
    return debate_topic is not None

def test_emergency_override_logic():
    """⚡ Test emergency override for crisis situations"""
    
    print(f"\n" + "="*80)
    print("⚡ PHASE 5A.2 TEST: EMERGENCY OVERRIDE LOGIC")
    print("Testing that Jack's crisis decisions bypass normal debate protocols")
    print("="*80)
    
    # Create crisis situation with Jack's emergency decision
    print(f"\n📋 SCENARIO 4: EMERGENCY CRISIS OVERRIDE")
    print("-" * 50)
    
    emergency_decisions = [
        AgentDecision(
            agent_role=AgentRole.CRISIS_MANAGER,
            decision_type="crisis_response_immediate",
            parameters={"action": "emergency_action", "bypass_normal_protocols": True},
            confidence=0.95,
            priority=9,  # High priority crisis
            reasoning="Jack: EMERGENCY - Health inspection crisis requires immediate action"
        ),
        AgentDecision(
            agent_role=AgentRole.INVENTORY_MANAGER,
            decision_type="inventory_audit",
            parameters={"audit_level": "comprehensive"},
            confidence=0.8,
            priority=8,
            reasoning="Hermione: Comprehensive inventory audit needed for crisis response"
        ),
        AgentDecision(
            agent_role=AgentRole.CUSTOMER_SERVICE,
            decision_type="crisis_communication",
            parameters={"customer_outreach": "immediate"},
            confidence=0.9,
            priority=7,
            reasoning="Elle: Immediate customer communication about crisis situation"
        )
    ]
    
    # Crisis store status
    crisis_store_status = {
        "day": 30,
        "cash": 100.0,
        "inventory": {"chips": 0, "soda": 0, "candy": 0},
        "active_crises": ["health_inspection"]
    }
    
    # Test emergency override
    debate_engine = CharacterDebateEngine(provider="mock")
    debate_topic = debate_engine.should_trigger_debate(emergency_decisions, crisis_store_status)
    
    print(f"🔍 RESULT: Debate Topic = {debate_topic}")
    print(f"⚡ EMERGENCY ANALYSIS:")
    print(f"   - Jack's Priority: 9 (Emergency Level)")
    print(f"   - Crisis Type: Health Inspection")
    print(f"   - Override Threshold: Crisis situations bypass debates")
    
    if debate_topic is None:
        print(f"✅ SUCCESS: Emergency override activated - no debate triggered")
        print(f"   → Jack's crisis decision proceeds immediately without debate")
    else:
        print(f"❌ FAILED: Debate triggered despite emergency override logic")
        
    return debate_topic is None

def test_comprehensive_smart_triggering():
    """🧠 Comprehensive test of the full smart triggering system"""
    
    print(f"\n" + "="*80)
    print("🧠 PHASE 5A.2 COMPREHENSIVE TEST: FULL SMART TRIGGERING SYSTEM")
    print("Testing complete coordination with smart debate triggering")
    print("="*80)
    
    # Initialize full system
    coordinator = MultiAgentCoordinator(provider="mock")
    
    # Register all specialists
    coordinator.register_specialist(InventoryManagerAgent(provider="mock"))
    coordinator.register_specialist(PricingAnalystAgent(provider="mock"))
    coordinator.register_specialist(CustomerServiceAgent(provider="mock"))
    coordinator.register_specialist(StrategyPlannerAgent(provider="mock"))
    coordinator.register_specialist(CrisisManagerAgent(provider="mock"))
    
    # Test scenario with mixed decisions
    store_status = {
        "day": 35,
        "cash": 250.0,
        "inventory": {"chips": 3, "soda": 1, "candy": 0, "cookies": 5}
    }
    
    context = {
        "season": "summer",
        "economic_condition": "normal",
        "yesterday_summary": {
            "revenue": 45.0,
            "profit": 12.0,
            "units_sold_by_product": {"chips": 5, "soda": 8, "candy": 3}
        }
    }
    
    print(f"\n📊 COMPREHENSIVE SCENARIO:")
    print(f"   - Day: {store_status['day']}")
    print(f"   - Cash: ${store_status['cash']:.2f}")
    print(f"   - Stockouts: Candy (0 units)")
    print(f"   - Mixed decision types expected")
    
    try:
        # Run full coordination with smart debate triggering
        print(f"\n🎭 EXECUTING FULL COORDINATION WITH SMART DEBATE TRIGGERING...")
        consensus = coordinator.coordinate_decisions(store_status, context)
        
        print(f"\n🏆 COORDINATION RESULTS:")
        print(f"   📋 Decisions Made: {len(consensus.final_decisions)}")
        print(f"   🎭 Debate Occurred: {'YES' if consensus.debate_occurred else 'NO'}")
        print(f"   🎯 Overall Confidence: {consensus.overall_confidence:.2f}")
        
        if consensus.debate_occurred and consensus.debate_resolution:
            print(f"   🎪 Debate Topic: {consensus.debate_resolution.debate_summary}")
            
        # Display business translation
        if consensus.business_translation:
            bt = consensus.business_translation
            print(f"\n💼 BUSINESS DECISION TRANSLATION:")
            print(f"   💰 Pricing Decisions: {len(bt.pricing_decisions)} products")
            print(f"   📦 Ordering Decisions: {len(bt.ordering_decisions)} products")
            print(f"   🎯 Decision Confidence: {bt.decision_confidence:.2f}")
            print(f"   👑 Primary Decision Maker: {bt.primary_decision_maker.value if bt.primary_decision_maker else 'Consensus'}")
            
        return True
        
    except Exception as e:
        print(f"❌ ERROR in comprehensive test: {e}")
        return False

def main():
    """Run all Phase 5A.2 smart debate triggering tests"""
    
    print("🚀" * 40)
    print("PHASE 5A.2: SMART DEBATE TRIGGERING SYSTEM")
    print("Domain Authority Respect & Intelligent Conflict Detection")
    print("🚀" * 40)
    
    test_results = []
    
    # Run all tests
    test_results.append(("Domain Authority Respect", test_domain_authority_respect()))
    test_results.append(("Cross-Domain Conflict Detection", test_cross_domain_conflict_detection()))
    test_results.append(("Resource Conflict Triggering", test_resource_conflict_triggering()))
    test_results.append(("Emergency Override Logic", test_emergency_override_logic()))
    test_results.append(("Comprehensive Smart Triggering", test_comprehensive_smart_triggering()))
    
    # Display results summary
    print(f"\n" + "🏆" * 80)
    print("PHASE 5A.2 TEST RESULTS SUMMARY")
    print("🏆" * 80)
    
    passed_tests = 0
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
        if result:
            passed_tests += 1
    
    print(f"\n📊 OVERALL RESULTS: {passed_tests}/{len(test_results)} tests passed")
    
    if passed_tests == len(test_results):
        print(f"\n🎉 PHASE 5A.2 IMPLEMENTATION SUCCESS!")
        print(f"✅ Smart debate triggering system fully operational")
        print(f"✅ Domain authority respected - no unnecessary debates")
        print(f"✅ Cross-domain conflicts properly detected")
        print(f"✅ Resource conflicts trigger appropriate debates")
        print(f"✅ Emergency override logic working correctly")
    else:
        print(f"\n⚠️ PHASE 5A.2 IMPLEMENTATION NEEDS ATTENTION")
        print(f"Some tests failed - review smart debate triggering logic")

if __name__ == "__main__":
    main() 