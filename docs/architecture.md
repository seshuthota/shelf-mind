# Technical Architecture
*Implementation Details and Engine Structure*

## Overview

ShelfMind implements a sophisticated modular architecture with enterprise-grade separation of concerns. The system consists of 6 AI agents, 10 specialized engines, and comprehensive core systems that work together to create the most advanced convenience store business simulation ever built.

---

## 🏗️ **Enterprise Directory Structure**

```
ShelfMind/
├── src/                             # 📦 ENTERPRISE SOURCE STRUCTURE
│   ├── agents/                      # 🤖 All AI agent specialists (6 agents)
│   │   ├── scrooge_agent.py         # 🤖 Master AI agent with 8-dimensional business mastery
│   │   ├── inventory_manager_agent.py    # 📚 HERMIONE GRANGER - Mathematical inventory specialist
│   │   ├── pricing_analyst_agent.py      # 💰 GORDON GEKKO - Ruthless pricing warfare specialist
│   │   ├── customer_service_agent.py     # 👥 ELLE WOODS - Customer psychology specialist
│   │   ├── strategic_planner_agent.py    # 🎯 TYRION LANNISTER - Strategic planning specialist
│   │   └── crisis_manager_agent.py       # 🚨 JACK BAUER - Crisis management specialist
│   ├── engines/                     # 🏭 Business simulation engines (10 engines)
│   │   ├── store_engine.py          # 🏪 Core store orchestration (165 lines)
│   │   ├── customer_engine.py       # 🎯 Customer psychology & segmentation (220 lines)
│   │   ├── competitor_engine.py     # 🔥 Ultra-aggressive competitor AI (302 lines)
│   │   ├── supplier_engine.py       # 🏭 Supplier management & delivery (225 lines)
│   │   ├── market_events_engine.py  # 🌍 Seasonal market events & weather system (180 lines)
│   │   ├── crisis_engine.py         # 🚨 Crisis management & emergency response system
│   │   ├── analytics_engine.py      # 🧠 Performance analysis & strategic intelligence (467 lines)
│   │   ├── strategic_planning_engine.py  # 🎯 Strategic planning & optimization system (553 lines)
│   │   ├── learning_adaptation_engine.py # 🧠 Learning & adaptation systems (663 lines)
│   │   └── growth_expansion_engine.py    # 🚀 Growth & expansion intelligence system (382 lines)
│   ├── core/                        # 📦 Core models, prompts, and coordination
│   │   ├── models.py                # 📊 Data structures & product definitions
│   │   ├── agent_prompts.py         # 🎭 Character personality management system
│   │   └── multi_agent_engine.py    # 🤖 Multi-agent coordination & hybrid bridge system
│   └── __init__.py                  # Python package structure
├── docs/                           # 📚 Modular documentation
├── tests/                          # 🧪 All test files
├── main.py                         # 🚀 Interactive simulation & character ensemble dashboard
├── requirements.txt                # 📋 Project dependencies
└── README.md                       # 📋 Main project overview
```

---

## 🏪 **Core Store Engine Architecture**

### Store Engine (store_engine.py)
**Role**: Master orchestrator coordinating all business operations
**Lines**: 165 (refactored from 788 lines of bloated code)

```python
class StoreEngine:
    def __init__(self):
        # Initialize all specialized engines
        self.customer_engine = CustomerEngine()
        self.competitor_engine = CompetitorEngine()
        self.supplier_engine = SupplierEngine()
        self.market_events_engine = MarketEventsEngine()
        self.crisis_engine = CrisisEngine()
        self.analytics_engine = AnalyticsEngine()
        self.strategic_planning_engine = StrategicPlanningEngine()
        self.learning_adaptation_engine = LearningAdaptationEngine()
        self.growth_expansion_engine = GrowthExpansionEngine()
        
    def run_daily_operations(self):
        # Orchestrate all business operations
        self.advance_day()
        self.process_market_events()
        self.handle_pending_deliveries()
        self.simulate_customer_visits()
        self.process_competitor_moves()
        self.handle_crisis_events()
        self.update_analytics()
        return self.generate_daily_summary()
```

**Key Responsibilities**:
- Day progression and time management
- Coordination between all engines
- Daily business operation orchestration
- Financial tracking and cash management
- Inventory management and product catalog
- Dashboard data generation

---

## 🎯 **Customer & Market Engines**

### Customer Engine (customer_engine.py)
**Role**: Advanced customer psychology and behavioral simulation
**Lines**: 220

```python
class CustomerEngine:
    def __init__(self):
        self.price_sensitive_customers = []  # 60% of market
        self.brand_loyal_customers = []      # 40% of market
        
    def simulate_customer_visits(self, store_data):
        # Generate realistic customer visits based on:
        # - Seasonal demand patterns
        # - Weather effects
        # - Economic conditions
        # - Time of day factors
        
    def process_customer_purchase_decision(self, customer, products):
        # Sophisticated purchase logic:
        # - Price sensitivity calculations
        # - Brand loyalty strength
        # - Substitute product consideration
        # - Abandonment probability
```

**Key Features**:
- **Customer Segmentation**: 60% price-sensitive, 40% brand-loyal
- **Behavioral Psychology**: Realistic purchase patterns and loyalty
- **Seasonal Adaptation**: Customer preferences change with market conditions
- **Substitute Buying**: Customers consider alternatives when products unavailable

### Market Events Engine (market_events_engine.py)
**Role**: Seasonal market dynamics and environmental factors
**Lines**: 180

```python
class MarketEventsEngine:
    def __init__(self):
        self.current_season = "spring"
        self.weather_condition = "normal"
        self.economic_condition = "normal"
        self.current_holiday = None
        
    def advance_season(self):
        # 30-day season cycles with automatic progression
        
    def generate_weather_events(self):
        # Weather affecting product demand:
        # - Heat waves boost beverages
        # - Cold snaps increase comfort foods
        # - Rainy days affect shopping patterns
        
    def process_holiday_events(self):
        # Major holidays with demand spikes:
        # - Valentine's Day (chocolate 2.5x)
        # - Halloween (candy 3.0x)
        # - Summer picnics (outdoor foods 1.8x)
```

**Key Features**:
- **4-Season Cycles**: Spring, Summer, Fall, Winter with 30-day progression
- **Weather Events**: 5 weather types affecting specific product demand
- **Holiday Explosions**: 5 major holidays with massive demand spikes
- **Economic Cycles**: Boom, recession, recovery affecting spending patterns

---

## 🔥 **Competition & Supply Chain Engines**

### Competitor Engine (competitor_engine.py)
**Role**: Ultra-aggressive AI competitor with psychological warfare
**Lines**: 302

```python
class CompetitorEngine:
    def __init__(self):
        self.strategy_mode = "BALANCED"  # AGGRESSIVE, PREDATORY, PSYCHOLOGICAL, DEFENSIVE
        self.war_intensity = 0.0         # 0-10 scale
        self.revenge_mode = False
        self.move_history = []
        
    def execute_competitive_move(self, store_data):
        # 5-strategy AI system:
        # - AGGRESSIVE: Direct price cuts
        # - PREDATORY: Loss leader tactics
        # - PSYCHOLOGICAL: Fake retreats and chaos
        # - DEFENSIVE: Protect market share
        # - BALANCED: Mixed approach
        
    def escalate_war_intensity(self):
        # Dynamic escalation based on:
        # - Player aggression level
        # - Profit threat assessment
        # - Psychological warfare triggers
```

**Key Features**:
- **5 AI Strategies**: Each with unique competitive behavior
- **Psychological Warfare**: Revenge mode and fake retreat tactics
- **Dynamic Escalation**: 0-10 war intensity scale with dramatic descriptions
- **Multi-Move Tactics**: Up to 8 simultaneous pricing moves per turn

### Supplier Engine (supplier_engine.py)
**Role**: Multi-supplier ecosystem with delivery and payment management
**Lines**: 225

```python
class SupplierEngine:
    def __init__(self):
        self.suppliers = self.initialize_suppliers()  # 2 per product
        self.pending_deliveries = []
        self.accounts_payable = []  # NET-30 payment tracking
        
    def select_optimal_supplier(self, product, quantity):
        # Multi-factor optimization:
        # - Cost (including bulk discounts)
        # - Delivery speed (1-3 days)
        # - Reliability (95-99%)
        # - Payment terms (UPFRONT vs NET-30)
        # - Cash flow impact
        
    def process_delivery_attempts(self):
        # Realistic delivery simulation:
        # - Success/failure based on reliability
        # - Automatic refunds for failures
        # - Alternative supplier selection
```

**Key Features**:
- **Multi-Supplier Choice**: 2 suppliers per product with unique characteristics
- **Bulk Discounts**: 15-50 unit thresholds with 8-20% savings
- **Payment Terms**: UPFRONT vs NET-30 cash flow management
- **Delivery Tracking**: Real-time delivery status with failure handling

---

## 🧠 **Intelligence & Planning Engines**

### Analytics Engine (analytics_engine.py)
**Role**: Performance analysis and strategic intelligence
**Lines**: 467

```python
class AnalyticsEngine:
    def __init__(self):
        self.performance_analyzer = PerformanceAnalyzer()
        self.competitive_intelligence = CompetitiveIntelligence()
        self.inventory_optimizer = InventoryOptimizer()
        self.profitability_analyzer = ProfitabilityAnalyzer()
        
    def analyze_performance(self, store_data):
        # Comprehensive performance analysis:
        # - Decision quality scoring
        # - Trend identification
        # - Optimization opportunities
        # - Strategic recommendations
```

### Strategic Planning Engine (strategic_planning_engine.py)
**Role**: Strategic planning and optimization capabilities
**Lines**: 553

```python
class StrategicPlanningEngine:
    def __init__(self):
        self.inventory_optimizer = InventoryOptimizer()
        self.promotional_strategy = PromotionalStrategy()
        self.seasonal_planner = SeasonalPlanner()
        self.category_manager = CategoryManager()
        
    def optimize_inventory(self, store_data):
        # Scientific inventory optimization:
        # - EOQ calculations
        # - Reorder point analysis
        # - Carrying cost optimization
        # - Stockout risk assessment
```

### Learning & Adaptation Engine (learning_adaptation_engine.py)
**Role**: Self-improving AI with adaptive intelligence
**Lines**: 663

```python
class LearningAdaptationEngine:
    def __init__(self):
        self.customer_learning = CustomerLearning()
        self.product_trend_analyzer = ProductTrendAnalyzer()
        self.price_elasticity_tracker = PriceElasticityTracker()
        self.adaptive_strategy = AdaptiveStrategy()
        
    def analyze_customer_learning(self, store_data):
        # Dynamic customer analysis:
        # - Segment shift detection
        # - Behavior pattern recognition
        # - Lost sales analysis
        # - Market adaptation insights
```

### Growth & Expansion Engine (growth_expansion_engine.py)
**Role**: Business growth and expansion intelligence
**Lines**: 382

```python
class GrowthExpansionEngine:
    def __init__(self):
        self.product_evaluator = ProductEvaluator()
        self.service_expansion = ServiceExpansion()
        self.customer_retention = CustomerRetention()
        self.multi_location_expansion = MultiLocationExpansion()
        
    def evaluate_new_products(self, store_data):
        # New product opportunity analysis:
        # - Market demand assessment
        # - Seasonal timing analysis
        # - Profitability projections
        # - ROI calculations
```

---

## 🤖 **AI Agent Architecture**

### Master Agent (scrooge_agent.py)
**Role**: Master CEO coordinating all business operations
**Character**: Ebenezer Scrooge - Ruthless business strategist

```python
class ScroogeAgent:
    def __init__(self):
        self.memory = []  # Decision history and learning
        self.tools = self.initialize_business_tools()  # 25+ business tools
        
    def make_daily_decision(self, store_status, yesterday_summary):
        # 8-dimensional business decision making:
        # 1. Customer psychology analysis
        # 2. Competitive intelligence assessment
        # 3. Supply chain optimization
        # 4. Market condition adaptation
        # 5. Crisis management response
        # 6. Performance analytics review
        # 7. Strategic planning execution
        # 8. Learning-based adaptation
        
        # Character ensemble consultation
        character_insights = self.get_character_insights(store_status)
        
        # Strategic decision making with full context
        return self.execute_business_strategy(store_status, character_insights)
```

### Character Specialist Agents
Each character agent provides specialized expertise with unique personality:

```python
class CharacterAgent:
    def __init__(self, character_name, expertise_area):
        self.character_name = character_name
        self.expertise_area = expertise_area
        self.personality_traits = self.load_character_personality()
        
    def analyze_situation(self, store_data):
        # Character-specific analysis with personality voice
        return {
            'character': self.character_name,
            'expertise': self.expertise_area,
            'priority': self.calculate_priority(store_data),
            'insight': self.generate_character_insight(store_data),
            'reasoning': self.get_character_reasoning(store_data)
        }
```

**Character Specialties**:
- **Hermione Granger**: Mathematical inventory optimization
- **Gordon Gekko**: Ruthless pricing warfare strategy
- **Elle Woods**: Customer psychology and experience
- **Tyrion Lannister**: Strategic planning and resource allocation
- **Jack Bauer**: Crisis management and emergency response

---

## 📊 **Data Models & Core Systems**

### Core Data Models (models.py)
```python
@dataclass
class Product:
    name: str
    category: str
    cost: float
    base_price: float
    current_price: float
    stock: int
    seasonal_multipliers: Dict[str, float]
    spoilage_rate: float = 0.0

@dataclass
class Customer:
    customer_type: str  # "price_sensitive" or "brand_loyal"
    preferred_products: List[str]
    loyalty_strength: float
    price_sensitivity: float
    budget_range: Tuple[float, float]

@dataclass
class Supplier:
    name: str
    products: List[str]
    base_cost: float
    delivery_time: int  # days
    reliability: float  # 0-1
    payment_terms: str  # "UPFRONT" or "NET-30"
    bulk_discount_threshold: int
    bulk_discount_rate: float
```

### Character Personality System (agent_prompts.py)
```python
class CharacterPrompts:
    CHARACTER_PERSONALITIES = {
        "hermione": {
            "name": "Hermione Granger",
            "expertise": "Mathematical Inventory Management",
            "traits": ["analytical", "precise", "methodical"],
            "catchphrases": ["According to my calculations...", "The data clearly shows..."],
            "voice_style": "academic_precise"
        },
        "gekko": {
            "name": "Gordon Gekko", 
            "expertise": "Ruthless Pricing Warfare",
            "traits": ["aggressive", "profit_focused", "competitive"],
            "catchphrases": ["Greed is good", "Money never sleeps"],
            "voice_style": "wall_street_aggressive"
        }
        # ... other characters
    }
    
    @staticmethod
    def generate_character_prompt(character_name, expertise_context):
        # Dynamic personality-driven prompt generation
        # Maintains character voice consistency
        # Integrates business expertise with fictional personality
```

---

## 🔄 **System Integration & Communication**

### Multi-Agent Coordination (multi_agent_engine.py)
```python
class MultiAgentEngine:
    def __init__(self, store_engine):
        self.store_engine = store_engine
        self.character_agents = self.initialize_character_agents()
        
    def get_character_insights(self, store_data):
        # Parallel character analysis
        insights = []
        for agent in self.character_agents.values():
            insight = agent.analyze_situation(store_data)
            insights.append(insight)
        
        # Priority-based sorting
        return sorted(insights, key=lambda x: x.priority, reverse=True)

class HybridMultiAgentBridge:
    def __init__(self, scrooge_agent, multi_agent_engine):
        self.scrooge_agent = scrooge_agent
        self.multi_agent_engine = multi_agent_engine
        
    def execute_daily_operations(self, store_data):
        # Scrooge makes actual business decisions
        business_decision = self.scrooge_agent.make_daily_decision(store_data)
        
        # Characters provide analysis and insights
        character_insights = self.multi_agent_engine.get_character_insights(store_data)
        
        return {
            'business_decision': business_decision,
            'character_insights': character_insights
        }
```

### Engine Communication Pattern
```python
# Example engine interaction flow
def daily_business_cycle():
    # 1. Market events affect customer behavior
    market_conditions = market_events_engine.get_current_conditions()
    
    # 2. Customer behavior influences demand
    customer_visits = customer_engine.simulate_visits(market_conditions)
    
    # 3. Competitor reacts to our moves
    competitor_moves = competitor_engine.execute_moves(our_prices)
    
    # 4. Supply chain processes deliveries
    delivery_results = supplier_engine.process_deliveries()
    
    # 5. Crisis events may disrupt operations
    crisis_events = crisis_engine.check_for_crises()
    
    # 6. Analytics engine processes all data
    analytics_insights = analytics_engine.analyze_performance(all_data)
    
    # 7. Strategic planning generates recommendations
    strategic_plan = strategic_planning_engine.generate_plan(all_data)
    
    # 8. Learning engine adapts strategies
    learning_insights = learning_adaptation_engine.update_strategies(all_data)
    
    # 9. Growth engine identifies opportunities
    growth_opportunities = growth_expansion_engine.evaluate_opportunities(all_data)
```

---

## 🚀 **Performance & Scalability**

### System Performance Metrics
- **Total Lines of Code**: ~3,500 lines across all engines and agents
- **Modular Architecture**: 10 specialized engines with single responsibility
- **Agent Tools**: 25+ business tools across all agents
- **Character Personalities**: 5 complete fictional character implementations
- **Stress Test Validation**: 21-day continuous operation with 100% uptime

### Scalability Features
- **Engine Independence**: Each engine can be modified without affecting others
- **Clean Interfaces**: Well-defined APIs between all components
- **Horizontal Scaling**: Easy to add new engines, agents, or characters
- **Testing Isolation**: Individual engines can be tested independently
- **Production Ready**: Enterprise-grade error handling and logging

### Development Benefits
- **Maintainable**: Clear separation of concerns makes code easy to understand
- **Extensible**: New features can be added without disrupting existing systems
- **Testable**: Modular design enables comprehensive unit testing
- **Debuggable**: Each engine can be analyzed independently
- **Collaborative**: Different developers can work on different engines

---

## 🔧 **Development & Deployment**

### Development Environment Setup
```bash
# Clone repository
git clone https://github.com/user/ShelfMind.git
cd ShelfMind

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your OpenAI API key to .env

# Run the simulation
python main.py
```

### Testing Framework
```bash
# Run unit tests
python -m pytest tests/

# Run stress tests
python tests/stress_test_crisis.py

# Run specific engine tests
python tests/test_phase4a.py
```

### Deployment Considerations
- **API Keys**: Secure OpenAI API key management
- **Environment Variables**: Production configuration management
- **Logging**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Graceful failure handling across all engines
- **Resource Management**: Efficient memory and compute usage

**🏆 The ShelfMind architecture represents the most sophisticated modular business simulation system ever created - enterprise-ready, character-driven, and infinitely extensible!** 