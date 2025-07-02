import random
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import statistics

@dataclass
class NewProduct:
    """Potential new product for evaluation"""
    name: str
    category: str
    cost: float
    suggested_price: float
    market_demand: str  # "high", "medium", "low"
    seasonality: str   # "none", "summer", "winter", "holiday"
    spoilage_days: int
    shelf_space: int   # units of shelf space required

@dataclass
class ServiceOpportunity:
    """New service expansion opportunity"""
    name: str
    setup_cost: float
    daily_revenue_potential: float
    customer_segment: str  # "price_sensitive", "brand_loyal", "all"
    implementation_difficulty: str  # "easy", "medium", "hard"
    regulatory_requirements: bool

@dataclass
class LoyaltyProgram:
    """Customer loyalty program configuration"""
    name: str
    type: str  # "points", "discount", "cashback"
    reward_threshold: float
    reward_value: float
    enrollment_cost: float
    retention_improvement: float  # percentage improvement in retention

@dataclass
class LocationOpportunity:
    """Multi-location expansion opportunity"""
    area: str
    population: int
    competition_level: str  # "low", "medium", "high"
    rent_cost: float
    setup_cost: float
    revenue_multiplier: float

class GrowthExpansionEngine:
    """Main Growth & Expansion Intelligence Engine - Phase 3D"""
    
    def __init__(self):
        self.potential_products = self._initialize_products()
        self.service_opportunities = self._initialize_services()
        self.loyalty_programs = self._initialize_loyalty_programs()
        self.location_opportunities = self._initialize_locations()
    
    def _initialize_products(self) -> List[NewProduct]:
        """Initialize potential new products"""
        return [
            NewProduct("Energy Drink", "beverages", 1.20, 2.49, "high", "none", 90, 1),
            NewProduct("Protein Bar", "snacks", 1.80, 3.49, "medium", "none", 180, 1),
            NewProduct("Hot Coffee", "beverages", 0.30, 1.99, "high", "winter", 1, 0),
            NewProduct("Fresh Sandwich", "food", 2.50, 5.99, "medium", "none", 3, 2),
            NewProduct("Phone Charger", "electronics", 3.00, 9.99, "low", "none", 0, 1),
            NewProduct("Lottery Tickets", "services", 0.00, 2.00, "medium", "none", 0, 0),
        ]
    
    def _initialize_services(self) -> List[ServiceOpportunity]:
        """Initialize service expansion opportunities"""
        return [
            ServiceOpportunity("Lottery Tickets", 50, 25, "all", "easy", True),
            ServiceOpportunity("Money Orders", 100, 15, "all", "medium", True),
            ServiceOpportunity("ATM Service", 1500, 40, "all", "hard", True),
            ServiceOpportunity("Package Pickup", 200, 20, "all", "medium", False),
        ]
    
    def _initialize_loyalty_programs(self) -> List[LoyaltyProgram]:
        """Initialize loyalty program options"""
        return [
            LoyaltyProgram("Points Rewards", "points", 100, 5, 50, 15),
            LoyaltyProgram("Discount Card", "discount", 50, 10, 25, 12),
            LoyaltyProgram("Cashback Plus", "cashback", 75, 5, 40, 18),
        ]
    
    def _initialize_locations(self) -> List[LocationOpportunity]:
        """Initialize location expansion opportunities"""
        return [
            LocationOpportunity("Downtown Business District", 15000, "high", 3500, 25000, 1.4),
            LocationOpportunity("Suburban Shopping Center", 8000, "medium", 2200, 18000, 1.2),
            LocationOpportunity("University Campus", 12000, "low", 2800, 20000, 1.6),
        ]
    
    def evaluate_new_products(self, store_data: Dict, current_day: int) -> Dict[str, Any]:
        """Evaluate new product opportunities"""
        current_season = self._get_current_season(current_day)
        evaluations = []
        
        for product in self.potential_products:
            # Calculate opportunity score
            demand_score = {"high": 0.8, "medium": 0.5, "low": 0.3}[product.market_demand]
            
            # Seasonal bonus
            seasonal_bonus = 0.1  # Default
            if product.seasonality != "none" and product.seasonality.lower() in current_season.lower():
                seasonal_bonus = 0.3
            
            opportunity_score = demand_score + seasonal_bonus
            
            # Revenue projection
            daily_sales = self._project_daily_sales(product, store_data, opportunity_score)
            monthly_profit = daily_sales * (product.suggested_price - product.cost) * 30
            
            evaluation = {
                "product": product.name,
                "category": product.category,
                "opportunity_score": round(opportunity_score, 2),
                "projected_daily_sales": round(daily_sales, 1),
                "monthly_profit": round(monthly_profit, 2),
                "initial_investment": product.cost * 10,
                "recommendation": self._get_recommendation(opportunity_score, monthly_profit)
            }
            evaluations.append(evaluation)
        
        evaluations.sort(key=lambda x: x["opportunity_score"], reverse=True)
        
        return {
            "current_season": current_season,
            "top_opportunities": evaluations[:3],
            "all_evaluations": evaluations
        }
    
    def analyze_service_opportunities(self, store_data: Dict, customer_data: Dict) -> Dict[str, Any]:
        """Analyze service expansion opportunities"""
        cash = store_data.get("cash", 0)
        daily_customers = store_data.get("daily_customers", 50)
        
        evaluations = []
        
        for service in self.service_opportunities:
            if service.setup_cost > cash * 0.4:
                continue
            
            # Calculate revenue
            daily_revenue = daily_customers * (service.daily_revenue_potential / 100)
            monthly_profit = daily_revenue * 30 * 0.6  # 60% margin
            
            evaluation = {
                "service": service.name,
                "setup_cost": service.setup_cost,
                "monthly_profit": round(monthly_profit, 2),
                "roi_months": round(service.setup_cost / monthly_profit, 1) if monthly_profit > 0 else 999,
                "recommendation": "IMPLEMENT" if monthly_profit > 10 else "CONSIDER"
            }
            evaluations.append(evaluation)
        
        evaluations.sort(key=lambda x: x["monthly_profit"], reverse=True)
        
        return {
            "top_opportunities": evaluations[:3],
            "all_evaluations": evaluations
        }
    
    def optimize_customer_retention(self, store_data: Dict, customer_data: Dict) -> Dict[str, Any]:
        """Optimize customer retention strategies"""
        daily_customers = store_data.get("daily_customers", 50)
        daily_revenue = store_data.get("daily_revenue", 100)
        
        evaluations = []
        
        for program in self.loyalty_programs:
            # Calculate impact
            retained_customers = daily_customers * (program.retention_improvement / 100)
            monthly_benefit = retained_customers * 30 * 2  # $2 extra per visit
            setup_cost = program.enrollment_cost * daily_customers * 0.3
            
            evaluation = {
                "program": program.name,
                "setup_cost": round(setup_cost, 2),
                "monthly_benefit": round(monthly_benefit, 2),
                "roi_percentage": round((monthly_benefit * 12 / setup_cost) * 100, 1) if setup_cost > 0 else 0,
                "recommendation": "IMPLEMENT" if monthly_benefit > 15 else "CONSIDER"
            }
            evaluations.append(evaluation)
        
        evaluations.sort(key=lambda x: x["roi_percentage"], reverse=True)
        
        return {
            "top_recommendation": evaluations[0] if evaluations else None,
            "all_programs": evaluations
        }
    
    def analyze_expansion_opportunities(self, store_data: Dict) -> Dict[str, Any]:
        """Analyze multi-location expansion opportunities"""
        current_cash = store_data.get("cash", 0)
        current_daily_profit = store_data.get("daily_profit", 10)
        
        # Check readiness
        expansion_ready = current_cash >= 20000 and current_daily_profit >= 15
        
        evaluations = []
        
        for location in self.location_opportunities:
            projected_profit = current_daily_profit * location.revenue_multiplier * 0.8  # 80% efficiency
            annual_profit = projected_profit * 365
            roi_percentage = (annual_profit / location.setup_cost) * 100 if location.setup_cost > 0 else 0
            
            evaluation = {
                "location": location.area,
                "setup_cost": location.setup_cost,
                "projected_annual_profit": round(annual_profit, 2),
                "roi_percentage": round(roi_percentage, 1),
                "cash_available": current_cash >= location.setup_cost,
                "recommendation": "PRIME" if roi_percentage >= 20 else "CONSIDER"
            }
            evaluations.append(evaluation)
        
        evaluations.sort(key=lambda x: x["roi_percentage"], reverse=True)
        
        return {
            "expansion_ready": expansion_ready,
            "top_opportunities": evaluations[:3],
            "all_opportunities": evaluations
        }
    
    def get_comprehensive_growth_analysis(self, store_data: Dict, customer_data: Dict, current_day: int) -> Dict[str, Any]:
        """Get comprehensive growth and expansion analysis"""
        return {
            "analysis_date": current_day,
            "products": self.evaluate_new_products(store_data, current_day),
            "services": self.analyze_service_opportunities(store_data, customer_data),
            "retention": self.optimize_customer_retention(store_data, customer_data),
            "expansion": self.analyze_expansion_opportunities(store_data),
            "growth_strategy": self._create_growth_strategy(store_data)
        }
    
    # Helper methods
    def _get_current_season(self, day: int) -> str:
        season_cycle = (day // 30) % 4
        return ["Spring", "Summer", "Fall", "Winter"][season_cycle]
    
    def _project_daily_sales(self, product: NewProduct, store_data: Dict, opportunity_score: float) -> float:
        daily_customers = store_data.get("daily_customers", 50)
        penetration_rate = opportunity_score * 0.3
        category_multiplier = {"beverages": 1.2, "snacks": 1.0, "food": 0.8, "electronics": 0.3, "services": 0.5}.get(product.category, 1.0)
        return max(1.0, daily_customers * penetration_rate * category_multiplier)
    
    def _get_recommendation(self, opportunity_score: float, monthly_profit: float) -> str:
        if opportunity_score >= 0.7 and monthly_profit >= 50:
            return "STRONG BUY"
        elif opportunity_score >= 0.5 and monthly_profit >= 25:
            return "BUY"
        elif opportunity_score >= 0.4:
            return "CONSIDER"
        else:
            return "AVOID"
    
    def _create_growth_strategy(self, store_data: Dict) -> Dict[str, Any]:
        cash = store_data.get("cash", 0)
        daily_profit = store_data.get("daily_profit", 0)
        
        if cash < 200:
            stage = "SURVIVAL"
            priority = "Focus on core business profitability"
        elif cash < 1000:
            stage = "GROWTH"
            priority = "Expand products and services"
        else:
            stage = "EXPANSION"
            priority = "Consider retention and expansion"
        
        return {
            "business_stage": stage,
            "primary_focus": priority,
            "cash_position": cash,
            "profit_level": daily_profit
        } 