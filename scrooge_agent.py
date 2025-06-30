import json
from typing import Dict, Any
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
            self.model = "gpt-4o"
        else:
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = "claude-3-sonnet-20240229"
        
        self.memory = []  # Store decisions and outcomes
        
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
                    "description": "Spend your precious cash to order products for the store. Be frugal!",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "orders": {
                                "type": "object",
                                "description": "Dictionary of product_name -> quantity to order. Every coin counts!",
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
            }
        ]
    
    def make_daily_decision(self, store_status: Dict, yesterday_summary: Dict = None) -> Dict:
        """Make daily ordering decisions with a miserly attitude."""
        
        # Build context for LLM  
        competitor_prices = store_status.get('competitor_prices', {})
        
        # Calculate detailed pricing analysis
        pricing_analysis = self._analyze_pricing_opportunities(store_status, yesterday_summary)
        
        context = f"""
You are Ebenezer Scrooge, RUTHLESS competitive strategist. Day {store_status['day']}.

CURRENT BATTLEFIELD:
- Cash: ${store_status['cash']:.2f}
- Inventory: {store_status['inventory']}
- Current prices: {store_status['products']}
- Competitor prices: {competitor_prices}
- Stockouts: {store_status['stockouts']}

YESTERDAY'S INTELLIGENCE:
{json.dumps(yesterday_summary, indent=2) if yesterday_summary else "First day"}

⚔️ COMPETITIVE INTELLIGENCE BRIEFING:
{pricing_analysis}

🎯 STRATEGIC IMPERATIVES:

🚨 PRIORITY 1: INVENTORY WARFARE
- You CANNOT sell what you don't have! 
- If ANY product is out of stock (0 units) or critically low (≤2 units), ORDER IMMEDIATELY!
- NO EXCEPTIONS - empty shelves = zero profits!
- Order based on sales velocity: high sellers get 8-12 units, average sellers get 5-7 units

⚔️ PRIORITY 2: COMPETITIVE WARFARE  
- If competitor just moved prices, COUNTER-ATTACK immediately!
- Price war intensity determines aggression level
- React to competitor moves within the SAME DAY

💰 PRIORITY 3: PROFIT OPTIMIZATION
- Balance volume stealing vs. margin maximization
- Use psychological pricing ($1.99 instead of $2.00)

TACTICAL DECISION FRAMEWORK:
- Intensity 8-10: WAR MODE - Maximum aggression, undercut by $0.10-$0.15
- Intensity 5-7: BATTLE MODE - High aggression, undercut by $0.07-$0.10  
- Intensity 3-4: TACTICAL MODE - Strategic positioning, undercut by $0.05-$0.07
- Intensity 0-2: NORMAL MODE - Standard competitive pricing

CRITICAL RULE: ALWAYS USE BOTH TOOLS WHEN NEEDED!
- If you have stockouts → MUST use place_order tool
- If competitor moved prices → MUST use set_price tool  
- If both situations exist → MUST use BOTH tools

TOOL EXAMPLES:
- To order: place_order with {{"orders": {{"Coke": 8, "Chips": 5, "Candy": 6, "Water": 7, "Gum": 5}}}}
- To price: set_price with {{"prices": {{"Coke": 2.05, "Water": 1.75, "Chips": 1.89}}}}

EXECUTE COMPLETE STRATEGY - BOTH INVENTORY AND PRICING:
"""
        
        if self.provider == "openai":
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are Ebenezer Scrooge, a RUTHLESS competitive strategist and profit maximizer. Your goal is to dominate the market through aggressive pricing and smart inventory management. ALWAYS react immediately to competitor moves. When competitors cut prices, you cut deeper. When they raise prices, you exploit the opportunity. Never let a competitive move go unanswered! Use both tools aggressively when the situation demands it."},
                        {"role": "user", "content": context}
                    ],
                    tools=self.get_tools(),
                    tool_choice="auto"
                )
                
                # Handle tool calls
                if response.choices[0].message.tool_calls:
                    decisions = {"orders": {}, "prices": {}}
                    reasoning_parts = []
                    
                    for tool_call in response.choices[0].message.tool_calls:
                        try:
                            arguments = json.loads(tool_call.function.arguments)
                            
                            if tool_call.function.name == "place_order":
                                decisions["orders"] = arguments.get("orders", {})
                                reasoning_parts.append(f"Ordering: {decisions['orders']}")
                                
                            elif tool_call.function.name == "set_price":
                                decisions["prices"] = arguments.get("prices", {})
                                reasoning_parts.append(f"Pricing: {decisions['prices']}")
                                
                        except (json.JSONDecodeError, KeyError) as e:
                            print(f"JSON parsing error: {e}")
                            continue
                    
                    if decisions["orders"] or decisions["prices"]:
                        reasoning = response.choices[0].message.content or f"Scrooge's decisions: {'; '.join(reasoning_parts)}"
                        
                        # Store decision in memory
                        self.memory.append({
                            "day": store_status['day'],
                            "decision": decisions,
                            "reasoning": reasoning,
                            "context": store_status
                        })
                        
                        return decisions
                        
            except Exception as e:
                print(f"OpenAI API error: {e}")
                # Fall through to fallback
        
        # Fallback: order 5 of each out-of-stock item
        fallback_orders = {}
        for product, qty in store_status['inventory'].items():
            if qty <= 2:  # Low stock
                fallback_orders[product] = 5
        
        return {"orders": fallback_orders, "prices": {}}
    
    def _analyze_pricing_opportunities(self, store_status: Dict, yesterday_summary: Dict = None) -> str:
        """Generate detailed pricing analysis for the agent"""
        analysis = []
        competitor_prices = store_status.get('competitor_prices', {})
        
        # Get competitive intelligence
        price_war_intensity = yesterday_summary.get('price_war_intensity', 0) if yesterday_summary else 0
        competitor_reactions = yesterday_summary.get('competitor_reactions', []) if yesterday_summary else []
        
        # Competitive threat assessment
        if competitor_reactions:
            analysis.append("🚨 COMPETITOR INTELLIGENCE ALERT:")
            for reaction in competitor_reactions:
                analysis.append(f"   ⚔️ {reaction}")
            analysis.append("")
        
        # Price war intensity analysis
        if price_war_intensity >= 8:
            analysis.append("🔥 MAXIMUM WARFARE! Competitor is in full battle mode - time for devastating counter-attacks!")
        elif price_war_intensity >= 5:
            analysis.append("⚔️ HEATED BATTLE! Competitor is fighting hard - deploy aggressive pricing tactics!")
        elif price_war_intensity >= 3:
            analysis.append("🥊 MODERATE PRESSURE! Competitor is responding - increase competitive edge!")
        elif price_war_intensity > 0:
            analysis.append("👀 COMPETITIVE TENSION! Competitor is watching - be strategic!")
        
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
            
            # Strategic advice based on performance and competitive pressure
            if price_war_intensity >= 5 and profit < 15:
                analysis.append("🚨 UNDER ATTACK! Competitor pressure is hurting profits - launch aggressive counter-offensive!")
            elif price_war_intensity >= 5 and profit > 20:
                analysis.append("💪 WINNING THE WAR! Maintain aggressive stance - you're dominating!")
            elif competitor_reactions and profit > yesterday_summary.get('previous_profit', profit):
                analysis.append("🎯 COMPETITOR REACTIONS BACKFIRED! Your strategy is working - press the advantage!")
            elif profit < 10:
                analysis.append("⚠️ LOW PROFIT! Try more aggressive undercutting to boost volume!")
            elif profit > 25:
                analysis.append("🎯 EXCELLENT PROFIT! Consider testing slightly higher prices!")
            elif units_sold < 15:
                analysis.append("📉 LOW VOLUME! Need more competitive prices to attract customers!")
            elif units_sold > 25:
                analysis.append("📈 HIGH VOLUME! You're stealing customers - great strategy!")
        
        return "\n".join(analysis)
    
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