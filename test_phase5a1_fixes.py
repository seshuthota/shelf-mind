#!/usr/bin/env python3
"""
Phase 5A.1 Fixes Validation Test
Tests the data mismatch fixes between StoreEngine output and multi-agent input
"""

from src.engines.store_engine import StoreEngine
from src.core.multi_agent_engine import MultiAgentCoordinator, HybridAgentBridge
from src.agents.inventory_manager_agent import InventoryManagerAgent
from src.agents.pricing_analyst_agent import PricingAnalystAgent
from src.agents.customer_service_agent import CustomerServiceAgent
from src.agents.strategic_planner_agent import StrategicPlannerAgent
from src.agents.crisis_manager_agent import CrisisManagerAgent

def test_data_flow_fixes():
    """Test that the data flow fixes work correctly"""
    print("🧪 TESTING PHASE 5A.1 DATA FLOW FIXES")
    print("=" * 50)
    
    # 1. Create StoreEngine and get status
    print("\n1. Creating StoreEngine and getting status...")
    store = StoreEngine(starting_cash=200.0)
    store_status = store.get_status()
    print(f"✅ Store status keys: {list(store_status.keys())}")
    print(f"✅ Inventory format: {type(list(store_status['inventory'].values())[0])}")
    
    # 2. Create fake yesterday_summary
    yesterday_summary = {
        'units_sold_by_product': {'Coke': 3, 'Water': 2, 'Chips': 1},
        'revenue': 15.50,
        'profit': 8.20,
        'total_revenue': 15.50
    }
    print(f"✅ Yesterday summary created: {list(yesterday_summary.keys())}")
    
    # 3. Test individual agent data handling
    print("\n2. Testing individual agent data handling...")
    
    try:
        inventory_agent = InventoryManagerAgent(provider="mock")
        context = {'yesterday_summary': yesterday_summary}
        decision = inventory_agent.analyze_situation(store_status, context)
        print(f"✅ InventoryManagerAgent: Success - {decision.decision_type}")
        print(f"   Priority: {decision.priority}, Confidence: {decision.confidence:.2f}")
    except Exception as e:
        print(f"❌ InventoryManagerAgent failed: {e}")
        
    try:
        pricing_agent = PricingAnalystAgent(provider="mock")
        decision = pricing_agent.analyze_situation(store_status, context)
        print(f"✅ PricingAnalystAgent: Success - {decision.decision_type}")
        print(f"   Priority: {decision.priority}, Confidence: {decision.confidence:.2f}")
    except Exception as e:
        print(f"❌ PricingAnalystAgent failed: {e}")
    
    # 4. Test MultiAgentCoordinator
    print("\n3. Testing MultiAgentCoordinator...")
    
    try:
        coordinator = MultiAgentCoordinator(provider="mock")
        coordinator.register_specialist(InventoryManagerAgent(provider="mock"))
        coordinator.register_specialist(PricingAnalystAgent(provider="mock"))
        
        # Test coordinate_decisions with our fixes
        consensus = coordinator.coordinate_decisions(store_status, context)
        print(f"✅ MultiAgentCoordinator: Success")
        print(f"   Decisions: {len(consensus.final_decisions)}")
        print(f"   Overall confidence: {consensus.overall_confidence:.2f}")
        print(f"   Business translation: {'Yes' if consensus.business_translation else 'No'}")
        
    except Exception as e:
        print(f"❌ MultiAgentCoordinator failed: {e}")
        import traceback
        print(f"   Error details: {traceback.format_exc()}")
    
    # 5. Test full HybridAgentBridge
    print("\n4. Testing full HybridAgentBridge...")
    
    try:
        coordinator = MultiAgentCoordinator(provider="mock")
        coordinator.register_specialist(InventoryManagerAgent(provider="mock"))
        coordinator.register_specialist(PricingAnalystAgent(provider="mock"))
        coordinator.register_specialist(CustomerServiceAgent(provider="mock"))
        
        bridge = HybridAgentBridge(None, coordinator)
        bridge.set_mode("multi")
        
        decision = bridge.make_daily_decision(store_status, yesterday_summary)
        print(f"✅ HybridAgentBridge: Success")
        print(f"   Mode: {decision.get('mode', 'unknown')}")
        print(f"   Character control active: {decision.get('character_control_active', False)}")
        print(f"   Decisions: {decision.get('specialist_decisions', 0)}")
        
        if 'prices' in decision:
            print(f"   Pricing decisions: {len(decision['prices'])}")
        if 'orders' in decision:
            print(f"   Ordering decisions: {len(decision['orders'])}")
            
    except Exception as e:
        print(f"❌ HybridAgentBridge failed: {e}")
        import traceback
        print(f"   Error details: {traceback.format_exc()}")
    
    print("\n" + "=" * 50)
    print("🎯 PHASE 5A.1 FIXES VALIDATION COMPLETE")

if __name__ == "__main__":
    test_data_flow_fixes() 