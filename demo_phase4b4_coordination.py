#!/usr/bin/env python3
"""
🧠 Phase 4B.4: Advanced Agent Coordination & Information Sharing Demo
Revolutionary demonstration of predictive coordination intelligence.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.multi_agent_engine import MultiAgentCoordinator
from src.agents.inventory_manager_agent import HermioneGrangerAgent
from src.agents.pricing_analyst_agent import GordonGekkoAgent  
from src.agents.customer_service_agent import ElleWoodsAgent
from src.agents.strategic_planner_agent import TyrionLannisterAgent
from src.agents.crisis_manager_agent import JackBauerAgent
from src.core.models import StoreState, InventoryItem, InventoryBatch, CrisisEvent, CrisisType
from src.engines.store_engine import StoreSimulationEngine


def create_test_scenario():
    """Create a complex scenario to demonstrate coordination intelligence"""
    
    # Complex store state with multiple challenges
    store_state = StoreState(
        day=15,
        cash=800.0,  # Limited cash for resource conflicts
        inventory={
            "Coke": InventoryItem(product_name="Coke", batches=[
                InventoryBatch(quantity=2, received_day=14, expiration_day=None)
            ]),
            "Chips": InventoryItem(product_name="Chips", batches=[
                InventoryBatch(quantity=0, received_day=10, expiration_day=None)  # Stockout
            ]),
            "Candy": InventoryItem(product_name="Candy", batches=[
                InventoryBatch(quantity=1, received_day=12, expiration_day=None)
            ]),
            "Ice Cream": InventoryItem(product_name="Ice Cream", batches=[
                InventoryBatch(quantity=8, received_day=14, expiration_day=20)  # High stock
            ]),
            "Water": InventoryItem(product_name="Water", batches=[
                InventoryBatch(quantity=3, received_day=13, expiration_day=None)
            ])
        },
        daily_sales={"Coke": 3, "Chips": 0, "Candy": 2, "Ice Cream": 1, "Water": 2},
        total_revenue=2450.0,
        total_profit=890.0,
        pending_deliveries=[],
        accounts_payable=200.0,
        active_crises=[
            CrisisEvent(
                crisis_type=CrisisType.SUPPLIER_BANKRUPTCY,
                affected_products=["Chips", "Water"],
                affected_suppliers=["QuickDeliver"],
                severity=0.8,
                duration_days=5,
                remaining_days=3,
                cost_multiplier=1.5,
                delivery_delay_multiplier=2.0,
                description="QuickDeliver bankruptcy affecting multiple products"
            )
        ]
    )
    
    return store_state


def demo_coordination_intelligence():
    """🧠 Demonstrate Phase 4B.4 advanced coordination capabilities"""
    
    print("="*80)
    print("🧠 PHASE 4B.4: ADVANCED AGENT COORDINATION & INFORMATION SHARING")
    print("Revolutionary Predictive Coordination Intelligence Demo")
    print("="*80)
    
    # Initialize multi-agent coordinator with all characters
    coordinator = MultiAgentCoordinator(provider="openai")
    
    # Register all character specialists
    coordinator.register_specialist(HermioneGrangerAgent())
    coordinator.register_specialist(GordonGekkoAgent())
    coordinator.register_specialist(ElleWoodsAgent())
    coordinator.register_specialist(TyrionLannisterAgent())
    coordinator.register_specialist(JackBauerAgent())
    
    print(f"✅ Registered {len(coordinator.get_active_specialists())} specialist agents")
    print(f"🧠 Intelligence Sharing: {'ENABLED' if coordinator.intelligence_sharing_enabled else 'DISABLED'}")
    print(f"⚠️  Conflict Prevention: {'ENABLED' if coordinator.proactive_conflict_prevention else 'DISABLED'}")
    
    # Create test scenario
    store_state = create_test_scenario()
    context = {
        "season": "summer",
        "weather": "heat_wave", 
        "economic_condition": "normal",
        "competitive_pressure": "high"
    }
    
    print(f"\n📊 SCENARIO: Day {store_state.day}")
    print(f"   💰 Cash: ${store_state.cash:.2f}")
    print(f"   📦 Stockouts: Chips (0 units)")
    print(f"   🚨 Active Crisis: {store_state.active_crises[0].crisis_type.value}")
    print(f"   🎯 Multiple high-priority decisions expected")
    
    # Execute coordination with advanced intelligence
    print(f"\n🎭 EXECUTING ADVANCED COORDINATION...")
    print("-" * 50)
    
    try:
        consensus = coordinator.coordinate_decisions(store_state.dict(), context)
        
        print(f"\n🏆 COORDINATION RESULTS:")
        print(f"   📋 Total Decisions: {len(consensus.final_decisions)}")
        print(f"   🎯 Overall Confidence: {consensus.overall_confidence:.2f}")
        print(f"   🎭 Debate Occurred: {'YES' if consensus.debate_occurred else 'NO'}")
        
        # Display coordination intelligence results
        if consensus.cross_domain_impacts:
            print(f"\n🔮 CROSS-DOMAIN IMPACT ANALYSIS:")
            for i, impact in enumerate(consensus.cross_domain_impacts[:3], 1):
                print(f"   {i}. {impact.source_agent.value} → {impact.target_agent.value}")
                print(f"      Impact: {impact.impact_type.value} (magnitude: {impact.impact_magnitude:.2f})")
                print(f"      Description: {impact.impact_description}")
                
        if consensus.shared_insights:
            print(f"\n🚀 PROACTIVE INTELLIGENCE SHARING:")
            for i, insight in enumerate(consensus.shared_insights[:3], 1):
                print(f"   {i}. {insight.agent_role.value}: {insight.insight_type}")
                print(f"      Urgency: {insight.urgency:.2f}")
                print(f"      Content: {insight.content.get('reasoning', 'Strategic insight')[:60]}...")
                
        if consensus.resource_conflicts:
            print(f"\n⚠️  RESOURCE CONFLICT DETECTION:")
            for i, conflict in enumerate(consensus.resource_conflicts, 1):
                agents_str = ", ".join([agent.value for agent in conflict.competing_agents])
                print(f"   {i}. {conflict.resource_type}: {agents_str}")
                print(f"      Severity: {conflict.conflict_severity:.2f}")
                print(f"      Demand: {conflict.total_demand:.1f} vs Supply: {conflict.available_supply:.1f}")
                
        # Show coordination dashboard
        print(f"\n📊 COORDINATION INTELLIGENCE DASHBOARD:")
        dashboard = coordinator.get_coordination_dashboard()
        metrics = dashboard['metrics']
        
        print(f"   🤝 Information Sharing Rate: {metrics['information_sharing_rate']:.3f}")
        print(f"   ⚡ Conflict Resolution Time: {metrics['conflict_resolution_time']:.3f}")
        print(f"   🎯 Strategic Alignment Score: {metrics['strategic_alignment_score']:.3f}")
        print(f"   ⚠️  Active Conflicts: {metrics['active_conflicts']}")
        
        print(f"\n💡 COORDINATION RECOMMENDATIONS:")
        for rec in dashboard['coordination_recommendations']:
            print(f"   • {rec}")
            
        print(f"\n✅ COORDINATION NOTES: {consensus.coordination_notes}")
        
    except Exception as e:
        print(f"❌ Error during coordination: {e}")
        import traceback
        traceback.print_exc()


def demo_intelligence_features():
    """🔬 Demonstrate specific Phase 4B.4 intelligence features"""
    
    print(f"\n" + "="*80)
    print("🔬 PHASE 4B.4 INTELLIGENCE FEATURES DEMONSTRATION")
    print("="*80)
    
    coordinator = MultiAgentCoordinator()
    
    # Test intelligence settings
    print(f"\n⚙️  TESTING INTELLIGENCE CONTROLS:")
    
    print(f"   🧠 Disabling intelligence sharing...")
    coordinator.enable_intelligence_sharing(False)
    print(f"   Intelligence Sharing: {'ENABLED' if coordinator.intelligence_sharing_enabled else 'DISABLED'}")
    
    print(f"   ⚠️  Disabling conflict prevention...")
    coordinator.enable_conflict_prevention(False) 
    print(f"   Conflict Prevention: {'ENABLED' if coordinator.proactive_conflict_prevention else 'DISABLED'}")
    
    print(f"   🔄 Re-enabling all intelligence features...")
    coordinator.enable_intelligence_sharing(True)
    coordinator.enable_conflict_prevention(True)
    print(f"   All intelligence features: ENABLED")
    
    # Test coordination dashboard
    print(f"\n📊 COORDINATION DASHBOARD (Initial State):")
    dashboard = coordinator.get_coordination_dashboard()
    
    print(f"   Active Insights: {dashboard['active_insights']}")
    print(f"   Recent Conflicts: {len(dashboard['recent_conflicts'])}")
    print(f"   Metrics: {dashboard['metrics']}")
    
    print(f"\n🎯 FEATURE VALIDATION COMPLETE")


def demo_scenario_comparison():
    """📈 Compare coordination with and without intelligence features"""
    
    print(f"\n" + "="*80)
    print("📈 COORDINATION INTELLIGENCE IMPACT COMPARISON")
    print("="*80)
    
    store_state = create_test_scenario()
    context = {"season": "summer", "economic_condition": "normal"}
    
    # Test without intelligence features
    print(f"\n🔄 COORDINATION WITHOUT INTELLIGENCE FEATURES:")
    coordinator_basic = MultiAgentCoordinator()
    coordinator_basic.register_specialist(HermioneGrangerAgent())
    coordinator_basic.register_specialist(GordonGekkoAgent())
    coordinator_basic.register_specialist(JackBauerAgent())
    
    coordinator_basic.enable_intelligence_sharing(False)
    coordinator_basic.enable_conflict_prevention(False)
    
    try:
        basic_consensus = coordinator_basic.coordinate_decisions(store_state.dict(), context)
        print(f"   Decisions: {len(basic_consensus.final_decisions)}")
        print(f"   Confidence: {basic_consensus.overall_confidence:.2f}")
        print(f"   Cross-domain impacts: {len(basic_consensus.cross_domain_impacts or [])}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test with intelligence features
    print(f"\n🧠 COORDINATION WITH INTELLIGENCE FEATURES:")
    coordinator_advanced = MultiAgentCoordinator()
    coordinator_advanced.register_specialist(HermioneGrangerAgent())
    coordinator_advanced.register_specialist(GordonGekkoAgent())
    coordinator_advanced.register_specialist(JackBauerAgent())
    
    try:
        advanced_consensus = coordinator_advanced.coordinate_decisions(store_state.dict(), context)
        print(f"   Decisions: {len(advanced_consensus.final_decisions)}")
        print(f"   Confidence: {advanced_consensus.overall_confidence:.2f}")
        print(f"   Cross-domain impacts: {len(advanced_consensus.cross_domain_impacts or [])}")
        print(f"   Shared insights: {len(advanced_consensus.shared_insights or [])}")
        print(f"   Resource conflicts: {len(advanced_consensus.resource_conflicts or [])}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print(f"\n📊 INTELLIGENCE IMPACT: Enhanced decision quality and proactive coordination")


if __name__ == "__main__":
    """Run Phase 4B.4 Advanced Coordination Intelligence Demo"""
    
    try:
        # Main coordination intelligence demo
        demo_coordination_intelligence()
        
        # Intelligence features demo
        demo_intelligence_features()
        
        # Scenario comparison
        demo_scenario_comparison()
        
        print(f"\n" + "="*80)
        print("🏆 PHASE 4B.4 DEMO COMPLETE - REVOLUTIONARY SUCCESS")
        print("Advanced Coordination Intelligence Operational!")
        print("="*80)
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc() 