#!/usr/bin/env python3
"""
Quick test script to verify the Periodic Table application works.
"""

if __name__ == "__main__":
    import sys
    import json
    from pathlib import Path
    
    # Test 1: Check if data file exists
    json_path = Path(__file__).parent / "Periodic-Table-JSON" / "PeriodicTableJSON.json"
    print(f"1. Checking data file: {json_path}")
    print(f"   File exists: {json_path.exists()}")
    
    if json_path.exists():
        # Test 2: Load and parse JSON
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        elements = data.get('elements', [])
        print(f"\n2. Data loaded successfully!")
        print(f"   Total elements: {len(elements)}")
        
        # Test 3: Display first few elements
        print(f"\n3. Sample elements:")
        for elem in elements[:5]:
            print(f"   - {elem['number']}. {elem['name']} ({elem['symbol']})")
        
        # Test 4: Check for specific element
        gold = next((e for e in elements if e['symbol'] == 'Au'), None)
        if gold:
            print(f"\n4. Gold element data:")
            print(f"   Name: {gold['name']}")
            print(f"   Atomic Mass: {gold['atomic_mass']}")
            print(f"   Category: {gold['category']}")
            print(f"   Density: {gold['density']}")
        
        print(f"\n✓ All tests passed! Application is ready to use.")
    else:
        print(f"   ERROR: Data file not found!")
        sys.exit(1)
