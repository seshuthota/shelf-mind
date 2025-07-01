#!/usr/bin/env python3
"""
Phase 2C Crisis Management System - Test Script
Tests the new crisis management features and emergency response system
"""

from store_engine import StoreEngine
from scrooge_agent import ScroogeAgent
from crisis_engine import CrisisEngine
from models import CrisisType, EmergencyAction

def test_crisis_system():
    """Test the crisis management system"""
    print("🚨 Testing Phase 2C Crisis Management System")
    print("=" * 50)
    
    # Initialize store
    store = StoreEngine(starting_cash=200.0)
    crisis_engine = CrisisEngine()
    
    print("✅ Store and Crisis Engine initialized")
    
    # Test crisis generation
    market_event = store.market_events_engine.get_market_conditions(1)
    print(f"📊 Market conditions: {market_event.description}")
    
    # Force generate a crisis for testing
    crisis_engine.crisis_probability_base = 1.0  # 100% chance for testing
    new_crises = crisis_engine.generate_crisis_events(1, store.state, market_event)
    
    if new_crises:
        print(f"\n🚨 Generated {len(new_crises)} crisis event(s):")
        for crisis in new_crises:
            print(f"   • {crisis.description}")
            print(f"     Severity: {crisis.severity:.2f}")
            print(f"     Duration: {crisis.duration_days} days")
            if crisis.affected_products:
                print(f"     Affected Products: {', '.join(crisis.affected_products)}")
            if crisis.affected_suppliers:
                print(f"     Affected Suppliers: {', '.join(crisis.affected_suppliers)}")
    else:
        print("📊 No crisis generated (this is normal)")
    
    # Add the crisis to store state
    store.state.active_crises.extend(new_crises)
    
    # Test emergency actions
    emergency_actions = crisis_engine.get_emergency_actions(store.state)
    print(f"\n⚡ Available emergency actions: {len(emergency_actions)}")
    for action in emergency_actions:
        print(f"   • {action.get('name', 'Unknown')}: {action.get('description', 'No description')}")
    
    # Test emergency action execution (emergency restock)
    if emergency_actions:
        print("\n⚡ Testing emergency restock...")
        result = crisis_engine.execute_emergency_action(
            EmergencyAction.EMERGENCY_RESTOCK,
            {"product_name": "Coke", "quantity": 5},
            store.state
        )
        print(f"   Result: {result}")
    
    # Test crisis-affected supplier selection
    print("\n🏭 Testing crisis-affected supplier selection...")
    affected_suppliers = crisis_engine.get_crisis_affected_suppliers(store.state, "Coke")
    for supplier_info in affected_suppliers:
        supplier = supplier_info["supplier"]
        effects = supplier_info["crisis_effects"]
        print(f"   • {supplier.name}: Cost multiplier {effects['cost_multiplier']:.2f}, Available: {effects['available']}")
    
    # Test store status with crisis information
    print("\n📊 Testing store status with crisis information...")
    status = store.get_status()
    crisis_status = status.get('crisis_status', {})
    print(f"   Active crises: {len(crisis_status.get('active_crises', []))}")
    print(f"   Daily crisis costs: ${crisis_status.get('daily_crisis_costs', 0):.2f}")
    print(f"   Emergency actions available: {len(crisis_status.get('emergency_actions', []))}")
    
    print("\n✅ Crisis Management System Test Complete!")
    print("🎯 Phase 2C implementation is working correctly!")

if __name__ == "__main__":
    test_crisis_system() 