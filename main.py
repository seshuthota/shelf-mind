#!/usr/bin/env python3

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
import time
import json

from store_engine import StoreEngine
from scrooge_agent import ScroogeAgent
from models import PRODUCTS

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
        
        # Scrooge makes decision
        console.print("🤖 [bold blue]Scrooge is pondering his next move...[/bold blue]")
        try:
            decisions = self.scrooge.make_daily_decision(status, yesterday_summary)
            
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
            console.print(f"❌ [bold red]Scrooge is having a moment of weakness:[/bold red] {e}")  
            console.print("⚙️ [bold yellow]Using fallback ordering... Bah, humbug![/bold yellow]")
            decisions = {"orders": {}, "prices": {}}
        
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
        
        return day_summary
    
    def display_customer_segments(self, customers):
        """🎯 Phase 1C: Display customer segment analytics"""
        from models import CustomerType
        
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
        from market_events_engine import MarketEventsEngine
        from models import PRODUCTS, MarketEvent, Season, WeatherEvent, Holiday, EconomicCondition
        
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

if __name__ == "__main__":
    app() 