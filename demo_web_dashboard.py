#!/usr/bin/env python3
"""
🌐 Phase 5A.4: ShelfMind Web Dashboard Demo
Comprehensive demonstration of the revolutionary web interface for character-controlled business AI
"""

import os
import sys
import asyncio
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def print_banner():
    """Print the demo banner"""
    print("=" * 100)
    print("🌐 SHELFMIND WEB DASHBOARD DEMO - PHASE 5A.4")
    print("🚀 Revolutionary Character-Controlled Business AI with Interactive Web Interface")
    print("=" * 100)
    print()
    print("🎯 DEMO OBJECTIVES:")
    print("   ✅ Launch professional web dashboard with real-time updates")
    print("   ✅ Demonstrate 5 character agents with 25 specialized tools")
    print("   ✅ Show interactive simulation control and monitoring")
    print("   ✅ Display live financial metrics and inventory tracking")
    print("   ✅ Showcase crisis management and emergency response")
    print()
    print("🎭 CHARACTER ENSEMBLE:")
    print("   👩‍🔬 HERMIONE GRANGER - Inventory Management (5 analytical tools)")
    print("   💼 GORDON GEKKO - Pricing Strategy (5 market warfare tools)")
    print("   💖 ELLE WOODS - Customer Psychology (5 relationship tools)")
    print("   🎯 TYRION LANNISTER - Strategic Planning (5 intelligence tools)")
    print("   🚨 JACK BAUER - Crisis Management (5 emergency response tools)")
    print()
    print("🛠️  TECHNICAL FEATURES:")
    print("   • FastAPI backend with WebSocket real-time updates")
    print("   • Modern responsive frontend with interactive controls")
    print("   • Complete simulation state visibility and control")
    print("   • Professional-grade dashboard suitable for business presentations")
    print("   • Cross-platform compatibility (desktop, tablet, mobile)")
    print()
    print("=" * 100)

def print_access_info():
    """Print access information"""
    print("\n🌐 ACCESS INFORMATION:")
    print("   📊 Main Dashboard: http://localhost:8000")
    print("   📡 API Documentation: http://localhost:8000/docs")
    print("   🔌 WebSocket Endpoint: ws://localhost:8000/ws")
    print("   📋 API Status: http://localhost:8000/api/status")
    print()
    print("🎮 DASHBOARD CONTROLS:")
    print("   ▶️  Start Simulation - Begin character-controlled operations")
    print("   ⏸️  Stop Simulation - Pause all character decisions")
    print("   🔄 Reset Simulation - Return to initial state")
    print("   ⚡ Speed Control - Adjust simulation speed (0.1s - 5.0s per day)")
    print()
    print("📊 REAL-TIME MONITORING:")
    print("   • Executive summary with key business metrics")
    print("   • Live inventory grid with stockout/low-stock alerts")
    print("   • Character agent status and decision tracking")
    print("   • Activity log with real-time event streaming")
    print("   • Performance trends and analytics")
    print()

def print_demo_guide():
    """Print demonstration guide"""
    print("🎯 DEMONSTRATION GUIDE:")
    print()
    print("1️⃣  INITIAL SETUP:")
    print("   • Open http://localhost:8000 in your browser")
    print("   • Verify all 5 character agents are displayed and active")
    print("   • Check that WebSocket connection shows 'Connected'")
    print()
    print("2️⃣  START SIMULATION:")
    print("   • Click 'Start Simulation' button")
    print("   • Watch real-time activity log for character decisions")
    print("   • Observe inventory changes and financial metrics")
    print("   • Note how each character uses their specialized tools")
    print()
    print("3️⃣  CHARACTER ANALYSIS:")
    print("   • Watch Hermione analyze inventory levels with her tools")
    print("   • See Gekko make pricing decisions based on market analysis")
    print("   • Observe Elle's customer psychology and relationship building")
    print("   • Note Tyrion's strategic planning and long-term vision")
    print("   • Monitor Jack's crisis detection and emergency protocols")
    print()
    print("4️⃣  INTERACTIVE FEATURES:")
    print("   • Adjust simulation speed with the slider")
    print("   • Pause and resume simulation as needed")
    print("   • Reset simulation to test different scenarios")
    print("   • Watch real-time updates without page refresh")
    print()
    print("5️⃣  PROFESSIONAL DEMONSTRATION:")
    print("   • Show executive summary for business stakeholders")
    print("   • Highlight character autonomy and decision-making authority")
    print("   • Demonstrate tool visibility and performance tracking")
    print("   • Showcase crisis management and emergency response")
    print()

def check_environment():
    """Check if environment is properly set up"""
    print("🔍 ENVIRONMENT CHECK:")
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("   ✅ .env file found")
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print("   ✅ Environment variables loaded")
        except ImportError:
            print("   ⚠️  python-dotenv not installed, but .env file exists")
    else:
        print("   ⚠️  No .env file found - make sure API keys are set")
    
    # Check required dependencies
    required_deps = [
        'fastapi', 'uvicorn', 'websockets', 'jinja2', 
        'python-multipart', 'aiofiles', 'openai', 'anthropic'
    ]
    
    missing_deps = []
    for dep in required_deps:
        try:
            __import__(dep.replace('-', '_'))
            print(f"   ✅ {dep}")
        except ImportError:
            missing_deps.append(dep)
            print(f"   ❌ {dep} - MISSING")
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("💡 Install with: pip install " + " ".join(missing_deps))
        return False
    
    print("   ✅ All dependencies installed")
    return True

def launch_web_server():
    """Launch the web server"""
    print("\n🚀 LAUNCHING WEB SERVER...")
    print("   • Starting FastAPI application")
    print("   • Initializing WebSocket connections")
    print("   • Loading character agents and tools")
    print("   • Setting up real-time simulation engine")
    print()
    
    try:
        import uvicorn
        from src.web.api import app
        
        print("✅ Web server components loaded successfully")
        print("🌐 Starting server on http://localhost:8000")
        print()
        print("🎉 DEMO READY! Open your browser and start the simulation!")
        print("   (Press Ctrl+C to stop the server)")
        print()
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting web server: {e}")
        sys.exit(1)

def main():
    """Main demo function"""
    print_banner()
    
    if not check_environment():
        print("\n❌ Environment check failed. Please install missing dependencies.")
        sys.exit(1)
    
    print_access_info()
    print_demo_guide()
    
    print("\n" + "=" * 100)
    print("🚀 READY TO LAUNCH SHELFMIND WEB DASHBOARD")
    print("=" * 100)
    
    # Give user a moment to read
    input("\n📖 Press Enter to launch the web dashboard (or Ctrl+C to exit)...")
    
    launch_web_server()

if __name__ == "__main__":
    main() 