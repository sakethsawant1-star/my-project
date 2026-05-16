import json
import os
from phase3 import load_data

restaurants = load_data()
locations = set(r.get('location', '') for r in restaurants)
print(f"Available locations: {locations}")
