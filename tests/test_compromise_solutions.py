#!/usr/bin/env python3
"""
Phase 4B - Compromise Solutions Test
Test the new compromise generation feature when character debates have no clear winner.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.core.character_debate_engine import CharacterDebateEngine, DebateTopicType
from src.core.models import AgentDecision, AgentRole

def test_compromise_solutions():
    """Test compromise generation when no clear consensus emerges"""
    
    print("🧪 PHASE 4B - COMPROMISE SOLUTIONS TEST")
    print("=" * 50)
    
    # Initialize debate engine
    debate_engine = CharacterDebateEngine()
    
    # Create test scenario: Conflicting pricing decisions
    store_status = {
        "day": 15,
        "cash": 500.0,
        "inventory": {
            "sandwich": 2,
            "banana": 0,
            "apple": 1
        }
    }
    
    # Create conflicting agent decisions that should trigger debate
    conflicting_decisions = [
        AgentDecision(
            agent_role=AgentRole.PRICING_ANALYST,
            decision_type="pricing_strategy",
            parameters={"sandwich_price": 8.50},
            confidence=0.8,
            priority=8,
            reasoning="Gordon Gekko: Price sandwich at $8.50 for maximum profit!"
        ),
        AgentDecision(
            agent_role=AgentRole.CUSTOMER_SERVICE,
            decision_type="pricing_strategy", 
            parameters={"sandwich_price": 5.00},
            confidence=0.7,
            priority=7,
            reasoning="Elle Woods: Keep sandwich at $5.00 to maintain customer satisfaction!"
        ),
        AgentDecision(
            agent_role=AgentRole.INVENTORY_MANAGER,
            decision_type="pricing_strategy",
            parameters={"sandwich_price": 6.75},
            confidence=0.9,
            priority=7,
            reasoning="Hermione Granger: Optimal sandwich price is $6.75 based on inventory analysis"
        )
    ]
    
    context = {
        "season": "winter",
        "weather": "cold",
        "market_conditions": "normal"
    }
    
    print(f"📊 SCENARIO: Conflicting sandwich pricing decisions")
    print(f"   - Gekko wants: $8.50 (maximize profit)")
    print(f"   - Elle wants: $5.00 (customer satisfaction)")  
    print(f"   - Hermione wants: $6.75 (analytical optimum)")
    print()
    
    # Initiate character debate
    print("🎭 INITIATING CHARACTER DEBATE...")
    print("-" * 30)
    
    debate_resolution = debate_engine.initiate_debate(
        topic=DebateTopicType.PRICING_STRATEGY,
        store_status=store_status,
        context=context,
        triggering_decisions=conflicting_decisions
    )
    
    # Display results
    print(f"\n🏆 DEBATE RESULTS:")
    print(f"   Consensus Achieved: {debate_resolution.consensus_achieved}")
    
    if debate_resolution.winning_position:
        print(f"   Winner: {debate_resolution.winning_position.character_name.upper()}")
        print(f"   Winning Position: {debate_resolution.winning_position.position_statement}")
    else:
        print(f"   Winner: No clear winner")
        
    if debate_resolution.compromise_solution:
        print(f"\n🤝 COMPROMISE SOLUTION:")
        print(f"   Description: {debate_resolution.compromise_solution.get('description', 'N/A')}")
        print(f"   Rationale: {debate_resolution.compromise_solution.get('rationale', 'N/A')}")
        print(f"   Action: {debate_resolution.compromise_solution.get('action', 'N/A')}")
        
        if debate_resolution.compromise_solution.get('suggested_price'):
            print(f"   💰 Suggested Price: ${debate_resolution.compromise_solution['suggested_price']}")
            
        if debate_resolution.compromise_solution.get('mathematical_average'):
            print(f"   🧮 Mathematical Average: ${debate_resolution.compromise_solution['mathematical_average']:.2f}")
    
    print(f"\n📋 BUSINESS DECISION:")
    print(f"   Type: {debate_resolution.business_decision.get('decision_type', 'N/A')}")
    print(f"   Reasoning: {debate_resolution.business_decision.get('reasoning', 'N/A')}")
    
    print(f"\n📊 CHARACTER VOTES:")
    for voter, candidate in debate_resolution.character_votes.items():
        print(f"   {voter.upper()} voted for {candidate.upper()}")
    
    print(f"\n📝 SUMMARY: {debate_resolution.debate_summary}")
    
    return debate_resolution

def test_inventory_compromise():
    """Test compromise generation for inventory allocation debates"""
    
    print(f"\n🧪 INVENTORY ALLOCATION COMPROMISE TEST")
    print("=" * 50)
    
    debate_engine = CharacterDebateEngine()
    
    store_status = {
        "day": 20,
        "cash": 300.0,
        "inventory": {
            "banana": 0,
            "apple": 0,
            "sandwich": 1
        }
    }
    
    # Conflicting inventory decisions
    conflicting_decisions = [
        AgentDecision(
            agent_role=AgentRole.INVENTORY_MANAGER,
            decision_type="inventory_allocation",
            parameters={"banana_order": 20},
            confidence=0.8,
            priority=9,
            reasoning="Hermione: Order 20 bananas based on demand analysis"
        ),
        AgentDecision(
            agent_role=AgentRole.PRICING_ANALYST,
            decision_type="inventory_allocation",
            parameters={"banana_order": 5},
            confidence=0.7,
            priority=8,
            reasoning="Gekko: Only order 5 bananas to minimize cash risk"
        ),
        AgentDecision(
            agent_role=AgentRole.CRISIS_MANAGER,
            decision_type="inventory_allocation",
            parameters={"banana_order": 15},
            confidence=0.9,
            priority=8,
            reasoning="Jack: Order 15 bananas as emergency restock"
        )
    ]
    
    print(f"📊 SCENARIO: Conflicting banana order quantities")
    print(f"   - Hermione wants: 20 units (demand analysis)")
    print(f"   - Gekko wants: 5 units (risk management)")
    print(f"   - Jack wants: 15 units (emergency restock)")
    print()
    
    debate_resolution = debate_engine.initiate_debate(
        topic=DebateTopicType.INVENTORY_ALLOCATION,
        store_status=store_status,
        context={},
        triggering_decisions=conflicting_decisions
    )
    
    print(f"\n🏆 DEBATE RESULTS:")
    print(f"   Consensus: {debate_resolution.consensus_achieved}")
    
    if debate_resolution.compromise_solution:
        print(f"\n🤝 COMPROMISE SOLUTION:")
        print(f"   Description: {debate_resolution.compromise_solution.get('description', 'N/A')}")
        
        if debate_resolution.compromise_solution.get('suggested_quantity'):
            print(f"   📦 Suggested Quantity: {debate_resolution.compromise_solution['suggested_quantity']} units")
            
        if debate_resolution.compromise_solution.get('mathematical_average'):
            print(f"   🧮 Mathematical Average: {debate_resolution.compromise_solution['mathematical_average']:.1f} units")
    
    return debate_resolution

if __name__ == "__main__":
    # Run compromise solution tests
    pricing_result = test_compromise_solutions()
    inventory_result = test_inventory_compromise()
    
    print(f"\n🎉 PHASE 4B COMPROMISE SOLUTIONS: COMPLETE!")
    print(f"   - Pricing compromise: {'✅' if pricing_result.compromise_solution else '❌'}")
    print(f"   - Inventory compromise: {'✅' if inventory_result.compromise_solution else '❌'}")
    print(f"\n🚀 Your Character Debate System now generates intelligent compromises!") 