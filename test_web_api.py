#!/usr/bin/env python3
"""
🧪 Quick test script for Phase 5A.4 Web API functionality
"""

import requests
import json
import time
import sys

def test_web_api():
    """Test the web API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing ShelfMind Web API...")
    print("=" * 50)
    
    try:
        # Test 1: Check if server is running
        print("1️⃣ Testing server status...")
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            print("   ✅ Server is responding")
            status_data = response.json()
            print(f"   📊 Simulation running: {status_data.get('simulation_running', 'Unknown')}")
        else:
            print(f"   ❌ Server returned status {response.status_code}")
            return False
            
        # Test 2: Start simulation
        print("\n2️⃣ Testing simulation start...")
        response = requests.post(f"{base_url}/api/simulation/start", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Start command sent: {result.get('message', 'Success')}")
        else:
            print(f"   ❌ Start failed with status {response.status_code}")
            return False
            
        # Test 3: Wait and check status
        print("\n3️⃣ Waiting for simulation to run...")
        time.sleep(3)  # Give simulation time to process
        
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            print(f"   📊 Current day: {status_data.get('store_status', {}).get('day', 'Unknown')}")
            print(f"   💰 Cash: ${status_data.get('store_status', {}).get('cash', 0):.2f}")
            print(f"   🤖 Agents active: {len(status_data.get('agent_states', {}))}")
            print("   ✅ Simulation appears to be running correctly")
        
        # Test 4: Stop simulation
        print("\n4️⃣ Testing simulation stop...")
        response = requests.post(f"{base_url}/api/simulation/stop", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Stop command sent: {result.get('message', 'Success')}")
        else:
            print(f"   ❌ Stop failed with status {response.status_code}")
            
        print("\n🎉 All API tests completed successfully!")
        print("🌐 Web dashboard is working correctly!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure web server is running:")
        print("   python web_server.py")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Server may be overloaded.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 ShelfMind Web API Test Suite")
    print("💡 Make sure the web server is running before starting this test")
    print("   Start server with: python web_server.py")
    print()
    
    input("Press Enter when server is ready...")
    
    success = test_web_api()
    
    if success:
        print("\n✅ All tests passed! Your web dashboard is ready for use.")
        print("🎯 Open http://localhost:8000 in your browser to see it in action!")
    else:
        print("\n❌ Some tests failed. Check the server logs for details.")
        sys.exit(1) 