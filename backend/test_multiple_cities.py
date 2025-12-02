from agent_tools.services import get_city_population

def test_multiple_cities():
    cities = ["Shanghai", "Beijing", "New York", "London", "Tokyo"]
    
    for city in cities:
        print(f"Testing {city} population lookup...")
        result = get_city_population(city)
        
        if result["status"] == "success":
            print(f"  Population found: {result['population']}")
        else:
            print(f"  Error: {result['error_message']}")
        print()

if __name__ == "__main__":
    test_multiple_cities()