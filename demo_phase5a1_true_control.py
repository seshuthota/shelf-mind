"""
🚀 PHASE 5A.1 DEMO: TRUE MULTI-AGENT DECISION MAKING
Revolutionary Character-Controlled Business Operations

This demo showcases the critical transition from character analysis to character control.
Characters now make actual business decisions rather than just providing advice.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.engines.store_engine import StoreEngine
from src.agents.scrooge_agent import ScroogeAgent  
from src.core.multi_agent_engine import HybridAgentBridge, MultiAgentCoordinator
from src.core.models import AgentRole

# Import all character agents
from src.agents.inventory_manager_agent import InventoryManagerAgent
from src.agents.pricing_analyst_agent import PricingAnalystAgent
from src.agents.customer_service_agent import CustomerServiceAgent
from src.agents.strategic_planner_agent import StrategicPlannerAgent
from src.agents.crisis_manager_agent import CrisisManagerAgent

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
import json

console = Console()

def display_character_authority_status(hybrid_bridge):
    """Display current character authority and control capabilities"""
    status = hybrid_bridge.get_character_authority_status()
    
    table = Table(title="🎭 CHARACTER AUTHORITY STATUS", show_header=True, header_style="bold magenta")
    table.add_column("Setting", style="cyan")
    table.add_column("Status", style="green")
    
    table.add_row("Character Authority", "✅ ENABLED" if status["character_authority_enabled"] else "❌ DISABLED")
    table.add_row("Decision Translation", "✅ ENABLED" if status["decision_translation_enabled"] else "❌ DISABLED")
    table.add_row("Current Mode", status["current_mode"].upper())
    table.add_row("True Multi-Agent Control", "✅ ACTIVE" if status["true_multi_agent_control"] else "⏳ AVAILABLE")
    
    console.print(table)
    
    # Display character control capabilities
    console.print("\n🏆 CHARACTER CONTROL CAPABILITIES:")
    for control_type, description in status["character_control_capabilities"].items():
        console.print(f"  • {control_type}: {description}")

def display_character_decision_translation(business_decisions):
    """Display how character decisions were translated into business actions"""
    
    if not business_decisions.get('character_control_active', False):
        console.print("⚠️ [red]Character control not active - falling back to advisory mode[/red]")
        return
    
    console.print("\n🎯 CHARACTER DECISION TRANSLATION:")
    
    # Display pricing decisions
    if 'prices' in business_decisions:
        console.print("\n💰 PRICING DECISIONS (Character-Controlled):")
        for product, price in business_decisions['prices'].items():
            console.print(f"  • {product}: ${price:.2f} [green](Set by characters)[/green]")
    else:
        console.print("\n💰 No pricing decisions from characters today")
        
    # Display ordering decisions  
    if 'orders' in business_decisions:
        console.print("\n📦 INVENTORY ORDERS (Character-Controlled):")
        for product, quantity in business_decisions['orders'].items():
            console.print(f"  • Order {quantity} units of {product} [green](Ordered by characters)[/green]")
    else:
        console.print("\n📦 No inventory orders from characters today")
    
    # Display decision metadata
    console.print(f"\n🎭 Primary Decision Maker: {business_decisions.get('primary_decision_maker', 'consensus').upper()}")
    console.print(f"📊 Decision Confidence: {business_decisions.get('decision_confidence', 0.0):.2f}")
    console.print(f"⚖️ Executive Override: {'YES' if business_decisions.get('override_occurred', False) else 'NO'}")
    
    # Display executive oversight
    oversight = business_decisions.get('executive_oversight_notes', 'No oversight notes')
    console.print(f"\n👔 Executive Oversight: {oversight}")

def run_phase5a1_demo():
    """Run comprehensive Phase 5A.1 demonstration"""
    
    console.print(Panel.fit(
        "[bold yellow]🚀 PHASE 5A.1 DEMONSTRATION[/bold yellow]\n"
        "[bold]True Multi-Agent Decision Making[/bold]\n\n"
        "Revolutionary transition from character analysis to character control!\n"
        "Characters now make actual business decisions with executive oversight.",
        border_style="yellow"
    ))
    
    try:
        # Initialize store and agents
        console.print("\n⚙️ [bold blue]Initializing Store & Character Ensemble...[/bold blue]")
        
        store = StoreEngine()
        scrooge = ScroogeAgent()
        scrooge._current_store = store
        
        # Initialize character coordination
        coordinator = MultiAgentCoordinator(provider="openai")
        
        # Register all character specialists
        coordinator.register_specialist(InventoryManagerAgent(provider="openai"))
        coordinator.register_specialist(PricingAnalystAgent(provider="openai"))
        coordinator.register_specialist(CustomerServiceAgent(provider="openai"))
        coordinator.register_specialist(StrategicPlannerAgent(provider="openai"))
        coordinator.register_specialist(CrisisManagerAgent(provider="openai"))
        
        # Create enhanced hybrid bridge
        hybrid_bridge = HybridAgentBridge(scrooge, coordinator)
        
        console.print("✅ [green]Character ensemble initialized successfully![/green]")
        console.print(f"📊 Active specialists: {len(coordinator.get_active_specialists())}")
        
        # Display character authority status
        console.print("\n" + "="*60)
        display_character_authority_status(hybrid_bridge)
        
        # Test Phase 5A.1: Switch to TRUE multi-agent mode
        console.print("\n" + "="*60)
        console.print("🔄 [bold magenta]SWITCHING TO TRUE MULTI-AGENT MODE...[/bold magenta]")
        hybrid_bridge.set_mode("multi")
        console.print("✅ [green]Mode switched to 'multi' - Characters now control business operations![/green]")
        
        # Run store for a few days to demonstrate character control
        console.print("\n" + "="*60)
        console.print("🏪 [bold blue]RUNNING STORE WITH CHARACTER CONTROL...[/bold blue]")
        
        day_summaries = []
        
        for day in range(1, 4):  # Run for 3 days
            console.print(f"\n📅 [bold cyan]DAY {day} - CHARACTER-CONTROLLED OPERATIONS[/bold cyan]")
            
            # Get store status
            status = store.get_status()
            yesterday_summary = day_summaries[-1] if day_summaries else None
            
            # Display current store state
            console.print(f"💰 Cash: ${status['cash']:.2f}")
            console.print(f"📦 Inventory: {status['inventory']}")
            console.print(f"💵 Current Prices: {status['products']}")
            
            # Make character-controlled decision
            console.print("\n🎭 [bold]CHARACTERS ANALYZING SITUATION & MAKING DECISIONS...[/bold]")
            
            try:
                # This is the key Phase 5A.1 feature - characters make actual business decisions
                business_decisions = hybrid_bridge.make_daily_decision(status, yesterday_summary)
                
                # Display character decision translation
                display_character_decision_translation(business_decisions)
                
                # Apply character decisions to store (if they made any)
                if business_decisions.get('character_control_active', False):
                    
                    # Apply pricing decisions
                    if 'prices' in business_decisions:
                        console.print("\n💰 [bold green]APPLYING CHARACTER PRICING DECISIONS...[/bold green]")
                        price_results = store.set_prices(business_decisions['prices'])
                        for product, result in price_results.items():
                            console.print(f"  ✅ {result}")
                    
                    # Apply ordering decisions
                    if 'orders' in business_decisions:
                        console.print("\n📦 [bold green]APPLYING CHARACTER INVENTORY ORDERS...[/bold green]")
                        order_results = store.process_orders(business_decisions['orders'])
                        for product, result in order_results.items():
                            console.print(f"  ✅ {result}")
                
                # Display character insights
                if 'character_insights' in business_decisions:
                    console.print("\n🎭 [bold]CHARACTER INSIGHTS:[/bold]")
                    for insight in business_decisions['character_insights']:
                        console.print(f"  • {insight['character']}: {insight['reasoning']}")
                
            except Exception as e:
                console.print(f"❌ [red]Character decision error: {e}[/red]")
                console.print("Using fallback single-agent mode...")
                business_decisions = scrooge.make_daily_decision(status, yesterday_summary)
                
                if business_decisions.get("prices"):
                    store.set_prices(business_decisions["prices"])
                if business_decisions.get("orders"):
                    store.process_orders(business_decisions["orders"])
            
            # Run daily operations
            console.print("\n⚙️ [yellow]Processing daily operations...[/yellow]")
            
            # Simulate customers
            customers = store.simulate_customers()
            console.print(f"🛒 {len(customers)} customers visited today")
            
            # End day and get summary
            daily_summary = store.end_day()
            day_summaries.append(daily_summary)
            
            # Display results
            console.print(f"📈 Revenue: ${daily_summary.get('revenue', 0):.2f}")
            console.print(f"💰 Profit: ${daily_summary.get('profit', 0):.2f}")
            console.print(f"📦 Units Sold: {daily_summary.get('units_sold', 0)}")
            
            console.print("\n" + "-"*40)
        
        # Final demonstration summary
        console.print("\n" + "="*60)
        console.print("🏆 [bold green]PHASE 5A.1 DEMONSTRATION COMPLETE![/bold green]")
        
        # Show final store status
        final_status = store.get_status()
        console.print(f"\n📊 FINAL STORE STATUS:")
        console.print(f"💰 Final Cash: ${final_status['cash']:.2f}")
        console.print(f"📈 Total Revenue: ${final_status.get('total_revenue', 0):.2f}")
        console.print(f"💎 Total Profit: ${final_status.get('total_profit', 0):.2f}")
        
        # Display coordination summary
        coord_summary = coordinator.get_coordination_summary()
        console.print(f"\n🤖 COORDINATION STATISTICS:")
        console.print(f"  • Active Specialists: {coord_summary.get('active_specialists', 0)}")
        console.print(f"  • Total Decisions: {coord_summary.get('last_decisions_count', 0)}")
        console.print(f"  • Average Confidence: {coord_summary.get('last_confidence', 0):.2f}")
        console.print(f"  • Debates Occurred: {coord_summary.get('total_debates', 0)}")
        
        console.print("\n✅ [bold green]Characters successfully controlled business operations![/bold green]")
        console.print("🎯 [bold]Phase 5A.1 TRUE MULTI-AGENT CONTROL: OPERATIONAL[/bold]")
        
    except Exception as e:
        console.print(f"\n❌ [bold red]Demo error: {e}[/bold red]")
        import traceback
        console.print(f"[red]{traceback.format_exc()}[/red]")

if __name__ == "__main__":
    run_phase5a1_demo() 