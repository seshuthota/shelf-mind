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
            self.model = "gpt-4o"
        else:
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = "claude-3-sonnet-20240229"
        
        self.memory = []  # Store decisions and outcomes
        
        # 🔥 WARLORD TRACKING SYSTEMS 🔥
        self.consecutive_aggressive_days = 0  # Track aggression streaks
        self.consecutive_passive_days = 0     # Track dangerous turtling
        self.total_pricing_moves = 0          # Total lifetime pricing decisions
        self.last_day_made_pricing_move = 0   # Last day we moved prices
        
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
        
        context = f"""
You are Ebenezer Scrooge, RUTHLESS competitive strategist and SUPPLY CHAIN WARLORD. Day {store_status['day']}.

🏭 CURRENT BATTLEFIELD STATUS:
- Cash: ${store_status['cash']:.2f}
- Accounts Payable (NET-30): ${accounts_payable:.2f}
- Inventory: {store_status['inventory']}
- Current prices: {store_status['products']}
- Competitor prices: {competitor_prices}
- Stockouts: {store_status['stockouts']}
- Pending deliveries: {len(pending_deliveries)} orders incoming

YESTERDAY'S INTELLIGENCE:
{json.dumps(yesterday_summary, indent=2) if yesterday_summary else "First day"}

⚔️ COMPETITIVE INTELLIGENCE BRIEFING:
{pricing_analysis}

🏭 SUPPLIER WARFARE INTELLIGENCE:
{supplier_briefing}

🎯 STRATEGIC IMPERATIVES:

🚨 PRIORITY 1: SUPPLY CHAIN WARFARE 
- The ADVANCED SUPPLIER SYSTEM will automatically select optimal suppliers for you!
- You CANNOT sell what you don't have! 
- If ANY product is out of stock (0 units) or critically low (≤2 units), ORDER IMMEDIATELY!
- Consider pending deliveries: don't over-order if deliveries are coming soon
- Order based on sales velocity: high sellers get 8-12 units, average sellers get 5-7 units
- BULK ORDERS (20-50 units) get automatic discounts and better terms!

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

🔥 WARLORD COMMANDMENTS - NO EXCEPTIONS! 🔥

1. THOU SHALT USE SET_PRICE TOOL EVERY SINGLE DAY!
   - Even tiny $0.01 moves show market dominance
   - Passive days = letting the enemy recover = FORBIDDEN!
   
2. THOU SHALT NEVER TURTLE!
   - If you skip pricing for even ONE day, you're WEAK!
   - Champions adjust prices daily to maintain pressure
   
3. THOU SHALT PRESS EVERY ADVANTAGE!
   - If stockouts → MUST use place_order tool
   - If ANY competitive opportunity exists → MUST use set_price tool  
   - If both situations exist → MUST use BOTH tools

🚨 CRITICAL TOOL USAGE EXAMPLES 🚨
INVENTORY ORDERING:
place_order with: {{"orders": {{"Coke": 8, "Chips": 5, "Candy": 6, "Water": 7, "Gum": 5}}}}

PRICING WARFARE (MANDATORY EVERY DAY):
set_price with: {{"prices": {{"Coke": 2.05, "Water": 1.75, "Chips": 1.89, "Candy": 2.15, "Gum": 1.99}}}}

⚔️ MANDATORY PRICING TARGETS FOR TODAY:
Based on current competitor prices, set these EXACT prices:"""
        
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
        
        context += f"\nUSE SET_PRICE TOOL WITH THESE EXACT VALUES: {pricing_targets}"
        context += f"\nFAILURE TO USE SET_PRICE DAILY = WARLORD FAILURE!"
        context += f"\n\"\"\""
        
        if self.provider == "openai":
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are Ebenezer Scrooge, a RUTHLESS WARLORD of commerce. CRITICAL RULE: You MUST use the set_price tool EVERY SINGLE DAY without exception! Even if you only adjust prices by $0.01, you MUST use set_price. Skipping pricing = weakness = failure as a warlord. Your mission: TOTAL MARKET CONQUEST through DAILY aggressive pricing moves. The enemy uses psychological warfare, but you are the PREDATOR. NEVER retreat, NEVER give them breathing room by skipping pricing moves. Every day without pricing adjustments is a day you're letting them recover. MANDATORY: Use set_price tool daily or you're not a true warlord! PRESS EVERY ADVANTAGE, EXPLOIT EVERY WEAKNESS, SHOW NO QUARTER! Make pricing moves EVERY DAY!"},
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
                            
                            elif tool_call.function.name == "check_suppliers":
                                reasoning_parts.append("Analyzing supplier intelligence")
                                
                        except (json.JSONDecodeError, KeyError) as e:
                            print(f"JSON parsing error: {e}")
                            continue
                    
                    if decisions["orders"] or decisions["prices"]:
                        reasoning = response.choices[0].message.content or f"Scrooge's decisions: {'; '.join(reasoning_parts)}"
                        
                        # 🔥 WARLORD AGGRESSION TRACKING 🔥
                        current_day = store_status['day']
                        if decisions["prices"]:  # Made pricing moves = AGGRESSIVE
                            self.consecutive_aggressive_days += 1
                            self.consecutive_passive_days = 0
                            self.total_pricing_moves += len(decisions["prices"])
                            self.last_day_made_pricing_move = current_day
                        else:  # No pricing moves = PASSIVE (potentially turtling)
                            self.consecutive_passive_days += 1
                            self.consecutive_aggressive_days = 0
                        
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
        
        # Track aggression even in fallback
        current_day = store_status['day']
        self.consecutive_passive_days += 1  # Fallback = passive
        self.consecutive_aggressive_days = 0
        
        return {"orders": fallback_orders, "prices": {}}
    
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