import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_crypto_agent_import():
    print("Testing crypto agent import...")
    try:
        from crypto_tools import get_crypto_price, root_agent
        print("Successfully imported crypto agent and tools")
        
        # Test that the agent exists and has the expected properties
        print(f"Agent name: {root_agent.name}")
        print(f"Agent description: {root_agent.description}")
        
        # Test the get_crypto_price function directly
        result = get_crypto_price("bitcoin")
        print(f"Direct function call result: {result}")
        
    except ImportError as e:
        print(f"Import error: {e}")

if __name__ == "__main__":
    test_crypto_agent_import()