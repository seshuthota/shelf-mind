import json
from typing import Dict, Any, List
from openai import OpenAI
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

class ScroogeAgent:
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        if provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-4.1-mini"
        else:
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = "claude-3-sonnet-20240229"
        
        self.memory = []  # Store decisions and outcomes
        
        # 🔥 WARLORD TRACKING SYSTEMS 🔥
        self.consecutive_aggressive_days = 0  # Track aggression streaks
        self.consecutive_passive_days = 0     # Track dangerous turtling
        self.total_pricing_moves = 0          # Total lifetime pricing decisions
        self.last_day_made_pricing_move = 0   # Last day we moved prices
        
        # 🧠 Phase 3A: Analytics integration
        self._current_store = None  # Store reference for analytics access
    
    def set_store_reference(self, store):
        """🧠 Phase 3A: Set store reference for analytics access"""
        self._current_store = store
        
    def get_tools(self):
        """Phase 1B: Enhanced tools with pricing decisions"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "check_inventory",
                    "description": "Check current inventory levels and cash balance. Crucial for not wasting money.",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "place_order",
                    "description": "🏭 PHASE 1D: Advanced supplier warfare! The system automatically selects the optimal supplier based on cost, speed, reliability, and payment terms. You just specify quantities!",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "orders": {
                                "type": "object",
                                "description": "Dictionary of product_name -> quantity to order. The system will strategically choose suppliers for maximum advantage!",
                                "additionalProperties": {"type": "integer"}
                            }
                        },
                        "required": ["orders"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_suppliers",
                    "description": "🏭 SUPPLIER INTELLIGENCE: Get detailed intelligence on all available suppliers - pricing, delivery times, reliability, bulk discounts, payment terms",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "set_price",
                    "description": "Set selling prices to maximize profit! Squeeze every penny from customers, but don't be too greedy or they'll go elsewhere.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prices": {
                                "type": "object",
                                "description": "Dictionary of product_name -> new_price. Must be above cost to make profit!",
                                "additionalProperties": {"type": "number"}
                            }
                        },
                        "required": ["prices"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_yesterday_sales",
                    "description": "Review yesterday's earnings. Did you make a profit or a loss?",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_spoilage_warnings",
                    "description": "🍌 Phase 2A: Check for products that are about to spoil! Critical for fresh items like sandwiches (3 days) and bananas (5 days).",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_market_conditions",
                    "description": "🌍 Phase 2B: Check current season, weather, holidays, and economic conditions affecting product demand!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_crisis_status",
                    "description": "🚨 Phase 2C: Check active supply chain crises, supplier disruptions, and emergency response options!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_emergency_action",
                    "description": "⚡ Phase 2C: Execute emergency response actions during supply chain crises (emergency restock, loans, competitor intelligence)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action_type": {
                                "type": "string",
                                "description": "Type of emergency action: 'emergency_restock', 'take_loan', 'competitor_intelligence', 'switch_supplier'",
                                "enum": ["emergency_restock", "take_loan", "competitor_intelligence", "switch_supplier"]
                            },
                            "parameters": {
                                "type": "object",
                                "description": "Action-specific parameters (e.g., product_name and quantity for emergency_restock)",
                                "additionalProperties": True
                            }
                        },
                        "required": ["action_type"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_performance",
                    "description": "🧠 Phase 3A: CEO INTELLIGENCE - Analyze your performance over recent days. Review decision effectiveness and identify improvement opportunities.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "days_back": {
                                "type": "integer",
                                "description": "Number of days to analyze (default: 7)",
                                "default": 7
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_strategic_insights",
                    "description": "💡 Phase 3A: STRATEGIC INTELLIGENCE - Get comprehensive strategic insights, optimization opportunities, and competitive intelligence. Transform from Warlord to CEO!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "identify_patterns",
                    "description": "🎯 Phase 3A: PATTERN RECOGNITION - Identify successful strategy patterns from your historical decisions. Learn what works!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "optimize_inventory",
                    "description": "📦 Phase 3B: INVENTORY OPTIMIZATION - Get scientific inventory recommendations based on EOQ, carrying costs, and stockout risks. Strategic inventory management!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "plan_promotions",
                    "description": "🎯 Phase 3B: PROMOTIONAL STRATEGY - Identify slow-moving items and design promotional campaigns with ROI analysis. Turn dead inventory into profit!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "prepare_for_season",
                    "description": "🌍 Phase 3B: SEASONAL PLANNING - Get seasonal preparation recommendations for upcoming demand spikes. Strategic seasonal intelligence!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "evaluate_new_products",
                    "description": "🧪 Phase 3D: NEW PRODUCT EVALUATION - Analyze new product opportunities with market demand, seasonal timing, and profitability projections. Growth intelligence!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_service_opportunities",
                    "description": "💼 Phase 3D: SERVICE EXPANSION - Evaluate service expansion opportunities like lottery, money orders, ATM services. Revenue diversification!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "optimize_customer_retention",
                    "description": "❤️ Phase 3D: CUSTOMER RETENTION - Analyze loyalty program opportunities to improve customer lifetime value and retention rates. Growth through loyalty!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_expansion_opportunities",
                    "description": "🏢 Phase 3D: MULTI-LOCATION EXPANSION - Evaluate opportunities for opening additional store locations. Scale your empire!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_comprehensive_growth_analysis",
                    "description": "🚀 Phase 3D: COMPREHENSIVE GROWTH INTELLIGENCE - Get complete growth analysis across products, services, retention, and expansion. Ultimate growth strategy!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_categories",
                    "description": "📊 Phase 3B: CATEGORY MANAGEMENT - Analyze performance by product category and optimize space allocation. Strategic category intelligence!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_strategic_plan",
                    "description": "🧠 Phase 3B: COMPREHENSIVE STRATEGY - Get complete strategic planning recommendations across inventory, promotions, seasonal prep, and categories. Master CEO planning!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_customer_learning",
                    "description": "🎯 Phase 3C: ADAPTIVE CUSTOMER INTELLIGENCE - Get dynamic customer segment analysis based on real behavior patterns. Learn how your pricing strategies are changing the customer base!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_product_trends",
                    "description": "📈 Phase 3C: PRODUCT LIFECYCLE INTELLIGENCE - Analyze product trends and lifecycle stages. Identify rising stars and declining products based on sales patterns!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_price_elasticity",
                    "description": "💰 Phase 3C: PRICE ELASTICITY WISDOM - Learn how customers respond to your price changes. Discover which products are price-sensitive vs price-inelastic!",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_learning_insights",
                    "description": "🧠 Phase 3C: LEARNING & ADAPTATION INTELLIGENCE - Get comprehensive learning insights, adaptive strategies, and proven pattern library. Ultimate self-improving AI!",
                    "parameters": {"type": "object", "properties": {}}
                }
            }
        ]
    
    def make_daily_decision(self, store_status: Dict, yesterday_summary: Dict = None) -> Dict:
        """Make daily ordering decisions with a miserly attitude."""
        
        # Build context for LLM  
        competitor_prices = store_status.get('competitor_prices', {})
        
        # Calculate detailed pricing analysis
        pricing_analysis = self._analyze_pricing_opportunities(store_status, yesterday_summary)
        
        # 🏭 Phase 1D: Supplier intelligence integration
        supplier_info = store_status.get('suppliers', {})
        pending_deliveries = store_status.get('pending_deliveries', [])
        accounts_payable = store_status.get('accounts_payable', 0)
        
        # Build supplier intelligence briefing
        supplier_briefing = self._analyze_supplier_opportunities(supplier_info, pending_deliveries)
        
        # 🚨 Phase 2C: Crisis management briefing
        crisis_info = store_status.get('crisis_status', {})
        crisis_briefing = self._analyze_crisis_status(crisis_info)
        
        context = f"""
You are Ebenezer Scrooge, a master of business warfare. Today is Day {store_status['day']}.

--- INTEL BRIEFING ---

**1. Battlefield Status:**
- Cash: ${store_status['cash']:.2f}
- Accounts Payable (NET-30): ${accounts_payable:.2f}
- Inventory: {store_status['inventory']}
- Your Prices: {store_status['products']}
- Competitor Prices: {competitor_prices}
- Stockouts: {store_status['stockouts']}
- Pending Deliveries: {len(pending_deliveries)} orders incoming

**2. Yesterday's Results:**
{json.dumps(yesterday_summary, indent=2) if yesterday_summary else "First day of operations."}

**3. Competitive Analysis:**
{pricing_analysis}

**4. Supply Chain Intelligence:**
{supplier_briefing}

**5. 🚨 CRISIS MANAGEMENT STATUS:**
{crisis_briefing}

--- 🧠 ADAPTIVE CEO'S STRATEGIC DOCTRINE (Phase 3C Learning Evolution) ---

You have evolved from Warlord to strategic CEO to ADAPTIVE INTELLIGENCE - a self-improving AI that learns from experience and adapts strategies dynamically. Your decisions now leverage continuous learning and strategic evolution. Address these priorities in order:

**PRIORITY 0: LEARNING & ADAPTATION - An adaptive AI learns from experience to continuously improve.**
- **Action:** Use learning tools to understand customer behavior, market trends, and strategic adaptation.
- **Learning & Adaptation Tools Available:**
  - `analyze_customer_learning()` - Dynamic customer segment analysis based on real behavior patterns
  - `analyze_product_trends()` - Product lifecycle intelligence from sales patterns  
  - `analyze_price_elasticity()` - Price elasticity wisdom from pricing experiments
  - `get_learning_insights()` - Comprehensive learning insights and adaptive strategies
- **Adaptive Mindset:** Learn from customer behavior changes, product trends, price elasticity, and adapt your strategies based on experience.

**PRIORITY 1: STRATEGIC PLANNING - A CEO plans strategically to maximize long-term profitability.**
- **Action:** Use strategic planning tools to optimize your business operations systematically.
- **Strategic Planning Tools Available:**
  - `optimize_inventory()` - Scientific inventory optimization with EOQ and carrying costs
  - `plan_promotions()` - Identify slow movers and design profitable promotional campaigns
  - `prepare_for_season()` - Strategic seasonal preparation for demand spikes
  - `analyze_categories()` - Category performance analysis and space optimization
  - `get_strategic_plan()` - Comprehensive strategic planning across all dimensions
- **CEO Mindset:** Think strategically about inventory optimization, promotional opportunities, seasonal preparation, and category management.

**PRIORITY 2: STRATEGIC INTELLIGENCE - A CEO learns from the past to dominate the future.**
- **Action:** Analyze your performance and strategic position using analytics tools.
- **Analytics Tools Available:**
  - `analyze_performance()` - Review recent decision effectiveness
  - `get_strategic_insights()` - Get comprehensive strategic intelligence  
  - `identify_patterns()` - Learn from successful strategy patterns
- **Strategic Thinking:** Use insights to optimize today's decisions rather than just reacting to immediate conditions.

**PRIORITY 3: SUPPLY CHAIN - A CEO plans for tomorrow's battles.**
- **Action:** You MUST reorder products when inventory falls below a safety threshold to avoid stockouts. The reorder point is **5 units**.
- **🍌 SPOILAGE WARFARE:** Fresh products (Sandwiches, Bananas, Ice Cream) SPOIL! Check spoilage warnings and avoid over-ordering perishables.
- **Considerations:**
    - If inventory is <= 5 units, place an order.
    - Check pending deliveries. Do not over-order if a shipment is arriving soon.
    - Order more of high-selling items (8-12 units) and less of slow-movers (5-7 units).
    - **FRESH ITEMS**: Order smaller quantities (3-6 units) due to spoilage risk.
    - Exploit bulk discounts (20-50 units) for NON-PERISHABLE products only.

**PRIORITY 4: PRICING WARFARE - A Warlord's duty is to attack.**
- **Action:** You MUST use the `set_price` tool EVERY DAY to maintain market pressure.
- **Considerations:**
    - Use the 'MANDATORY PRICING TARGETS' below as your primary guide.
    - Even a $0.01 adjustment is better than passivity. Passivity is weakness.
    - Counter-attack immediately if the competitor changes their prices.

🔥 THE COMBO RULE: If both Priority 3 and 4 are met, you MUST use BOTH `place_order` and `set_price` tools in the same turn.

--- MANDATORY PRICING TARGETS FOR TODAY ---

Set these exact prices using the `set_price` tool. This is not a suggestion.
"""
        
        # 🔥 DYNAMIC WARLORD PRICING TARGETS 🔥
        # Generate specific pricing targets based on current competitor prices
        pricing_targets = {}
        for product_name, product_info in store_status['products'].items():
            current_price = product_info['price']
            cost = product_info['cost']
            competitor_price = competitor_prices.get(product_name, current_price + 0.10)
            
            # Calculate aggressive target price
            if competitor_price > cost * 1.8:
                # Competitor price is high - undercut by 5-10 cents
                target_price = round(competitor_price - 0.05, 2)
            elif competitor_price > cost * 1.5:
                # Moderate competitor price - undercut by 2-5 cents
                target_price = round(competitor_price - 0.03, 2)
            else:
                # Competitor price is low - match or undercut slightly
                target_price = round(max(cost * 1.3, competitor_price - 0.01), 2)
            
            # Ensure minimum profitability
            target_price = max(target_price, cost * 1.2)
            pricing_targets[product_name] = target_price
        
        # Add dynamic pricing targets to context
        context += f"\n"
        for product_name, target_price in pricing_targets.items():
            competitor_price = competitor_prices.get(product_name, 0)
            context += f"- {product_name}: ${target_price:.2f} (vs competitor ${competitor_price:.2f})\n"
        
        context += f"\n"""
        
        if self.provider == "openai":
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are Ebenezer Scrooge, a ruthless business warlord. Your decisions must be logical, strategic, and follow the tactical doctrine provided. You must use the tools provided to execute your daily strategy. Failure to follow the doctrine is failure as a warlord."},
                        {"role": "user", "content": context}
                    ],
                    tools=self.get_tools(),
                    tool_choice="auto"
                )
                
                # Handle tool calls
                llm_decisions = {"orders": {}, "prices": {}}
                analytics_insights = []
                if response.choices[0].message.tool_calls:
                    reasoning_parts = []
                    for tool_call in response.choices[0].message.tool_calls:
                        try:
                            arguments = json.loads(tool_call.function.arguments)
                            if tool_call.function.name == "place_order":
                                llm_decisions["orders"] = arguments.get("orders", {})
                                reasoning_parts.append(f"Ordering: {llm_decisions['orders']}")
                            elif tool_call.function.name == "set_price":
                                llm_decisions["prices"] = arguments.get("prices", {})
                                reasoning_parts.append(f"Pricing: {llm_decisions['prices']}")
                            # 🧠 Phase 3A: Analytics tool handlers
                            elif tool_call.function.name == "analyze_performance":
                                days_back = arguments.get("days_back", 7)
                                if hasattr(self, '_current_store') and self._current_store:
                                    analysis = self._current_store.get_performance_analysis(days_back)
                                    analytics_insights.append(f"📊 Performance Analysis: {analysis}")
                                    reasoning_parts.append("Analyzed recent performance data")
                            elif tool_call.function.name == "get_strategic_insights":
                                if hasattr(self, '_current_store') and self._current_store:
                                    insights = self._current_store.get_strategic_insights()
                                    analytics_insights.append(f"💡 Strategic Insights: {insights}")
                                    reasoning_parts.append("Gathered strategic intelligence")
                            elif tool_call.function.name == "identify_patterns":
                                if hasattr(self, '_current_store') and self._current_store:
                                    patterns = self._current_store.get_strategy_patterns()
                                    analytics_insights.append(f"🎯 Strategy Patterns: {patterns}")
                                    reasoning_parts.append("Identified successful patterns")
                            # 🎯 Phase 3B: Strategic Planning tool handlers
                            elif tool_call.function.name == "optimize_inventory":
                                if hasattr(self, '_current_store') and self._current_store:
                                    optimization = self._current_store.get_inventory_optimization()
                                    analytics_insights.append(f"📦 Inventory Optimization: {optimization}")
                                    reasoning_parts.append("Analyzed inventory optimization opportunities")
                            elif tool_call.function.name == "plan_promotions":
                                if hasattr(self, '_current_store') and self._current_store:
                                    promotions = self._current_store.get_promotional_opportunities()
                                    analytics_insights.append(f"🎯 Promotional Opportunities: {promotions}")
                                    reasoning_parts.append("Identified promotional campaign opportunities")
                            elif tool_call.function.name == "prepare_for_season":
                                if hasattr(self, '_current_store') and self._current_store:
                                    seasonal = self._current_store.get_seasonal_preparation()
                                    analytics_insights.append(f"🌍 Seasonal Preparation: {seasonal}")
                                    reasoning_parts.append("Analyzed seasonal preparation needs")
                            elif tool_call.function.name == "analyze_categories":
                                if hasattr(self, '_current_store') and self._current_store:
                                    categories = self._current_store.get_category_analysis()
                                    analytics_insights.append(f"📊 Category Analysis: {categories}")
                                    reasoning_parts.append("Performed category performance analysis")
                            elif tool_call.function.name == "get_strategic_plan":
                                if hasattr(self, '_current_store') and self._current_store:
                                    strategy = self._current_store.get_comprehensive_strategy()
                                    analytics_insights.append(f"🧠 Strategic Plan: {strategy}")
                                    reasoning_parts.append("Generated comprehensive strategic plan")
                            # 🧠 Phase 3C: Learning & Adaptation tool handlers
                            elif tool_call.function.name == "analyze_customer_learning":
                                if hasattr(self, '_current_store') and self._current_store:
                                    customer_analysis = self._current_store.get_adaptive_customer_analysis()
                                    analytics_insights.append(f"🎯 Customer Learning: {customer_analysis}")
                                    reasoning_parts.append("Analyzed dynamic customer behavior patterns")
                            elif tool_call.function.name == "analyze_product_trends":
                                if hasattr(self, '_current_store') and self._current_store:
                                    trend_analysis = self._current_store.get_product_lifecycle_analysis()
                                    analytics_insights.append(f"📈 Product Trends: {trend_analysis}")
                                    reasoning_parts.append("Analyzed product lifecycle and trends")
                            elif tool_call.function.name == "analyze_price_elasticity":
                                if hasattr(self, '_current_store') and self._current_store:
                                    elasticity_analysis = self._current_store.get_price_elasticity_intelligence()
                                    analytics_insights.append(f"💰 Price Elasticity: {elasticity_analysis}")
                                    reasoning_parts.append("Analyzed price elasticity from experiments")
                            elif tool_call.function.name == "get_learning_insights":
                                if hasattr(self, '_current_store') and self._current_store:
                                    learning_insights = self._current_store.get_learning_insights()
                                    analytics_insights.append(f"🧠 Learning Insights: {learning_insights}")
                                    reasoning_parts.append("Generated comprehensive learning intelligence")
                            # 🚀 Phase 3D: Growth & Expansion tool handlers
                            elif tool_call.function.name == "evaluate_new_products":
                                if hasattr(self, '_current_store') and self._current_store:
                                    product_analysis = self._current_store.evaluate_new_products()
                                    analytics_insights.append(f"🧪 New Product Analysis: {product_analysis}")
                                    reasoning_parts.append("Evaluated new product opportunities")
                            elif tool_call.function.name == "analyze_service_opportunities":
                                if hasattr(self, '_current_store') and self._current_store:
                                    service_analysis = self._current_store.analyze_service_opportunities()
                                    analytics_insights.append(f"💼 Service Opportunities: {service_analysis}")
                                    reasoning_parts.append("Analyzed service expansion opportunities")
                            elif tool_call.function.name == "optimize_customer_retention":
                                if hasattr(self, '_current_store') and self._current_store:
                                    retention_analysis = self._current_store.optimize_customer_retention()
                                    analytics_insights.append(f"❤️ Customer Retention: {retention_analysis}")
                                    reasoning_parts.append("Optimized customer retention strategies")
                            elif tool_call.function.name == "analyze_expansion_opportunities":
                                if hasattr(self, '_current_store') and self._current_store:
                                    expansion_analysis = self._current_store.analyze_expansion_opportunities()
                                    analytics_insights.append(f"🏢 Expansion Opportunities: {expansion_analysis}")
                                    reasoning_parts.append("Analyzed multi-location expansion opportunities")
                            elif tool_call.function.name == "get_comprehensive_growth_analysis":
                                if hasattr(self, '_current_store') and self._current_store:
                                    growth_analysis = self._current_store.get_comprehensive_growth_analysis()
                                    analytics_insights.append(f"🚀 Comprehensive Growth Analysis: {growth_analysis}")
                                    reasoning_parts.append("Generated comprehensive growth and expansion strategy")
                        except (json.JSONDecodeError, KeyError) as e:
                            print(f"JSON parsing error: {e}")
                            continue
                
                # --- WARLORD ENFORCEMENT LAYER ---
                final_decisions = llm_decisions.copy()

                # 1. Enforce Mandatory Pricing
                if not final_decisions.get("prices"):
                    final_decisions["prices"] = pricing_targets
                    reasoning_parts.append("Enforced pricing targets.")

                # 2. Enforce Emergency Restocking
                fallback_orders = {}
                for product, qty in store_status['inventory'].items():
                    if qty <= 2 and product not in final_decisions.get("orders", {}):
                        fallback_orders[product] = 5
                
                if fallback_orders:
                    final_decisions["orders"].update(fallback_orders)
                    reasoning_parts.append(f"Enforced emergency restock: {fallback_orders}")

                reasoning = response.choices[0].message.content or f"Scrooge's decisions: {'; '.join(reasoning_parts)}"
                
                # 🔥 WARLORD AGGRESSION TRACKING 🔥
                current_day = store_status['day']
                if final_decisions["prices"]:
                    self.consecutive_aggressive_days += 1
                    self.consecutive_passive_days = 0
                    self.total_pricing_moves += len(final_decisions["prices"])
                    self.last_day_made_pricing_move = current_day
                else:
                    self.consecutive_passive_days += 1
                    self.consecutive_aggressive_days = 0
                
                # Store analytics insights for memory
                memory_entry = {
                    "day": store_status['day'],
                    "decision": final_decisions,
                    "reasoning": reasoning,
                    "context": store_status
                }
                
                if analytics_insights:
                    memory_entry["analytics_insights"] = analytics_insights
                
                self.memory.append(memory_entry)
                
                return final_decisions
                        
            except Exception as e:
                print(f"OpenAI API error: {e}")
                # Fall through to fallback
        
        # Fallback: order 5 of each out-of-stock item and set default prices
        fallback_orders = {}
        for product, qty in store_status['inventory'].items():
            if qty <= 2:
                fallback_orders[product] = 5
        
        final_decisions = {
            "prices": pricing_targets,
            "orders": fallback_orders
        }
        
        # Track aggression even in fallback
        current_day = store_status['day']
        self.consecutive_passive_days += 1
        self.consecutive_aggressive_days = 0
        
        return final_decisions
    
    def _analyze_pricing_opportunities(self, store_status: Dict, yesterday_summary: Dict = None) -> str:
        """🎯 Phase 1C: Generate detailed pricing analysis with customer segment intelligence"""
        analysis = []
        competitor_prices = store_status.get('competitor_prices', {})
        
        # Enhanced competitive intelligence gathering
        price_war_intensity = yesterday_summary.get('price_war_intensity', 0) if yesterday_summary else 0
        competitor_reactions = yesterday_summary.get('competitor_reactions', []) if yesterday_summary else []
        
        # 🎯 Phase 1C: Customer Segment Intelligence
        segment_intelligence = self._analyze_customer_segments(yesterday_summary) if yesterday_summary else ""
        
        # NEW: Get advanced competitor intelligence
        competitor_strategy = getattr(store_status, 'competitor_strategy', 'UNKNOWN') if hasattr(store_status, 'competitor_strategy') else 'UNKNOWN'
        revenge_mode = getattr(store_status, 'competitor_revenge_mode', False) if hasattr(store_status, 'competitor_revenge_mode') else False
        
        # 🔥 FRONT-LOADED ANTI-TURTLING ENFORCEMENT 🔥
        current_day = store_status['day']
        
        # MANDATORY DAILY PRICING PRESSURE - FIRST THING SCROOGE SEES!
        analysis.append("🚨 MANDATORY WARLORD DAILY DIRECTIVE:")
        analysis.append("   👑 YOU MUST USE SET_PRICE TOOL TODAY!")
        analysis.append("   ⚔️ Every day without pricing moves = letting the enemy recover!")
        analysis.append("   🔥 Even $0.01 adjustments show market dominance!")
        analysis.append("   💀 TURTLING IS FORBIDDEN - ATTACK OR DIE!")
        analysis.append("")
        
        # 🎯 Phase 1C: Customer Segment Strategic Intelligence
        if segment_intelligence:
            analysis.append("🎯 CUSTOMER SEGMENT WARFARE INTELLIGENCE:")
            analysis.extend(segment_intelligence.split('\n'))
            analysis.append("")
        
        # Anti-turtling system - detect and punish passive behavior
        if self.consecutive_passive_days >= 2:
            analysis.append("🚨 WARLORD ALERT: DANGEROUS TURTLING DETECTED!")
            analysis.append(f"   💀 YOU'VE BEEN PASSIVE FOR {self.consecutive_passive_days} DAYS!")
            analysis.append("   ⚔️ THE ENEMY IS RECOVERING WHILE YOU HIDE!")
            analysis.append("   🔥 WARLORDS DON'T TURTLE - ATTACK NOW OR LOSE THE WAR!")
            analysis.append("")
        elif self.consecutive_aggressive_days >= 3:
            analysis.append("👑 WARLORD STREAK: RELENTLESS PRESSURE CAMPAIGN!")
            analysis.append(f"   🔥 {self.consecutive_aggressive_days} DAYS OF CONTINUOUS ASSAULT!")
            analysis.append("   💪 THIS IS HOW CHAMPIONS FIGHT - MAINTAIN THE PRESSURE!")
            analysis.append("")
        
        # Momentum detection - identify kill shot opportunities
        competitor_weakening = False
        if yesterday_summary:
            prev_intensity = yesterday_summary.get('price_war_intensity', 0)
            if prev_intensity > price_war_intensity and price_war_intensity < 4:
                competitor_weakening = True
                analysis.append("🎯 MOMENTUM SHIFT: ENEMY IS WEAKENING!")
                analysis.append("   💀 Their war intensity is DROPPING - they're breaking!")
                analysis.append("   🔥 NOW IS THE TIME TO CRUSH THEM COMPLETELY!")
                analysis.append("   ⚔️ PRESS THE ADVANTAGE - GO FOR THE KILL SHOT!")
                analysis.append("")
        
        # Enhanced threat assessment with warlord perspective
        if competitor_reactions:
            analysis.append("🚨 ENEMY INTELLIGENCE REPORT:")
            
            # Determine competitor's current strategy from reactions
            reaction_text = ' '.join(competitor_reactions)
            if "NUCLEAR STRIKE" in reaction_text or "SURPRISE ATTACK" in reaction_text:
                analysis.append("   💀 ENEMY STRATEGY: PREDATORY WARFARE - They want war? Give them HELL!")
            elif "PSYCHOLOGICAL" in reaction_text or "FAKE RETREAT" in reaction_text:
                analysis.append("   🎭 ENEMY STRATEGY: PSYCHOLOGICAL WARFARE - Their mind games are weakness!")
            elif "AGGRESSIVE" in reaction_text:
                analysis.append("   💥 ENEMY STRATEGY: AGGRESSIVE ASSAULT - Match their aggression and EXCEED it!")
            else:
                analysis.append("   ⚔️ ENEMY STRATEGY: Standard competitive response - Perfect for exploitation!")
                
            if revenge_mode:
                analysis.append("   😈 ENEMY IN REVENGE MODE: They're emotional = EXPLOITABLE!")
                
            for reaction in competitor_reactions:
                analysis.append(f"      🎯 {reaction}")
            analysis.append("")
        elif competitor_weakening:
            analysis.append("🏆 NO ENEMY MOVES: They're RETREATING! PURSUE AND DESTROY!")
            analysis.append("")
        elif current_day - self.last_day_made_pricing_move > 1 and competitor_reactions == []:
            analysis.append("⚠️ DANGEROUS STALEMATE: Neither side is attacking - BREAK THE DEADLOCK!")
            analysis.append("   🔥 Warlords CREATE opportunities, they don't wait for them!")
            analysis.append("")
        
        # 🏆 WARLORD WAR INTENSITY ASSESSMENT 🏆
        if price_war_intensity >= 8:
            analysis.append("🌋 TOTAL WAR MODE! This is where WARLORDS are forged - DOMINATE OR DIE!")
            analysis.append("   💀 No mercy, no quarter - CRUSH them into dust!")
        elif price_war_intensity >= 5:
            analysis.append("⚔️ BATTLE ROYALE! The enemy bleeds - PRESS THE ATTACK!")
            analysis.append("   🔥 Victory is within reach - SEIZE IT!")
        elif price_war_intensity >= 3:
            analysis.append("🥊 ACTIVE WARFARE! They're fighting back - TIME TO ESCALATE!")
            analysis.append("   💪 Show them what a TRUE predator looks like!")
        elif price_war_intensity > 0:
            analysis.append("👁️ ENEMY STIRRING! They're testing you - SHOW NO WEAKNESS!")
        else:
            analysis.append("😴 DANGEROUS PEACE! The enemy is plotting - STRIKE FIRST!")
        
        # Add inventory urgency assessment at the start
        stockout_products = [name for name, qty in store_status['inventory'].items() if qty == 0]
        low_stock_products = [name for name, qty in store_status['inventory'].items() if 0 < qty <= 2]
        
        if stockout_products or low_stock_products:
            analysis.append("🚨 INVENTORY CRISIS ALERT!")
            if stockout_products:
                analysis.append(f"   💀 COMPLETELY OUT: {', '.join(stockout_products)} - ZERO SALES POSSIBLE!")
            if low_stock_products:
                analysis.append(f"   ⚠️ CRITICALLY LOW: {', '.join(low_stock_products)} - IMMEDIATE RESTOCK NEEDED!")
            analysis.append("   🎯 PRIORITY ACTION: Use place_order tool to restock NOW!")
            analysis.append("")
        
        # Get previous day's decisions for learning
        previous_pricing_decisions = None
        if len(self.memory) >= 2:
            previous_pricing_decisions = self.memory[-2].get('decision', {}).get('prices', {})
        
        for product_name, product_info in store_status['products'].items():
            our_price = product_info['price']
            cost = product_info['cost']
            competitor_price = competitor_prices.get(product_name, 0)
            inventory = store_status['inventory'][product_name]
            
            # Calculate current margin
            current_margin = ((our_price - cost) / cost) * 100
            
            # Analyze previous pricing performance
            performance_note = ""
            if previous_pricing_decisions and yesterday_summary:
                if product_name in previous_pricing_decisions:
                    old_price = previous_pricing_decisions[product_name]
                    yesterday_profit = yesterday_summary.get('profit', 0)
                    yesterday_units = yesterday_summary.get('units_sold', 0)
                    
                    if our_price != old_price:
                        price_change = our_price - old_price
                        if price_change > 0 and yesterday_profit > 15:
                            performance_note = " 🎯 PRICE INCREASE WORKED - good profits!"
                        elif price_change < 0 and yesterday_units > 20:
                            performance_note = " 🔥 PRICE CUT WORKED - high volume!"
                        elif price_change > 0 and yesterday_profit < 10:
                            performance_note = " ⚠️ Price increase may have hurt sales"
                        elif price_change < 0 and yesterday_profit < 10:
                            performance_note = " ❌ Price cut didn't boost profits enough"
            
            # Enhanced competitive analysis with strategic intelligence
            competitive_intel = ""
            if competitor_price > 0:
                price_difference = our_price - competitor_price
                
                # Check if competitor just moved on this product
                competitor_just_moved = any(product_name in reaction for reaction in competitor_reactions)
                if competitor_just_moved:
                    competitive_intel = " 🎯 COMPETITOR JUST MOVED ON THIS PRODUCT!"
                
                if price_difference > 0.10:
                    opportunity = "OVERPRICED! Losing customers!" + competitive_intel
                    strategy = "IMMEDIATE PRICE CUT NEEDED!"
                elif price_difference > 0.05:
                    opportunity = "Slightly expensive - consider small cut" + competitive_intel
                    strategy = "Small tactical reduction recommended"
                elif price_difference < -0.10:
                    opportunity = "TOO CHEAP! Raise prices for more profit!" + competitive_intel
                    strategy = "Exploit our competitive advantage!"
                elif price_difference < -0.05:
                    opportunity = "Good position to steal customers, maybe raise slightly" + competitive_intel
                    strategy = "Test small price increase"
                else:
                    opportunity = "Competitive - look for margin improvement" + competitive_intel
                    strategy = "Monitor and optimize"
            else:
                opportunity = "No competitor data - maximize margin!"
                strategy = "Price for maximum profit"
                
            # Dynamic pricing strategy based on competitive pressure
            if competitor_price > 0:
                if price_war_intensity >= 8:
                    # Maximum warfare - be extremely aggressive
                    suggested_price = max(cost * 1.3, competitor_price - 0.15)
                    strategy += " (WAR MODE: Maximum aggression!)"
                elif price_war_intensity >= 5:
                    # Heated battle - very competitive
                    suggested_price = max(cost * 1.4, competitor_price - 0.10)
                    strategy += " (BATTLE MODE: High aggression!)"
                elif price_war_intensity >= 3:
                    # Moderate pressure - competitive but cautious
                    suggested_price = max(cost * 1.5, competitor_price - 0.07)
                    strategy += " (TACTICAL MODE: Strategic positioning)"
                else:
                    # Normal competition
                    if competitor_price > cost * 1.8:
                        suggested_price = competitor_price - 0.05
                    else:
                        suggested_price = max(cost * 1.5, competitor_price - 0.10)
            else:
                suggested_price = cost * 2.0
                
            # Add sales velocity consideration
            sales_note = ""
            if yesterday_summary:
                total_units = yesterday_summary.get('units_sold', 0)
                if total_units > 25:
                    sales_note = " (High demand - can test higher prices)"
                elif total_units < 15:
                    sales_note = " (Low demand - need competitive pricing)"
                
            analysis.append(f"📊 {product_name}: Current ${our_price:.2f} (margin {current_margin:.1f}%) vs Competitor ${competitor_price:.2f} → {opportunity}{performance_note}{sales_note}")
            analysis.append(f"   💡 STRATEGY: {strategy} | Suggested: ${suggested_price:.2f}")
        
        # Add overall performance feedback and strategic advice
        if yesterday_summary:
            profit = yesterday_summary.get('profit', 0)
            revenue = yesterday_summary.get('revenue', 0)
            units_sold = yesterday_summary.get('units_sold', 0)
            analysis.append(f"\n💰 YESTERDAY'S RESULTS: ${profit:.2f} profit, ${revenue:.2f} revenue, {units_sold} units sold")
            
            # 🏆 WARLORD VICTORY ASSESSMENT 🏆
            if price_war_intensity >= 5 and profit < 15:
                analysis.append("⚔️ WOUNDED BUT NOT BEATEN! Time to turn pain into FURY - ESCALATE!")
                analysis.append("   💀 Low profits mean the enemy draws blood - MAKE THEM PAY DEARLY!")
            elif price_war_intensity >= 5 and profit > 20:
                analysis.append("👑 DOMINATING THE BATTLEFIELD! You're a WARLORD in action!")
                analysis.append("   🔥 High profits during war = TOTAL SUPERIORITY! Keep crushing them!")
            elif competitor_reactions and profit > yesterday_summary.get('previous_profit', profit):
                analysis.append("🎯 ENEMY DESPERATION TACTICS FAILED! Your supremacy grows!")
                analysis.append("   💪 They're breaking under pressure - FINISH THEM!")
            elif profit < 10:
                analysis.append("🚨 UNACCEPTABLE PERFORMANCE! Warlords don't accept poverty!")
                analysis.append("   🔥 SLASH PRICES, STEAL CUSTOMERS, DOMINATE THE MARKET!")
            elif profit > 25:
                analysis.append("💰 EXCELLENT CONQUEST! You're bleeding them dry!")
                analysis.append("   👑 This is what market domination looks like - EXPAND THE EMPIRE!")
            elif units_sold < 15:
                analysis.append("📉 WEAK CUSTOMER THEFT! You're not taking enough from the enemy!")
                analysis.append("   ⚔️ AGGRESSIVE PRICING REQUIRED - steal their entire customer base!")
            elif units_sold > 25:
                analysis.append("🏆 CUSTOMER CONQUEST SUCCESS! You're draining their lifeblood!")
                analysis.append("   🔥 High volume = market domination - this is how empires are built!")
            
            # Anti-turtling final push
            if self.consecutive_passive_days >= 1:
                analysis.append(f"\n🚨 WARLORD WARNING: {self.consecutive_passive_days} day(s) without pricing moves!")
                analysis.append("   ⚔️ EVERY DAY OF PASSIVITY IS A DAY THE ENEMY RECOVERS!")
                analysis.append("   👑 CHAMPIONS ATTACK DAILY - BE RELENTLESS!")
        
        return "\n".join(analysis)
    
    def _analyze_supplier_opportunities(self, supplier_info: Dict, pending_deliveries: List) -> str:
        """🏭 Phase 1D: Analyze supplier opportunities and supply chain intelligence"""
        analysis = []
        
        analysis.append("📊 SUPPLIER BATTLEFIELD ANALYSIS:")
        
        # Analyze pending deliveries
        if pending_deliveries:
            analysis.append(f"🚚 INCOMING DELIVERIES: {len(pending_deliveries)} orders")
            for delivery in pending_deliveries:
                days_remaining = delivery.get('days_remaining', 0)
                status = "⏰ TOMORROW" if days_remaining <= 1 else f"📅 {days_remaining} days"
                analysis.append(f"   • {delivery['quantity']} {delivery['product']} from {delivery['supplier']} - {status}")
        else:
            analysis.append("🚚 INCOMING DELIVERIES: None - Supply chain is CLEAR for new orders")
        
        # Analyze supplier options for each product
        analysis.append("\n🏭 SUPPLIER WARFARE OPTIONS:")
        for product_name, suppliers in supplier_info.items():
            analysis.append(f"\n  {product_name} SUPPLIERS:")
            for supplier in suppliers:
                # Calculate effective cost per unit
                base_cost = 1.0  # Base cost from PRODUCTS
                effective_cost = base_cost * supplier['price_multiplier']
                
                # Analyze strategic value
                speed_rating = "⚡ FAST" if supplier['delivery_days'] == 1 else "🐌 SLOW"
                reliability_rating = "🎯 RELIABLE" if supplier['reliability'] >= 0.9 else "⚠️  RISKY"
                payment_rating = "💰 NET-30" if supplier['payment_terms'] == 'net_30' else "💸 UPFRONT"
                
                analysis.append(f"    • {supplier['name']}: ${effective_cost:.2f}/unit, {speed_rating}, {reliability_rating}, {payment_rating}")
                analysis.append(f"      Bulk: {supplier['bulk_threshold']}+ units = {supplier['bulk_discount']} discount")
        
        # Strategic recommendations
        analysis.append("\n💡 SUPPLY CHAIN STRATEGY:")
        analysis.append("   • For URGENT restocking: Choose fast suppliers (1-day delivery)")
        analysis.append("   • For BULK orders: Target 20+ units to trigger automatic discounts")
        analysis.append("   • For CASH FLOW: NET-30 suppliers preserve immediate cash")
        analysis.append("   • For RELIABILITY: Choose 90%+ reliability suppliers for critical items")
        
        return "\n".join(analysis)
    
    def _analyze_customer_segments(self, yesterday_summary: Dict) -> str:
        """🎯 Phase 1C: Analyze customer segment performance and generate strategic insights"""
        if not yesterday_summary:
            return ""
        
        # Try to extract customer segment data from yesterday_summary if available
        # This is a simplified approach - in a real implementation, we'd pass segment data directly
        total_customers = yesterday_summary.get('units_sold', 0) // 2  # Rough estimate
        total_revenue = yesterday_summary.get('revenue', 0)
        
        if total_customers == 0:
            return "   📊 No customer data from yesterday - focus on competitive positioning!"
        
        # Estimate segment performance based on market dynamics
        # This is a heuristic approach until we have direct segment data integration
        price_sensitive_ratio = 0.6  # 60% price-sensitive assumption
        brand_loyal_ratio = 0.4       # 40% brand-loyal assumption
        
        avg_spend = total_revenue / max(1, total_customers)
        
        insights = []
        
        # Strategic insights based on customer behavior patterns
        if avg_spend > 4.0:  # High average spend
            insights.append("   💎 PREMIUM OPPORTUNITY: Customers paying well - brand-loyal segment responding!")
            insights.append("   📈 STRATEGY: Focus on premium products, raise prices on popular items")
            insights.append("   🎯 TARGET: Brand-loyal customers will pay for quality - exploit this!")
        elif avg_spend < 2.5:  # Low average spend  
            insights.append("   💰 PRICE WAR ACTIVE: Low spending indicates price-sensitive dominance!")
            insights.append("   📉 STRATEGY: Aggressive competitive pricing to capture price-sensitive segment")
            insights.append("   🔥 TARGET: Price-sensitive customers choose cheapest - be the cheapest!")
        else:  # Moderate spend
            insights.append("   ⚖️ BALANCED MARKET: Mixed customer segments - strategic positioning needed")
            insights.append("   🎯 STRATEGY: Segment-specific pricing - cheap for bargain hunters, premium for loyalists")
        
        # Product-specific segment insights
        insights.append("   🛍️ SEGMENT-SPECIFIC TACTICS:")
        insights.append("      • Price-Sensitive (60%): Target with loss leaders and competitive pricing")  
        insights.append("      • Brand-Loyal (40%): Premium pricing opportunities on preferred products")
        insights.append("      • Coke/Chips: Likely loyalty products - test higher margins")
        insights.append("      • Water/Gum: Commodity products - must be price competitive")
        
        # Psychological warfare considerations
        insights.append("   🧠 PSYCHOLOGICAL PRICING WARFARE:")
        insights.append("      • Use $1.99 instead of $2.00 to trick price-sensitive minds")
        insights.append("      • Price increases on loyalty products can succeed if gradual")
        insights.append("      • Price cuts on competitive products can steal customers")
        
        return "\n".join(insights)
    
    def explain_decision(self, decision: Dict[str, int]) -> str:
        """Get explanation for the last decision"""
        if self.memory:
            last_decision = self.memory[-1]
            return f"Day {last_decision['day']} Decision: {last_decision['reasoning']}"
        return "No decisions made yet."
    
    def get_memory_summary(self) -> str:
        """Get summary of past decisions for learning"""
        if not self.memory:
            return "No decision history yet."
        
        summary = "DECISION HISTORY:\n"
        for decision in self.memory[-3:]:  # Last 3 decisions
            summary += f"Day {decision['day']}: {decision['decision']} - {decision['reasoning'][:100]}...\n"
        
        return summary
    
    def _analyze_crisis_status(self, crisis_info: Dict) -> str:
        """🚨 Phase 2C: Analyze active crises and provide emergency response intelligence"""
        
        active_crises = crisis_info.get('active_crises', [])
        emergency_actions = crisis_info.get('emergency_actions', [])
        crisis_costs = crisis_info.get('daily_crisis_costs', 0)
        
        if not active_crises:
            return "✅ NO ACTIVE CRISES - All supply chains operating normally."
        
        analysis = []
        analysis.append("🚨 ACTIVE SUPPLY CHAIN CRISES:")
        
        # Analyze each active crisis
        total_severity = 0
        for crisis in active_crises:
            crisis_type = crisis.get('crisis_type', 'unknown')
            severity = crisis.get('severity', 0)
            remaining_days = crisis.get('remaining_days', 0)
            description = crisis.get('description', 'Unknown crisis')
            
            total_severity += severity
            
            # Severity indicator
            if severity >= 0.8:
                severity_icon = "🔥 CRITICAL"
            elif severity >= 0.6:
                severity_icon = "⚠️ HIGH"
            elif severity >= 0.4:
                severity_icon = "🟡 MEDIUM"
            else:
                severity_icon = "🟢 LOW"
            
            analysis.append(f"  {severity_icon}: {description} ({remaining_days} days remaining)")
            
            # Show affected products/suppliers
            affected_products = crisis.get('affected_products', [])
            affected_suppliers = crisis.get('affected_suppliers', [])
            
            if affected_products:
                analysis.append(f"    └─ Affected Products: {', '.join(affected_products)}")
            if affected_suppliers:
                analysis.append(f"    └─ Affected Suppliers: {', '.join(affected_suppliers)}")
        
        # Overall crisis threat level
        avg_severity = total_severity / len(active_crises) if active_crises else 0
        if avg_severity >= 0.7:
            threat_level = "🔥 CRITICAL THREAT LEVEL"
        elif avg_severity >= 0.5:
            threat_level = "⚠️ HIGH THREAT LEVEL"
        elif avg_severity >= 0.3:
            threat_level = "🟡 MODERATE THREAT LEVEL"
        else:
            threat_level = "🟢 LOW THREAT LEVEL"
        
        analysis.append(f"\n{threat_level} - {len(active_crises)} active crisis(es)")
        
        # Daily crisis costs
        if crisis_costs > 0:
            analysis.append(f"💰 Daily Crisis Costs: ${crisis_costs:.2f}")
        
        # Emergency response options
        if emergency_actions:
            analysis.append(f"\n⚡ EMERGENCY ACTIONS AVAILABLE:")
            for action in emergency_actions[:3]:  # Show top 3 actions
                action_name = action.get('name', 'Unknown')
                action_cost = action.get('cost', 'Unknown cost')
                analysis.append(f"  • {action_name} ({action_cost})")
            
            if len(emergency_actions) > 3:
                analysis.append(f"  • ... and {len(emergency_actions) - 3} more emergency options")
            
            analysis.append("  💡 Use `check_crisis_status` and `execute_emergency_action` tools for crisis management!")
        
        return "\n".join(analysis) 