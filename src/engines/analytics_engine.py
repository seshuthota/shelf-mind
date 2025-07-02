from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import statistics
from src.core.models import StoreState, PRODUCTS, CustomerType

@dataclass
class DecisionOutcome:
    """Track individual decision outcomes for pattern analysis"""
    day: int
    decision_type: str  # 'pricing', 'inventory', 'supplier', 'crisis'
    decision_data: Dict[str, Any]
    market_context: Dict[str, Any]  # Season, weather, competition, etc.
    immediate_outcome: Dict[str, Any]  # Sales, profit, reactions
    effectiveness_score: float  # 0-100 calculated performance score

@dataclass 
class PerformanceMetrics:
    """Daily performance tracking"""
    day: int
    revenue: float
    profit: float
    profit_margin: float
    inventory_turnover: float
    pricing_accuracy: float  # How well prices matched demand
    competitive_position: float  # Market position vs competitor
    crisis_response_quality: float  # Emergency management effectiveness
    overall_score: float

@dataclass
class StrategyPattern:
    """Identified successful strategy patterns"""
    pattern_name: str
    conditions: Dict[str, Any]  # When this pattern works
    actions: Dict[str, Any]     # What actions to take
    success_rate: float         # Historical success rate
    avg_profit_impact: float    # Average profit improvement
    confidence_score: float     # How reliable this pattern is

class AnalyticsEngine:
    """🧠 Phase 3A: Performance Analysis & Strategic Intelligence Engine
    
    Transform Scrooge from tactical Warlord to strategic CEO with:
    - Historical decision analysis and pattern recognition
    - Performance optimization recommendations  
    - Strategic insight generation
    - Self-learning and adaptation capabilities
    """
    
    def __init__(self):
        self.decision_history: List[DecisionOutcome] = []
        self.performance_history: List[PerformanceMetrics] = []
        self.strategy_patterns: List[StrategyPattern] = []
        self.learning_insights: List[str] = []
        
        # Performance tracking
        self.daily_scores = defaultdict(list)
        self.strategy_effectiveness = defaultdict(list)
        self.competitive_intelligence = defaultdict(list)
        
        # Pattern recognition
        self.seasonal_patterns = defaultdict(dict)
        self.pricing_patterns = defaultdict(dict) 
        self.crisis_patterns = defaultdict(dict)
        
    def record_decision(self, decision_type: str, decision_data: Dict, 
                       store_state: StoreState, market_context: Dict) -> None:
        """📊 Record a decision for future analysis"""
        
        # Calculate immediate context
        immediate_context = {
            'cash_before': store_state.cash,
            'inventory_levels': {name: item.total_quantity for name, item in store_state.inventory.items()},
            'day': store_state.day,
            'active_crises': len(store_state.active_crises),
            'pending_deliveries': len(store_state.pending_deliveries)
        }
        
        # Create decision record (outcome will be updated later)
        decision = DecisionOutcome(
            day=store_state.day,
            decision_type=decision_type,
            decision_data=decision_data,
            market_context=market_context,
            immediate_outcome=immediate_context,
            effectiveness_score=0.0  # Will be calculated after seeing results
        )
        
        self.decision_history.append(decision)
    
    def update_decision_outcome(self, day: int, outcome_data: Dict) -> None:
        """📈 Update decision outcomes after seeing results"""
        
        # Find decisions from this day
        day_decisions = [d for d in self.decision_history if d.day == day]
        
        for decision in day_decisions:
            # Calculate effectiveness score based on decision type
            if decision.decision_type == 'pricing':
                decision.effectiveness_score = self._calculate_pricing_effectiveness(decision, outcome_data)
            elif decision.decision_type == 'inventory': 
                decision.effectiveness_score = self._calculate_inventory_effectiveness(decision, outcome_data)
            elif decision.decision_type == 'crisis':
                decision.effectiveness_score = self._calculate_crisis_effectiveness(decision, outcome_data)
            
            # Update outcome data
            decision.immediate_outcome.update(outcome_data)
    
    def calculate_daily_performance(self, store_state: StoreState, 
                                  competitor_info: Dict, yesterday_data: Dict = None) -> PerformanceMetrics:
        """📊 Calculate comprehensive daily performance metrics"""
        
        revenue = store_state.total_revenue
        profit = store_state.total_profit
        profit_margin = (profit / revenue * 100) if revenue > 0 else 0
        
        # Calculate inventory turnover (approximate)
        total_inventory_value = sum(
            item.total_quantity * PRODUCTS[name].cost 
            for name, item in store_state.inventory.items()
        )
        inventory_turnover = revenue / total_inventory_value if total_inventory_value > 0 else 0
        
        # Calculate competitive position
        competitive_position = self._calculate_competitive_position(store_state, competitor_info)
        
        # Calculate pricing accuracy
        pricing_accuracy = self._calculate_pricing_accuracy(store_state, yesterday_data)
        
        # Calculate crisis response quality
        crisis_response_quality = self._calculate_crisis_response_quality(store_state)
        
        # Overall strategic score
        overall_score = (
            profit_margin * 0.3 +
            competitive_position * 0.25 +
            pricing_accuracy * 0.2 + 
            inventory_turnover * 20 * 0.15 +  # Scale inventory turnover
            crisis_response_quality * 0.1
        )
        
        metrics = PerformanceMetrics(
            day=store_state.day,
            revenue=revenue,
            profit=profit,
            profit_margin=profit_margin,
            inventory_turnover=inventory_turnover,
            pricing_accuracy=pricing_accuracy,
            competitive_position=competitive_position,
            crisis_response_quality=crisis_response_quality,
            overall_score=overall_score
        )
        
        self.performance_history.append(metrics)
        return metrics
    
    def identify_strategy_patterns(self, min_confidence: float = 0.7) -> List[StrategyPattern]:
        """🎯 Identify successful strategy patterns from historical data"""
        
        if len(self.decision_history) < 7:  # Need at least a week of data
            return []
        
        patterns = []
        
        # Seasonal pricing patterns
        seasonal_pricing = self._analyze_seasonal_pricing_patterns()
        if seasonal_pricing:
            patterns.extend(seasonal_pricing)
        
        # Crisis response patterns
        crisis_patterns = self._analyze_crisis_response_patterns()
        if crisis_patterns:
            patterns.extend(crisis_patterns)
        
        # Competitive warfare patterns
        competitive_patterns = self._analyze_competitive_patterns()
        if competitive_patterns:
            patterns.extend(competitive_patterns)
        
        # Filter by confidence threshold
        high_confidence_patterns = [p for p in patterns if p.confidence_score >= min_confidence]
        
        self.strategy_patterns = high_confidence_patterns
        return high_confidence_patterns
    
    def generate_strategic_insights(self, current_state: StoreState, 
                                  market_context: Dict, competitor_info: Dict) -> Dict[str, Any]:
        """💡 Generate strategic insights and optimization recommendations"""
        
        insights = {
            'performance_trends': self._analyze_performance_trends(),
            'optimization_opportunities': self._identify_optimization_opportunities(current_state),
            'strategic_recommendations': self._generate_strategic_recommendations(current_state, market_context),
            'competitive_intelligence': self._analyze_competitive_intelligence(competitor_info),
            'risk_warnings': self._identify_strategic_risks(current_state),
            'learning_summary': self._generate_learning_summary()
        }
        
        return insights
    
    def get_performance_analysis(self, days_back: int = 7) -> Dict[str, Any]:
        """📈 Get comprehensive performance analysis for recent period"""
        
        if not self.performance_history:
            return {'error': 'No performance data available yet'}
        
        recent_metrics = self.performance_history[-days_back:] if len(self.performance_history) >= days_back else self.performance_history
        
        if not recent_metrics:
            return {'error': 'Insufficient data for analysis'}
        
        analysis = {
            'period': f'Last {len(recent_metrics)} days',
            'average_performance': {
                'profit_margin': statistics.mean([m.profit_margin for m in recent_metrics]),
                'competitive_position': statistics.mean([m.competitive_position for m in recent_metrics]),
                'overall_score': statistics.mean([m.overall_score for m in recent_metrics])
            },
            'trends': self._calculate_performance_trends(recent_metrics),
            'best_day': max(recent_metrics, key=lambda x: x.overall_score),
            'worst_day': min(recent_metrics, key=lambda x: x.overall_score),
            'strategy_effectiveness': self._analyze_strategy_effectiveness(recent_metrics)
        }
        
        return analysis
    
    # Internal analysis methods
    
    def _calculate_pricing_effectiveness(self, decision: DecisionOutcome, outcome: Dict) -> float:
        """Calculate how effective pricing decisions were"""
        
        # Factors: sales volume, profit margin, competitive response
        sales_factor = min(100, sum(outcome.get('daily_sales', {}).values()) * 10)
        profit_factor = max(0, min(100, outcome.get('daily_profit', 0) * 2))
        competitive_factor = 100 - (outcome.get('price_war_intensity', 0) * 10)
        
        return (sales_factor * 0.4 + profit_factor * 0.4 + competitive_factor * 0.2)
    
    def _calculate_inventory_effectiveness(self, decision: DecisionOutcome, outcome: Dict) -> float:
        """Calculate how effective inventory decisions were"""
        
        # Factors: stockout prevention, spoilage minimization, cash flow
        stockout_factor = 100 - (len(outcome.get('stockouts', [])) * 20)
        spoilage_factor = 100 - (outcome.get('total_spoilage_cost', 0) * 10)
        cash_factor = min(100, outcome.get('cash_after', 0) / 100)
        
        return (stockout_factor * 0.4 + spoilage_factor * 0.3 + cash_factor * 0.3)
    
    def _calculate_crisis_effectiveness(self, decision: DecisionOutcome, outcome: Dict) -> float:
        """Calculate how effective crisis response was"""
        
        # Factors: crisis resolution speed, financial impact, business continuity
        resolution_factor = 100 - (outcome.get('crisis_duration', 1) * 10)
        financial_factor = 100 - (outcome.get('crisis_cost', 0) * 5)
        continuity_factor = 100 if outcome.get('business_continued', True) else 50
        
        return (resolution_factor * 0.4 + financial_factor * 0.4 + continuity_factor * 0.2)
    
    def _calculate_competitive_position(self, store_state: StoreState, competitor_info: Dict) -> float:
        """Calculate competitive market position (0-100)"""
        
        # Compare prices, market share, competitive intensity
        if not competitor_info:
            return 50  # Neutral position
        
        price_advantage = competitor_info.get('price_advantage_score', 50)
        war_intensity = competitor_info.get('war_intensity', 0)
        market_position = max(0, min(100, price_advantage - (war_intensity * 5)))
        
        return market_position
    
    def _calculate_pricing_accuracy(self, store_state: StoreState, yesterday_data: Dict = None) -> float:
        """Calculate how well prices matched demand"""
        
        if not yesterday_data:
            return 50
        
        # Analyze price vs sales correlation
        sales_data = yesterday_data.get('daily_sales', {})
        total_sales = sum(sales_data.values())
        
        if total_sales == 0:
            return 30  # Poor pricing if no sales
        
        # Higher sales generally indicates good pricing
        return min(100, total_sales * 5)
    
    def _calculate_crisis_response_quality(self, store_state: StoreState) -> float:
        """Calculate quality of crisis management"""
        
        active_crises = len(store_state.active_crises)
        
        if active_crises == 0:
            return 100  # No crises = perfect score
        
        # Score based on business continuity during crises
        if store_state.cash > 50:  # Still have operational cash
            return max(50, 100 - (active_crises * 15))
        else:
            return max(20, 60 - (active_crises * 20))
    
    def _analyze_performance_trends(self) -> Dict[str, str]:
        """Analyze performance trends over time"""
        
        if len(self.performance_history) < 3:
            return {'trend': 'insufficient_data'}
        
        recent = self.performance_history[-3:]
        scores = [m.overall_score for m in recent]
        
        if scores[-1] > scores[0] + 5:
            trend = 'improving'
        elif scores[-1] < scores[0] - 5:
            trend = 'declining'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'score_change': scores[-1] - scores[0],
            'current_score': scores[-1]
        }
    
    def _identify_optimization_opportunities(self, store_state: StoreState) -> List[str]:
        """Identify specific optimization opportunities"""
        
        opportunities = []
        
        # Cash flow optimization
        if store_state.cash < 100:
            opportunities.append("💰 Cash flow warning: Consider emergency actions or price increases")
        
        # Inventory optimization
        low_stock = [name for name, item in store_state.inventory.items() if item.total_quantity <= 3]
        if low_stock:
            opportunities.append(f"📦 Inventory warning: Low stock on {', '.join(low_stock)}")
        
        # Crisis management
        if store_state.active_crises:
            opportunities.append("🚨 Active crises require immediate attention and strategic response")
        
        return opportunities
    
    def _generate_strategic_recommendations(self, store_state: StoreState, market_context: Dict) -> List[str]:
        """Generate strategic recommendations based on analysis"""
        
        recommendations = []
        
        # Seasonal recommendations
        season = market_context.get('season', 'spring')
        if season == 'summer':
            recommendations.append("🌞 Summer strategy: Focus on beverages and ice cream pricing")
        elif season == 'winter':
            recommendations.append("❄️ Winter strategy: Emphasize comfort foods and hot beverages")
        
        # Market condition recommendations
        economic = market_context.get('economic_condition', 'normal')
        if economic == 'recession':
            recommendations.append("📉 Recession strategy: Focus on value pricing and essential items")
        elif economic == 'boom':
            recommendations.append("📈 Economic boom: Consider premium pricing on luxury items")
        
        return recommendations
    
    def _analyze_competitive_intelligence(self, competitor_info: Dict) -> Dict[str, Any]:
        """Analyze competitive intelligence and provide strategic guidance"""
        
        analysis = {
            'competitive_threat_level': competitor_info.get('war_intensity', 0),
            'competitor_strategy': competitor_info.get('strategy', 'unknown'),
            'recommended_response': 'maintain_position'
        }
        
        war_intensity = competitor_info.get('war_intensity', 0)
        if war_intensity > 7:
            analysis['recommended_response'] = 'aggressive_counter'
        elif war_intensity > 4:
            analysis['recommended_response'] = 'defensive_positioning'
        
        return analysis
    
    def _identify_strategic_risks(self, store_state: StoreState) -> List[str]:
        """Identify potential strategic risks"""
        
        risks = []
        
        # Financial risks
        if store_state.cash < 50:
            risks.append("💸 CRITICAL: Low cash reserves - bankruptcy risk")
        
        # Operational risks
        if store_state.accounts_payable > store_state.cash:
            risks.append("💳 DEBT RISK: Accounts payable exceeds available cash")
        
        # Crisis risks
        if len(store_state.active_crises) > 2:
            risks.append("🚨 CRISIS OVERLOAD: Multiple simultaneous crises")
        
        return risks
    
    def _generate_learning_summary(self) -> List[str]:
        """Generate summary of key learnings"""
        
        if len(self.decision_history) < 5:
            return ["📚 More data needed for comprehensive learning analysis"]
        
        learnings = []
        
        # Analyze pricing decision effectiveness
        pricing_decisions = [d for d in self.decision_history if d.decision_type == 'pricing']
        if pricing_decisions:
            avg_effectiveness = statistics.mean([d.effectiveness_score for d in pricing_decisions])
            if avg_effectiveness > 70:
                learnings.append("🎯 STRENGTH: Pricing decisions consistently effective")
            else:
                learnings.append("⚠️ OPPORTUNITY: Pricing strategy needs optimization")
        
        # Analyze crisis management
        crisis_decisions = [d for d in self.decision_history if d.decision_type == 'crisis']
        if crisis_decisions:
            avg_crisis_response = statistics.mean([d.effectiveness_score for d in crisis_decisions])
            if avg_crisis_response > 75:
                learnings.append("🛡️ STRENGTH: Excellent crisis management capabilities")
            else:
                learnings.append("🚨 PRIORITY: Crisis response protocols need improvement")
        
        return learnings
    
    def _analyze_seasonal_pricing_patterns(self) -> List[StrategyPattern]:
        """Analyze seasonal pricing effectiveness"""
        # Implementation for seasonal pattern analysis
        return []  # Placeholder for now
    
    def _analyze_crisis_response_patterns(self) -> List[StrategyPattern]:
        """Analyze crisis response effectiveness"""
        # Implementation for crisis pattern analysis  
        return []  # Placeholder for now
    
    def _analyze_competitive_patterns(self) -> List[StrategyPattern]:
        """Analyze competitive strategy effectiveness"""
        # Implementation for competitive pattern analysis
        return []  # Placeholder for now
    
    def _calculate_performance_trends(self, metrics: List[PerformanceMetrics]) -> Dict:
        """Calculate performance trends from metrics"""
        if len(metrics) < 2:
            return {'trend': 'insufficient_data'}
        
        first_score = metrics[0].overall_score
        last_score = metrics[-1].overall_score
        
        return {
            'direction': 'improving' if last_score > first_score else 'declining',
            'change': last_score - first_score
        }
    
    def _analyze_strategy_effectiveness(self, metrics: List[PerformanceMetrics]) -> Dict:
        """Analyze which strategies have been most effective"""
        
        avg_score = statistics.mean([m.overall_score for m in metrics])
        best_day = max(metrics, key=lambda x: x.overall_score)
        
        return {
            'average_effectiveness': avg_score,
            'best_performance_day': best_day.day,
            'best_performance_score': best_day.overall_score
        } 