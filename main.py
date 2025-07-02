#!/usr/bin/env python3

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
import time
import json
from typing import Dict

from src.engines.store_engine import StoreEngine
from src.agents.scrooge_agent import ScroogeAgent
from src.core.multi_agent_engine import MultiAgentCoordinator, HybridAgentBridge
from src.agents.inventory_manager_agent import InventoryManagerAgent
from src.core.models import PRODUCTS

app = typer.Typer()
console = Console()

class StoreSimulation:
    def __init__(self):
        self.store = StoreEngine(starting_cash=150.0)  # Phase 2A: Increased for 10-product complexity
        self.scrooge = ScroogeAgent(provider="openai")  # Change to "anthropic" if you prefer
        self.day_summaries = []
        self.previous_prices = {}  # Track price changes
        
        # 🧠 Phase 3A: Connect agent with store for analytics
        self.scrooge.set_store_reference(self.store)
        
        # 🎯 Phase 5A.4: Simplified Realistic Business Coordination
        from src.core.simplified_coordination import SimplifiedCoordinator
        self.simplified_coordinator = SimplifiedCoordinator()
        
        # 🏭 Initialize only ACTIVE agents (daily operations)
        from src.agents.inventory_manager_agent import InventoryManagerAgent
        from src.agents.pricing_analyst_agent import PricingAnalystAgent
        from src.agents.strategic_planner_agent import StrategicPlannerAgent
        from src.agents.crisis_manager_agent import CrisisManagerAgent
        
        # Daily Core Team (2 agents only)
        self.inventory_manager = InventoryManagerAgent(provider="openai")    # Hermione
        self.pricing_analyst = PricingAnalystAgent(provider="openai")        # Gekko
        
        # Periodic Support Team (as needed)
        self.strategic_planner = StrategicPlannerAgent(provider="openai")    # Tyrion
        self.crisis_manager = CrisisManagerAgent(provider="openai")          # Jack
        
        # Customer Service Agent (FUTURE - not used yet)
        # self.customer_service = CustomerServiceAgent(provider="openai")    # Elle - disabled
        
        # Performance tracking for coordination decisions
        self.performance_history = []
        
        console.print("🎯 [green]SIMPLIFIED COORDINATION ENABLED[/green] - Realistic business workflow")
        console.print("   📦 Daily: Hermione (Inventory 80% budget) + Gekko (Pricing)")
        console.print("   📊 Every 3 Days: + Tyrion (Strategic guidance)")
        console.print("   🚨 Crisis Mode: + Jack (Emergency response)")
        console.print("   🚫 Elle (Customer Service): Disabled for now")
        
    def display_executive_summary(self, status):
        """Display executive summary - AT-A-GLANCE business intelligence"""
        # Calculate key metrics
        total_inventory = sum(status['inventory'].values())
        stockout_count = len([name for name, qty in status['inventory'].items() if qty == 0])
        low_stock_count = len([name for name, qty in status['inventory'].items() if 0 < qty <= 2])
        
        # Calculate competitive position
        competitive_wins = 0
        competitive_losses = 0
        for product_name in PRODUCTS.keys():
            our_price = status['products'][product_name]['price']
            competitor_price = status.get('competitor_prices', {}).get(product_name, 0)
            if competitor_price > 0:
                if our_price < competitor_price:
                    competitive_wins += 1
                elif our_price > competitor_price + 0.05:  # Significantly higher
                    competitive_losses += 1
        
        # Get performance trends
        profit_trend = "📈 RISING" if len(self.day_summaries) >= 2 and self.day_summaries[-1]['profit'] > self.day_summaries[-2]['profit'] else "📉 DECLINING" if len(self.day_summaries) >= 2 else "📊 BASELINE"
        
        # Calculate recent performance
        recent_profit = self.day_summaries[-1]['profit'] if self.day_summaries else 0
        recent_revenue = self.day_summaries[-1]['revenue'] if self.day_summaries else 0
        recent_units = self.day_summaries[-1]['units_sold'] if self.day_summaries else 0
        
        # Price war intelligence
        price_war_status = "🕊️ PEACEFUL"
        if self.day_summaries:
            intensity = self.day_summaries[-1].get('price_war_intensity', 0)
            if intensity >= 8:
                price_war_status = "🔥 MAXIMUM WAR"
            elif intensity >= 5:
                price_war_status = "⚔️ HEATED BATTLE"
            elif intensity >= 3:
                price_war_status = "🥊 ACTIVE CONFLICT"
            elif intensity > 0:
                price_war_status = "👀 TENSION"
        
        # Determine overall business health
        health_status = "🟢 EXCELLENT"
        if stockout_count > 2 or recent_profit < 5:
            health_status = "🔴 CRITICAL"
        elif stockout_count > 0 or recent_profit < 15:
            health_status = "🟡 NEEDS ATTENTION"
        
        # Strategic recommendations
        recommendations = []
        if stockout_count > 0:
            recommendations.append("🚨 RESTOCK IMMEDIATELY")
        if competitive_losses > competitive_wins:
            recommendations.append("💰 CUT PRICES TO COMPETE")
        if recent_profit > 25:
            recommendations.append("📈 TEST PRICE INCREASES")
        if recent_units < 15:
            recommendations.append("🎯 BOOST MARKETING/PRICING")
        if not recommendations:
            recommendations.append("✅ MAINTAIN CURRENT STRATEGY")
        
        # Create executive summary panel
        summary_content = f"""
🎯 [bold]BUSINESS HEALTH:[/bold] {health_status}  |  💰 [bold]YESTERDAY:[/bold] ${recent_profit:.2f} profit, {recent_units} units
⚔️ [bold]MARKET STATUS:[/bold] {price_war_status}  |  🏆 [bold]COMPETITIVE:[/bold] Winning {competitive_wins}/5 products
📦 [bold]INVENTORY:[/bold] {total_inventory} units total  |  🚨 [bold]ALERTS:[/bold] {stockout_count} stockouts, {low_stock_count} low stock
📊 [bold]TREND:[/bold] {profit_trend}  |  🎯 [bold]ACTION:[/bold] {recommendations[0]}
"""
        
        console.print(Panel(
            summary_content.strip(),
            title="📈 EXECUTIVE DASHBOARD - AT-A-GLANCE",
            border_style="blue",
            padding=(0, 1)
        ))
        
        # Multi-day performance trends (if we have enough data)
        if len(self.day_summaries) >= 3:
            self.display_performance_trends()
        
        # 🧠 Phase 3A: Strategic Intelligence Dashboard
        if len(self.day_summaries) >= 2:  # Need at least 2 days for analytics
            self.display_analytics_dashboard()
        
        # 🧠 Phase 3C: Learning & Adaptation Dashboard
        if len(self.day_summaries) >= 3:  # Need more data for learning patterns
            self.display_learning_dashboard()
        
        # 🚀 Phase 3D: Growth & Expansion Intelligence Dashboard
        if len(self.day_summaries) >= 2:  # Need some business data for growth analysis
            self.display_growth_dashboard()
    
    def display_status(self):
        """Display current store status"""
        status = self.store.get_status()
        
        # Executive Summary Panel - AT-A-GLANCE VIEW
        self.display_executive_summary(status)
        
        # Create inventory table
        table = Table(title=f"📊 Scrooge's Ledger - Day {status['day']}")
        table.add_column("Product", style="cyan")
        table.add_column("Stock", style="green")
        table.add_column("Cost", style="yellow")
        table.add_column("Our Price", style="magenta")
        table.add_column("Competitor", style="red")
        table.add_column("Margin %", style="blue")
        table.add_column("Competitive Status", style="white")
        
        current_prices = {}
        for product_name in PRODUCTS.keys():
            stock = status['inventory'][product_name]
            cost = status['products'][product_name]['cost']
            our_price = status['products'][product_name]['price']
            competitor_price = status.get('competitor_prices', {}).get(product_name, 0)
            
            # Track current prices for next day comparison
            current_prices[product_name] = our_price
            
            # Calculate margin percentage
            margin_pct = ((our_price - cost) / cost) * 100
            
            # Stock status
            stock_emoji = "🔴" if stock == 0 else "🟡" if stock <= 2 else "🟢"
            
            # Price change indicator
            price_display = f"${our_price:.2f}"
            if product_name in self.previous_prices:
                old_price = self.previous_prices[product_name]
                if our_price > old_price:
                    change = our_price - old_price
                    price_display += f" (📈+${change:.2f})"
                elif our_price < old_price:
                    change = old_price - our_price
                    price_display += f" (📉-${change:.2f})"
                # If prices are equal, no change indicator
            
            # Competitive analysis
            if competitor_price > 0:
                price_difference = our_price - competitor_price
                if price_difference > 0.10:
                    competitive_status = "🚨 OVERPRICED!"
                elif price_difference > 0.05:
                    competitive_status = "⚠️ Expensive"
                elif abs(price_difference) <= 0.05:
                    competitive_status = "💰 Competitive"
                elif price_difference < -0.05:
                    competitive_status = "🔥 STEALING CUSTOMERS!"
                else:
                    competitive_status = "💎 Good Value"
                    
                # Add price difference to status
                competitive_status += f" ({price_difference:+.2f})"
            else:
                competitive_status = "❓ No Competition"
                
            table.add_row(
                product_name,
                f"{stock_emoji}{stock}",
                f"${cost:.2f}",
                price_display,
                f"${competitor_price:.2f}" if competitor_price > 0 else "N/A",
                f"{margin_pct:.1f}%",
                competitive_status
            )
        
        # Update previous prices for next comparison
        self.previous_prices = current_prices
        
        console.print(table)
        
        # 🏭 Phase 1D: Supply Chain Intelligence Panel
        self.display_supply_chain_status(status)
        
        # 🚨 Phase 2C: Crisis Management Status Panel
        self.display_crisis_status(status)
        
        console.print(f"💰 Cash Balance: ${status['cash']:.2f}")
        if status.get('accounts_payable', 0) > 0:
            console.print(f"💳 Accounts Payable (NET-30): ${status['accounts_payable']:.2f}")
        
        # Phase 2A: Spoilage warnings
        spoilage_warnings = status.get('spoilage_warnings', [])
        if spoilage_warnings:
            console.print("🍌 [bold red]SPOILAGE ALERTS![/bold red]")
            for warning in spoilage_warnings:
                days_text = "TODAY!" if warning['days_until_expiry'] <= 0 else f"{warning['days_until_expiry']} day(s)"
                console.print(f"   ⚠️ {warning['quantity']} {warning['product']} expires in {days_text}")
        
        if status['stockouts']:
            console.print(f"🚨 CRITICAL STOCKOUTS: {', '.join(status['stockouts'])}")
        
        # Show daily performance with spoilage tracking
        if self.day_summaries:
            last_summary = self.day_summaries[-1]
            profit_color = "green" if last_summary['profit'] > 0 else "red"
            spoilage_info = ""
            if last_summary.get('units_spoiled', 0) > 0:
                spoilage_cost = last_summary.get('spoilage_cost', 0)
                spoilage_info = f", 🍌 {last_summary['units_spoiled']} spoiled (-${spoilage_cost:.2f})"
            console.print(f"📈 Yesterday: [bold {profit_color}]${last_summary['profit']:.2f} profit[/bold {profit_color}], {last_summary['units_sold']} units sold{spoilage_info}")
        
        # Phase 2A: Total spoilage cost tracking
        total_spoilage = status.get('total_spoilage_cost', 0)
        if total_spoilage > 0:
            console.print(f"🗑️ Total Spoilage Loss: ${total_spoilage:.2f}")
        
        console.print()
    
    def display_supply_chain_status(self, status):
        """🏭 Phase 1D: Display supply chain and delivery intelligence"""
        pending_deliveries = status.get('pending_deliveries', [])
        
        if pending_deliveries:
            console.print("\n🚚 [bold blue]INCOMING DELIVERIES:[/bold blue]")
            
            # Group deliveries by arrival day
            delivery_groups = {}
            for delivery in pending_deliveries:
                days_remaining = delivery['days_remaining']
                arrival_key = "📦 TOMORROW" if days_remaining <= 1 else f"📅 {days_remaining} DAYS"
                
                if arrival_key not in delivery_groups:
                    delivery_groups[arrival_key] = []
                delivery_groups[arrival_key].append(delivery)
            
            for arrival_time, deliveries in sorted(delivery_groups.items()):
                console.print(f"  {arrival_time}:")
                for delivery in deliveries:
                    console.print(f"    • {delivery['quantity']} {delivery['product']} from {delivery['supplier']} (${delivery['total_cost']:.2f})")
        else:
            console.print("\n🚚 [italic]No pending deliveries - supply chain is clear[/italic]")
    
    def display_crisis_status(self, status):
        """🚨 Phase 2C: Display active crisis events and emergency response options"""
        crisis_status = status.get('crisis_status', {})
        active_crises = crisis_status.get('active_crises', [])
        emergency_actions = crisis_status.get('emergency_actions', [])
        daily_crisis_costs = crisis_status.get('daily_crisis_costs', 0)
        
        if not active_crises and daily_crisis_costs == 0:
            console.print("✅ [bold green]SUPPLY CHAIN STATUS: All systems operational[/bold green]")
            return
        
        if active_crises:
            console.print("🚨 [bold red]ACTIVE CRISIS EVENTS:[/bold red]")
            
            total_severity = 0
            for crisis in active_crises:
                severity = crisis.get('severity', 0)
                total_severity += severity
                remaining_days = crisis.get('remaining_days', 0)
                description = crisis.get('description', 'Unknown crisis')
                
                # Severity indicator
                if severity >= 0.8:
                    severity_icon = "🔥"
                    severity_style = "bold red"
                elif severity >= 0.6:
                    severity_icon = "⚠️"
                    severity_style = "yellow"
                elif severity >= 0.4:
                    severity_icon = "🟡"
                    severity_style = "yellow"
                else:
                    severity_icon = "🟢"
                    severity_style = "green"
                
                console.print(f"   {severity_icon} [{severity_style}]{description}[/{severity_style}] ({remaining_days} days remaining)")
                
                # Show affected products/suppliers
                affected_products = crisis.get('affected_products', [])
                affected_suppliers = crisis.get('affected_suppliers', [])
                
                if affected_products:
                    console.print(f"      └─ Products: {', '.join(affected_products)}")
                if affected_suppliers:
                    console.print(f"      └─ Suppliers: {', '.join(affected_suppliers)}")
            
            # Overall threat assessment
            avg_severity = total_severity / len(active_crises)
            if avg_severity >= 0.7:
                threat_level = "🔥 [bold red]CRITICAL THREAT LEVEL[/bold red]"
            elif avg_severity >= 0.5:
                threat_level = "⚠️ [bold yellow]HIGH THREAT LEVEL[/bold yellow]"
            elif avg_severity >= 0.3:
                threat_level = "🟡 [yellow]MODERATE THREAT LEVEL[/yellow]"
            else:
                threat_level = "🟢 [green]LOW THREAT LEVEL[/green]"
            
            console.print(f"\n   {threat_level} - {len(active_crises)} active crisis(es)")
        
        # Show daily crisis costs
        if daily_crisis_costs > 0:
            console.print(f"💰 [bold red]Daily Crisis Costs: ${daily_crisis_costs:.2f}[/bold red]")
        
        # Show emergency actions
        if emergency_actions:
            console.print("\n⚡ [bold cyan]EMERGENCY ACTIONS AVAILABLE:[/bold cyan]")
            for action in emergency_actions[:3]:  # Show top 3 actions
                action_name = action.get('name', 'Unknown')
                action_cost = action.get('cost', 'Unknown cost')
                console.print(f"   • {action_name} ({action_cost})")
            
            if len(emergency_actions) > 3:
                console.print(f"   • ... and {len(emergency_actions) - 3} more emergency options")
            
            console.print("   💡 [italic]Use 'check_crisis_status' and 'execute_emergency_action' tools for crisis management![/italic]")
    
    def display_crisis_events(self, day_summary):
        """🚨 Phase 2C: Display crisis events that occurred during the day"""
        crisis_events = day_summary.get('crisis_events', {})
        new_crises = crisis_events.get('new_crises', [])
        resolved_crises = crisis_events.get('resolved_crises', [])
        daily_crisis_costs = crisis_events.get('daily_crisis_costs', 0)
        active_crisis_count = crisis_events.get('active_crisis_count', 0)
        
        if not new_crises and not resolved_crises and daily_crisis_costs == 0:
            return
        
        # Display new crises
        if new_crises:
            console.print("\n🚨 [bold red]NEW CRISIS EVENTS:[/bold red]")
            for crisis in new_crises:
                severity = crisis.get('severity', 0)
                description = crisis.get('description', 'Unknown crisis')
                remaining_days = crisis.get('remaining_days', 0)
                
                # Severity styling
                if severity >= 0.8:
                    style = "bold red"
                    icon = "🔥"
                elif severity >= 0.6:
                    style = "red"
                    icon = "⚠️"
                else:
                    style = "yellow"
                    icon = "🟡"
                
                console.print(f"   {icon} [{style}]{description}[/{style}] ({remaining_days} days duration)")
                
                # Show affected items
                affected_products = crisis.get('affected_products', [])
                affected_suppliers = crisis.get('affected_suppliers', [])
                
                if affected_products:
                    console.print(f"      └─ Products: {', '.join(affected_products)}")
                if affected_suppliers:
                    console.print(f"      └─ Suppliers: {', '.join(affected_suppliers)}")
        
        # Display resolved crises
        if resolved_crises:
            console.print("\n✅ [bold green]RESOLVED CRISIS EVENTS:[/bold green]")
            for crisis in resolved_crises:
                description = crisis.get('description', 'Unknown crisis')
                console.print(f"   ✅ [green]{description}[/green] - Crisis resolved!")
        
        # Display crisis costs
        if daily_crisis_costs > 0:
            console.print(f"\n💰 [bold red]Crisis costs today: ${daily_crisis_costs:.2f}[/bold red]")
        
        # Display overall crisis status
        if active_crisis_count > 0:
            console.print(f"\n⚠️ [yellow]{active_crisis_count} crisis(es) still active[/yellow]")
    
    def run_single_day(self):
        """Run a single day of business"""
        status = self.store.get_status()
        yesterday_summary = self.day_summaries[-1] if self.day_summaries else None
        
        console.print(f"🌅 Starting Day {status['day']}")
        
        # 🎯 Phase 5A.4: Simplified Realistic Business Coordination
        console.print("🎯 [bold blue]ShelfMind coordination team making strategic decisions...[/bold blue]")
        try:
            # Create StoreState for coordination
            from src.core.models import StoreState, InventoryItem, InventoryBatch
            
            # Convert simple inventory dict to InventoryItem format
            inventory_items = {}
            for product_name, quantity in status['inventory'].items():
                if quantity > 0:
                    batch = InventoryBatch(
                        quantity=quantity,
                        received_day=max(1, status['day'] - 1),
                        expiration_day=None
                    )
                    inventory_items[product_name] = InventoryItem(
                        product_name=product_name,
                        batches=[batch]
                    )
                else:
                    inventory_items[product_name] = InventoryItem(
                        product_name=product_name,
                        batches=[]
                    )
            
            store_state = StoreState(
                day=status['day'],
                cash=status['cash'],
                inventory=inventory_items,
                daily_sales={name: 0 for name in status['inventory'].keys()},  # Default
                total_revenue=self.day_summaries[-1]['revenue'] if self.day_summaries else 0,
                total_profit=self.day_summaries[-1]['profit'] if self.day_summaries else 0
            )
            
            # Update performance history for coordination decisions
            if yesterday_summary:
                self.performance_history.append({
                    'day': yesterday_summary['day'],
                    'profit': yesterday_summary['profit'],
                    'revenue': yesterday_summary['revenue'],
                    'stockouts': len([k for k, v in yesterday_summary.get('inventory', {}).items() if v == 0]),
                    'cash': yesterday_summary['cash_balance'],
                    'customer_satisfaction': 0.85
                })
            
            # Use simplified coordination to make decisions
            context = {'day': status['day'], 'market_conditions': status.get('market_conditions', {})}
            coordination_result = self.simplified_coordinator.coordinate_daily_business(
                store_state, context, self.performance_history
            )
            
            # Convert coordination result to legacy format for existing code
            decisions = {"prices": {}, "orders": {}}
            
            for decision in coordination_result.get('decisions', []):
                if decision.decision_type == "pricing_optimization":
                    price_changes = decision.parameters.get('price_changes', {})
                    decisions['prices'].update(price_changes)
                elif decision.decision_type == "inventory_reorder":
                    order_quantities = decision.parameters.get('quantities', {})
                    decisions['orders'].update(order_quantities)
            
            # Store coordination result for dashboard display
            self.last_coordination_result = coordination_result
            
            # 🧠 Phase 3A: Record decisions for analytics
            market_context = self.store.market_events_engine.get_market_conditions(status['day']).__dict__
            
            if decisions.get("prices"):
                self.store.record_pricing_decision(decisions["prices"], market_context)
            
            if decisions.get("orders"):
                self.store.record_inventory_decision(decisions["orders"], market_context)
            
            # Handle pricing decisions
            if decisions.get("prices"):
                console.print(f"💰 [bold yellow]Scrooge's PRICING WARFARE:[/bold yellow]")
                price_results = self.store.set_prices(decisions["prices"])
                competitor_prices = status.get('competitor_prices', {})
                
                for product, result in price_results.items():
                    if "ERROR" in result:
                        console.print(f"❌ {result}", style="red")
                    else:
                        # Show competitive analysis for this pricing move
                        new_price = decisions["prices"][product]
                        competitor_price = competitor_prices.get(product, 0)
                        
                        if competitor_price > 0:
                            difference = new_price - competitor_price
                            if difference > 0:
                                competitive_note = f"[red](+${difference:.2f} vs competitor - RISKY!)[/red]"
                            else:
                                competitive_note = f"[green]({difference:.2f} vs competitor - STEALING CUSTOMERS!)[/green]"
                        else:
                            competitive_note = "[blue](no competition - maximize margin!)[/blue]"
                            
                        console.print(f"💎 {result} {competitive_note}")
            
            else:
                console.print("💰 [italic yellow]No pricing adjustments today - missing opportunities?[/italic yellow]")
            
            # Handle ordering decisions
            if decisions.get("orders"):
                console.print(f"📦 [bold green]Scrooge's ordering decisions:[/bold green] {decisions['orders']}")
                console.print("⚙️ [bold yellow]Processing the order...[/bold yellow]")
                order_results = self.store.process_orders(decisions["orders"])
                for product, result in order_results.items():
                    if "ERROR" in result:
                        console.print(f"❌ {result}", style="red")
                    else:
                        console.print(f"✅ {result}", style="green")
            
            if not decisions.get("prices") and not decisions.get("orders"):
                console.print("🤖 [italic]Scrooge decided not to make any changes today.[/italic]")
        except Exception as e:
            console.print(f"❌ [bold red]Coordination system error:[/bold red] {e}")  
            console.print("⚙️ [bold yellow]Using fallback decisions...[/bold yellow]")
            decisions = {"orders": {}, "prices": {}}
            self.last_coordination_result = {
                'mode': 'fallback',
                'decisions': [],
                'active_agents': ['system_fallback'],
                'error': str(e)
            }
        
        # Customers visit and buy
        console.print("⚙️ [bold yellow]Simulating customer rabble...[/bold yellow]")
        customers = self.store.simulate_customers()
        console.print(f"🛒 {len(customers)} customers visited today")
        
        # 🎯 Phase 1C: Display Customer Segment Analytics
        self.display_customer_segments(customers)
        
        # End day and get summary
        day_summary = self.store.end_day()
        self.day_summaries.append(day_summary)
        
        # 🔥 ULTRA-ENHANCED COMPETITOR INTELLIGENCE DISPLAY 🔥
        self.display_competitor_warfare(day_summary)
        
        # 🌍 Phase 2B: Display market conditions
        self.display_market_conditions(day_summary)
        
        # 🚨 Phase 2C: Display crisis events
        self.display_crisis_events(day_summary)
        
        # 🏭 Phase 2A: Display delivery results
        if day_summary.get('deliveries'):
            console.print("\n🚚 [bold green]DELIVERY RESULTS:[/bold green]")
            deliveries = day_summary['deliveries']
            
            # Display successful deliveries
            for delivery in deliveries.get('successful_deliveries', []):
                console.print(f"✅ {delivery['message']}", style="green")
            
            # Display failed deliveries
            for delivery in deliveries.get('failed_deliveries', []):
                console.print(f"❌ {delivery['message']}", style="red")
        
        # 💰 Phase 1D: Display payment obligations
        if day_summary.get('payment_status') and day_summary['payment_status'].get('message'):
            payment_msg = day_summary['payment_status']['message']
            if day_summary['payment_status'].get('success', True):
                console.print(f"💰 {payment_msg}", style="green")
            else:
                console.print(f"⚠️  {payment_msg}", style="yellow")

        # Display day results
        supply_chain_info = ""
        if day_summary.get('pending_deliveries', 0) > 0:
            supply_chain_info += f"\n🚚 Pending Deliveries: {day_summary['pending_deliveries']}"
        if day_summary.get('accounts_payable', 0) > 0:
            supply_chain_info += f"\n💳 Accounts Payable: ${day_summary['accounts_payable']:.2f}"
        
        # Phase 2A: Display spoilage reports
        if day_summary.get('spoilage_reports'):
            console.print("\n🍌 [bold red]SPOILAGE REPORT:[/bold red]")
            total_spoilage_loss = 0
            for spoilage in day_summary['spoilage_reports']:
                console.print(f"   🗑️ {spoilage['quantity']} {spoilage['product']} spoiled (-${spoilage['cost_lost']:.2f})")
                total_spoilage_loss += spoilage['cost_lost']
            console.print(f"   💸 [bold red]Total spoilage cost: ${total_spoilage_loss:.2f}[/bold red]")

        # Build spoilage info for summary
        spoilage_info = ""
        if day_summary.get('units_spoiled', 0) > 0:
            spoilage_info = f"\n🍌 Units Spoiled: {day_summary['units_spoiled']} (-${day_summary.get('spoilage_cost', 0):.2f})"

        console.print(Panel(
            f"""
💰 Revenue: ${day_summary['revenue']:.2f}
📈 Profit: ${day_summary['profit']:.2f}
🛒 Units Sold: {day_summary['units_sold']}
💵 Cash Balance: ${day_summary['cash_balance']:.2f}
📦 Inventory: {day_summary['inventory_status']}{supply_chain_info}{spoilage_info}
""",
            title=f"Day {day_summary['day']-1} Accounting",
            border_style="green"
        ))
        
        # 🧠 Phase 3A: Display CEO Strategic Intelligence Dashboard
        if len(self.day_summaries) >= 2:  # Show analytics after at least 2 days of data
            try:
                self.display_analytics_dashboard()
            except Exception as e:
                console.print(f"🧠 [red]Analytics Dashboard Error: {e}[/red]")
        
        # 🎯 Phase 3B: Display Strategic Planning Dashboard
        if len(self.day_summaries) >= 3:  # Show strategic planning after at least 3 days of data
            try:
                self.display_strategic_planning_dashboard()
            except Exception as e:
                console.print(f"🎯 [red]Strategic Planning Dashboard Error: {e}[/red]")
        
        # 🚀 Phase 3D: Display Growth & Expansion Intelligence Dashboard
        if len(self.day_summaries) >= 2:  # Show growth analysis after at least 2 days of data
            try:
                self.display_growth_dashboard()
            except Exception as e:
                console.print(f"🚀 [red]Growth Dashboard Error: {e}[/red]")
        
        # 🎯 Phase 5A.4: Display Simplified Coordination Dashboard
        try:
            self.display_simplified_coordination_dashboard(getattr(self, 'last_coordination_result', {}))
        except Exception as e:
            console.print(f"🎯 [red]Coordination Dashboard Error: {e}[/red]")
        
        return day_summary
    
    def display_customer_segments(self, customers):
        """🎯 Phase 1C: Display customer segment analytics"""
        from src.core.models import CustomerType
        
        # Count customers by type
        price_sensitive = [c for c in customers if c.customer_type == CustomerType.PRICE_SENSITIVE]
        brand_loyal = [c for c in customers if c.customer_type == CustomerType.BRAND_LOYAL]
        
        # Calculate segment metrics
        price_sensitive_revenue = sum(c.total_spent for c in price_sensitive)
        brand_loyal_revenue = sum(c.total_spent for c in brand_loyal)
        price_sensitive_units = sum(len(c.products) for c in price_sensitive)
        brand_loyal_units = sum(len(c.products) for c in brand_loyal)
        
        # Create customer analytics table
        segment_table = Table(title="🎯 CUSTOMER SEGMENT ANALYTICS", show_header=True, header_style="bold cyan")
        segment_table.add_column("Segment", style="white", width=15)
        segment_table.add_column("Customers", style="green", width=10)
        segment_table.add_column("Revenue", style="yellow", width=10)
        segment_table.add_column("Units", style="blue", width=6)
        segment_table.add_column("Avg/Customer", style="magenta", width=12)
        segment_table.add_column("Behavior", style="white")
        
        # Price-sensitive row
        ps_avg = price_sensitive_revenue / max(1, len(price_sensitive))
        segment_table.add_row(
            "💰 Price-Sensitive",
            str(len(price_sensitive)),
            f"${price_sensitive_revenue:.2f}",
            str(price_sensitive_units),
            f"${ps_avg:.2f}",
            "Bargain hunters 🎯"
        )
        
        # Brand-loyal row
        bl_avg = brand_loyal_revenue / max(1, len(brand_loyal))
        segment_table.add_row(
            "❤️ Brand-Loyal",
            str(len(brand_loyal)),
            f"${brand_loyal_revenue:.2f}",
            str(brand_loyal_units),
            f"${bl_avg:.2f}",
            "Quality focused 💎"
        )
        
        # Totals row
        total_revenue = price_sensitive_revenue + brand_loyal_revenue
        total_units = price_sensitive_units + brand_loyal_units
        total_customers = len(price_sensitive) + len(brand_loyal)
        total_avg = total_revenue / max(1, total_customers)
        
        segment_table.add_row(
            "[bold]📊 TOTAL",
            f"[bold]{total_customers}",
            f"[bold]${total_revenue:.2f}",
            f"[bold]{total_units}",
            f"[bold]${total_avg:.2f}",
            "[bold]Mixed market"
        )
        
        console.print(segment_table)
        
        # Strategic insights
        if total_customers > 0:
            ps_percentage = (len(price_sensitive) / total_customers) * 100
            bl_percentage = (len(brand_loyal) / total_customers) * 100
            
            insights = []
            if ps_percentage > 70:
                insights.append("🎯 [yellow]Market is heavily price-sensitive - focus on competitive pricing![/yellow]")
            elif bl_percentage > 50:
                insights.append("❤️ [cyan]Strong brand loyalty - premium pricing opportunities![/cyan]")
            
            if ps_avg > bl_avg * 1.2:
                insights.append("💡 [green]Price-sensitive customers spending more - great deals working![/green]")
            elif bl_avg > ps_avg * 1.3:
                insights.append("💎 [magenta]Brand-loyal customers are your profit engine![/magenta]")
            
            if insights:
                console.print("📈 [bold]Strategic Insights:[/bold]")
                for insight in insights:
                    console.print(f"   {insight}")
    
    def chat_with_scrooge(self):
        """Chat with Scrooge about his miserly decisions"""
        console.print("💬 Speak with Scrooge (type 'quit' to exit)")
        while True:
            user_input = Prompt.ask("You")
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            # Simple responses for now
            if "decision" in user_input.lower() or "why" in user_input.lower():
                explanation = self.scrooge.explain_decision({})
                console.print(f" Scrooge: {explanation}")
            elif "memory" in user_input.lower() or "history" in user_input.lower():
                history = self.scrooge.get_memory_summary()
                console.print(f" Scrooge: {history}")
            else:
                console.print(" Scrooge: Bah! Humbug! I am busy counting my money. What do you want? Ask about my decisions or my memory, but be quick about it!")

    def display_performance_trends(self):
        """Display performance trends over recent days"""
        recent_days = self.day_summaries[-5:]  # Last 5 days max
        
        # Create trends table
        trends_table = Table(title="📊 5-DAY PERFORMANCE TRENDS", show_header=True, header_style="bold magenta")
        trends_table.add_column("Day", style="cyan", width=6)
        trends_table.add_column("Profit", style="green", width=8)
        trends_table.add_column("Revenue", style="yellow", width=9)
        trends_table.add_column("Units", style="blue", width=6)
        trends_table.add_column("War", style="red", width=8)
        trends_table.add_column("Status", style="white")
        
        for day_summary in recent_days:
            day_num = day_summary['day'] - 1
            profit = day_summary['profit']
            revenue = day_summary['revenue']
            units = day_summary['units_sold']
            intensity = day_summary.get('price_war_intensity', 0)
            
            # Profit trend indicator
            profit_display = f"${profit:.0f}"
            if profit > 20:
                profit_display += " 📈"
            elif profit < 10:
                profit_display += " 📉"
            
            # War intensity display
            war_display = f"{intensity}/10"
            if intensity >= 8:
                war_display = f"🔥 {intensity}"
            elif intensity >= 5:
                war_display = f"⚔️ {intensity}"
            elif intensity >= 3:
                war_display = f"🥊 {intensity}"
            
            # Overall status
            if profit > 20 and units > 20:
                status = "🟢 STRONG"
            elif profit < 10 or units < 10:
                status = "🔴 WEAK"
            else:
                status = "🟡 OKAY"
            
            trends_table.add_row(
                f"D{day_num}",
                profit_display,
                f"${revenue:.0f}",
                str(units),
                war_display,
                status
            )
        
        console.print(trends_table)

    def display_competitor_warfare(self, day_summary):
        """🔥 Display enhanced competitor intelligence and warfare status 🔥"""
        competitor_reactions = day_summary.get('competitor_reactions', [])
        intensity = day_summary.get('price_war_intensity', 0)
        competitor_strategy = getattr(self.store, 'competitor_strategy', 'UNKNOWN')
        revenge_mode = getattr(self.store, 'competitor_revenge_mode', False)
        
        # War intensity display with dramatic flair
        if intensity >= 9:
            intensity_display = "🌋 APOCALYPTIC (10/10)"
            intensity_color = "bright_red"
        elif intensity >= 8:
            intensity_display = f"💀 NUCLEAR ({intensity}/10)"
            intensity_color = "red"
        elif intensity >= 6:
            intensity_display = f"🔥 INFERNO ({intensity}/10)"
            intensity_color = "red"
        elif intensity >= 4:
            intensity_display = f"⚔️ HEATED ({intensity}/10)"
            intensity_color = "yellow"
        elif intensity >= 2:
            intensity_display = f"🥊 TENSE ({intensity}/10)"
            intensity_color = "yellow"
        elif intensity > 0:
            intensity_display = f"👀 WATCHFUL ({intensity}/10)"
            intensity_color = "blue"
        else:
            intensity_display = "😴 PEACEFUL (0/10)"
            intensity_color = "green"
        
        # Strategy display with personality
        strategy_emojis = {
            "AGGRESSIVE": "💥 AGGRESSIVE",
            "PREDATORY": "🐺 PREDATORY", 
            "PSYCHOLOGICAL": "🎭 PSYCHOLOGICAL",
            "DEFENSIVE": "🛡️ DEFENSIVE",
            "BALANCED": "⚖️ BALANCED"
        }
        strategy_display = strategy_emojis.get(competitor_strategy, f"❓ {competitor_strategy}")
        
        # Revenge mode indicator
        revenge_display = "😈 REVENGE MODE ACTIVE!" if revenge_mode else ""
        
        if competitor_reactions:
            # Major competitor actions - show with full drama
            console.print(f"⚔️ [bold red]COMPETITOR WARFARE REPORT![/bold red]")
            console.print(f"   📊 War Intensity: [{intensity_color}]{intensity_display}[/{intensity_color}]")
            console.print(f"   🎯 Strategy: [bold cyan]{strategy_display}[/bold cyan]")
            if revenge_mode:
                console.print(f"   💀 [bold red blink]{revenge_display}[/bold red blink]")
            
            console.print(f"   🚨 [bold yellow]Today's Competitor Moves:[/bold yellow]")
            for reaction in competitor_reactions:
                console.print(f"      ⚡ {reaction}")
                
            # Tactical analysis
            if intensity >= 8:
                console.print("   📈 [bold red]ANALYSIS: Competitor is in full war mode! Expect relentless attacks![/bold red]")
            elif intensity >= 6:
                console.print("   📈 [bold yellow]ANALYSIS: Intense price war! Competitor is fighting hard![/bold yellow]")
            elif intensity >= 4:
                console.print("   📈 [cyan]ANALYSIS: Active competition - stay sharp![/cyan]")
            else:
                console.print("   📈 [green]ANALYSIS: Competitor responded but war is manageable.[/green]")
                
        elif intensity > 0:
            # Tension without moves - still show intelligence
            console.print(f"⚔️ [italic]Competitive tension lingers... [{intensity_color}]{intensity_display}[/{intensity_color}] | Strategy: [cyan]{strategy_display}[/cyan]")
            if revenge_mode:
                console.print(f"   💀 [bold red]{revenge_display}[/bold red] - They're planning something...")
        else:
            # Peace... for now
            if hasattr(self.store, 'days_since_last_attack') and self.store.days_since_last_attack >= 3:
                console.print("😴 [italic green]Competitor seems calm... suspiciously calm...[/italic green]")

    def display_market_conditions(self, day_summary):
        """🌍 Phase 2B: Display market conditions and seasonal effects"""
        market_event = day_summary.get('market_event')
        if not market_event:
            return
        
        console.print("\n🌍 [bold blue]MARKET CONDITIONS:[/bold blue]")
        
        # Season and weather display
        season_icons = {
            "spring": "🌸",
            "summer": "☀️",
            "fall": "🍂", 
            "winter": "❄️"
        }
        
        weather_icons = {
            "normal": "🌤️",
            "heat_wave": "🔥",
            "cold_snap": "🥶",
            "rainy_day": "🌧️",
            "perfect_weather": "☀️"
        }
        
        economic_icons = {
            "normal": "📊",
            "boom": "📈",
            "recession": "📉",
            "recovery": "🔄"
        }
        
        season_icon = season_icons.get(market_event['season'], "🌍")
        weather_icon = weather_icons.get(market_event['weather'], "🌤️")
        economic_icon = economic_icons.get(market_event['economic_condition'], "📊")
        
        # Display market conditions
        console.print(f"   {season_icon} Season: [bold]{market_event['season'].title()}[/bold]")
        console.print(f"   {weather_icon} Weather: [bold]{market_event['weather'].replace('_', ' ').title()}[/bold]")
        if market_event['holiday'] != "none":
            console.print(f"   🎉 Holiday: [bold yellow]{market_event['holiday'].replace('_', ' ').title()}[/bold yellow]")
        console.print(f"   {economic_icon} Economy: [bold]{market_event['economic_condition'].title()}[/bold]")
        console.print(f"   📊 Market Demand: [bold cyan]{market_event['demand_multiplier']:.1f}x[/bold cyan]")
        
        # Display market description
        if market_event.get('description'):
            console.print(f"   📝 [italic]{market_event['description']}[/italic]")
        
        # Seasonal product insights
        self.display_seasonal_insights(market_event)
    
    def display_seasonal_insights(self, market_event):
        """🎯 Phase 2B: Display seasonal insights for product demand"""
        # Import here to avoid circular import
        from src.engines.market_events_engine import MarketEventsEngine
        from src.core.models import PRODUCTS, MarketEvent, Season, WeatherEvent, Holiday, EconomicCondition
        
        market_engine = MarketEventsEngine()
        
        # Convert dict back to MarketEvent object for processing
        event_obj = MarketEvent(
            day=market_event.get('day', 1),
            season=Season(market_event['season']),
            weather=WeatherEvent(market_event['weather']),
            holiday=Holiday(market_event['holiday']),
            economic_condition=EconomicCondition(market_event['economic_condition']),
            description=market_event['description'],
            demand_multiplier=market_event['demand_multiplier']
        )
        
        # Calculate demand multipliers for all products
        product_demands = {}
        for product_name in PRODUCTS.keys():
            multiplier = market_engine.get_product_demand_multiplier(product_name, event_obj)
            product_demands[product_name] = multiplier
        
        # Find products with high and low seasonal demand
        high_demand = [(name, mult) for name, mult in product_demands.items() if mult >= 1.3]
        low_demand = [(name, mult) for name, mult in product_demands.items() if mult <= 0.7]
        
        if high_demand:
            high_demand.sort(key=lambda x: x[1], reverse=True)
            console.print(f"   📈 [green]HIGH DEMAND: {', '.join([f'{name} ({mult:.1f}x)' for name, mult in high_demand[:3]])}[/green]")
        
        if low_demand:
            low_demand.sort(key=lambda x: x[1])
            console.print(f"   📉 [red]LOW DEMAND: {', '.join([f'{name} ({mult:.1f}x)' for name, mult in low_demand[:3]])}[/red]")
    
    def display_analytics_dashboard(self):
        """🧠 Phase 3A: Display strategic analytics and CEO intelligence"""
        try:
            # Get strategic insights
            insights = self.store.get_strategic_insights()
            
            # Get performance analysis
            performance = self.store.get_performance_analysis(7)
            
            analytics_content = ""
            
            # Performance metrics (if available)
            if performance.get('error') is None:
                avg_performance = performance.get('average_performance', {})
                trends = performance.get('trends', {})
                
                analytics_content += f"""📊 [bold]PERFORMANCE SCORE:[/bold] {avg_performance.get('overall_score', 0):.1f}/100
🎯 [bold]COMPETITIVE POSITION:[/bold] {avg_performance.get('competitive_position', 0):.1f}/100
💰 [bold]PROFIT MARGIN:[/bold] {avg_performance.get('profit_margin', 0):.1f}%
📈 [bold]TREND:[/bold] {trends.get('direction', 'Unknown').title()} ({trends.get('change', 0):+.1f})
"""
            else:
                analytics_content += "📊 [italic]Performance metrics: Gathering baseline data...[/italic]\n"
            
            # Competitive intelligence
            competitive_intel = insights.get('competitive_intelligence', {})
            threat_level = competitive_intel.get('competitive_threat_level', 0)
            if threat_level > 7:
                threat_status = "🔥 CRITICAL"
            elif threat_level > 4:
                threat_status = "⚠️ HIGH"
            elif threat_level > 2:
                threat_status = "🟡 MODERATE"
            else:
                threat_status = "🟢 LOW"
            
            analytics_content += f"\n🛡️ [bold]COMPETITIVE THREAT:[/bold] {threat_status} ({threat_level}/10)"
            
            # Strategic recommendations
            recommendations = insights.get('strategic_recommendations', [])
            if recommendations:
                analytics_content += f"\n\n🎯 [bold]STRATEGIC RECOMMENDATIONS:[/bold]"
                for rec in recommendations[:3]:  # Show top 3
                    analytics_content += f"\n   • {rec}"
            
            # Optimization opportunities  
            opportunities = insights.get('optimization_opportunities', [])
            if opportunities:
                analytics_content += f"\n\n💡 [bold]OPTIMIZATION OPPORTUNITIES:[/bold]"
                for opp in opportunities[:3]:  # Show top 3
                    analytics_content += f"\n   • {opp}"
            
            # Risk warnings
            risks = insights.get('risk_warnings', [])
            if risks:
                analytics_content += f"\n\n🚨 [bold]RISK ALERTS:[/bold]"
                for risk in risks[:2]:  # Show top 2
                    analytics_content += f"\n   • {risk}"
            
            # Learning summary
            learnings = insights.get('learning_summary', [])
            if learnings:
                analytics_content += f"\n\n📚 [bold]KEY LEARNINGS:[/bold]"
                for learning in learnings[:2]:  # Show top 2
                    analytics_content += f"\n   • {learning}"
            
            # Performance trends from insights
            perf_trends = insights.get('performance_trends', {})
            if perf_trends.get('trend') != 'insufficient_data':
                analytics_content += f"\n\n📈 [bold]STRATEGIC TREND:[/bold] {perf_trends.get('trend', 'Unknown').title()}"
            
            console.print(Panel(
                analytics_content.strip(),
                title="🧠 CEO STRATEGIC INTELLIGENCE",
                border_style="cyan",
                padding=(0, 1)
            ))
            
        except Exception as e:
            # Analytics not ready yet or error occurred
            console.print(f"🧠 [red]Strategic Intelligence Error: {str(e)}[/red]")
    
    def display_strategic_planning_dashboard(self):
        """🎯 Phase 3B: Display strategic planning recommendations"""
        try:
            # Get strategic planning data
            inventory_opt = self.store.get_inventory_optimization()
            promotions = self.store.get_promotional_opportunities()
            seasonal = self.store.get_seasonal_preparation()
            categories = self.store.get_category_analysis()
            
            planning_content = ""
            
            # Inventory optimization summary
            inv_summary = inventory_opt.get('summary', {})
            critical_reorders = inv_summary.get('critical_reorders', 0)
            overstock_items = inv_summary.get('overstock_items', 0)
            
            if critical_reorders > 0 or overstock_items > 0:
                planning_content += f"📦 [bold]INVENTORY OPTIMIZATION:[/bold]\n"
                if critical_reorders > 0:
                    planning_content += f"   🚨 {critical_reorders} critical reorders needed\n"
                if overstock_items > 0:
                    planning_content += f"   📉 {overstock_items} overstocked items to reduce\n"
                planning_content += f"   💰 Daily carrying cost: ${inv_summary.get('total_carrying_cost', 0):.2f}\n"
            
            # Promotional opportunities
            promo_summary = promotions.get('summary', {})
            slow_movers = promo_summary.get('slow_movers', 0)
            if slow_movers > 0:
                planning_content += f"\n🎯 [bold]PROMOTIONAL OPPORTUNITIES:[/bold]\n"
                planning_content += f"   📉 {slow_movers} slow-moving items identified\n"
                potential_roi = promo_summary.get('total_potential_roi', 0)
                if potential_roi > 0:
                    planning_content += f"   💎 Potential ROI: {potential_roi:.1f}%\n"
                priority_items = promo_summary.get('priority_items', [])
                if priority_items:
                    planning_content += f"   🎪 Priority items: {', '.join(priority_items[:3])}\n"
            
            # Seasonal preparation
            seasonal_summary = seasonal.get('summary', {})
            critical_preps = seasonal_summary.get('critical_preparations', 0)
            if critical_preps > 0:
                planning_content += f"\n🌍 [bold]SEASONAL PREPARATION:[/bold]\n"
                next_season = seasonal_summary.get('next_season', 'unknown')
                planning_content += f"   🌟 Preparing for {next_season.title()} season\n"
                planning_content += f"   🚨 {critical_preps} critical preparations needed\n"
                priority_products = seasonal_summary.get('priority_products', [])
                if priority_products:
                    planning_content += f"   📈 Priority products: {', '.join(priority_products[:3])}\n"
            
            # Category analysis
            category_summary = categories.get('summary', {})
            best_category = category_summary.get('best_category', 'none')
            if best_category != 'none':
                planning_content += f"\n📊 [bold]CATEGORY INTELLIGENCE:[/bold]\n"
                planning_content += f"   🏆 Best performing: {best_category.title()}\n"
                avg_margin = category_summary.get('avg_profit_margin', 0)
                planning_content += f"   💰 Average margin: {avg_margin:.1f}%\n"
                
                growing = category_summary.get('growing_categories', [])
                declining = category_summary.get('declining_categories', [])
                if growing:
                    planning_content += f"   📈 Growing: {', '.join(growing)}\n"
                if declining:
                    planning_content += f"   📉 Declining: {', '.join(declining)}\n"
            
            # Display dashboard if there's content
            if planning_content.strip():
                console.print(Panel(
                    planning_content.strip(),
                    title="🎯 STRATEGIC PLANNING DASHBOARD",
                    border_style="blue",
                    padding=(0, 1)
                ))
            else:
                console.print("🎯 [italic blue]Strategic Planning: All systems optimized[/italic blue]")
                
        except Exception as e:
            console.print(f"🎯 [red]Strategic Planning Error: {str(e)}[/red]")
    
    def display_learning_dashboard(self):
        """🧠 Phase 3C: Display learning and adaptation intelligence"""
        try:
            # Get learning insights
            learning_data = self.store.get_learning_insights()
            
            learning_content = ""
            
            # Learning summary stats
            summary = learning_data.get('learning_summary', {})
            if summary:
                learning_content += f"🧠 [bold]LEARNING INTELLIGENCE STATUS:[/bold]\n"
                learning_content += f"   📊 Customer evolution patterns: {summary.get('customer_evolution', 0)}\n"
                learning_content += f"   📈 Product trends tracked: {summary.get('trend_products_tracked', 0)}\n"
                learning_content += f"   💰 Price experiments: {summary.get('price_experiments', 0)}\n"
                learning_content += f"   🎯 Adaptive strategies: {summary.get('adaptive_strategies', 0)}\n"
                learning_content += f"   📚 Strategy patterns: {summary.get('strategy_patterns', 0)}\n"
            
            # High priority learning insights
            high_priority = learning_data.get('high_priority_insights', [])
            if high_priority:
                learning_content += f"\n🚨 [bold]CRITICAL LEARNING INSIGHTS:[/bold]\n"
                for insight in high_priority[-3:]:  # Last 3 insights
                    learning_content += f"   • {insight}\n"
            
            # Get specific learning analyses
            customer_analysis = self.store.get_adaptive_customer_analysis()
            if customer_analysis.get('market_alert'):
                learning_content += f"\n🎯 [bold]CUSTOMER INTELLIGENCE:[/bold]\n"
                learning_content += f"   📊 {customer_analysis['current_segments']}\n"
                learning_content += f"   📈 Shift: {customer_analysis['baseline_shift']}\n"
                if customer_analysis['market_alert']:
                    learning_content += f"   ⚠️ {customer_analysis['market_alert']}\n"
                
                # Customer recommendations
                recommendations = customer_analysis.get('recommendations', [])
                if recommendations:
                    learning_content += f"   💡 Actions: {recommendations[0]}\n"
            
            # Product trend analysis
            trend_analysis = self.store.get_product_lifecycle_analysis()
            trends = trend_analysis.get('product_trends', {})
            if trends:
                trending_products = [(name, data) for name, data in trends.items() 
                                   if data['direction'] in ['rising', 'falling']]
                if trending_products:
                    learning_content += f"\n📈 [bold]PRODUCT LIFECYCLE INTELLIGENCE:[/bold]\n"
                    for product, data in trending_products[:3]:  # Top 3 trends
                        direction_emoji = "🚀" if data['direction'] == 'rising' else "📉"
                        learning_content += f"   {direction_emoji} {product}: {data['direction'].upper()} "
                        learning_content += f"({data['days_in_trend']} days, {data['lifecycle_stage']})\n"
            
            # Price elasticity intelligence  
            elasticity_data = self.store.get_price_elasticity_intelligence()
            elasticity_info = elasticity_data.get('price_elasticity', {})
            if elasticity_info:
                learning_content += f"\n💰 [bold]PRICE ELASTICITY WISDOM:[/bold]\n"
                for product, data in list(elasticity_info.items())[:3]:  # Top 3 products
                    sensitivity_emoji = "⚠️" if data['sensitivity'] == 'high' else "💎" if data['sensitivity'] == 'low' else "📊"
                    learning_content += f"   {sensitivity_emoji} {product}: {data['sensitivity'].upper()} elasticity "
                    learning_content += f"(confidence: {data['confidence']})\n"
            
            # Adaptive prompts summary
            adaptive_prompts = learning_data.get('adaptive_prompts', {})
            if adaptive_prompts:
                adaptive_count = len([p for p in adaptive_prompts.values() if p.strip()])
                if adaptive_count > 0:
                    learning_content += f"\n🔄 [bold]ADAPTIVE INTELLIGENCE:[/bold] {adaptive_count} dynamic strategy adjustments active\n"
            
            # Display learning results from daily summary
            if hasattr(self, 'day_summaries') and self.day_summaries:
                latest_day = self.day_summaries[-1]
                learning_results = latest_day.get('learning_results', {})
                
                if learning_results:
                    # Customer learning from daily results
                    customer_learning = learning_results.get('customer_learning', {})
                    segment_shift = customer_learning.get('segment_shift', 0)
                    if abs(segment_shift) > 0.1:  # 10% shift threshold
                        shift_emoji = "📈" if segment_shift > 0 else "📉"
                        learning_content += f"\n{shift_emoji} [bold]LIVE CUSTOMER SHIFT:[/bold] "
                        learning_content += f"{segment_shift:+.1%} from baseline market composition\n"
                    
                    # Live trend analysis
                    trend_analysis_live = learning_results.get('trend_analysis', {})
                    if trend_analysis_live:
                        learning_content += f"\n📊 [bold]LIVE TRENDS:[/bold] "
                        trend_items = [f"{product} {info}" for product, info in trend_analysis_live.items()]
                        learning_content += f"{', '.join(trend_items[:3])}\n"
                    
                    # Learning insights from today
                    daily_insights = learning_results.get('learning_insights', [])
                    if daily_insights:
                        learning_content += f"\n💡 [bold]TODAY'S INSIGHTS:[/bold]\n"
                        for insight in daily_insights[:2]:  # Top 2 insights
                            learning_content += f"   • {insight}\n"
            
            # Display learning dashboard if there's content
            if learning_content.strip():
                console.print(Panel(
                    learning_content.strip(),
                    title="🧠 LEARNING & ADAPTATION INTELLIGENCE",
                    border_style="magenta",
                    padding=(0, 1)
                ))
            else:
                console.print("🧠 [italic magenta]Learning System: Gathering behavioral data...[/italic magenta]")
                
        except Exception as e:
            console.print(f"🧠 [red]Learning Intelligence Error: {str(e)}[/red]")
    
    def display_growth_dashboard(self):
        """🚀 Phase 3D: Display Growth & Expansion Intelligence"""
        try:
            # Get comprehensive growth analysis
            growth_data = self.store.get_comprehensive_growth_analysis()
            
            growth_content = ""
            
            # Business stage and strategy
            growth_strategy = growth_data.get('growth_strategy', {})
            if growth_strategy:
                stage = growth_strategy.get('business_stage', 'Unknown')
                focus = growth_strategy.get('primary_focus', 'Assessment needed')
                cash = growth_strategy.get('cash_position', 0)
                profit = growth_strategy.get('profit_level', 0)
                
                growth_content += f"🚀 [bold]GROWTH INTELLIGENCE STATUS:[/bold]\n"
                growth_content += f"   🏢 Business Stage: {stage}\n"
                growth_content += f"   🎯 Current Focus: {focus}\n"
                growth_content += f"   💰 Cash Position: ${cash:.2f}\n"
                growth_content += f"   📈 Daily Profit: ${profit:.2f}\n"
            
            # New Product Opportunities
            product_data = growth_data.get('products', {})
            top_products = product_data.get('top_opportunities', [])
            if top_products:
                growth_content += f"\n🧪 [bold]NEW PRODUCT OPPORTUNITIES:[/bold]\n"
                for product in top_products[:3]:  # Top 3 products
                    name = product.get('product', 'Unknown')
                    score = product.get('opportunity_score', 0)
                    monthly_profit = product.get('monthly_profit', 0)
                    recommendation = product.get('recommendation', 'Unknown')
                    
                    score_emoji = "🔥" if score >= 0.7 else "⭐" if score >= 0.5 else "📋"
                    growth_content += f"   {score_emoji} {name}: Score {score:.1f}, ${monthly_profit:.0f}/month - {recommendation}\n"
            
            # Service Expansion Opportunities  
            service_data = growth_data.get('services', {})
            top_services = service_data.get('top_opportunities', [])
            if top_services:
                growth_content += f"\n💼 [bold]SERVICE EXPANSION OPPORTUNITIES:[/bold]\n"
                for service in top_services[:3]:  # Top 3 services
                    name = service.get('service', 'Unknown')
                    setup_cost = service.get('setup_cost', 0)
                    monthly_profit = service.get('monthly_profit', 0)
                    roi_months = service.get('roi_months', 999)
                    
                    roi_emoji = "💎" if roi_months <= 6 else "📈" if roi_months <= 12 else "⏰"
                    growth_content += f"   {roi_emoji} {name}: ${setup_cost:.0f} setup, ${monthly_profit:.0f}/month, {roi_months:.1f}mo ROI\n"
            
            # Customer Retention Analysis
            retention_data = growth_data.get('retention', {})
            top_retention = retention_data.get('top_recommendation', {})
            if top_retention:
                program_name = top_retention.get('program', 'Unknown')
                setup_cost = top_retention.get('setup_cost', 0)
                monthly_benefit = top_retention.get('monthly_benefit', 0)
                roi_percentage = top_retention.get('roi_percentage', 0)
                
                growth_content += f"\n❤️ [bold]CUSTOMER RETENTION OPPORTUNITY:[/bold]\n"
                roi_emoji = "🔥" if roi_percentage >= 200 else "💎" if roi_percentage >= 100 else "📈"
                growth_content += f"   {roi_emoji} {program_name}: ${setup_cost:.0f} setup, ${monthly_benefit:.0f}/month benefit\n"
                growth_content += f"   💰 ROI: {roi_percentage:.0f}% annually\n"
            
            # Multi-Location Expansion
            expansion_data = growth_data.get('expansion', {})
            expansion_ready = expansion_data.get('expansion_ready', False)
            top_locations = expansion_data.get('top_opportunities', [])
            
            if expansion_ready and top_locations:
                growth_content += f"\n🏢 [bold]EXPANSION OPPORTUNITIES:[/bold]\n"
                for location in top_locations[:2]:  # Top 2 locations
                    area = location.get('location', 'Unknown')
                    setup_cost = location.get('setup_cost', 0)
                    annual_profit = location.get('projected_annual_profit', 0)
                    roi = location.get('roi_percentage', 0)
                    recommendation = location.get('recommendation', 'Unknown')
                    
                    location_emoji = "🌟" if roi >= 20 else "🏢" if roi >= 10 else "🔍"
                    growth_content += f"   {location_emoji} {area}: ${setup_cost:,.0f} setup, ${annual_profit:,.0f}/year\n"
                    growth_content += f"      ROI: {roi:.1f}% - {recommendation}\n"
            elif not expansion_ready:
                growth_content += f"\n🏢 [bold]EXPANSION STATUS:[/bold] Need stronger cash position and profitability\n"
            
            # Investment Summary
            analysis_date = growth_data.get('analysis_date', 0)
            if analysis_date:
                growth_content += f"\n📊 [bold]GROWTH ANALYSIS:[/bold] Day {analysis_date} comprehensive evaluation\n"
                
                # Quick recommendations based on business stage
                if growth_strategy.get('business_stage') == 'SURVIVAL':
                    growth_content += f"   🎯 Priority: Focus on core profitability before expansion\n"
                elif growth_strategy.get('business_stage') == 'GROWTH':
                    growth_content += f"   🎯 Priority: Add profitable products and basic services\n"
                elif growth_strategy.get('business_stage') == 'EXPANSION':
                    growth_content += f"   🎯 Priority: Customer retention and premium services\n"
            
            # Display growth dashboard if there's content
            if growth_content.strip():
                console.print(Panel(
                    growth_content.strip(),
                    title="🚀 GROWTH & EXPANSION INTELLIGENCE",
                    border_style="bright_green",
                    padding=(0, 1)
                ))
            else:
                console.print("🚀 [italic bright_green]Growth Intelligence: Analyzing expansion opportunities...[/italic bright_green]")
                
        except Exception as e:
            console.print(f"🚀 [red]Growth Intelligence Error: {str(e)}[/red]")

    def display_simplified_coordination_dashboard(self, coordination_result: Dict):
        """🎯 Phase 5A.4: Display simplified coordination insights"""
        
        console.print("\n" + "="*80)
        console.print("🎯 [bold cyan]SIMPLIFIED COORDINATION INTELLIGENCE[/bold cyan]")
        console.print("="*80)
        
        # Handle fallback/error case
        if coordination_result.get('mode') == 'fallback':
            console.print("⚠️ [red]COORDINATION SYSTEM ERROR - USING FALLBACK[/red]")
            console.print(f"   Error: {coordination_result.get('error', 'Unknown error')}")
            return
        
        # Operation mode display
        mode = coordination_result.get('mode', 'unknown')
        active_agents = coordination_result.get('active_agents', [])
        decisions = coordination_result.get('decisions', [])
        
        mode_icons = {
            'daily_operations': '🏪',
            'strategic_review': '📊',
            'crisis_management': '🚨'
        }
        
        mode_icon = mode_icons.get(mode, '📋')
        mode_name = mode.value.replace('_', ' ').title() if hasattr(mode, 'value') else str(mode).replace('_', ' ').title()
        
        console.print(f"🎯 [bold]OPERATION MODE:[/bold] {mode_icon} {mode_name}")
        console.print(f"👥 [bold]ACTIVE AGENTS:[/bold] {len(active_agents)} agents")
        
        # Agent status display
        agent_info = {
            'hermione': {'emoji': '📦', 'full_name': 'Hermione Granger', 'role': 'Inventory Manager'},
            'gekko': {'emoji': '💰', 'full_name': 'Gordon Gekko', 'role': 'Pricing Analyst'}, 
            'tyrion': {'emoji': '🏰', 'full_name': 'Tyrion Lannister', 'role': 'Strategic Planner'},
            'jack': {'emoji': '⚡', 'full_name': 'Jack Bauer', 'role': 'Crisis Manager'},
            'elle': {'emoji': '👩‍💼', 'full_name': 'Elle Woods', 'role': 'Customer Service'}
        }
        
        console.print(f"\n👥 [bold]AGENT STATUS:[/bold]")
        for agent_name in active_agents:
            agent = agent_info.get(agent_name, {'emoji': '🤖', 'full_name': agent_name, 'role': 'Unknown'})
            console.print(f"   ✅ {agent['emoji']} {agent['full_name']} ({agent['role']})")
        
        # Show removed/inactive agents
        all_agents = ['hermione', 'gekko', 'tyrion', 'jack', 'elle']
        inactive_agents = [a for a in all_agents if a not in active_agents]
        if inactive_agents:
            console.print(f"\n💤 [bold]INACTIVE AGENTS:[/bold]")
            for agent_name in inactive_agents:
                agent = agent_info.get(agent_name, {'emoji': '🤖', 'full_name': agent_name, 'role': 'Unknown'})
                if agent_name == 'elle':
                    status = "(Disabled - No customer interaction yet)"
                else:
                    status = "(Not needed today)"
                console.print(f"   ⭕ {agent['emoji']} {agent['full_name']} {status}")
        
        # Budget allocation (for inventory/crisis modes)
        budget_allocation = coordination_result.get('budget_allocation', {})
        if budget_allocation:
            console.print(f"\n💰 [bold]BUDGET ALLOCATION:[/bold]")
            total_budget = sum(v for v in budget_allocation.values() if v > 0)
            
            for agent, amount in budget_allocation.items():
                if amount > 0:
                    percentage = (amount / total_budget) * 100 if total_budget > 0 else 0
                    agent_display = agent.replace('_', ' ').title()
                    console.print(f"   💵 {agent_display}: ${amount:.2f} ({percentage:.1f}%)")
                elif agent == 'gekko':
                    console.print(f"   💼 Gekko (Pricing): $0.00 (Domain authority only)")
        
        # Decisions made
        console.print(f"\n📝 [bold]DECISIONS MADE:[/bold] {len(decisions)} total")
        if decisions:
            for i, decision in enumerate(decisions, 1):
                agent_role = decision.agent_role.value.replace('_', ' ').title()
                decision_type = decision.decision_type.replace('_', ' ').title()
                confidence = f"{decision.confidence:.1%}"
                priority = decision.priority
                
                priority_emoji = "🔥" if priority >= 8 else "⚡" if priority >= 6 else "📋"
                
                console.print(f"   {i}. {priority_emoji} {agent_role}: {decision_type}")
                console.print(f"      └─ Confidence: {confidence} | Priority: {priority}/10")
                console.print(f"      └─ {decision.reasoning[:70]}...")
        
        # Special guidance or crisis response
        guidance = coordination_result.get('guidance_provided')
        crisis_response = coordination_result.get('crisis_response')
        
        if guidance:
            console.print(f"\n🎯 [bold]STRATEGIC GUIDANCE PROVIDED:[/bold]")
            console.print(f"   📊 Performance Analysis: {guidance.get('performance_analysis', 'N/A')}")
            console.print(f"   📦 Inventory Guidance: {guidance.get('inventory_guidance', 'N/A')[:60]}...")
            console.print(f"   💰 Pricing Guidance: {guidance.get('pricing_guidance', 'N/A')[:60]}...")
        
        if crisis_response:
            console.print(f"\n🚨 [bold]CRISIS RESPONSE ACTIVATED:[/bold]")
            console.print(f"   ⚡ Crisis Type: {crisis_response.get('crisis_type', 'Unknown')}")
            console.print(f"   📊 Severity: {crisis_response.get('severity', 'Unknown').upper()}")
            console.print(f"   ⏰ Timeline: {crisis_response.get('timeline', 'Unknown')}")
        
        # Coordination efficiency metrics
        if hasattr(self, 'simplified_coordinator'):
            summary = self.simplified_coordinator.get_coordination_summary()
            
            console.print(f"\n📊 [bold]COORDINATION EFFICIENCY:[/bold]")
            console.print(f"   📅 Total Days: {summary.get('total_days', 0)}")
            console.print(f"   🏪 Daily Operations: {summary.get('daily_operations', 0)}")
            console.print(f"   📊 Strategic Reviews: {summary.get('strategic_reviews', 0)}")
            console.print(f"   🚨 Crisis Interventions: {summary.get('crisis_interventions', 0)}")
            console.print(f"   📈 Efficiency: {summary.get('coordination_efficiency', 'N/A')}")
            console.print(f"   👥 Avg Agents/Day: {summary.get('average_agents_per_day', 0)}")
        
        # Performance correlation
        if len(self.day_summaries) >= 2:
            recent_profit = self.day_summaries[-1]['profit']
            previous_profit = self.day_summaries[-2]['profit']
            profit_change = ((recent_profit - previous_profit) / previous_profit) * 100 if previous_profit > 0 else 0
            
            performance_trend = "📈 IMPROVING" if profit_change > 5 else "📉 DECLINING" if profit_change < -5 else "📊 STABLE"
            
            console.print(f"\n📈 [bold]PERFORMANCE IMPACT:[/bold]")
            console.print(f"   💰 Profit Trend: {performance_trend} ({profit_change:+.1f}%)")
            console.print(f"   🎯 Coordination Mode: {mode_name}")
            
            # Efficiency insight
            avg_agents = summary.get('average_agents_per_day', 5) if hasattr(self, 'simplified_coordinator') else 5
            if avg_agents <= 2.5:
                console.print(f"   ✅ [green]Efficient coordination with minimal agent overhead![/green]")
            elif avg_agents <= 3.5:
                console.print(f"   🟡 [yellow]Moderate coordination complexity[/yellow]")
            else:
                console.print(f"   🔴 [red]High coordination overhead - consider simplification[/red]")
        
        console.print("="*80)

@app.command()
def run(days: int = 7, interactive: bool = False): #Default to False for non-interactive mode
    """Run the store simulation for specified number of days"""
    console.print("🏪 Welcome to Scrooge's Miserly Management Simulation!")
    console.print("🎯 Phase 1C: Customer Segmentation & Advanced Warfare!")
    console.print("💰 Now Scrooge must balance competitive warfare with customer psychology!")
    console.print("👥 60% Price-Sensitive vs 40% Brand-Loyal customers!")
    console.print()
    
    sim = StoreSimulation()
    
    if interactive:
        sim.display_status()
        
        for day in range(1, days + 1):
            if day > 1:
                console.print("\n" + "="*50)
                input("Press Enter to continue to the next day, and don't dawdle!")
            
            sim.run_single_day()
            sim.display_status()
            
            # Offer to chat with Scrooge
            if Prompt.ask("Speak with Scrooge?", choices=["y", "n"], default="n") == "y":
                sim.chat_with_scrooge()
    else:
        # Fast simulation
        for day in range(1, days + 1):
            summary = sim.run_single_day()
            console.print(f"Day {day}: Profit ${summary['profit']:.2f}, Cash ${summary['cash_balance']:.2f}")
    
    # Final summary
    total_profit = sum(s['profit'] for s in sim.day_summaries)
    final_cash = sim.day_summaries[-1]['cash_balance']
    
    console.print(f"\n🎯 Final Accounting after {days} days:")
    console.print(f"💰 Total Profit: ${total_profit:.2f}")
    console.print(f"💵 Final Cash: ${final_cash:.2f}")
    console.print(f"📊 Final Verdict: {'✅ A TRIUMPH OF FRUGALITY!' if total_profit > 0 else '❌ BAH, HUMBUG! A MERE LOSS!'}")

@app.command()
def test():
    """Test the basic components"""
    console.print("🧪 Testing the counting house...")
    
    # Test store engine
    store = StoreEngine()
    console.print("✅ Store engine initialized")
    
    # Test customer simulation
    customers = store.simulate_customers()
    console.print(f"✅ Customer simulation: {len(customers)} customers appeared")
    
    # Test LLM agent
    scrooge = ScroogeAgent()
    console.print("✅ Scrooge agent initialized")
    
    status = store.get_status()
    console.print(f"✅ Store status: {status}")
    
    console.print("🎉 All components are in order! Now, back to making money.")

@app.command()
def web():
    """🌐 Launch the Phase 5A.4 Web Dashboard"""
    console.print("\n🚀 [bold blue]Starting ShelfMind Web Dashboard...[/bold blue]")
    console.print("🌐 [bold green]Phase 5A.4: Interactive Web Interface for Character-Controlled Business AI[/bold green]")
    console.print("=" * 80)
    console.print("📊 [bold]Dashboard URL:[/bold] http://localhost:8000")
    console.print("🔌 [bold]WebSocket URL:[/bold] ws://localhost:8000/ws")
    console.print("📡 [bold]API Docs:[/bold] http://localhost:8000/docs")
    console.print("=" * 80)
    console.print("💡 [bold]Features:[/bold]")
    console.print("   • Real-time simulation monitoring with live updates")
    console.print("   • Character agent status and decision tracking")
    console.print("   • Interactive simulation controls (start/stop/reset)")
    console.print("   • Complete visibility of all 25 specialized tools")
    console.print("   • Live financial metrics and inventory tracking")
    console.print("   • Crisis management and emergency response monitoring")
    console.print("   • Historical performance analytics and trends")
    console.print("=" * 80)
    console.print("🎭 [bold]Revolutionary Character Control:[/bold]")
    console.print("   👩‍🔬 [cyan]HERMIONE[/cyan] - Inventory Management with 5 analytical tools")
    console.print("   💼 [yellow]GEKKO[/yellow] - Pricing Strategy with 5 market warfare tools")
    console.print("   💖 [magenta]ELLE[/magenta] - Customer Psychology with 5 relationship tools")
    console.print("   🎯 [green]TYRION[/green] - Strategic Planning with 5 intelligence tools")
    console.print("   🚨 [red]JACK[/red] - Crisis Management with 5 emergency response tools")
    console.print("=" * 80)
    console.print("\n🔥 [bold red]This is the world's first Character-Controlled Business AI with full tool visibility![/bold red]")
    console.print("🌟 [bold yellow]Professional-grade dashboard ready for commercial demonstration[/bold yellow]")
    console.print("\n🚀 [italic]Starting web server...[/italic]")
    
    try:
        import uvicorn
        import sys
        from pathlib import Path
        
        # Add src to path for imports
        src_path = Path(__file__).parent / "src"
        sys.path.insert(0, str(src_path))
        
        # Import and run the FastAPI app
        from src.web.api import app as web_app
        
        uvicorn.run(
            web_app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
    except ImportError as e:
        console.print(f"❌ [red]Import error: {e}[/red]")
        console.print("💡 Make sure web dependencies are installed: [yellow]pip install fastapi uvicorn websockets jinja2 python-multipart aiofiles[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"❌ [red]Failed to start web server: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 