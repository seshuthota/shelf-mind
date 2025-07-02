"""
🎭 Phase 4B Character Debate System Test

Tests the revolutionary character debate engine with business scenarios.
Demonstrates personality-driven conflict resolution and consensus building.
"""

import sys
sys.path.append('.')

from src.core.character_debate_engine import CharacterDebateEngine, DebateTopicType
from src.core.multi_agent_engine import MultiAgentCoordinator, AgentDecision, AgentRole
from src.agents.inventory_manager_agent import InventoryManagerAgent
from src.agents.pricing_analyst_agent import PricingAnalystAgent
from src.agents.customer_service_agent import CustomerServiceAgent
from src.agents.strategic_planner_agent import StrategyPlannerAgent
from src.agents.crisis_manager_agent import CrisisManagerAgent

def test_character_debate_system():
    """🎭 Test the complete character debate system with a crisis scenario"""
    
    print("\n" + "="*80)
    print("🎭 PHASE 4B CHARACTER DEBATE SYSTEM TEST")
    print("Revolutionary Character-Driven Business Decision Making")
    print("="*80)
    
    # Initialize the multi-agent coordinator with character debates
    coordinator = MultiAgentCoordinator(provider="openai")
    
    # Register all character specialists
    hermione = InventoryManagerAgent(provider="openai")
    gekko = PricingAnalystAgent(provider="openai")  
    elle = CustomerServiceAgent(provider="openai")
    tyrion = StrategyPlannerAgent(provider="openai")
    jack = CrisisManagerAgent(provider="openai")
    
    coordinator.register_specialist(hermione)
    coordinator.register_specialist(gekko)
    coordinator.register_specialist(elle)
    coordinator.register_specialist(tyrion)
    coordinator.register_specialist(jack)
    
    print(f"📋 CHARACTERS REGISTERED: HERMIONE, GEKKO, ELLE, TYRION, JACK")
    
    # Create a crisis business scenario that should trigger debates
    crisis_store_status = {
        'day': 15,
        'cash': 50.25,  # Low cash situation
        'inventory': {
            'Coke': 0,      # Complete stockout
            'Chips': 1,     # Critical low stock
            'Candy': 0,     # Complete stockout
            'Gum': 3,       # Low stock
            'Cookies': 8    # Adequate stock
        },
        'war_intensity': 9,  # High competitive pressure
        'recent_sales': {
            'Coke': 15,
            'Chips': 12,
            'Candy': 8
        }
    }
    
    crisis_context = {
        'yesterday_summary': {
            'revenue': 45.50,
            'profit': -12.30,
            'units_sold_by_product': {
                'Coke': 8,
                'Chips': 6,
                'Candy': 4,
                'Gum': 2,
                'Cookies': 3
            }
        },
        'competitor_moves': {
            'aggressive_pricing': True,
            'promotional_campaigns': True
        },
        'market_conditions': {
            'season': 'peak_summer',
            'weather': 'hot',
            'customer_traffic': 'high'
        }
    }
    
    print(f"\n🚨 CRISIS SCENARIO INITIATED:")
    print(f"   💰 Cash: ${crisis_store_status['cash']:.2f} (LOW)")
    print(f"   📦 Stockouts: Coke, Candy (CRITICAL)")
    print(f"   ⚔️ War Intensity: {crisis_store_status['war_intensity']}/10 (EXTREME)")
    print(f"   📉 Yesterday Profit: ${crisis_context['yesterday_summary']['profit']:.2f} (LOSS)")
    
    # Run the coordination system (this should trigger character debates)
    print(f"\n🎯 INITIATING CHARACTER COORDINATION...")
    try:
        consensus = coordinator.coordinate_decisions(crisis_store_status, crisis_context)
        
        print(f"\n📊 COORDINATION RESULTS:")
        print(f"   Decisions Made: {len(consensus.final_decisions)}")
        print(f"   Overall Confidence: {consensus.overall_confidence:.2f}")
        print(f"   Debate Occurred: {'YES' if consensus.debate_occurred else 'NO'}")
        print(f"   Coordination Notes: {consensus.coordination_notes}")
        
        if consensus.debate_resolution:
            print(f"\n🏆 DEBATE RESOLUTION:")
            print(f"   Topic: {consensus.debate_resolution.business_decision['decision_type']}")
            print(f"   Winner: {consensus.debate_resolution.winning_position.character_name.upper() if consensus.debate_resolution.winning_position else 'None'}")
            print(f"   Summary: {consensus.debate_resolution.debate_summary}")
            print(f"   Consensus Achieved: {'YES' if consensus.debate_resolution.consensus_achieved else 'NO'}")
            
            # Show character votes
            if consensus.debate_resolution.character_votes:
                print(f"\n🗳️ CHARACTER VOTING RESULTS:")
                for voter, candidate in consensus.debate_resolution.character_votes.items():
                    print(f"   {voter.upper()} voted for: {candidate.upper()}")
        
        # Show individual character decisions
        print(f"\n🎭 CHARACTER SPECIALIST DECISIONS:")
        for decision in consensus.final_decisions:
            character_name = get_character_name_from_role(decision.agent_role)
            print(f"\n   {character_name.upper()} ({decision.agent_role.value}):")
            print(f"     Decision: {decision.decision_type}")
            print(f"     Priority: {decision.priority}/10")
            print(f"     Confidence: {decision.confidence:.2f}")
            print(f"     Reasoning: {decision.reasoning[:150]}...")
            
    except Exception as e:
        print(f"❌ ERROR during character coordination: {e}")
        import traceback
        traceback.print_exc()
    
    # Show debate engine statistics
    print(f"\n📈 DEBATE ENGINE STATISTICS:")
    coordinator_summary = coordinator.get_coordination_summary()
    print(f"   Total Debates: {coordinator_summary.get('total_debates', 0)}")
    print(f"   Debate Rate: {coordinator_summary.get('debate_rate', '0%')}")
    print(f"   Last Debate Topic: {coordinator_summary.get('last_debate_topic', 'None')}")
    print(f"   Last Debate Winner: {coordinator_summary.get('last_debate_winner', 'None')}")
    print(f"   Active Specialists: {len(coordinator_summary.get('active_specialists', []))}")
    
    print(f"\n✅ CHARACTER DEBATE SYSTEM TEST COMPLETED")
    print("="*80)

def test_specific_debate_topic():
    """Test a specific debate topic directly"""
    
    print(f"\n🎯 TESTING SPECIFIC DEBATE TOPIC: INVENTORY ALLOCATION")
    
    # Initialize debate engine
    debate_engine = CharacterDebateEngine(provider="openai")
    
    # Create inventory crisis scenario
    store_status = {
        'day': 20,
        'cash': 75.00,
        'inventory': {
            'Coke': 0,      # Stockout
            'Chips': 1,     # Critical
            'Candy': 0,     # Stockout
            'Gum': 2,       # Low
            'Cookies': 5    # Adequate
        }
    }
    
    context = {
        'yesterday_summary': {
            'units_sold_by_product': {
                'Coke': 12,  # High demand
                'Chips': 8,
                'Candy': 6,
                'Gum': 3,
                'Cookies': 2
            }
        }
    }
    
    # Create conflicting decisions that should trigger debate
    triggering_decisions = [
        AgentDecision(
            agent_role=AgentRole.INVENTORY_MANAGER,
            decision_type="emergency_restock",
            parameters={'products': ['Coke', 'Candy']},
            confidence=0.9,
            reasoning="Critical stockouts need immediate attention",
            priority=9
        ),
        AgentDecision(
            agent_role=AgentRole.CUSTOMER_SERVICE,
            decision_type="customer_retention_focus",
            parameters={'priority': 'customer_satisfaction'},
            confidence=0.8,
            reasoning="Must prioritize customer experience over profits",
            priority=8
        ),
        AgentDecision(
            agent_role=AgentRole.STRATEGIC_PLANNER,
            decision_type="strategic_product_mix",
            parameters={'focus': 'high_margin_products'},
            confidence=0.85,
            reasoning="Focus on profitable product mix for long-term success",
            priority=7
        )
    ]
    
    try:
        # Initiate the debate
        resolution = debate_engine.initiate_debate(
            DebateTopicType.INVENTORY_ALLOCATION,
            store_status,
            context,
            triggering_decisions
        )
        
        print(f"\n🎊 DEBATE COMPLETED SUCCESSFULLY!")
        print(f"   Business Decision: {resolution.business_decision}")
        
    except Exception as e:
        print(f"❌ ERROR during specific debate test: {e}")
        import traceback
        traceback.print_exc()

def get_character_name_from_role(agent_role):
    """Helper function to get character name from agent role"""
    role_to_character = {
        AgentRole.INVENTORY_MANAGER: "hermione",
        AgentRole.PRICING_ANALYST: "gekko", 
        AgentRole.CUSTOMER_SERVICE: "elle",
        AgentRole.STRATEGIC_PLANNER: "tyrion",
        AgentRole.CRISIS_MANAGER: "jack"
    }
    return role_to_character.get(agent_role, "unknown")

if __name__ == "__main__":
    # Run the comprehensive test
    test_character_debate_system()
    
    # Uncomment to test specific debate topic
    # test_specific_debate_topic() 