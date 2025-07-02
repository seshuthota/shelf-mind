"""
💰 Gordon Gekko - Pricing Analyst Agent
Phase 4A.2: Character-based pricing warfare specialist
"""

from typing import Dict, List, Any, Optional
import json
from src.core.multi_agent_engine import BaseSpecialistAgent, AgentRole, AgentDecision
from src.core.agent_prompts import AgentPrompts
from src.core.models import PRODUCTS

class PricingAnalystAgent(BaseSpecialistAgent):
    """💰 Phase 4A.2: Gordon Gekko - Ruthless Pricing Warfare Specialist
    
    "Greed works in pricing warfare!"
    
    Responsible for:
    - Competitive pricing analysis and market domination
    - Psychological pricing warfare strategies  
    - Profit margin optimization and revenue maximization
    - Market positioning and competitive intelligence
    """
    
    def __init__(self, provider: str = "openai"):
        super().__init__(AgentRole.PRICING_ANALYST, provider)
        
    def _define_specializations(self) -> List[str]:
        """Define Gordon Gekko's pricing warfare specializations"""
        return [
            "competitive_pricing_analysis",
            "market_warfare_strategy", 
            "psychological_pricing",
            "profit_maximization",
            "competitive_intelligence"
        ]
    
    def analyze_situation(self, store_status: Dict, context: Dict) -> AgentDecision:
        """💰 Gordon Gekko analyzes pricing situation with predatory precision"""
        
        # Gather pricing intelligence with Gekko's aggressive approach
        competitive_analysis = self._analyze_competitive_landscape(store_status)
        pricing_opportunities = self._identify_pricing_opportunities(store_status, context)
        market_psychology = self._analyze_market_psychology(store_status, context)
        
        # Generate pricing warfare strategy
        action_plan = self._create_pricing_strategy(competitive_analysis, pricing_opportunities, market_psychology)
        
        # Calculate confidence based on market advantage
        confidence = self._calculate_confidence(store_status, competitive_analysis)
        
        # Determine priority (pricing wars are always urgent for Gekko)
        priority = self._determine_priority(competitive_analysis, market_psychology)
        
        # 🎭 Generate Gekko's reasoning with character personality
        gekko_reasoning = self._generate_gekko_reasoning(competitive_analysis, pricing_opportunities, action_plan)
        
        return AgentDecision(
            agent_role=self.role,
            decision_type="pricing_warfare",
            parameters=action_plan,
            confidence=confidence,
            reasoning=gekko_reasoning,
            priority=priority
        )
    
    def _analyze_competitive_landscape(self, store_status: Dict) -> Dict:
        """Analyze competitive pricing with predatory precision"""
        current_prices = store_status.get('current_prices', {})
        competitor_prices = store_status.get('competitor_prices', {})
        
        competitive_analysis = {
            'underpriced_products': [],  # We're too cheap - money left on table
            'overpriced_products': [],   # We're too expensive - losing customers  
            'competitive_products': [],  # Evenly matched - warfare opportunity
            'dominating_products': [],   # We're winning - maintain advantage
            'price_gaps': {},           # Exact price differences vs competitor
            'market_position': 'unknown'
        }
        
        winning_count = 0
        total_products = len(current_prices)
        
        for product, our_price in current_prices.items():
            competitor_price = competitor_prices.get(product, our_price)
            price_gap = our_price - competitor_price
            
            competitive_analysis['price_gaps'][product] = price_gap
            
            if price_gap < -0.10:  # We're significantly cheaper
                competitive_analysis['dominating_products'].append(product)
                winning_count += 1
            elif price_gap > 0.10:  # We're significantly more expensive
                competitive_analysis['overpriced_products'].append(product)
            elif abs(price_gap) <= 0.05:  # Close competition
                competitive_analysis['competitive_products'].append(product)
            elif price_gap < 0:  # Slightly cheaper
                competitive_analysis['underpriced_products'].append(product)
                winning_count += 0.5
        
        # Determine overall market position
        win_rate = winning_count / total_products if total_products > 0 else 0
        if win_rate >= 0.7:
            competitive_analysis['market_position'] = 'dominating'
        elif win_rate >= 0.4:
            competitive_analysis['market_position'] = 'competitive'
        else:
            competitive_analysis['market_position'] = 'defensive'
            
        return competitive_analysis
    
    def _identify_pricing_opportunities(self, store_status: Dict, context: Dict) -> Dict:
        """Identify pricing opportunities with Wall Street ruthlessness"""
        current_prices = store_status.get('current_prices', {})
        inventory = store_status.get('inventory', {})
        
        opportunities = {
            'margin_expansion': [],      # Products where we can raise prices
            'volume_capture': [],        # Products where we should cut prices
            'psychological_pricing': [], # Products for $X.99 psychology
            'premium_positioning': [],   # High-margin luxury positioning
            'loss_leader_candidates': [] # Products for customer acquisition
        }
        
        for product, price in current_prices.items():
            stock_level = inventory.get(product, 0)
            
            # High stock + competitive price = margin expansion opportunity
            if stock_level >= 5 and price < 3.0:
                opportunities['margin_expansion'].append(product)
                
            # Low stock + high price = volume capture needed
            if stock_level <= 2:
                opportunities['volume_capture'].append(product)
                
            # Products ending in .00 = psychological pricing opportunity
            if price == int(price):
                opportunities['psychological_pricing'].append(product)
                
            # High-value products = premium positioning
            if price >= 3.0:
                opportunities['premium_positioning'].append(product)
                
            # Popular products = loss leader candidates
            if product.lower() in ['coke', 'water', 'chips']:
                opportunities['loss_leader_candidates'].append(product)
        
        return opportunities
    
    def _analyze_market_psychology(self, store_status: Dict, context: Dict) -> Dict:
        """Analyze market psychology for maximum manipulation"""
        yesterday_summary = context.get('yesterday_summary', {})
        
        psychology = {
            'customer_price_sensitivity': 'medium',  # Based on segment data
            'competitive_pressure': 'medium',        # Based on war intensity
            'demand_patterns': {},                   # Product-specific demand
            'psychological_triggers': [],            # Pricing psychology opportunities
            'market_sentiment': 'neutral'            # Overall market mood
        }
        
        # Analyze customer segments for price sensitivity
        if yesterday_summary:
            price_sensitive_revenue = yesterday_summary.get('price_sensitive_revenue', 0)
            total_revenue = yesterday_summary.get('total_revenue', 1)
            
            if price_sensitive_revenue / total_revenue > 0.6:
                psychology['customer_price_sensitivity'] = 'high'
            elif price_sensitive_revenue / total_revenue < 0.4:
                psychology['customer_price_sensitivity'] = 'low'
        
        return psychology
    
    def _create_pricing_strategy(self, competitive_analysis: Dict, opportunities: Dict, psychology: Dict) -> Dict:
        """Create Gekko's ruthless pricing warfare strategy"""
        strategy = {
            'recommended_price_changes': {},
            'warfare_tactics': [],
            'psychological_moves': [],
            'profit_optimization': [],
            'competitive_responses': []
        }
        
        # Gekko's aggressive pricing moves
        for product in competitive_analysis['overpriced_products']:
            strategy['recommended_price_changes'][product] = 'decrease_aggressive'
            strategy['warfare_tactics'].append(f"PRICE WAR: Cut {product} to steal market share")
            
        for product in competitive_analysis['underpriced_products']:
            strategy['recommended_price_changes'][product] = 'increase_margin'
            strategy['profit_optimization'].append(f"MARGIN EXPANSION: Raise {product} for profit")
            
        for product in opportunities['psychological_pricing']:
            strategy['psychological_moves'].append(f"PSYCHOLOGY: Price {product} at $X.99")
            
        return strategy
    
    def _calculate_confidence(self, store_status: Dict, competitive_analysis: Dict) -> float:
        """Calculate Gekko's confidence in market domination"""
        base_confidence = 0.85  # Gekko is always confident
        
        # Boost confidence when dominating market
        if competitive_analysis['market_position'] == 'dominating':
            return min(0.95, base_confidence + 0.10)
        elif competitive_analysis['market_position'] == 'defensive':
            return max(0.70, base_confidence - 0.15)
            
        return base_confidence
    
    def _determine_priority(self, competitive_analysis: Dict, psychology: Dict) -> int:
        """Determine priority - pricing wars are always urgent for Gekko"""
        if competitive_analysis['overpriced_products']:
            return 5  # High priority - losing customers
        elif competitive_analysis['market_position'] == 'defensive':
            return 4  # Medium-high priority - need to fight back
        elif competitive_analysis['underpriced_products']:
            return 3  # Medium priority - money left on table
        else:
            return 2  # Low priority - maintaining dominance
    
    def _generate_gekko_reasoning(self, competitive_analysis: Dict, opportunities: Dict, action_plan: Dict) -> str:
        """💰 Generate Gordon Gekko's character-based reasoning"""
        personality = AgentPrompts.get_agent_personality(AgentRole.PRICING_ANALYST)
        
        reasoning_parts = []
        
        # Gekko's aggressive market analysis
        if competitive_analysis['overpriced_products']:
            overpriced_list = ', '.join(competitive_analysis['overpriced_products'])
            reasoning_parts.append(f"💰 GEKKO'S ANALYSIS: 'We're bleeding money! {len(competitive_analysis['overpriced_products'])} products overpriced ({overpriced_list}). This is unacceptable!'")
            
        if competitive_analysis['underpriced_products']:
            underpriced_list = ', '.join(competitive_analysis['underpriced_products'])
            reasoning_parts.append(f"💎 GEKKO'S OPPORTUNITY: 'Money is sitting on the table! {len(competitive_analysis['underpriced_products'])} products underpriced ({underpriced_list}). Time to maximize margins!'")
            
        if competitive_analysis['dominating_products']:
            dominating_list = ', '.join(competitive_analysis['dominating_products'])
            reasoning_parts.append(f"⚔️ GEKKO'S WARFARE: 'We're crushing the competition on {len(competitive_analysis['dominating_products'])} products ({dominating_list}). Maintain the pressure!'")
            
        # Gekko's strategic recommendations
        if action_plan['recommended_price_changes']:
            changes_count = len(action_plan['recommended_price_changes'])
            reasoning_parts.append(f"📈 GEKKO'S STRATEGY: 'I recommend {changes_count} strategic price moves. Every penny counts in market warfare!'")
            
        if action_plan['warfare_tactics']:
            tactics_count = len(action_plan['warfare_tactics'])
            reasoning_parts.append(f"⚡ GEKKO'S TACTICS: '{tactics_count} aggressive moves identified. We don't just compete - we dominate!'")
            
        if not reasoning_parts:
            reasoning_parts.append(f"👑 GEKKO'S ASSESSMENT: 'Market position is strong, but greed never sleeps. Always looking for the next opportunity!'")
        
        # Add Gekko's characteristic sign-off  
        gekko_conclusion = f"\n💰 GEKKO'S CONCLUSION: 'The point is, greed works! Every price decision is a strategic weapon in market warfare!' (Market Position: {competitive_analysis['market_position']})"
        
        return " | ".join(reasoning_parts) + gekko_conclusion 