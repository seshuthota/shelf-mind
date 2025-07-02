#!/usr/bin/env python3
"""
🌐 Phase 5A.4: FastAPI Backend for ShelfMind Web Dashboard
Real-time simulation data serving with WebSocket support
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Any, Optional
import json
import asyncio
import logging
from pathlib import Path
import os

from ..engines.store_engine import StoreEngine
from ..core.multi_agent_engine import MultiAgentCoordinator, HybridAgentBridge
from ..agents.scrooge_agent import ScroogeAgent
from ..agents.inventory_manager_agent import InventoryManagerAgent
from ..agents.pricing_analyst_agent import PricingAnalystAgent
from ..agents.customer_service_agent import CustomerServiceAgent
from ..agents.strategic_planner_agent import StrategicPlannerAgent
from ..agents.crisis_manager_agent import CrisisManagerAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSimulationManager:
    """Manages the simulation for web interface"""
    
    def __init__(self):
        self.simulation_running = False
        self.simulation_speed = 1.0  # seconds between days
        self.clients: List[WebSocket] = []
        
        # Initialize simulation components
        self._init_simulation()
        
    def _init_simulation(self):
        """Initialize the simulation system"""
        self.store = StoreEngine(starting_cash=150.0)
        self.scrooge = ScroogeAgent(provider="openai")
        self.scrooge.set_store_reference(self.store)
        
        # Multi-agent system
        self.multi_agent_coordinator = MultiAgentCoordinator(provider="openai")
        self.hybrid_bridge = HybridAgentBridge(self.scrooge, self.multi_agent_coordinator)
        
        # Register all character agents
        self.inventory_manager = InventoryManagerAgent(provider="openai")
        self.pricing_analyst = PricingAnalystAgent(provider="openai")
        self.customer_service = CustomerServiceAgent(provider="openai")
        self.strategic_planner = StrategicPlannerAgent(provider="openai")
        self.crisis_manager = CrisisManagerAgent(provider="openai")
        
        # Register specialists
        self.multi_agent_coordinator.register_specialist(self.inventory_manager)
        self.multi_agent_coordinator.register_specialist(self.pricing_analyst)
        self.multi_agent_coordinator.register_specialist(self.customer_service)
        self.multi_agent_coordinator.register_specialist(self.strategic_planner)
        self.multi_agent_coordinator.register_specialist(self.crisis_manager)
        
        # Start in multi-agent mode
        self.hybrid_bridge.set_mode("multi")
        
        self.day_summaries = []
        
    async def add_client(self, websocket: WebSocket):
        """Add a new WebSocket client"""
        await websocket.accept()
        self.clients.append(websocket)
        logger.info(f"Client connected. Total clients: {len(self.clients)}")
        
        # Send initial state to new client
        await self.send_to_client(websocket, {
            "type": "initial_state",
            "data": self.get_current_state()
        })
        
    async def remove_client(self, websocket: WebSocket):
        """Remove a disconnected client"""
        if websocket in self.clients:
            self.clients.remove(websocket)
            logger.info(f"Client disconnected. Remaining clients: {len(self.clients)}")
            
    async def broadcast_update(self, data: Dict[str, Any]):
        """Broadcast update to all connected clients"""
        if not self.clients:
            return
            
        message = json.dumps(data)
        disconnected_clients = []
        
        for client in self.clients:
            try:
                await client.send_text(message)
            except Exception as e:
                logger.warning(f"Failed to send to client: {e}")
                disconnected_clients.append(client)
                
        # Remove disconnected clients
        for client in disconnected_clients:
            await self.remove_client(client)
            
    async def send_to_client(self, client: WebSocket, data: Dict[str, Any]):
        """Send data to a specific client"""
        try:
            await client.send_text(json.dumps(data))
        except Exception as e:
            logger.warning(f"Failed to send to specific client: {e}")
            
    def get_current_state(self) -> Dict[str, Any]:
        """Get complete current simulation state"""
        status = self.store.get_status()
        
        # Get agent states
        agent_states = {}
        if hasattr(self.multi_agent_coordinator, 'specialist_agents'):
            for role, agent in self.multi_agent_coordinator.specialist_agents.items():
                agent_name = agent.__class__.__name__.replace('Agent', '')
                agent_states[agent_name] = {
                    'status': 'active',
                    'last_action': getattr(agent, 'last_decision_summary', 'Ready'),
                    'confidence': getattr(agent, 'last_confidence', 1.0),
                    'tools_active': 5 if hasattr(agent, 'tools') else 0  # Simplified - each agent has 5 tools
                }
        
        return {
            'store_status': status,
            'agent_states': agent_states,
            'simulation_running': self.simulation_running,
            'simulation_speed': self.simulation_speed,
            'day_summaries': self.day_summaries[-10:] if self.day_summaries else [],  # Last 10 days
            'performance_metrics': self._calculate_performance_metrics()
        }
        
    def _calculate_performance_metrics(self) -> Dict[str, Any]:
        """Calculate key performance metrics"""
        if not self.day_summaries:
            return {}
            
        recent_summary = self.day_summaries[-1] if self.day_summaries else {}
        
        return {
            'daily_profit': recent_summary.get('profit', 0),
            'daily_revenue': recent_summary.get('revenue', 0),
            'daily_units_sold': recent_summary.get('units_sold', 0),
            'cash_position': self.store.get_status().get('cash', 0),
            'inventory_value': sum(
                qty * self.store.current_prices.get(product, 0) 
                for product, qty in self.store.get_status().get('inventory', {}).items()
            ),
            'profit_trend': 'rising' if len(self.day_summaries) >= 2 and 
                          self.day_summaries[-1].get('profit', 0) > self.day_summaries[-2].get('profit', 0) 
                          else 'declining' if len(self.day_summaries) >= 2 else 'stable'
        }
        
    async def run_simulation_day(self):
        """Run a single simulation day and broadcast updates"""
        if not self.simulation_running:
            return
            
        try:
            # Get current status
            status = self.store.get_status()
            yesterday_summary = self.day_summaries[-1] if self.day_summaries else {}
            
            # Broadcast start of day
            await self.broadcast_update({
                "type": "day_start",
                "data": {"day": status['day']}
            })
            
            # Make agent decisions
            decisions = self.hybrid_bridge.make_daily_decision(status, yesterday_summary)
            
            # Broadcast agent decisions
            await self.broadcast_update({
                "type": "agent_decisions",
                "data": decisions
            })
            
            # Apply decisions to store
            if decisions.get('prices'):
                for product, price in decisions['prices'].items():
                    self.store.update_price(product, price)
                    
            if decisions.get('orders'):
                order_results = self.store.process_orders(decisions['orders'])
                await self.broadcast_update({
                    "type": "order_results", 
                    "data": order_results
                })
                
            # Simulate customer activity
            customers = self.store.simulate_customers()
            await self.broadcast_update({
                "type": "customer_activity",
                "data": {"customers": len(customers), "purchases": sum(len(c.products) for c in customers)}
            })
            
            # End day and get summary
            day_summary = self.store.end_day()
            self.day_summaries.append(day_summary)
            
            # Broadcast day complete
            await self.broadcast_update({
                "type": "day_complete",
                "data": {
                    "summary": day_summary,
                    "current_state": self.get_current_state()
                }
            })
            
        except Exception as e:
            logger.error(f"Error running simulation day: {e}")
            await self.broadcast_update({
                "type": "error",
                "data": {"message": str(e)}
            })

# Initialize global simulation manager
sim_manager = WebSimulationManager()

# Create FastAPI app
app = FastAPI(
    title="ShelfMind Web Dashboard",
    description="Phase 5A.4: Interactive Web Interface for Character-Controlled Business AI",
    version="5.4.0"
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
@app.get("/")
async def get_dashboard():
    """Serve the main dashboard"""
    return FileResponse("src/web/static/index.html")

@app.get("/api/status")
async def get_status():
    """Get current simulation status"""
    return sim_manager.get_current_state()

@app.post("/api/simulation/start")
async def start_simulation():
    """Start the simulation"""
    sim_manager.simulation_running = True
    
    # Start simulation loop
    asyncio.create_task(simulation_loop())
    
    return {"status": "started", "message": "Simulation started successfully"}

@app.post("/api/simulation/stop")
async def stop_simulation():
    """Stop the simulation"""
    sim_manager.simulation_running = False
    return {"status": "stopped", "message": "Simulation stopped"}

@app.post("/api/simulation/reset")
async def reset_simulation():
    """Reset the simulation"""
    sim_manager.simulation_running = False
    sim_manager._init_simulation()
    
    await sim_manager.broadcast_update({
        "type": "simulation_reset",
        "data": sim_manager.get_current_state()
    })
    
    return {"status": "reset", "message": "Simulation reset successfully"}

@app.post("/api/simulation/speed/{speed}")
async def set_simulation_speed(speed: float):
    """Set simulation speed (seconds between days)"""
    if speed < 0.1 or speed > 10.0:
        raise HTTPException(status_code=400, detail="Speed must be between 0.1 and 10.0 seconds")
        
    sim_manager.simulation_speed = speed
    return {"status": "updated", "speed": speed}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await sim_manager.add_client(websocket)
    
    try:
        while True:
            # Keep connection alive and handle client messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle client commands
            if message.get("type") == "ping":
                await sim_manager.send_to_client(websocket, {"type": "pong"})
                
    except WebSocketDisconnect:
        await sim_manager.remove_client(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await sim_manager.remove_client(websocket)

async def simulation_loop():
    """Main simulation loop"""
    while sim_manager.simulation_running:
        await sim_manager.run_simulation_day()
        await asyncio.sleep(sim_manager.simulation_speed)

# Serve static files
static_dir = Path("src/web/static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 