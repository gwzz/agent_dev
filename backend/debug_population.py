import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_tools.services.population import get_city_population

def debug_shanghai_population():
    print("Testing Shanghai population lookup...")
    result = get_city_population("Shanghai")
    print(f"Result: {result}")

    if result["status"] == "success":
        print(f"Population found: {result['population']}")
    else:
        print(f"Error: {result['error_message']}")

if __name__ == "__main__":
    debug_shanghai_population()