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
        self.store = StoreEngine(starting_cash=100.0)
        self.scrooge = ScroogeAgent(provider="openai")  # Change to "anthropic" if you prefer
        self.day_summaries = []
        self.previous_prices = {}  # Track price changes
        
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
        
        console.print(f"💰 Cash Balance: ${status['cash']:.2f}")
        if status.get('accounts_payable', 0) > 0:
            console.print(f"💳 Accounts Payable (NET-30): ${status['accounts_payable']:.2f}")
        
        if status['stockouts']:
            console.print(f"🚨 CRITICAL STOCKOUTS: {', '.join(status['stockouts'])}")
        
        # Show daily performance if available
        if self.day_summaries:
            last_summary = self.day_summaries[-1]
            profit_color = "green" if last_summary['profit'] > 0 else "red"
            console.print(f"📈 Yesterday: [bold {profit_color}]${last_summary['profit']:.2f} profit[/bold {profit_color}], {last_summary['units_sold']} units sold")
        
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
    
    def run_single_day(self):
        """Run a single day of business"""
        status = self.store.get_status()
        yesterday_summary = self.day_summaries[-1] if self.day_summaries else None
        
        console.print(f"🌅 Starting Day {status['day']}")
        
        # Scrooge makes decision
        console.print("🤖 [bold blue]Scrooge is pondering his next move...[/bold blue]")
        try:
            decisions = self.scrooge.make_daily_decision(status, yesterday_summary)
            
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
        
        # 🏭 Phase 1D: Display delivery results
        if day_summary.get('deliveries'):
            console.print("\n🚚 [bold green]DELIVERY RESULTS:[/bold green]")
            for delivery in day_summary['deliveries']:
                if delivery['success']:
                    console.print(f"✅ {delivery['message']}", style="green")
                else:
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
        
        console.print(Panel(
            f"""
💰 Revenue: ${day_summary['revenue']:.2f}
📈 Profit: ${day_summary['profit']:.2f}
🛒 Units Sold: {day_summary['units_sold']}
💵 Cash Balance: ${day_summary['cash_balance']:.2f}
📦 Inventory: {day_summary['inventory_status']}{supply_chain_info}
""",
            title=f"Day {day_summary['day']-1} Accounting",
            border_style="green"
        ))
        
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