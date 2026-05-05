import json
import os
from phase3 import load_data, filter_restaurants

restaurants = load_data()
print(f"Loaded {len(restaurants)} restaurants.")
if restaurants:
    print(restaurants[0])

candidates = filter_restaurants(restaurants, "Banashankari", "low", "Any")
print(f"Found {len(candidates)} candidates.")
