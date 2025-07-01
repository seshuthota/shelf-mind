import random
from typing import Dict, List
from models import (
    MarketEvent, Season, WeatherEvent, Holiday, EconomicCondition, PRODUCTS
)


class MarketEventsEngine:
    """🌍 Phase 2B: Market Events Engine - Seasonal Demand & Dynamic Market Conditions
    
    FEATURES:
    - 4-season cycle with realistic progression
    - Weather events affecting product demand
    - Holiday spikes for seasonal products  
    - Economic cycles (boom/recession/recovery)
    - Product-specific seasonal multipliers
    """
    
    def __init__(self):
        self.current_season = Season.SPRING
        self.current_economic_condition = EconomicCondition.NORMAL
        self.economic_cycle_duration = 0  # Days remaining in current cycle
        self.season_start_day = 1
        self.season_length = 30  # Each season lasts ~30 days
        
        # Economic cycle tracking
        self.boom_probability = 0.15    # 15% chance per month
        self.recession_probability = 0.10  # 10% chance per month
        
    def get_market_conditions(self, day: int) -> MarketEvent:
        """🌍 Generate daily market conditions with seasonal effects"""
        
        # Update season based on day progression
        self._update_season(day)
        
        # Update economic conditions
        self._update_economic_conditions(day)
        
        # Generate weather event
        weather = self._generate_weather_event()
        
        # Check for holidays
        holiday = self._check_for_holiday(day)
        
        # Calculate overall market demand multiplier
        demand_multiplier = self._calculate_demand_multiplier(weather, holiday)
        
        # Generate descriptive text
        description = self._generate_market_description(weather, holiday)
        
        return MarketEvent(
            day=day,
            season=self.current_season,
            weather=weather,
            holiday=holiday,
            economic_condition=self.current_economic_condition,
            description=description,
            demand_multiplier=demand_multiplier
        )
    
    def get_product_demand_multiplier(self, product_name: str, market_event: MarketEvent) -> float:
        """🎯 Calculate total demand multiplier for specific product"""
        base_multiplier = 1.0
        
        # Seasonal effect
        product = PRODUCTS[product_name]
        seasonal_mult = product.seasonal_multiplier.get(market_event.season.value, 1.0)
        
        # Weather effects on specific products
        weather_mult = self._get_weather_product_multiplier(product_name, market_event.weather)
        
        # Holiday effects on specific products
        holiday_mult = self._get_holiday_product_multiplier(product_name, market_event.holiday)
        
        # Economic effects (affects all products)
        economic_mult = self._get_economic_multiplier(market_event.economic_condition)
        
        # Combine all effects
        total_multiplier = (base_multiplier * seasonal_mult * weather_mult * 
                          holiday_mult * economic_mult * market_event.demand_multiplier)
        
        return max(0.1, total_multiplier)  # Minimum 10% demand
    
    def _update_season(self, day: int):
        """Update current season based on day progression"""
        days_since_season_start = day - self.season_start_day
        
        if days_since_season_start >= self.season_length:
            # Advance to next season
            seasons = [Season.SPRING, Season.SUMMER, Season.FALL, Season.WINTER]
            current_index = seasons.index(self.current_season)
            self.current_season = seasons[(current_index + 1) % 4]
            self.season_start_day = day
            
    def _update_economic_conditions(self, day: int):
        """Update economic conditions with realistic cycles"""
        if self.economic_cycle_duration > 0:
            self.economic_cycle_duration -= 1
        else:
            # Time to potentially change economic conditions
            if self.current_economic_condition == EconomicCondition.NORMAL:
                # Could enter boom or recession
                rand = random.random()
                if rand < self.boom_probability:
                    self.current_economic_condition = EconomicCondition.BOOM
                    self.economic_cycle_duration = random.randint(20, 40)  # 20-40 days
                elif rand < self.boom_probability + self.recession_probability:
                    self.current_economic_condition = EconomicCondition.RECESSION
                    self.economic_cycle_duration = random.randint(30, 60)  # 30-60 days
                else:
                    self.economic_cycle_duration = random.randint(15, 30)  # Stay normal
                    
            elif self.current_economic_condition == EconomicCondition.BOOM:
                # Boom ends, might enter normal or recession
                if random.random() < 0.7:
                    self.current_economic_condition = EconomicCondition.NORMAL
                    self.economic_cycle_duration = random.randint(20, 40)
                else:
                    self.current_economic_condition = EconomicCondition.RECESSION
                    self.economic_cycle_duration = random.randint(25, 50)
                    
            elif self.current_economic_condition == EconomicCondition.RECESSION:
                # Recession ends, enter recovery then normal
                self.current_economic_condition = EconomicCondition.RECOVERY
                self.economic_cycle_duration = random.randint(15, 30)
                
            elif self.current_economic_condition == EconomicCondition.RECOVERY:
                # Recovery leads to normal
                self.current_economic_condition = EconomicCondition.NORMAL
                self.economic_cycle_duration = random.randint(20, 40)
    
    def _generate_weather_event(self) -> WeatherEvent:
        """Generate weather event based on season"""
        season_weather = {
            Season.SPRING: {
                WeatherEvent.NORMAL: 0.6,
                WeatherEvent.RAINY_DAY: 0.25,
                WeatherEvent.PERFECT_WEATHER: 0.15
            },
            Season.SUMMER: {
                WeatherEvent.NORMAL: 0.5,
                WeatherEvent.HEAT_WAVE: 0.3,
                WeatherEvent.PERFECT_WEATHER: 0.2
            },
            Season.FALL: {
                WeatherEvent.NORMAL: 0.65,
                WeatherEvent.RAINY_DAY: 0.2,
                WeatherEvent.COLD_SNAP: 0.15
            },
            Season.WINTER: {
                WeatherEvent.NORMAL: 0.6,
                WeatherEvent.COLD_SNAP: 0.35,
                WeatherEvent.RAINY_DAY: 0.05
            }
        }
        
        weather_probs = season_weather[self.current_season]
        rand = random.random()
        cumulative = 0
        
        for weather, prob in weather_probs.items():
            cumulative += prob
            if rand <= cumulative:
                return weather
                
        return WeatherEvent.NORMAL
    
    def _check_for_holiday(self, day: int) -> Holiday:
        """Check if current day is a holiday (simplified calendar)"""
        # Simplified holiday calendar based on day numbers
        holiday_calendar = {
            14: Holiday.VALENTINES_DAY,     # Day 14 = Valentine's Day
            45: Holiday.SPRING_BREAK,       # Day 45 = Spring Break
            75: Holiday.SUMMER_PICNIC,      # Day 75 = Summer Picnic Season
            105: Holiday.HALLOWEEN,         # Day 105 = Halloween
            135: Holiday.WINTER_HOLIDAYS    # Day 135 = Winter Holidays
        }
        
        # Check for exact matches and nearby dates (±2 days)
        for holiday_day, holiday in holiday_calendar.items():
            if abs(day - holiday_day) <= 2:
                return holiday
                
        return Holiday.NONE
    
    def _calculate_demand_multiplier(self, weather: WeatherEvent, holiday: Holiday) -> float:
        """Calculate overall market demand multiplier"""
        base_multiplier = 1.0
        
        # Weather effects
        weather_effects = {
            WeatherEvent.NORMAL: 1.0,
            WeatherEvent.HEAT_WAVE: 1.2,      # More customers out shopping
            WeatherEvent.COLD_SNAP: 0.8,      # Fewer customers venture out
            WeatherEvent.RAINY_DAY: 0.9,      # Slight decrease in foot traffic
            WeatherEvent.PERFECT_WEATHER: 1.1  # Great day for shopping
        }
        
        # Holiday effects
        holiday_effects = {
            Holiday.NONE: 1.0,
            Holiday.VALENTINES_DAY: 1.3,
            Holiday.SPRING_BREAK: 1.2,
            Holiday.SUMMER_PICNIC: 1.4,
            Holiday.HALLOWEEN: 1.5,
            Holiday.WINTER_HOLIDAYS: 1.6
        }
        
        return base_multiplier * weather_effects[weather] * holiday_effects[holiday]
    
    def _get_weather_product_multiplier(self, product_name: str, weather: WeatherEvent) -> float:
        """Get weather-specific multipliers for products"""
        weather_product_effects = {
            WeatherEvent.HEAT_WAVE: {
                "Water": 2.0, "Coke": 1.5, "Ice Cream": 1.8,
                "Sandwiches": 1.2  # People want cold/refreshing items
            },
            WeatherEvent.COLD_SNAP: {
                "Chocolate": 1.3, "Crackers": 1.2,  # Comfort foods
                "Ice Cream": 0.5, "Water": 0.7      # Less appealing when cold
            },
            WeatherEvent.RAINY_DAY: {
                "Chocolate": 1.2, "Crackers": 1.1,  # Comfort foods
                "Sandwiches": 0.8  # Less outdoor eating
            },
            WeatherEvent.PERFECT_WEATHER: {
                "Sandwiches": 1.3, "Chips": 1.2, "Water": 1.2  # Great for outdoor activities
            }
        }
        
        return weather_product_effects.get(weather, {}).get(product_name, 1.0)
    
    def _get_holiday_product_multiplier(self, product_name: str, holiday: Holiday) -> float:
        """Get holiday-specific multipliers for products"""
        holiday_product_effects = {
            Holiday.VALENTINES_DAY: {
                "Chocolate": 2.5, "Candy": 1.8  # Romance boost
            },
            Holiday.SPRING_BREAK: {
                "Water": 1.4, "Chips": 1.3, "Sandwiches": 1.2  # Travel/outdoor activities
            },
            Holiday.SUMMER_PICNIC: {
                "Water": 1.6, "Chips": 1.5, "Sandwiches": 1.8, "Ice Cream": 1.4
            },
            Holiday.HALLOWEEN: {
                "Candy": 3.0, "Chocolate": 2.0  # Massive candy demand
            },
            Holiday.WINTER_HOLIDAYS: {
                "Chocolate": 1.8, "Candy": 1.5, "Crackers": 1.3  # Holiday treats
            }
        }
        
        return holiday_product_effects.get(holiday, {}).get(product_name, 1.0)
    
    def _get_economic_multiplier(self, economic_condition: EconomicCondition) -> float:
        """Get economic condition multipliers affecting all products"""
        economic_effects = {
            EconomicCondition.NORMAL: 1.0,
            EconomicCondition.BOOM: 1.3,      # People spend more
            EconomicCondition.RECESSION: 0.7,  # People spend less
            EconomicCondition.RECOVERY: 1.1    # Gradually increasing spending
        }
        
        return economic_effects[economic_condition]
    
    def _generate_market_description(self, weather: WeatherEvent, holiday: Holiday) -> str:
        """Generate descriptive text for market conditions"""
        descriptions = []
        
        # Weather descriptions
        weather_desc = {
            WeatherEvent.NORMAL: "Pleasant weather",
            WeatherEvent.HEAT_WAVE: "🔥 HEAT WAVE - customers seeking cool relief!",
            WeatherEvent.COLD_SNAP: "🥶 COLD SNAP - comfort food demand rising!",
            WeatherEvent.RAINY_DAY: "🌧️ Rainy day - customers want comfort items",
            WeatherEvent.PERFECT_WEATHER: "☀️ Perfect weather - ideal shopping conditions!"
        }
        descriptions.append(weather_desc[weather])
        
        # Holiday descriptions
        if holiday != Holiday.NONE:
            holiday_desc = {
                Holiday.VALENTINES_DAY: "💕 Valentine's Day - chocolate sales SOARING!",
                Holiday.SPRING_BREAK: "🌸 Spring Break season - travel snacks in demand!",
                Holiday.SUMMER_PICNIC: "🧺 Summer picnic season - outdoor food rush!",
                Holiday.HALLOWEEN: "🎃 Halloween - CANDY APOCALYPSE in progress!",
                Holiday.WINTER_HOLIDAYS: "🎄 Winter holidays - festive treat demand!"
            }
            descriptions.append(holiday_desc[holiday])
        
        # Economic descriptions
        economic_desc = {
            EconomicCondition.BOOM: "📈 Economic BOOM - customers spending freely!",
            EconomicCondition.RECESSION: "📉 Economic recession - budget-conscious shoppers",
            EconomicCondition.RECOVERY: "🔄 Economic recovery - cautious optimism in spending"
        }
        
        if self.current_economic_condition != EconomicCondition.NORMAL:
            descriptions.append(economic_desc[self.current_economic_condition])
        
        return " | ".join(descriptions) 