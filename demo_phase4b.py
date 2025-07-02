#!/usr/bin/env python3
"""
🎭 Phase 4B Character Debate System Demo

Demonstrates the revolutionary character-driven business decision making system.
Shows how fictional characters debate business strategy with unique personalities.

This demo showcases the architecture and features without requiring API calls.
"""

import sys
import json
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

# Import Phase 4B components
from src.core.character_debate_engine import (
    CharacterDebateEngine, DebateTopicType, DebateStance, 
    CharacterPosition, CharacterRebuttal, DebateResolution
)
from src.core.multi_agent_engine import MultiAgentCoordinator, AgentRole, AgentDecision

def demo_character_debate_architecture():
    """Demonstrate the Phase 4B character debate system architecture"""
    
    print("\n" + "🎭" * 40)
    print("PHASE 4B: CHARACTER DEBATE SYSTEM DEMO")
    print("Revolutionary AI Business Decision Making")
    print("🎭" * 40)
    
    print("\n📋 SYSTEM ARCHITECTURE:")
    print("="*50)
    
    # Show character relationship matrix
    print("\n🤝 CHARACTER RELATIONSHIP DYNAMICS:")
    print("   (Scale: -1.0 to +1.0, where -1.0 = strong conflict, +1.0 = strong alliance)")
    
    relationships = {
        "HERMIONE": {"GEKKO": -0.3, "ELLE": 0.4, "TYRION": 0.6, "JACK": 0.1},
        "GEKKO": {"HERMIONE": -0.3, "ELLE": -0.2, "TYRION": 0.2, "JACK": 0.5},
        "ELLE": {"HERMIONE": 0.4, "GEKKO": -0.2, "TYRION": 0.3, "JACK": -0.1},
        "TYRION": {"HERMIONE": 0.6, "GEKKO": 0.2, "ELLE": 0.3, "JACK": 0.1},
        "JACK": {"HERMIONE": 0.1, "GEKKO": 0.5, "ELLE": -0.1, "TYRION": 0.1}
    }
    
    for character, relations in relationships.items():
        print(f"\n   {character}:")
        for other, score in relations.items():
            emoji = "🤝" if score > 0.2 else "⚔️" if score < -0.1 else "🤷"
            print(f"     {emoji} {other}: {score:+.1f}")
    
    # Show debate topics and triggers
    print(f"\n🎯 DEBATE TOPICS & TRIGGERS:")
    debate_topics = {
        "PRICING_STRATEGY": {
            "description": "Competitive pricing and market positioning",
            "key_players": ["GEKKO", "HERMIONE", "TYRION"],
            "trigger": "High competitive pressure or pricing conflicts"
        },
        "INVENTORY_ALLOCATION": {
            "description": "Resource allocation during supply constraints",
            "key_players": ["HERMIONE", "ELLE", "TYRION"],
            "trigger": "Multiple stockouts or supply chain crisis"
        },
        "CRISIS_RESPONSE": {
            "description": "Emergency business situation handling",
            "key_players": ["JACK", "TYRION", "HERMIONE"],
            "trigger": "Business emergency or system failure"
        }
    }
    
    for topic, info in debate_topics.items():
        print(f"\n   📌 {topic}:")
        print(f"      Description: {info['description']}")
        print(f"      Key Players: {', '.join(info['key_players'])}")
        print(f"      Trigger: {info['trigger']}")
    
    # Show character specializations
    print(f"\n🎭 CHARACTER SPECIALIZATIONS:")
    character_specs = {
        "HERMIONE GRANGER": {
            "role": "Inventory Manager",
            "traits": ["Methodical", "Data-driven", "Perfectionist"],
            "expertise": ["Stock optimization", "Supply chain", "Analytics"],
            "catchphrase": "Honestly! The numbers don't lie!"
        },
        "GORDON GEKKO": {
            "role": "Pricing Analyst", 
            "traits": ["Aggressive", "Profit-focused", "Competitive"],
            "expertise": ["Market positioning", "Competitive analysis", "Revenue optimization"],
            "catchphrase": "Greed is good, but precision is better!"
        },
        "ELLE WOODS": {
            "role": "Customer Service",
            "traits": ["Optimistic", "People-focused", "Relationship-builder"],
            "expertise": ["Customer experience", "Brand loyalty", "Communication"],
            "catchphrase": "Happy customers are profitable customers!"
        },
        "TYRION LANNISTER": {
            "role": "Strategic Planner",
            "traits": ["Cunning", "Long-term thinker", "Diplomatic"],
            "expertise": ["Strategic planning", "Risk assessment", "Negotiation"],
            "catchphrase": "I drink and I know things about business!"
        },
        "JACK BAUER": {
            "role": "Crisis Manager",
            "traits": ["Decisive", "Action-oriented", "Intense"],
            "expertise": ["Emergency response", "Rapid decision-making", "Problem-solving"],
            "catchphrase": "We don't have time for analysis paralysis!"
        }
    }
    
    for character, info in character_specs.items():
        print(f"\n   🎭 {character} - {info['role']}:")
        print(f"      Traits: {', '.join(info['traits'])}")
        print(f"      Expertise: {', '.join(info['expertise'])}")
        print(f"      Catchphrase: \"{info['catchphrase']}\"")

def demo_crisis_scenario():
    """Demonstrate a crisis scenario that would trigger character debates"""
    
    print(f"\n🚨 CRISIS SCENARIO SIMULATION")
    print("="*40)
    
    # Crisis scenario
    crisis_data = {
        "day": 18,
        "cash": 42.75,
        "inventory": {
            "Coke": 0,      # Critical stockout
            "Chips": 1,     # Dangerously low
            "Candy": 0,     # Critical stockout  
            "Gum": 2,       # Low stock
            "Cookies": 7    # Adequate
        },
        "war_intensity": 9,
        "competitor_actions": ["Aggressive pricing", "Promotional campaigns", "Product bundling"],
        "customer_complaints": 5,
        "yesterday_loss": -18.50
    }
    
    print(f"\n📊 CRISIS METRICS:")
    print(f"   💰 Cash Reserve: ${crisis_data['cash']:.2f} (CRITICAL)")
    print(f"   📦 Stockouts: {sum(1 for v in crisis_data['inventory'].values() if v == 0)} products")
    print(f"   ⚔️ Competitive Pressure: {crisis_data['war_intensity']}/10 (EXTREME)")
    print(f"   😡 Customer Complaints: {crisis_data['customer_complaints']}")
    print(f"   📉 Yesterday's Loss: ${crisis_data['yesterday_loss']:.2f}")
    
    # Character responses (simulated)
    character_responses = {
        "HERMIONE": {
            "position": "We need systematic inventory analysis and emergency restocking",
            "stance": "STRONGLY_AGREE",
            "priority": 9,
            "reasoning": "Mathematical analysis shows we're losing £2.50 per hour due to stockouts. Emergency action required!"
        },
        "GEKKO": {
            "position": "Aggressive pricing war to crush competition immediately",
            "stance": "STRONGLY_AGREE", 
            "priority": 8,
            "reasoning": "This is WAR! We price below cost, drive them out, then dominate the market!"
        },
        "ELLE": {
            "position": "Focus on customer retention through superior service",
            "stance": "AGREE",
            "priority": 7,
            "reasoning": "Customers are our greatest asset! Let's turn this crisis into loyalty opportunity!"
        },
        "TYRION": {
            "position": "Strategic retreat and resource consolidation",
            "stance": "NEUTRAL",
            "priority": 6,
            "reasoning": "Sometimes the best strategy is knowing when to fight and when to regroup."
        },
        "JACK": {
            "position": "Immediate emergency protocols and rapid response",
            "stance": "STRONGLY_AGREE",
            "priority": 10,
            "reasoning": "Every second counts! We implement emergency measures NOW!"
        }
    }
    
    print(f"\n🎭 CHARACTER POSITIONS:")
    for character, response in character_responses.items():
        stance_emoji = "🔥" if response["stance"] == "STRONGLY_AGREE" else "👍" if response["stance"] == "AGREE" else "🤷"
        print(f"\n   {stance_emoji} {character} (Priority: {response['priority']}/10):")
        print(f"      Position: {response['position']}")
        print(f"      Reasoning: \"{response['reasoning']}\"")
    
    # Simulated debate outcome
    print(f"\n🏆 DEBATE RESOLUTION SIMULATION:")
    print(f"   Topic: CRISIS_RESPONSE")
    print(f"   Participants: JACK, HERMIONE, GEKKO, ELLE, TYRION")
    print(f"   Winner: JACK BAUER (Emergency Response)")
    print(f"   Consensus: 3/5 characters agreed on immediate action")
    print(f"   Business Decision: Implement emergency protocols with systematic inventory support")
    
    # Show character vote simulation
    print(f"\n🗳️ VOTING RESULTS:")
    votes = {
        "JACK": "JACK",        # Self-vote
        "HERMIONE": "JACK",    # Agrees on urgency
        "GEKKO": "JACK",       # Respects decisive action
        "ELLE": "HERMIONE",    # Prefers systematic approach
        "TYRION": "TYRION"     # Strategic independence
    }
    
    vote_counts = {}
    for voter, candidate in votes.items():
        vote_counts[candidate] = vote_counts.get(candidate, 0) + 1
        print(f"   {voter} voted for: {candidate}")
    
    print(f"\n📊 FINAL VOTE COUNT:")
    for candidate, count in sorted(vote_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(votes)) * 100
        print(f"   {candidate}: {count}/5 votes ({percentage:.1f}%)")

def demo_system_integration():
    """Demonstrate how Phase 4B integrates with existing systems"""
    
    print(f"\n🔗 SYSTEM INTEGRATION DEMO")
    print("="*35)
    
    print(f"\n📊 MULTI-AGENT COORDINATOR STATUS:")
    print(f"   Mode: CHARACTER_ENSEMBLE")
    print(f"   Active Specialists: 5/5")
    print(f"   Debate System: OPERATIONAL")
    print(f"   Debate Threshold: 2 conflicting decisions")
    print(f"   Consensus Algorithm: EXPERTISE_WEIGHTED_VOTING")
    
    print(f"\n🎯 INTEGRATION CAPABILITIES:")
    integration_features = [
        "Single-agent compatibility (hybrid mode)",
        "Real-time character debate triggering", 
        "Personality-driven conflict resolution",
        "Business decision synthesis",
        "Character relationship learning",
        "Debate history tracking",
        "Performance analytics"
    ]
    
    for i, feature in enumerate(integration_features, 1):
        print(f"   {i}. {feature}")
    
    print(f"\n⚙️ SYSTEM MODES:")
    modes = {
        "SINGLE": "Traditional Scrooge-only decision making",
        "HYBRID": "Scrooge + character analysis (Phase 4A)",
        "MULTI": "Full character ensemble debates (Phase 4B)"
    }
    
    for mode, description in modes.items():
        print(f"   🔧 {mode}: {description}")
    
    print(f"\n📈 PHASE 4B BENEFITS:")
    benefits = [
        "Reduced decision-making bias through character diversity",
        "Enhanced creativity via personality conflicts",
        "Improved problem-solving through multiple perspectives", 
        "Transparent decision rationale with character reasoning",
        "Engaging business intelligence with fictional personalities",
        "Scalable conflict resolution for complex scenarios"
    ]
    
    for benefit in benefits:
        print(f"   ✅ {benefit}")

def main():
    """Run the complete Phase 4B demo"""
    
    print("🎭 SHELFMIND PHASE 4B DEMONSTRATION")
    print("Advanced Character Debate System")
    print("World's First Character-Driven Business AI")
    
    try:
        # Architecture overview
        demo_character_debate_architecture()
        
        # Crisis scenario
        demo_crisis_scenario()
        
        # System integration
        demo_system_integration()
        
        print(f"\n🎊 PHASE 4B DEMO COMPLETED!")
        print("="*50)
        
        print(f"\nNext Steps:")
        print(f"1. Run 'python tests/test_character_debates.py' for live testing")
        print(f"2. Integrate with store engine for real-time debates")
        print(f"3. Implement specialized character tools (Phase 4B.2)")
        print(f"4. Add character evolution and learning (Phase 4B.3)")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 