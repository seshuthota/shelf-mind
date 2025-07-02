#!/usr/bin/env python3
"""
🌐 Phase 5A.4: ShelfMind Web Dashboard Launcher
Standalone launcher for the web interface
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Launch the ShelfMind web dashboard"""
    print("🚀 Starting ShelfMind Web Dashboard...")
    print("🌐 Phase 5A.4: Interactive Web Interface for Character-Controlled Business AI")
    print("-" * 80)
    print("📊 Dashboard URL: http://localhost:8000")
    print("🔌 WebSocket URL: ws://localhost:8000/ws")
    print("📡 API Docs: http://localhost:8000/docs")
    print("-" * 80)
    print("💡 Features:")
    print("   • Real-time simulation monitoring")
    print("   • Character agent status tracking")
    print("   • Interactive simulation controls")
    print("   • 25 specialized tools visibility")
    print("   • Live financial and inventory data")
    print("-" * 80)
    
    # Set environment variables if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded from .env")
    else:
        print("⚠️  No .env file found - make sure to set your API keys")
    
    try:
        # Import and run the FastAPI app
        from src.web.api import app
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=False  # Set to True for development
        )
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 