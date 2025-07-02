"""
👥 Elle Woods - Customer Service Agent  
Phase 4A.2: Character-based customer experience specialist
"""

from typing import Dict, List, Any, Optional
import json
from src.core.multi_agent_engine import BaseSpecialistAgent, AgentRole, AgentDecision
from src.core.agent_prompts import AgentPrompts
from src.core.models import PRODUCTS

class CustomerServiceAgent(BaseSpecialistAgent):
    """👥 Phase 4A.2: Elle Woods - Customer Experience Specialist
    
    "Our customers deserve to feel totally fabulous!"
    
    Responsible for:
    - Customer satisfaction analysis and optimization
    - Customer segment behavior analysis
    - Loyalty program recommendations  
    - Service quality improvement strategies
    """
    
    def __init__(self, provider: str = "openai"):
        super().__init__(AgentRole.CUSTOMER_SERVICE, provider)
        
    def _define_specializations(self) -> List[str]:
        """Define Elle's customer psychology specializations"""
        return [
            "customer_satisfaction_analysis",
            "segment_behavior_psychology",
            "loyalty_program_optimization", 
            "service_quality_improvement",
            "customer_experience_design"
        ]
    
    def analyze_situation(self, store_status: Dict, context: Dict) -> AgentDecision:
        """👥 Elle Woods analyzes customer experience with psychology expertise"""
        
        # Gather customer intelligence with Elle's people-focused approach
        customer_satisfaction = self._analyze_customer_satisfaction(store_status, context)
        segment_analysis = self._analyze_customer_segments(store_status, context)
        service_quality = self._evaluate_service_quality(store_status, context)
        
        # Generate customer experience strategy
        action_plan = self._create_customer_strategy(customer_satisfaction, segment_analysis, service_quality)
        
        # Calculate confidence based on customer data quality
        confidence = self._calculate_confidence(store_status, customer_satisfaction)
        
        # Determine priority (customer happiness is always important to Elle)
        priority = self._determine_priority(customer_satisfaction, segment_analysis)
        
        # 🎭 Generate Elle's reasoning with character personality
        elle_reasoning = self._generate_elle_reasoning(customer_satisfaction, segment_analysis, action_plan)
        
        return AgentDecision(
            agent_role=self.role,
            decision_type="customer_experience",
            parameters=action_plan,
            confidence=confidence,
            reasoning=elle_reasoning,
            priority=priority
        )
    
    def _analyze_customer_satisfaction(self, store_status: Dict, context: Dict) -> Dict:
        """Analyze customer satisfaction with Elle's psychology insight"""
        yesterday_summary = context.get('yesterday_summary', {})
        inventory = store_status.get('inventory', {})
        
        satisfaction = {
            'stockout_impact': 0,           # How stockouts affect satisfaction
            'price_satisfaction': 'neutral', # Customer reaction to pricing
            'service_quality': 'good',       # Overall service experience
            'loyalty_indicators': [],        # Signs of customer loyalty
            'dissatisfaction_risks': [],     # Potential problems
            'satisfaction_score': 75         # Overall satisfaction percentage
        }
        
        # Analyze stockout impact on customer experience
        stockouts = [product for product, qty in inventory.items() if qty == 0]
        if stockouts:
            satisfaction['stockout_impact'] = len(stockouts) * 10  # 10% per stockout
            satisfaction['dissatisfaction_risks'].extend([f"Stockout disappointment: {product}" for product in stockouts])
            satisfaction['satisfaction_score'] -= len(stockouts) * 5
        
        # Analyze customer segment happiness
        if yesterday_summary:
            total_customers = yesterday_summary.get('total_customers', 0)
            if total_customers > 15:  # High traffic = good satisfaction
                satisfaction['loyalty_indicators'].append("High customer traffic indicates satisfaction")
                satisfaction['satisfaction_score'] += 5
            elif total_customers < 8:  # Low traffic = potential issues
                satisfaction['dissatisfaction_risks'].append("Low customer traffic may indicate dissatisfaction")
                satisfaction['satisfaction_score'] -= 10
        
        return satisfaction
    
    def _analyze_customer_segments(self, store_status: Dict, context: Dict) -> Dict:
        """Analyze customer segment behavior with Elle's social intelligence"""
        yesterday_summary = context.get('yesterday_summary', {})
        
        segments = {
            'price_sensitive_behavior': 'normal',    # How price-sensitive customers are acting
            'brand_loyal_behavior': 'normal',        # How brand-loyal customers are acting  
            'segment_balance': 'healthy',            # Overall segment mix health
            'engagement_opportunities': [],          # Ways to improve engagement
            'retention_risks': [],                   # Segment-specific risks
            'satisfaction_by_segment': {}            # Satisfaction levels per segment
        }
        
        if yesterday_summary:
            # Analyze segment revenue patterns
            price_sensitive_revenue = yesterday_summary.get('price_sensitive_revenue', 0)
            brand_loyal_revenue = yesterday_summary.get('brand_loyal_revenue', 0)
            total_revenue = price_sensitive_revenue + brand_loyal_revenue
            
            if total_revenue > 0:
                price_sensitive_ratio = price_sensitive_revenue / total_revenue
                
                if price_sensitive_ratio > 0.7:
                    segments['price_sensitive_behavior'] = 'dominant'
                    segments['engagement_opportunities'].append("Focus on value messaging for price-sensitive customers")
                elif price_sensitive_ratio < 0.3:
                    segments['brand_loyal_behavior'] = 'dominant'  
                    segments['engagement_opportunities'].append("Develop premium offerings for loyal customers")
        
        return segments
    
    def _evaluate_service_quality(self, store_status: Dict, context: Dict) -> Dict:
        """Evaluate service quality with Elle's attention to customer experience"""
        inventory = store_status.get('inventory', {})
        
        quality = {
            'product_availability': 'good',     # Stock availability score
            'variety_score': 'excellent',       # Product variety assessment
            'convenience_factors': [],          # What makes shopping convenient
            'improvement_areas': [],            # Areas needing attention
            'experience_enhancers': []          # Ways to make shopping fabulous
        }
        
        # Evaluate product availability
        total_products = len(inventory)
        stocked_products = len([qty for qty in inventory.values() if qty > 0])
        availability_rate = stocked_products / total_products if total_products > 0 else 1.0
        
        if availability_rate >= 0.9:
            quality['product_availability'] = 'excellent'
            quality['convenience_factors'].append("Excellent product availability")
        elif availability_rate >= 0.7:
            quality['product_availability'] = 'good'
        else:
            quality['product_availability'] = 'poor'
            quality['improvement_areas'].append("Multiple stockouts affecting customer choice")
        
        # Elle's experience enhancement suggestions
        quality['experience_enhancers'] = [
            "Create Instagram-worthy product displays",
            "Implement loyalty rewards program", 
            "Offer personalized recommendations",
            "Maintain consistently fresh inventory"
        ]
        
        return quality
    
    def _create_customer_strategy(self, satisfaction: Dict, segments: Dict, quality: Dict) -> Dict:
        """Create Elle's customer experience strategy"""
        strategy = {
            'satisfaction_improvements': [],     # Actions to boost satisfaction
            'segment_engagement': [],           # Segment-specific strategies
            'service_enhancements': [],         # Service quality improvements
            'loyalty_initiatives': [],          # Customer retention strategies
            'experience_upgrades': []           # Ways to make shopping fabulous
        }
        
        # Address satisfaction issues
        if satisfaction['satisfaction_score'] < 70:
            strategy['satisfaction_improvements'].append("Immediate satisfaction recovery needed")
            
        if satisfaction['stockout_impact'] > 0:
            strategy['satisfaction_improvements'].append("Stockout communication and alternatives")
            
        # Segment-specific strategies
        if segments['price_sensitive_behavior'] == 'dominant':
            strategy['segment_engagement'].append("Emphasize value and savings messaging")
        elif segments['brand_loyal_behavior'] == 'dominant':
            strategy['segment_engagement'].append("Focus on premium experience and exclusivity")
            
        # Service quality improvements
        for improvement in quality['improvement_areas']:
            strategy['service_enhancements'].append(improvement)
            
        # Elle's signature loyalty recommendations
        strategy['loyalty_initiatives'] = [
            "Points-based rewards system",
            "Exclusive customer events", 
            "Personalized shopping experience",
            "Social media engagement campaigns"
        ]
        
        return strategy
    
    def _calculate_confidence(self, store_status: Dict, satisfaction: Dict) -> float:
        """Calculate Elle's confidence in customer psychology analysis"""
        base_confidence = 0.80  # Elle is confident in people skills
        
        # Boost confidence with more customer data
        if satisfaction['satisfaction_score'] >= 80:
            return min(0.95, base_confidence + 0.15)
        elif satisfaction['satisfaction_score'] < 60:
            return max(0.65, base_confidence - 0.15)
            
        return base_confidence
    
    def _determine_priority(self, satisfaction: Dict, segments: Dict) -> int:
        """Determine priority - customer happiness is Elle's top concern"""
        if satisfaction['satisfaction_score'] < 60:
            return 5  # High priority - customer crisis
        elif satisfaction['stockout_impact'] > 20:
            return 4  # Medium-high priority - stockout affecting experience
        elif len(satisfaction['dissatisfaction_risks']) > 2:
            return 3  # Medium priority - multiple risk factors
        else:
            return 2  # Low priority - maintaining satisfaction
    
    def _generate_elle_reasoning(self, satisfaction: Dict, segments: Dict, action_plan: Dict) -> str:
        """👥 Generate Elle Woods' character-based reasoning"""
        personality = AgentPrompts.get_agent_personality(AgentRole.CUSTOMER_SERVICE)
        
        reasoning_parts = []
        
        # Elle's enthusiastic customer analysis
        satisfaction_score = satisfaction['satisfaction_score']
        if satisfaction_score >= 80:
            reasoning_parts.append(f"💖 ELLE'S ANALYSIS: 'OMG, our customers are like, totally satisfied ({satisfaction_score}%)! This is so fabulous!'")
        elif satisfaction_score >= 60:
            reasoning_parts.append(f"💕 ELLE'S ASSESSMENT: 'Our customer satisfaction is pretty good ({satisfaction_score}%), but we can totally make it even more amazing!'")
        else:
            reasoning_parts.append(f"😟 ELLE'S CONCERN: 'Like, our customer satisfaction ({satisfaction_score}%) needs serious attention! Our customers deserve to feel fabulous!'")
            
        # Elle's stockout empathy
        if satisfaction['stockout_impact'] > 0:
            stockout_impact = satisfaction['stockout_impact']
            reasoning_parts.append(f"💔 ELLE'S EMPATHY: 'Poor customers! Stockouts are affecting {stockout_impact}% of their experience. That's like, totally not okay!'")
            
        # Elle's segment psychology insights
        if segments['price_sensitive_behavior'] == 'dominant':
            reasoning_parts.append(f"💰 ELLE'S PSYCHOLOGY: 'Price-sensitive customers are dominating! They need to feel smart about their choices, not just cheap!'")
        elif segments['brand_loyal_behavior'] == 'dominant':
            reasoning_parts.append(f"💎 ELLE'S INSIGHT: 'Brand-loyal customers are our VIPs! They deserve premium treatment and exclusive experiences!'")
            
        # Elle's strategic recommendations
        if action_plan['satisfaction_improvements']:
            improvements_count = len(action_plan['satisfaction_improvements'])
            reasoning_parts.append(f"✨ ELLE'S STRATEGY: '{improvements_count} satisfaction improvements identified. Every customer interaction should be Instagram-worthy!'")
            
        if action_plan['loyalty_initiatives']:
            initiatives_count = len(action_plan['loyalty_initiatives'])
            reasoning_parts.append(f"💕 ELLE'S LOYALTY PLAN: '{initiatives_count} loyalty initiatives ready. Happy customers are the best marketing!'")
            
        if not reasoning_parts:
            reasoning_parts.append("🌟 ELLE'S ASSESSMENT: 'Customer experience is stable, but there's always room to make it more fabulous!'")
        
        # Add Elle's characteristic sign-off
        elle_conclusion = f"\n💖 ELLE'S CONCLUSION: 'Like, customer psychology is basically applied emotional intelligence! When customers feel valued, they become brand evangelists!' (Satisfaction: {satisfaction_score}%)"
        
        return " | ".join(reasoning_parts) + elle_conclusion 