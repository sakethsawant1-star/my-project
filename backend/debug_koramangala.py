import json
import os
from phase3 import load_data, filter_restaurants

restaurants = load_data()
koramangala = [r for r in restaurants if 'koramangala' in r.get('location', '').lower()]
print(f"Total Koramangala restaurants: {len(koramangala)}")

if koramangala:
    costs = [r.get('costForTwo', 0) for r in koramangala]
    print(f"Min cost: {min(costs)}, Max cost: {max(costs)}")
    
candidates = filter_restaurants(restaurants, "Koramangala", "medium", "Any")
print(f"Found {len(candidates)} candidates.")
