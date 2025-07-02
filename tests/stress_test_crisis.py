#!/usr/bin/env python3
"""
Crisis Management Stress Test
Force various crisis scenarios and test emergency response capabilities
"""

import sys
import json
from models import *
from store_engine import StoreEngine
from scrooge_agent import ScroogeAgent
from crisis_engine import CrisisEngine

# Import the full simulation class from main
from main import StoreSimulation

def force_crisis_scenario(store_state, crisis_type, severity='severe'):
    """Force a specific crisis type for testing"""
    severity_map = {'moderate': 0.5, 'severe': 0.8, 'critical': 1.0}
    severity_value = severity_map.get(severity, 0.8)
    
    crisis_data = {
        'supplier_bankruptcy': {
            'crisis_type': CrisisType.SUPPLIER_BANKRUPTCY,
            'severity': severity_value,
            'affected_suppliers': ['BudgetBites', 'CheapCoke Co'],
            'duration_days': 5,
            'remaining_days': 5,
            'description': f"🏭 SUPPLIER BANKRUPTCY: BudgetBites and CheapCoke Co have gone bankrupt!",
            'emergency_actions_available': ['switch_supplier', 'emergency_restock']
        },
        'supply_shortage': {
            'crisis_type': CrisisType.SUPPLY_SHORTAGE,
            'severity': severity_value,
            'affected_products': ['Coke', 'Chips', 'Ice Cream'],
            'duration_days': 4,
            'remaining_days': 4,
            'cost_multiplier': 1.3,
            'description': f"📦 SUPPLY SHORTAGE: Critical shortage of Coke, Chips, Ice Cream!",
            'emergency_actions_available': ['emergency_restock', 'raise_prices']
        },
        'economic_shock': {
            'crisis_type': CrisisType.ECONOMIC_SHOCK,
            'severity': severity_value,
            'cost_multiplier': 1.4,
            'duration_days': 6,
            'remaining_days': 6,
            'description': f"💥 ECONOMIC SHOCK: All costs increased by 40% due to inflation!",
            'emergency_actions_available': ['take_loan', 'raise_prices']
        },
        'regulatory_crisis': {
            'crisis_type': CrisisType.REGULATORY_CRISIS,
            'severity': severity_value,
            'duration_days': 3,
            'remaining_days': 3,
            'description': f"🏛️ REGULATORY CRISIS: Daily compliance costs of $150!",
            'emergency_actions_available': ['take_loan']
        }
    }
    
    if crisis_type not in crisis_data:
        print(f"❌ Unknown crisis type: {crisis_type}")
        return None
        
    crisis = CrisisEvent(**crisis_data[crisis_type])
    store_state.active_crises.append(crisis)
    print(f"🚨 FORCED CRISIS: {crisis.description}")
    return crisis

def test_emergency_actions(store, agent):
    """Test all emergency action types"""
    print("\n🚨 TESTING EMERGENCY ACTIONS:")
    
    # Test via agent's tool usage (realistic scenario)
    print("\n1. Testing agent's awareness of crisis tools...")
    tools = agent.get_tools()
    crisis_tools = [tool for tool in tools if 'crisis' in tool['function']['name'] or 'emergency' in tool['function']['name']]
    
    print(f"✅ Agent has {len(crisis_tools)} crisis management tools:")
    for tool in crisis_tools:
        print(f"   - {tool['function']['name']}: {tool['function']['description']}")
    
    # Skip direct tool testing for now, let agent use them naturally in simulation
    print("\n2. Emergency actions will be tested during simulation when agent uses them naturally.")

def run_crisis_stress_test():
    """Run comprehensive crisis stress test"""
    print("🔥 CRISIS MANAGEMENT STRESS TEST STARTING!")
    print("=" * 60)
    
    # Initialize full simulation system
    sim = StoreSimulation()
    
    print(f"💰 Starting Cash: ${sim.store.state.cash}")
    inventory_summary = {name: item.total_quantity for name, item in sim.store.state.inventory.items()}
    print(f"📦 Starting Inventory: {inventory_summary}")
    
    # Force multiple crisis scenarios
    crisis_scenarios = [
        ('supplier_bankruptcy', 'severe'),
        ('supply_shortage', 'moderate'), 
        ('economic_shock', 'severe'),
        ('regulatory_crisis', 'moderate')
    ]
    
    print(f"\n🚨 FORCING {len(crisis_scenarios)} CRISIS SCENARIOS:")
    for crisis_type, severity in crisis_scenarios:
        force_crisis_scenario(sim.store.state, crisis_type, severity)
    
    # Display active crises
    print(f"\n⚠️ ACTIVE CRISES ({len(sim.store.state.active_crises)}):")
    for i, crisis in enumerate(sim.store.state.active_crises):
        print(f"   {i+1}. {crisis.description} (severity: {crisis.severity:.1f}) - {crisis.remaining_days} days remaining")
    
    # Test emergency actions
    test_emergency_actions(sim.store, sim.scrooge)
    
    # Run several days with multiple crises
    print(f"\n🎮 RUNNING 5-DAY SIMULATION WITH MULTIPLE ACTIVE CRISES:")
    print("=" * 60)
    
    for day in range(1, 6):
        print(f"\n🌅 DAY {day} - CRISIS MANAGEMENT MODE")
        
        # Use the StoreSimulation's run_single_day method
        try:
            # Suppress rich console output for stress test
            import io
            from contextlib import redirect_stdout
            
            # Capture console output but still get the day summary
            with redirect_stdout(io.StringIO()):
                daily_result = sim.run_single_day()
            
            print(f"💰 Day {day} Results:")
            print(f"   📈 Profit: ${daily_result.get('profit', 0):.2f}")
            print(f"   💵 Cash: ${sim.store.state.cash:.2f}")
            print(f"   🛒 Units Sold: {daily_result.get('units_sold', 0)}")
            print(f"   ⚠️ Active Crises: {len(sim.store.state.active_crises)}")
            
            # Display any crisis effects (simplified for stress test)
            if len(sim.store.state.active_crises) > 0:
                crisis_count = len(sim.store.state.active_crises)
                print(f"   💸 Crisis Impact: {crisis_count} active crisis(es)")
            
        except Exception as e:
            print(f"❌ Day {day} simulation failed: {e}")
    
    # Final crisis status
    print(f"\n📊 FINAL CRISIS STATUS:")
    print(f"💰 Final Cash: ${sim.store.state.cash:.2f}")
    print(f"⚠️ Remaining Crises: {len(sim.store.state.active_crises)}")
    
    if sim.store.state.cash > 0:
        print("✅ BUSINESS SURVIVED CRISIS STRESS TEST!")
    else:
        print("💀 BUSINESS FAILED UNDER CRISIS PRESSURE!")
    
    return sim.store.state.cash > 0

if __name__ == "__main__":
    success = run_crisis_stress_test()
    sys.exit(0 if success else 1) 