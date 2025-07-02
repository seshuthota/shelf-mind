from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import json
import random
import os
from dotenv import load_dotenv

# Optional AI imports - gracefully handle missing dependencies
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OpenAI = None
    OPENAI_AVAILABLE = False

from src.core.models import AgentRole, AgentDecision
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
        self.client = None
        self.model = None
        
        if provider == "openai" and OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-4.1-mini"
        elif provider == "mock":
            # Mock provider for testing
            self.client = None
            self.model = "mock"
        else:
            # No AI client available or unsupported provider
            self.client = None
            self.model = "no_ai"
            
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
        
        # Generate compromise solution if no clear consensus
        compromise_solution = None
        if not consensus_achieved:
            compromise_solution = self._generate_compromise_solution(topic, positions, character_votes)
            print(f"\n🤝 COMPROMISE SOLUTION:")
            print(f"   {compromise_solution.get('description', 'No compromise available')}")
        
        # Generate business decision from debate outcome (includes compromise)
        business_decision = self._generate_business_decision(topic, winning_position, store_status, compromise_solution)
        
        # Create debate summary
        debate_summary = self._create_debate_summary(topic, positions, consensus_achieved, winning_position)
        
        return DebateResolution(
            winning_position=winning_position,
            consensus_achieved=consensus_achieved,
            compromise_solution=compromise_solution,
            character_votes=character_votes,
            debate_summary=debate_summary,
            business_decision=business_decision
        )
        
    def _calculate_character_votes(self, positions: List[CharacterPosition], 
                                 rebuttals: List[CharacterRebuttal]) -> Dict[str, str]:
        """Calculate which character each character would vote for"""
        votes = {}
        
        print(f"\n🗳️ VOTING CALCULATION:")
        
        for position in positions:
            character = position.character_name
            
            # Start with reduced self-vote to encourage cross-voting
            best_candidate = character
            best_score = position.confidence * 0.5  # Significantly reduce self-bias
            
            print(f"   {character.upper()} voting:")
            print(f"      Self-vote baseline: {best_score:.2f}")
            
            # Consider other characters based on relationships and argument quality
            for other_position in positions:
                if other_position.character_name == character:
                    continue
                    
                other_character = other_position.character_name
                
                # Calculate vote score based on relationship and argument strength
                relationship_score = self.character_relationships.get(character, {}).get(other_character, 0.0)
                argument_score = other_position.confidence
                
                # Enhanced scoring components
                relationship_bonus = max(0, relationship_score) * 0.3  # Only positive relationships help
                argument_weight = argument_score * 0.5
                
                # Add domain expertise bonus - characters respect expertise in relevant areas
                expertise_bonus = 0.0
                if other_position.agent_role == AgentRole.INVENTORY_MANAGER:
                    expertise_bonus = 0.25  # Hermione gets strong expertise bonus
                elif other_position.agent_role == AgentRole.STRATEGIC_PLANNER:
                    expertise_bonus = 0.35  # Tyrion gets highest expertise bonus for strategy
                elif other_position.agent_role == AgentRole.PRICING_ANALYST:
                    expertise_bonus = 0.20  # Gekko gets pricing expertise bonus
                elif other_position.agent_role == AgentRole.CRISIS_MANAGER:
                    expertise_bonus = 0.15  # Jack gets action expertise bonus
                    
                # Add stance strength bonus
                stance_bonus = 0.0
                if other_position.stance in [DebateStance.STRONGLY_AGREE, DebateStance.STRONGLY_DISAGREE]:
                    stance_bonus = 0.1  # Reward strong convictions
                    
                total_score = argument_weight + relationship_bonus + expertise_bonus + stance_bonus
                
                print(f"      vs {other_character}: rel={relationship_score:.2f} arg={argument_score:.2f} exp={expertise_bonus:.2f} total={total_score:.2f}")
                
                # Characters are more likely to vote for others with compelling arguments
                if total_score > best_score:
                    best_candidate = other_character
                    best_score = total_score
                    
            votes[character] = best_candidate
            print(f"      → VOTES FOR: {best_candidate.upper()} (score: {best_score:.2f})")
            
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
        
    def _generate_compromise_solution(self, topic: DebateTopicType, positions: List[CharacterPosition], 
                                    character_votes: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Generate a compromise solution when no clear winner emerges"""
        try:
            # Extract key parameters from positions
            position_summary = []
            numeric_values = []
            
            for pos in positions:
                position_summary.append(f"{pos.character_name.upper()}: {pos.position_statement}")
                # Extract numeric values for mathematical compromises
                import re
                numbers = re.findall(r'\d+(?:\.\d+)?', pos.position_statement)
                if numbers:
                    numeric_values.extend([float(n) for n in numbers])
            
            # Generate compromise using AI
            compromise_prompt = f"""
PHASE 4B CHARACTER DEBATE - COMPROMISE GENERATION

Topic: {topic.value.replace('_', ' ').title()}
Character Positions:
{chr(10).join(position_summary)}

Voting Results: {character_votes}

These characters have conflicting positions with no clear majority winner.
Generate a practical compromise solution that:
1. Addresses core concerns from multiple positions
2. Uses mathematical averaging for numeric values where appropriate
3. Balances different character priorities and expertise
4. Is actionable and specific for business implementation
5. Explains why this compromise makes business sense

Available numeric data for averaging: {numeric_values if numeric_values else 'None'}

Format your response as:
COMPROMISE: [One clear sentence describing the compromise]
RATIONALE: [Business justification for this compromise]
ACTION: [Specific business action to implement]
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a business mediator expert at finding practical compromises that satisfy multiple stakeholders."},
                    {"role": "user", "content": compromise_prompt}
                ],
                max_tokens=300,
                temperature=0.4  # Balanced creativity for compromise solutions
            )
            
            compromise_text = response.choices[0].message.content.strip()
            
            # Parse the compromise response
            compromise_data = self._parse_compromise_response(compromise_text, numeric_values)
            
            # Mathematical enhancement for numeric compromises
            if numeric_values and len(numeric_values) >= 2:
                avg_value = sum(numeric_values) / len(numeric_values)
                compromise_data["mathematical_average"] = avg_value
                
                if topic == DebateTopicType.PRICING_STRATEGY:
                    compromise_data["suggested_price"] = round(avg_value, 2)
                elif topic == DebateTopicType.INVENTORY_ALLOCATION:
                    compromise_data["suggested_quantity"] = int(avg_value)
            
            return compromise_data
            
        except Exception as e:
            print(f"Error generating compromise: {e}")
            # Simple fallback compromise
            fallback_description = "Balanced approach combining elements from multiple character positions"
            if numeric_values and len(numeric_values) >= 2:
                avg = sum(numeric_values) / len(numeric_values)
                fallback_description += f" (Average value: {avg:.2f})"
                
            return {
                "description": fallback_description,
                "rationale": "System-generated fallback compromise",
                "action": "Implement hybrid approach",
                "mathematical_average": avg if numeric_values else None
            }
    
    def _parse_compromise_response(self, response_text: str, numeric_values: List[float]) -> Dict[str, Any]:
        """Parse AI response to extract compromise components"""
        compromise_data = {
            "description": "",
            "rationale": "",
            "action": "",
            "mathematical_average": None
        }
        
        lines = response_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('COMPROMISE:'):
                compromise_data["description"] = line.replace('COMPROMISE:', '').strip()
            elif line.startswith('RATIONALE:'):
                compromise_data["rationale"] = line.replace('RATIONALE:', '').strip()
            elif line.startswith('ACTION:'):
                compromise_data["action"] = line.replace('ACTION:', '').strip()
        
        # Ensure we have a description
        if not compromise_data["description"]:
            compromise_data["description"] = "Balanced compromise solution"
            
        return compromise_data
        
    def _generate_business_decision(self, topic: DebateTopicType, winning_position: Optional[CharacterPosition],
                                  store_status: Dict, compromise_solution: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate actual business decision from debate outcome"""
        
        if not winning_position and not compromise_solution:
            return {
                "decision_type": "no_action",
                "reasoning": "No consensus achieved and no compromise found - maintaining status quo",
                "action_parameters": {}
            }
        
        # Use compromise solution if no clear winner
        if not winning_position and compromise_solution:
            return {
                "decision_type": f"{topic.value}_compromise",
                "reasoning": f"COMPROMISE SOLUTION: {compromise_solution.get('description', 'Balanced approach')}",
                "action_parameters": {
                    "compromise_rationale": compromise_solution.get('rationale', ''),
                    "compromise_action": compromise_solution.get('action', ''),
                    "mathematical_average": compromise_solution.get('mathematical_average'),
                    "suggested_price": compromise_solution.get('suggested_price'),
                    "suggested_quantity": compromise_solution.get('suggested_quantity'),
                    "confidence": 0.6,  # Moderate confidence for compromises
                    "character_lead": "consensus"
                }
            }
            
        # Use winning position if clear winner
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
        
    def should_trigger_debate(self, agent_decisions: List[AgentDecision], store_status: Dict, 
                             resource_conflicts: List = None) -> Optional[DebateTopicType]:
        """🧠 Phase 5A.2: Smart Debate Triggering - Respect Domain Authority
        
        Only trigger debates for:
        1. Cross-domain conflicts (e.g., Gekko's pricing conflicts with Hermione's inventory needs)
        2. Resource allocation conflicts (limited cash, competing supplier needs) 
        3. Strategic direction conflicts (conflicting long-term visions)
        4. Emergency situations override normal protocols
        
        NO DEBATE for domain-specific decisions within character expertise.
        """
        
        # Import domain authority constants
        from src.core.multi_agent_engine import CHARACTER_AUTHORITY_MATRIX
        
        print(f"\n🧠 SMART DEBATE ANALYSIS: Evaluating {len(agent_decisions)} decisions...")
        
        # 1. EMERGENCY OVERRIDE: Jack's crisis decisions bypass normal debate protocols
        crisis_decisions = [d for d in agent_decisions if d.agent_role.value == "crisis_manager" and d.priority >= 8]
        if crisis_decisions:
            print(f"⚡ EMERGENCY OVERRIDE: Jack's crisis decision bypasses debate protocols")
            return None  # No debate - crisis needs immediate action
            
        # 2. DOMAIN AUTHORITY RESPECT: Filter out domain-specific decisions
        cross_domain_decisions = []
        domain_specific_decisions = []
        
        for decision in agent_decisions:
            agent_domains = CHARACTER_AUTHORITY_MATRIX.get(decision.agent_role, {}).get("primary_domains", [])
            decision_type_lower = decision.decision_type.lower()
            
            # Check if decision falls within agent's primary domain
            is_domain_specific = any(domain in decision_type_lower or 
                                   any(domain_word in decision_type_lower for domain_word in domain.split('_'))
                                   for domain in agent_domains)
            
            if is_domain_specific and decision.priority < CHARACTER_AUTHORITY_MATRIX.get(decision.agent_role, {}).get("override_threshold", 7):
                domain_specific_decisions.append(decision)
                print(f"✅ DOMAIN AUTHORITY: {decision.agent_role.value} decides {decision.decision_type} (within expertise)")
            else:
                cross_domain_decisions.append(decision)
                
        # 3. CROSS-DOMAIN CONFLICT DETECTION
        cross_domain_conflicts = self._detect_cross_domain_conflicts(cross_domain_decisions, store_status)
        
        if cross_domain_conflicts:
            conflict_type, conflict_details = cross_domain_conflicts
            print(f"⚔️ CROSS-DOMAIN CONFLICT DETECTED: {conflict_type}")
            print(f"   Agents: {', '.join([d.agent_role.value for d in conflict_details['conflicting_decisions']])}")
            
            # Map conflict types to debate topics
            if "pricing" in conflict_type.lower() or "inventory" in conflict_type.lower():
                return DebateTopicType.INVENTORY_ALLOCATION if "inventory" in conflict_type.lower() else DebateTopicType.PRICING_STRATEGY
            elif "strategic" in conflict_type.lower():
                return DebateTopicType.STRATEGIC_PLANNING
            elif "customer" in conflict_type.lower():
                return DebateTopicType.CUSTOMER_SERVICE
            else:
                return DebateTopicType.STRATEGIC_PLANNING
                
        # 4. RESOURCE ALLOCATION CONFLICTS
        if resource_conflicts:
            severe_conflicts = [c for c in resource_conflicts if c.conflict_severity >= 0.7]
            if severe_conflicts:
                conflict = severe_conflicts[0]  # Handle most severe first
                print(f"💰 RESOURCE CONFLICT DETECTED: {conflict.resource_type}")
                print(f"   Demand: {conflict.total_demand:.1f} vs Supply: {conflict.available_supply:.1f}")
                print(f"   Competing agents: {', '.join([a.value for a in conflict.competing_agents])}")
                
                if conflict.resource_type == "cash":
                    return DebateTopicType.STRATEGIC_PLANNING  # Cash allocation is strategic
                elif "inventory" in conflict.resource_type:
                    return DebateTopicType.INVENTORY_ALLOCATION
                else:
                    return DebateTopicType.STRATEGIC_PLANNING
                    
        # 5. HIGH-STAKES BUSINESS SITUATIONS (Legacy logic as backup)
        high_priority_decisions = [d for d in agent_decisions if d.priority >= 8]
        if len(high_priority_decisions) >= 2:
            # Multiple critical decisions - may indicate business crisis
            decision_types = [d.decision_type for d in high_priority_decisions]
            
            print(f"⚠️ HIGH-STAKES SITUATION: {len(high_priority_decisions)} critical decisions detected")
            
            if any("crisis" in dt.lower() for dt in decision_types):
                return DebateTopicType.CRISIS_RESPONSE
            elif any("pricing" in dt.lower() for dt in decision_types):
                return DebateTopicType.PRICING_STRATEGY
            elif any("inventory" in dt.lower() for dt in decision_types):
                return DebateTopicType.INVENTORY_ALLOCATION
                
        # 6. BUSINESS CRISIS INDICATORS (Environmental factors)
        # IMPORTANT: Only trigger crisis debates if domain experts aren't already handling it!
        inventory = store_status.get('inventory', {})
        stockout_count = sum(1 for v in inventory.values() if v == 0)
        cash = store_status.get('cash', 0)
        
        # Check if domain experts are already handling their areas
        inventory_expert_deciding = any(d.agent_role.value == "inventory_manager" for d in domain_specific_decisions)
        crisis_expert_deciding = any(d.agent_role.value == "crisis_manager" for d in domain_specific_decisions)
        
        if stockout_count >= 3 and cash < 100 and not crisis_expert_deciding:  # Severe business crisis
            print(f"🚨 BUSINESS CRISIS: {stockout_count} stockouts with low cash (${cash:.2f}) - No crisis expert handling")
            return DebateTopicType.CRISIS_RESPONSE
        elif stockout_count >= 2 and not inventory_expert_deciding:  # Inventory crisis with no expert
            print(f"📦 INVENTORY CRISIS: {stockout_count} stockouts detected - No inventory expert handling")
            return DebateTopicType.INVENTORY_ALLOCATION
        elif stockout_count >= 2 and inventory_expert_deciding:
            print(f"📦 INVENTORY SITUATION: {stockout_count} stockouts detected - Hermione (expert) is handling it")
            
        print(f"✅ NO DEBATE NEEDED: All decisions within domain authority or no conflicts detected")
        return None
        
    def _detect_cross_domain_conflicts(self, decisions: List[AgentDecision], store_status: Dict) -> Optional[Tuple[str, Dict]]:
        """Detect conflicts between different agent domains"""
        
        if len(decisions) < 2:
            return None
            
        # Import domain authority constants
        from src.core.multi_agent_engine import CHARACTER_AUTHORITY_MATRIX
        
        # Group decisions by domain overlap
        conflicts = []
        
        for i, decision1 in enumerate(decisions):
            for j, decision2 in enumerate(decisions[i+1:], i+1):
                conflict = self._analyze_decision_conflict(decision1, decision2, store_status)
                if conflict:
                    conflicts.append(conflict)
                    
        if conflicts:
            # Return the most severe conflict
            most_severe = max(conflicts, key=lambda c: c['severity'])
            return most_severe['type'], {
                'conflicting_decisions': most_severe['decisions'],
                'severity': most_severe['severity'],
                'description': most_severe['description']
            }
            
        return None
        
    def _analyze_decision_conflict(self, decision1: AgentDecision, decision2: AgentDecision, 
                                 store_status: Dict) -> Optional[Dict]:
        """Analyze if two decisions conflict across domains"""
        
        # Same agent - no cross-domain conflict
        if decision1.agent_role == decision2.agent_role:
            return None
            
        # Pricing vs Inventory conflicts
        if ((decision1.agent_role.value == "pricing_analyst" and decision2.agent_role.value == "inventory_manager") or
            (decision1.agent_role.value == "inventory_manager" and decision2.agent_role.value == "pricing_analyst")):
            
            # Check for conflicting strategies
            d1_params = str(decision1.parameters).lower()
            d2_params = str(decision2.parameters).lower()
            d1_reasoning = decision1.reasoning.lower()
            d2_reasoning = decision2.reasoning.lower()
            
            # Detect conflicting approaches
            if (("aggressive" in d1_reasoning and "conservative" in d2_reasoning) or
                ("risk" in d1_reasoning and "safe" in d2_reasoning) or
                ("maximize" in d1_reasoning and "minimize" in d2_reasoning)):
                
                return {
                    'type': 'pricing_inventory_strategy_conflict',
                    'decisions': [decision1, decision2],
                    'severity': 0.8,
                    'description': f"Conflicting risk strategies between {decision1.agent_role.value} and {decision2.agent_role.value}"
                }
                
        # Customer Service vs Pricing conflicts  
        elif ((decision1.agent_role.value == "customer_service" and decision2.agent_role.value == "pricing_analyst") or
              (decision1.agent_role.value == "pricing_analyst" and decision2.agent_role.value == "customer_service")):
            
            # Check for customer satisfaction vs profit conflicts
            if ("price_increase" in str(decision1.parameters).lower() or "price_increase" in str(decision2.parameters).lower()):
                return {
                    'type': 'customer_pricing_conflict',
                    'decisions': [decision1, decision2],
                    'severity': 0.7,
                    'description': "Pricing decisions may conflict with customer satisfaction goals"
                }
                
        # Strategic vs Operational conflicts
        elif decision1.agent_role.value == "strategic_planner" or decision2.agent_role.value == "strategic_planner":
            strategic_decision = decision1 if decision1.agent_role.value == "strategic_planner" else decision2
            operational_decision = decision2 if decision1.agent_role.value == "strategic_planner" else decision1
            
            # Check for short-term vs long-term conflicts
            if (strategic_decision.priority >= 7 and operational_decision.priority >= 7 and
                abs(strategic_decision.priority - operational_decision.priority) >= 2):
                
                return {
                    'type': 'strategic_operational_conflict',
                    'decisions': [decision1, decision2],
                    'severity': 0.6,
                    'description': f"Strategic planning conflicts with {operational_decision.agent_role.value} operational priorities"
                }
                
        return None 