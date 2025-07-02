from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import json
import random
from openai import OpenAI
import os
from dotenv import load_dotenv

from src.core.multi_agent_engine import AgentRole, AgentDecision
from src.core.agent_prompts import AgentPrompts

load_dotenv()

class DebateTopicType(Enum):
    """Types of business debates that characters can engage in"""
    PRICING_STRATEGY = "pricing_strategy"
    INVENTORY_ALLOCATION = "inventory_allocation"
    CRISIS_RESPONSE = "crisis_response"
    STRATEGIC_PLANNING = "strategic_planning"
    CUSTOMER_SERVICE = "customer_service"
    COMPETITIVE_WARFARE = "competitive_warfare"

class DebateStance(Enum):
    """Character's stance in a debate"""
    STRONGLY_AGREE = "strongly_agree"
    AGREE = "agree"
    NEUTRAL = "neutral"
    DISAGREE = "disagree"
    STRONGLY_DISAGREE = "strongly_disagree"

@dataclass
class CharacterPosition:
    """Represents a character's position in a debate"""
    character_name: str
    agent_role: AgentRole
    stance: DebateStance
    position_statement: str
    supporting_arguments: List[str]
    confidence: float
    personality_reasoning: str

@dataclass
class CharacterRebuttal:
    """Represents a character's response to other positions"""
    character_name: str
    target_character: str
    rebuttal_text: str
    agreement_points: List[str]
    disagreement_points: List[str]
    personality_response: str

@dataclass
class DebateResolution:
    """Final outcome of a character debate"""
    winning_position: Optional[CharacterPosition]
    consensus_achieved: bool
    compromise_solution: Optional[Dict[str, Any]]
    character_votes: Dict[str, str]  # character_name -> vote_for_character
    debate_summary: str
    business_decision: Dict[str, Any]

class CharacterDebateEngine:
    """🎭 Phase 4B: Character Debate Engine
    
    Orchestrates structured debates between fictional character specialists.
    Creates engaging character-driven business decision making with personality conflicts.
    """
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        if provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-4.1-mini"
        else:
            raise NotImplementedError("Only OpenAI provider supported for debates currently")
            
        self.debate_history = []
        self.character_relationships = self._initialize_character_relationships()
        self.debate_topics = self._initialize_debate_topics()
        
    def _initialize_character_relationships(self) -> Dict[str, Dict[str, float]]:
        """Initialize character relationship dynamics (-1.0 to 1.0)"""
        return {
            "hermione": {
                "gekko": -0.3,      # Analytical vs Aggressive tension
                "elle": 0.4,        # Both detail-oriented, mutual respect
                "tyrion": 0.6,      # Intellectual alliance
                "jack": 0.1         # Neutral - different approaches
            },
            "gekko": {
                "hermione": -0.3,   # Impatient with over-analysis
                "elle": -0.2,       # Dismissive of "soft" customer focus
                "tyrion": 0.2,      # Respects strategic thinking
                "jack": 0.5         # Both aggressive, action-oriented
            },
            "elle": {
                "hermione": 0.4,    # Appreciates thoroughness
                "gekko": -0.2,      # Dislikes ruthless approach
                "tyrion": 0.3,      # Finds him charming and clever
                "jack": -0.1        # Concerned by his intensity
            },
            "tyrion": {
                "hermione": 0.6,    # Respects intellectual rigor
                "gekko": 0.2,       # Understands ambition
                "elle": 0.3,        # Enjoys her optimism
                "jack": 0.1         # Wary of his extremism
            },
            "jack": {
                "hermione": 0.1,    # Respects competence but impatient
                "gekko": 0.5,       # Shared aggressive mindset
                "elle": -0.1,       # Sees her as naive
                "tyrion": 0.1       # Cautious respect
            }
        }
        
    def _initialize_debate_topics(self) -> Dict[DebateTopicType, Dict]:
        """Initialize debate topic configurations"""
        return {
            DebateTopicType.PRICING_STRATEGY: {
                "description": "How aggressively should we respond to competitor pricing?",
                "key_stakeholders": ["gekko", "hermione", "tyrion"],
                "urgency_threshold": 7,
                "expected_positions": {
                    "gekko": "aggressive_pricing",
                    "hermione": "calculated_approach", 
                    "tyrion": "strategic_positioning"
                }
            },
            DebateTopicType.INVENTORY_ALLOCATION: {
                "description": "Which products should get priority during supply constraints?",
                "key_stakeholders": ["hermione", "elle", "tyrion"],
                "urgency_threshold": 8,
                "expected_positions": {
                    "hermione": "mathematical_optimization",
                    "elle": "customer_satisfaction_first",
                    "tyrion": "strategic_product_mix"
                }
            },
            DebateTopicType.CRISIS_RESPONSE: {
                "description": "How should we respond to this business emergency?",
                "key_stakeholders": ["jack", "tyrion", "hermione"],
                "urgency_threshold": 9,
                "expected_positions": {
                    "jack": "immediate_action",
                    "tyrion": "strategic_response",
                    "hermione": "systematic_analysis"
                }
            }
        }
        
    def initiate_debate(self, topic: DebateTopicType, store_status: Dict, context: Dict, 
                       triggering_decisions: List[AgentDecision]) -> DebateResolution:
        """🎭 Initiate a structured character debate on a business topic"""
        
        print(f"\n🎭 CHARACTER DEBATE INITIATED: {topic.value.upper()}")
        print("="*70)
        
        # Step 1: Identify debate participants
        participants = self._select_debate_participants(topic, triggering_decisions)
        print(f"📋 PARTICIPANTS: {', '.join([p.upper() for p in participants])}")
        
        # Step 2: Generate character positions
        positions = self._generate_character_positions(topic, participants, store_status, context, triggering_decisions)
        
        # Step 3: Present initial positions
        self._present_initial_positions(positions)
        
        # Step 4: Generate rebuttals and counter-arguments
        rebuttals = self._generate_character_rebuttals(positions, store_status, context)
        
        # Step 5: Build consensus or identify irreconcilable differences
        resolution = self._build_debate_consensus(topic, positions, rebuttals, store_status, context)
        
        # Step 6: Record debate in history
        self._record_debate_history(topic, positions, rebuttals, resolution)
        
        print(f"\n🏆 DEBATE RESOLUTION: {resolution.debate_summary}")
        print("="*70)
        
        return resolution
        
    def _select_debate_participants(self, topic: DebateTopicType, triggering_decisions: List[AgentDecision]) -> List[str]:
        """Select which characters should participate in this debate"""
        topic_config = self.debate_topics[topic]
        key_stakeholders = topic_config["key_stakeholders"]
        
        # Always include key stakeholders
        participants = key_stakeholders.copy()
        
        # Add characters whose decisions triggered the debate
        for decision in triggering_decisions:
            character_name = self._get_character_name_from_role(decision.agent_role)
            if character_name and character_name not in participants:
                participants.append(character_name)
                
        # Ensure we have 3-5 participants for a good debate
        if len(participants) < 3:
            # Add random participants to reach minimum
            all_characters = ["hermione", "gekko", "elle", "tyrion", "jack"]
            for char in all_characters:
                if char not in participants and len(participants) < 3:
                    participants.append(char)
                    
        return participants[:5]  # Maximum 5 participants
        
    def _generate_character_positions(self, topic: DebateTopicType, participants: List[str], 
                                    store_status: Dict, context: Dict, 
                                    triggering_decisions: List[AgentDecision]) -> List[CharacterPosition]:
        """Generate each character's position on the debate topic"""
        positions = []
        
        for character_name in participants:
            try:
                # Get character personality and expertise
                agent_role = self._get_agent_role_from_character(character_name)
                
                # Generate character's position using AI
                position = self._generate_single_character_position(
                    character_name, agent_role, topic, store_status, context, triggering_decisions
                )
                positions.append(position)
                
            except Exception as e:
                print(f"Warning: Failed to generate position for {character_name}: {e}")
                
        return positions
        
    def _generate_single_character_position(self, character_name: str, agent_role: AgentRole, 
                                          topic: DebateTopicType, store_status: Dict, context: Dict,
                                          triggering_decisions: List[AgentDecision]) -> CharacterPosition:
        """Generate a single character's position on the debate topic"""
        
        # Create debate prompt for this character
        prompt = self._create_character_debate_prompt(character_name, agent_role, topic, store_status, context, triggering_decisions)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a specialist in character-driven business debates. Generate authentic character positions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8  # Higher temperature for more character personality
            )
            
            # Parse the response to extract position components
            position_data = self._parse_character_position_response(response.choices[0].message.content)
            
            return CharacterPosition(
                character_name=character_name,
                agent_role=agent_role,
                stance=DebateStance(position_data.get("stance", "neutral")),
                position_statement=position_data.get("position_statement", ""),
                supporting_arguments=position_data.get("supporting_arguments", []),
                confidence=position_data.get("confidence", 0.7),
                personality_reasoning=position_data.get("personality_reasoning", "")
            )
            
        except Exception as e:
            print(f"Error generating position for {character_name}: {e}")
            # Return default position
            return CharacterPosition(
                character_name=character_name,
                agent_role=agent_role,
                stance=DebateStance.NEUTRAL,
                position_statement=f"{character_name.upper()} is analyzing the situation...",
                supporting_arguments=["Analysis in progress"],
                confidence=0.5,
                personality_reasoning="Default response due to system error"
            )
            
    def _create_character_debate_prompt(self, character_name: str, agent_role: AgentRole, 
                                      topic: DebateTopicType, store_status: Dict, context: Dict,
                                      triggering_decisions: List[AgentDecision]) -> str:
        """Create a prompt for character position generation"""
        
        # Get character personality details
        personality = AgentPrompts.get_agent_personality(agent_role)
        
        # Build context about the business situation
        business_context = self._build_business_context(store_status, context, triggering_decisions)
        
        # Create debate-specific prompt
        prompt = f"""
PHASE 4B CHARACTER DEBATE - POSITION GENERATION

CHARACTER: {character_name.upper()} ({personality.get('name', character_name)})
EXPERTISE: {personality.get('expertise', 'Business Operations')}
DEBATE TOPIC: {topic.value.replace('_', ' ').title()}

PERSONALITY TRAITS:
{chr(10).join([f"- {trait}" for trait in personality.get('traits', [])])}

CATCHPHRASES:
{chr(10).join([f"- {phrase}" for phrase in personality.get('catchphrases', [])])}

BUSINESS CONTEXT:
{business_context}

TASK: Generate {character_name.upper()}'s position on this debate topic. Respond in character with their unique personality, expertise, and speaking style.

REQUIRED FORMAT:
STANCE: [strongly_agree|agree|neutral|disagree|strongly_disagree]
POSITION: [One clear sentence stating your position]
ARGUMENTS: [3-5 supporting arguments in character voice]
CONFIDENCE: [0.0-1.0 confidence level]
REASONING: [Personality-driven explanation in character voice with catchphrases]

Remember: Stay true to {character_name.upper()}'s personality while providing real business insight!
"""
        
        return prompt
        
    def _build_business_context(self, store_status: Dict, context: Dict, triggering_decisions: List[AgentDecision]) -> str:
        """Build formatted business context for debate prompts"""
        lines = []
        
        # Current store status
        lines.append(f"📊 STORE STATUS:")
        lines.append(f"  Day: {store_status.get('day', 'Unknown')}")
        lines.append(f"  Cash: ${store_status.get('cash', 0):.2f}")
        
        # Inventory situation
        inventory = store_status.get('inventory', {})
        stockouts = [k for k, v in inventory.items() if v == 0]
        low_stock = [k for k, v in inventory.items() if 0 < v <= 2]
        
        if stockouts:
            lines.append(f"  🚨 STOCKOUTS: {', '.join(stockouts)}")
        if low_stock:
            lines.append(f"  ⚠️ LOW STOCK: {', '.join(low_stock)}")
            
        return "\n".join(lines)
        
    def _parse_character_position_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response to extract position components"""
        position_data = {
            "stance": "neutral",
            "position_statement": "",
            "supporting_arguments": [],
            "confidence": 0.7,
            "personality_reasoning": ""
        }
        
        lines = response_text.strip().split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('STANCE:'):
                stance_text = line.replace('STANCE:', '').strip().lower()
                if stance_text in ['strongly_agree', 'agree', 'neutral', 'disagree', 'strongly_disagree']:
                    position_data["stance"] = stance_text
                    
            elif line.startswith('POSITION:'):
                position_data["position_statement"] = line.replace('POSITION:', '').strip()
                
            elif line.startswith('ARGUMENTS:'):
                current_section = "arguments"
                arg_text = line.replace('ARGUMENTS:', '').strip()
                if arg_text:
                    position_data["supporting_arguments"].append(arg_text)
                    
            elif line.startswith('CONFIDENCE:'):
                try:
                    conf_text = line.replace('CONFIDENCE:', '').strip()
                    position_data["confidence"] = float(conf_text)
                except ValueError:
                    position_data["confidence"] = 0.7
                    
            elif line.startswith('REASONING:'):
                current_section = "reasoning"
                reasoning_text = line.replace('REASONING:', '').strip()
                if reasoning_text:
                    position_data["personality_reasoning"] = reasoning_text
                    
            elif current_section == "arguments" and line.startswith('-'):
                position_data["supporting_arguments"].append(line[1:].strip())
                
            elif current_section == "reasoning":
                if position_data["personality_reasoning"]:
                    position_data["personality_reasoning"] += " " + line
                else:
                    position_data["personality_reasoning"] = line
                    
        return position_data
        
    def _present_initial_positions(self, positions: List[CharacterPosition]):
        """Present all character positions in debate format"""
        print(f"\n🎤 INITIAL POSITIONS PRESENTED:")
        print("-" * 50)
        
        for position in positions:
            print(f"\n{position.character_name.upper()} ({position.stance.value.replace('_', ' ').title()}):")
            print(f"📍 POSITION: {position.position_statement}")
            print(f"🎭 REASONING: {position.personality_reasoning}")
            if position.supporting_arguments:
                print(f"💡 ARGUMENTS:")
                for i, arg in enumerate(position.supporting_arguments[:3], 1):
                    print(f"   {i}. {arg}")
                    
    def _generate_character_rebuttals(self, positions: List[CharacterPosition], 
                                    store_status: Dict, context: Dict) -> List[CharacterRebuttal]:
        """Generate character responses to each other's positions"""
        rebuttals = []
        
        print(f"\n🗣️ CHARACTER REBUTTALS:")
        print("-" * 30)
        
        for position in positions:
            # Each character responds to 1-2 other positions they disagree with most
            target_positions = self._select_rebuttal_targets(position, positions)
            
            for target_position in target_positions:
                try:
                    rebuttal = self._generate_single_rebuttal(position, target_position, store_status, context)
                    rebuttals.append(rebuttal)
                    
                    # Display rebuttal
                    print(f"\n{position.character_name.upper()} → {target_position.character_name.upper()}:")
                    print(f"🎭 {rebuttal.rebuttal_text}")
                    
                except Exception as e:
                    print(f"Warning: Failed to generate rebuttal from {position.character_name} to {target_position.character_name}: {e}")
                    
        return rebuttals
        
    def _select_rebuttal_targets(self, position: CharacterPosition, all_positions: List[CharacterPosition]) -> List[CharacterPosition]:
        """Select which positions this character should rebut"""
        targets = []
        
        for other_position in all_positions:
            if other_position.character_name == position.character_name:
                continue
                
            # Check stance compatibility
            stance_conflict = self._calculate_stance_conflict(position.stance, other_position.stance)
            
            # Check character relationship
            relationship_score = self.character_relationships.get(
                position.character_name, {}
            ).get(other_position.character_name, 0.0)
            
            # More likely to rebut if stances conflict or poor relationship
            rebut_probability = stance_conflict + (abs(relationship_score) if relationship_score < 0 else 0)
            
            if rebut_probability > 0.5 and len(targets) < 2:  # Max 2 rebuttals per character
                targets.append(other_position)
                
        return targets
        
    def _calculate_stance_conflict(self, stance1: DebateStance, stance2: DebateStance) -> float:
        """Calculate conflict level between two stances (0.0 to 1.0)"""
        stance_values = {
            DebateStance.STRONGLY_DISAGREE: -2,
            DebateStance.DISAGREE: -1,
            DebateStance.NEUTRAL: 0,
            DebateStance.AGREE: 1,
            DebateStance.STRONGLY_AGREE: 2
        }
        
        diff = abs(stance_values[stance1] - stance_values[stance2])
        return min(diff / 4.0, 1.0)  # Normalize to 0-1
        
    def _generate_single_rebuttal(self, rebutting_position: CharacterPosition, 
                                target_position: CharacterPosition, 
                                store_status: Dict, context: Dict) -> CharacterRebuttal:
        """Generate a single character's rebuttal to another character's position"""
        
        # Create rebuttal prompt
        prompt = f"""
CHARACTER DEBATE REBUTTAL

REBUTTING CHARACTER: {rebutting_position.character_name.upper()}
TARGET CHARACTER: {target_position.character_name.upper()}

YOUR POSITION: {rebutting_position.position_statement}
THEIR POSITION: {target_position.position_statement}

TASK: Generate {rebutting_position.character_name.upper()}'s response to {target_position.character_name.upper()}'s position. 
Stay in character with personality and speaking style. Be respectful but firm in disagreements.

REQUIRED FORMAT:
REBUTTAL: [One paragraph response in character voice]
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are generating character rebuttals for business debates. Maintain character personality."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            
            rebuttal_text = response.choices[0].message.content.strip()
            if rebuttal_text.startswith('REBUTTAL:'):
                rebuttal_text = rebuttal_text.replace('REBUTTAL:', '').strip()
            
            return CharacterRebuttal(
                character_name=rebutting_position.character_name,
                target_character=target_position.character_name,
                rebuttal_text=rebuttal_text,
                agreement_points=[],
                disagreement_points=[],
                personality_response=rebuttal_text
            )
            
        except Exception as e:
            print(f"Error generating rebuttal: {e}")
            return CharacterRebuttal(
                character_name=rebutting_position.character_name,
                target_character=target_position.character_name,
                rebuttal_text=f"{rebutting_position.character_name.upper()}: I need more time to analyze {target_position.character_name.upper()}'s position.",
                agreement_points=[],
                disagreement_points=[],
                personality_response="System error occurred"
            )
        
    def _build_debate_consensus(self, topic: DebateTopicType, positions: List[CharacterPosition], 
                              rebuttals: List[CharacterRebuttal], store_status: Dict, context: Dict) -> DebateResolution:
        """Build consensus from character positions and rebuttals"""
        
        print(f"\n🤝 BUILDING CONSENSUS:")
        print("-" * 25)
        
        # Calculate character voting based on expertise and relationships
        character_votes = self._calculate_character_votes(positions, rebuttals)
        
        # Determine if consensus was achieved
        consensus_achieved, winning_position = self._determine_consensus_outcome(positions, character_votes)
        
        # Generate business decision from debate outcome
        business_decision = self._generate_business_decision(topic, winning_position, store_status)
        
        # Create debate summary
        debate_summary = self._create_debate_summary(topic, positions, consensus_achieved, winning_position)
        
        return DebateResolution(
            winning_position=winning_position,
            consensus_achieved=consensus_achieved,
            compromise_solution=None,
            character_votes=character_votes,
            debate_summary=debate_summary,
            business_decision=business_decision
        )
        
    def _calculate_character_votes(self, positions: List[CharacterPosition], 
                                 rebuttals: List[CharacterRebuttal]) -> Dict[str, str]:
        """Calculate which character each character would vote for"""
        votes = {}
        
        for position in positions:
            character = position.character_name
            
            # Vote for themselves by default
            best_candidate = character
            best_score = position.confidence
            
            # Consider other characters based on relationships and argument quality
            for other_position in positions:
                if other_position.character_name == character:
                    continue
                    
                # Calculate vote score based on relationship and argument strength
                relationship_score = self.character_relationships.get(character, {}).get(other_position.character_name, 0.0)
                argument_score = other_position.confidence
                
                total_score = (relationship_score * 0.3) + (argument_score * 0.7)
                
                if total_score > best_score:
                    best_candidate = other_position.character_name
                    best_score = total_score
                    
            votes[character] = best_candidate
            
        return votes
        
    def _determine_consensus_outcome(self, positions: List[CharacterPosition], 
                                   character_votes: Dict[str, str]) -> Tuple[bool, Optional[CharacterPosition]]:
        """Determine if consensus was achieved and who won"""
        
        # Count votes
        vote_counts = {}
        for voter, candidate in character_votes.items():
            vote_counts[candidate] = vote_counts.get(candidate, 0) + 1
            
        # Find winner
        if not vote_counts:
            return False, None
            
        winner_name = max(vote_counts.keys(), key=lambda k: vote_counts[k])
        winner_votes = vote_counts[winner_name]
        
        # Consensus achieved if winner has majority (>50%)
        total_votes = len(character_votes)
        consensus_achieved = winner_votes > total_votes / 2
        
        # Find winning position
        winning_position = None
        for position in positions:
            if position.character_name == winner_name:
                winning_position = position
                break
                
        print(f"📊 VOTING RESULTS:")
        for candidate, votes in vote_counts.items():
            percentage = (votes / total_votes) * 100
            print(f"   {candidate.upper()}: {votes}/{total_votes} votes ({percentage:.1f}%)")
            
        return consensus_achieved, winning_position
        
    def _generate_business_decision(self, topic: DebateTopicType, winning_position: Optional[CharacterPosition],
                                  store_status: Dict) -> Dict[str, Any]:
        """Generate actual business decision from debate outcome"""
        
        if not winning_position:
            return {
                "decision_type": "no_action",
                "reasoning": "No consensus achieved - maintaining status quo",
                "action_parameters": {}
            }
            
        return {
            "decision_type": topic.value,
            "reasoning": f"Following {winning_position.character_name.upper()}'s recommendation: {winning_position.position_statement}",
            "action_parameters": {
                "confidence": winning_position.confidence,
                "character_lead": winning_position.character_name
            }
        }
            
    def _create_debate_summary(self, topic: DebateTopicType, positions: List[CharacterPosition],
                             consensus_achieved: bool, winning_position: Optional[CharacterPosition]) -> str:
        """Create human-readable debate summary"""
        
        participant_names = [pos.character_name.upper() for pos in positions]
        
        if consensus_achieved and winning_position:
            return f"{winning_position.character_name.upper()} won consensus on {topic.value.replace('_', ' ')} among {', '.join(participant_names)}"
        else:
            return f"No consensus reached on {topic.value.replace('_', ' ')} among {', '.join(participant_names)} - compromise needed"
            
    def _record_debate_history(self, topic: DebateTopicType, positions: List[CharacterPosition],
                             rebuttals: List[CharacterRebuttal], resolution: DebateResolution):
        """Record debate in history for future reference"""
        self.debate_history.append({
            "topic": topic,
            "participants": [pos.character_name for pos in positions],
            "positions": positions,
            "rebuttals": rebuttals,
            "resolution": resolution,
            "timestamp": len(self.debate_history) + 1
        })
        
    def _get_character_name_from_role(self, agent_role: AgentRole) -> Optional[str]:
        """Convert agent role to character name"""
        role_to_character = {
            AgentRole.INVENTORY_MANAGER: "hermione",
            AgentRole.PRICING_ANALYST: "gekko",
            AgentRole.CUSTOMER_SERVICE: "elle",
            AgentRole.STRATEGIC_PLANNER: "tyrion",
            AgentRole.CRISIS_MANAGER: "jack"
        }
        return role_to_character.get(agent_role)
        
    def _get_agent_role_from_character(self, character_name: str) -> AgentRole:
        """Convert character name to agent role"""
        character_to_role = {
            "hermione": AgentRole.INVENTORY_MANAGER,
            "gekko": AgentRole.PRICING_ANALYST,
            "elle": AgentRole.CUSTOMER_SERVICE,
            "tyrion": AgentRole.STRATEGIC_PLANNER,
            "jack": AgentRole.CRISIS_MANAGER
        }
        return character_to_role.get(character_name, AgentRole.INVENTORY_MANAGER)
        
    def should_trigger_debate(self, agent_decisions: List[AgentDecision], store_status: Dict) -> Optional[DebateTopicType]:
        """Determine if current situation should trigger a character debate"""
        
        # Check for high-priority conflicting decisions
        high_priority_decisions = [d for d in agent_decisions if d.priority >= 7]
        
        if len(high_priority_decisions) >= 2:
            # Multiple high-priority decisions - likely conflict
            
            # Determine debate topic based on decision types
            decision_types = [d.decision_type for d in high_priority_decisions]
            
            if any("pricing" in dt.lower() for dt in decision_types):
                return DebateTopicType.PRICING_STRATEGY
            elif any("inventory" in dt.lower() for dt in decision_types):
                return DebateTopicType.INVENTORY_ALLOCATION
            elif any("crisis" in dt.lower() for dt in decision_types):
                return DebateTopicType.CRISIS_RESPONSE
            else:
                return DebateTopicType.STRATEGIC_PLANNING
                
        # Check for business crisis situations
        inventory = store_status.get('inventory', {})
        stockout_count = sum(1 for v in inventory.values() if v == 0)
        
        if stockout_count >= 2:
            return DebateTopicType.INVENTORY_ALLOCATION
            
        return None 