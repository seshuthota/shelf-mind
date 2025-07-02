"""
👥 Elle Woods - Customer Service Agent  
Phase 4A.2: Character-based customer experience specialist
"""

from typing import Dict, List, Any, Optional
import json
from src.core.multi_agent_engine import BaseSpecialistAgent, AgentRole, AgentDecision
from src.core.agent_prompts import AgentPrompts
from src.core.models import PRODUCTS
from src.tools.customer_tools import CustomerTools

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
        self.tools = CustomerTools()
        
    def _define_specializations(self) -> List[str]:
        """Define Elle's customer psychology specializations"""
        return [
            "customer_satisfaction_analysis",
            "segment_behavior_psychology",
            "loyalty_program_optimization", 
            "service_quality_improvement",
            "customer_experience_design"
        ]
    
    def analyze_situation(self, store_state: Dict, context: Dict) -> AgentDecision:
        """👥 Elle Woods analyzes customer experience with psychology expertise"""
        
        # 🛠️ Phase 5A.3: EXPLICIT TOOL USAGE INTEGRATION
        tool_usage_log = []
        tool_results = {}
        
        print(f"\n💖 ELLE'S TOOL ANALYSIS BEGINS...")
        print(f"   🛠️ Deploying Elle's 5 Customer Psychology Tools...")
        
        # 🛠️ TOOL 1: Customer Satisfaction Analysis
        print(f"   💝 TOOL 1: Customer Satisfaction Analyzer → Running...")
        satisfaction_data = self.tools.customer_satisfaction_analyzer(store_state, context)
        tool_results['satisfaction_analyzer'] = satisfaction_data
        tool_usage_log.append({
            'tool_name': 'Customer Satisfaction Analyzer',
            'emoji': '💝',
            'data_points': len(satisfaction_data.get('satisfaction_drivers', [])) + len(satisfaction_data.get('dissatisfaction_risks', [])),
            'key_insight': f"Sentiment Score: {satisfaction_data.get('customer_sentiment_score', 0)}%"
        })
        print(f"      ✅ Sentiment Score: {satisfaction_data.get('customer_sentiment_score', 0)}% | {len(satisfaction_data.get('satisfaction_drivers', []))} drivers, {len(satisfaction_data.get('dissatisfaction_risks', []))} risks")
        
        # 🛠️ TOOL 2: Loyalty Program Optimizer
        print(f"   👑 TOOL 2: Loyalty Program Optimizer → Running...")
        loyalty_data = self.tools.loyalty_program_optimizer(store_state, context)
        tool_results['loyalty_optimizer'] = loyalty_data
        tool_usage_log.append({
            'tool_name': 'Loyalty Program Optimizer',
            'emoji': '👑',
            'data_points': len(loyalty_data.get('program_recommendations', [])),
            'key_insight': f"Loyalty Score: {loyalty_data.get('loyalty_metrics', {}).get('loyalty_score', 0)}"
        })
        print(f"      ✅ Loyalty Score: {loyalty_data.get('loyalty_metrics', {}).get('loyalty_score', 0)} | {len(loyalty_data.get('program_recommendations', []))} strategies")
        
        # 🛠️ TOOL 3: Brand Sentiment Monitor
        print(f"   ✨ TOOL 3: Brand Sentiment Monitor → Running...")
        sentiment_data = self.tools.brand_sentiment_monitor(store_state, context)
        tool_results['sentiment_monitor'] = sentiment_data
        brand_positioning = sentiment_data.get('brand_perception', {}).get('brand_positioning', 'unknown')
        tool_usage_log.append({
            'tool_name': 'Brand Sentiment Monitor',
            'emoji': '✨',
            'data_points': len(sentiment_data.get('reputation_action_plan', [])),
            'key_insight': f"Brand Position: {brand_positioning}"
        })
        print(f"      ✅ Brand Position: {brand_positioning} | {len(sentiment_data.get('reputation_action_plan', []))} action items")
        
        # 🛠️ TOOL 4: Service Quality Metrics
        print(f"   📊 TOOL 4: Service Quality Metrics → Running...")
        quality_data = self.tools.service_quality_metrics(store_state, context)
        tool_results['quality_metrics'] = quality_data
        service_score = quality_data.get('service_quality_index', 0)
        tool_usage_log.append({
            'tool_name': 'Service Quality Metrics',
            'emoji': '📊',
            'data_points': len(quality_data.get('improvement_recommendations', [])),
            'key_insight': f"Service Score: {service_score}%"
        })
        print(f"      ✅ Service Score: {service_score}% | {len(quality_data.get('improvement_recommendations', []))} improvements")
        
        # 🛠️ TOOL 5: Relationship Building Tools
        print(f"   💕 TOOL 5: Relationship Building Tools → Running...")
        relationship_data = self.tools.relationship_building_tools(store_state, context)
        tool_results['relationship_tools'] = relationship_data
        engagement_opportunities = len(relationship_data.get('engagement_strategies', []))
        tool_usage_log.append({
            'tool_name': 'Relationship Building Tools',
            'emoji': '💕',
            'data_points': engagement_opportunities,
            'key_insight': f"{engagement_opportunities} engagement opportunities"
        })
        print(f"      ✅ {engagement_opportunities} engagement opportunities identified")
        
        print(f"   🎯 TOOL ANALYSIS COMPLETE: 5/5 tools executed successfully")
        
        # Legacy analysis integration (keeping existing logic)
        customer_satisfaction = self._analyze_customer_satisfaction(store_state, context)
        segment_analysis = self._analyze_customer_segments(store_state, context)
        service_quality = self._evaluate_service_quality(store_state, context)
        
        # Generate customer experience strategy with tool integration
        action_plan = self._create_customer_strategy_with_tools(customer_satisfaction, segment_analysis, service_quality, tool_results)
        
        # Calculate confidence based on tool data quality
        confidence = self._calculate_confidence_with_tools(store_state, tool_results)
        
        # Determine priority with tool insights
        priority = self._determine_priority_with_tools(tool_results, customer_satisfaction)
        
        # 🎭 Generate Elle's reasoning with explicit tool integration
        elle_reasoning = self._generate_elle_reasoning_with_tools(tool_results, tool_usage_log, action_plan)
        
        # Store decision info for UI display
        self.last_decision_summary = f"Customer satisfaction analysis"
        self.last_confidence = confidence
        
        return AgentDecision(
            agent_role=self.role,
            decision_type="customer_experience",
            parameters={**action_plan, 'tool_usage_log': tool_usage_log, 'tool_results': tool_results},
            confidence=confidence,
            reasoning=elle_reasoning,
            priority=priority
        )
    
    def _analyze_customer_satisfaction(self, store_state: Dict, context: Dict) -> Dict:
        """Analyze customer satisfaction with Elle's psychology insight"""
        yesterday_summary = context.get('yesterday_summary', {})
        
        # Fix: Use dictionary access instead of StoreState attribute access
        inventory = store_state.get('inventory', {})
        
        satisfaction = {
            'stockout_impact': 0,           # How stockouts affect satisfaction
            'price_satisfaction': 'neutral', # Customer reaction to pricing
            'service_quality': 'good',       # Overall service experience
            'loyalty_indicators': [],        # Signs of customer loyalty
            'dissatisfaction_risks': [],     # Potential problems
            'satisfaction_score': 75         # Overall satisfaction percentage
        }
        
        # Analyze stockout impact on customer experience - handle both dict and int inventory values
        stockouts = []
        for product, qty in inventory.items():
            if isinstance(qty, dict):
                actual_qty = qty.get('total_quantity', 0)
            elif hasattr(qty, 'total_quantity'):
                actual_qty = qty.total_quantity
            else:
                actual_qty = qty
            
            if actual_qty == 0:
                stockouts.append(product)
        
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
    
    def _analyze_customer_segments(self, store_state: Dict, context: Dict) -> Dict:
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
    
    def _evaluate_service_quality(self, store_state: Dict, context: Dict) -> Dict:
        """Evaluate service quality with Elle's attention to customer experience"""
        
        # Fix: Use dictionary access instead of StoreState attribute access
        inventory = store_state.get('inventory', {})
        
        quality = {
            'product_availability': 'good',     # Stock availability score
            'variety_score': 'excellent',       # Product variety assessment
            'convenience_factors': [],          # What makes shopping convenient
            'improvement_areas': [],            # Areas needing attention
            'experience_enhancers': []          # Ways to make shopping fabulous
        }
        
        # Evaluate product availability - handle both dict and int inventory values
        total_products = len(inventory)
        stocked_products = 0
        
        for product, qty in inventory.items():
            if isinstance(qty, dict):
                actual_qty = qty.get('total_quantity', 0)
            elif hasattr(qty, 'total_quantity'):
                actual_qty = qty.total_quantity
            else:
                actual_qty = qty
                
            if actual_qty > 0:
                stocked_products += 1
        
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
    
    def _calculate_confidence(self, store_state: Dict, satisfaction: Dict) -> float:
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
        
        elle_reasoning = " | ".join(reasoning_parts) + elle_conclusion
        return elle_reasoning

    # 💖 PHASE 4B.2: ELLE'S SPECIALIZED CUSTOMER PSYCHOLOGY TOOLS 💖
    
    def customer_satisfaction_analyzer(self, store_status: Dict, context: Dict) -> Dict:
        """💝 TOOL 1: Advanced customer satisfaction analysis and sentiment monitoring"""
        return self.tools.customer_satisfaction_analyzer(store_status, context)
    
    def loyalty_program_optimizer(self, store_status: Dict, context: Dict) -> Dict:
        """👑 TOOL 2: Customer loyalty program optimization and retention strategies"""
        return self.tools.loyalty_program_optimizer(store_status, context)
    
    def brand_sentiment_monitor(self, store_status: Dict, context: Dict) -> Dict:
        """✨ TOOL 3: Brand sentiment monitoring and reputation management"""
        return self.tools.brand_sentiment_monitor(store_status, context)
    
    def service_quality_metrics(self, store_status: Dict, context: Dict) -> Dict:
        """⭐ TOOL 4: Comprehensive service quality measurement and optimization"""
        return self.tools.service_quality_metrics(store_status, context)
    
    def relationship_building_tools(self, store_status: Dict, context: Dict) -> Dict:
        """💕 TOOL 5: Advanced customer relationship building and engagement strategies"""
        return self.tools.relationship_building_tools(store_status, context)
    
    def _create_customer_strategy_with_tools(self, satisfaction: Dict, segments: Dict, quality: Dict, tool_results: Dict) -> Dict:
        """Create Elle's customer experience strategy integrating tool insights"""
        # Start with base strategy
        strategy = self._create_customer_strategy(satisfaction, segments, quality)
        
        # 🛠️ Phase 5A.3: Integrate tool insights into strategy
        tool_insights = {
            'tool_driven_actions': [],
            'data_backed_recommendations': [],
            'tool_performance_score': 0
        }
        
        # Integrate satisfaction analyzer insights
        if 'satisfaction_analyzer' in tool_results:
            sat_data = tool_results['satisfaction_analyzer']
            sentiment_score = sat_data.get('customer_sentiment_score', 0)
            
            if sentiment_score < 70:
                tool_insights['tool_driven_actions'].append(f"💝 SATISFACTION TOOL: Immediate intervention needed (Score: {sentiment_score}%)")
                strategy['satisfaction_improvements'].extend(sat_data.get('improvement_opportunities', []))
            
            tool_insights['data_backed_recommendations'].extend([
                f"💝 {driver}" for driver in sat_data.get('satisfaction_drivers', [])[:2]
            ])
        
        # Integrate loyalty optimizer insights
        if 'loyalty_optimizer' in tool_results:
            loyalty_data = tool_results['loyalty_optimizer']
            loyalty_score = loyalty_data.get('loyalty_metrics', {}).get('loyalty_score', 0)
            
            if loyalty_score > 50:
                tool_insights['tool_driven_actions'].append(f"👑 LOYALTY TOOL: Strong foundation detected (Score: {loyalty_score})")
                strategy['segment_engagement'].extend(loyalty_data.get('program_recommendations', [])[:2])
        
        # Integrate brand sentiment insights
        if 'sentiment_monitor' in tool_results:
            sentiment_data = tool_results['sentiment_monitor']
            brand_pos = sentiment_data.get('brand_perception', {}).get('brand_positioning', 'unknown')
            
            tool_insights['tool_driven_actions'].append(f"✨ BRAND TOOL: Position as {brand_pos}")
            strategy['service_enhancements'].extend(sentiment_data.get('reputation_action_plan', [])[:2])
        
        # Calculate tool performance score
        tool_insights['tool_performance_score'] = len([r for r in tool_results.values() if r]) * 20  # 20 points per successful tool
        
        strategy.update(tool_insights)
        return strategy
    
    def _calculate_confidence_with_tools(self, store_state: Dict, tool_results: Dict) -> float:
        """Calculate confidence enhanced by tool data quality"""
        # Generate satisfaction data for base confidence calculation
        dummy_context = {}
        satisfaction_data = self._analyze_customer_satisfaction(store_state, dummy_context)
        base_confidence = self._calculate_confidence(store_state, satisfaction_data)
        
        # 🛠️ Phase 5A.3: Boost confidence based on tool data richness
        tool_data_quality = 0
        total_tools = len(tool_results)
        
        for tool_name, tool_data in tool_results.items():
            if tool_data and isinstance(tool_data, dict):
                # Count non-empty data points
                data_points = sum(1 for v in tool_data.values() if v)
                tool_data_quality += min(data_points / 5, 1.0)  # Normalize to 1.0 per tool
        
        if total_tools > 0:
            tool_confidence_boost = (tool_data_quality / total_tools) * 0.15  # Up to 15% boost
            enhanced_confidence = min(base_confidence + tool_confidence_boost, 1.0)
        else:
            enhanced_confidence = base_confidence
        
        return enhanced_confidence
    
    def _determine_priority_with_tools(self, tool_results: Dict, satisfaction: Dict) -> int:
        """Determine priority enhanced by tool insights"""
        # Generate dummy segments data for base priority calculation
        dummy_segments = {
            'price_sensitive_behavior': 'normal',
            'brand_loyal_behavior': 'normal',
            'segment_balance': 'healthy'
        }
        base_priority = self._determine_priority(satisfaction, dummy_segments)
        
        # 🛠️ Phase 5A.3: Adjust priority based on tool findings
        priority_adjustments = 0
        
        # Check satisfaction tool for urgent issues
        if 'satisfaction_analyzer' in tool_results:
            sentiment_score = tool_results['satisfaction_analyzer'].get('customer_sentiment_score', 75)
            if sentiment_score < 50:
                priority_adjustments += 3  # Critical satisfaction issue
            elif sentiment_score < 70:
                priority_adjustments += 1  # Moderate issue
        
        # Check for service quality issues
        if 'quality_metrics' in tool_results:
            service_score = tool_results['quality_metrics'].get('service_quality_index', 75)
            if service_score < 60:
                priority_adjustments += 2  # Service crisis
        
        enhanced_priority = min(base_priority + priority_adjustments, 10)
        return enhanced_priority
    
    def _generate_elle_reasoning_with_tools(self, tool_results: Dict, tool_usage_log: List[Dict], action_plan: Dict) -> str:
        """Generate Elle's reasoning with explicit tool integration"""
        
        # 🛠️ Phase 5A.3: Start with tool usage summary
        reasoning = "💕 ELLE'S ASSESSMENT: 'Our customers deserve to feel fabulous!' | "
        
        # Display tool usage summary
        tools_used = len(tool_usage_log)
        reasoning += f"🛠️ TOOLS DEPLOYED: {tools_used}/5 customer psychology tools executed. "
        
        # Highlight key tool insights
        key_insights = []
        for tool_log in tool_usage_log:
            if tool_log.get('key_insight'):
                key_insights.append(f"{tool_log['emoji']} {tool_log['key_insight']}")
        
        reasoning += f"📊 KEY TOOL INSIGHTS: {' | '.join(key_insights[:3])}. "
        
        # Tool-driven recommendations
        tool_actions = action_plan.get('tool_driven_actions', [])
        if tool_actions:
            reasoning += f"🎯 TOOL-DRIVEN ACTIONS: {len(tool_actions)} data-backed strategies identified. "
            reasoning += f"Top priority: {tool_actions[0] if tool_actions else 'Maintain excellence'}. "
        
        # Performance metrics
        tool_performance = action_plan.get('tool_performance_score', 0)
        reasoning += f"⚡ TOOL PERFORMANCE: {tool_performance}% data coverage achieved. "
        
        # Elle's personality-driven conclusion
        if 'satisfaction_analyzer' in tool_results:
            sentiment_score = tool_results['satisfaction_analyzer'].get('customer_sentiment_score', 75)
            if sentiment_score >= 80:
                reasoning += "💖 ELLE'S CONCLUSION: 'Like, totally amazing! Our customers are loving the experience!'"
            elif sentiment_score >= 60:
                reasoning += "💛 ELLE'S CONCLUSION: 'We're doing well, but there's always room to make things more fabulous!'"
            else:
                reasoning += "💔 ELLE'S CONCLUSION: 'This is, like, a crisis! We need to show our customers how much we care!'"
        else:
            reasoning += "💕 ELLE'S CONCLUSION: 'Let's make every customer interaction absolutely fabulous!'"
        
        return reasoning 