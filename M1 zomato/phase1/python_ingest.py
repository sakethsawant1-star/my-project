import os
import pandas as pd
from datasets import load_dataset

print("Phase 1 (Python): Downloading full Zomato dataset from Hugging Face...")

# Download the full dataset directly using pandas
csv_url = "https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation/resolve/main/zomato.csv"
df = pd.read_csv(csv_url, nrows=10000)

print(f"Successfully downloaded {len(df)} rows.")

# Data Cleaning (mirroring our previous logic)
# Drop rows with missing critical fields
df = df.dropna(subset=['name', 'location', 'cuisines'])

# Clean Cost
def clean_cost(val):
    try:
        if pd.isna(val): return 500
        val = str(val).replace(',', '')
        return int(val)
    except:
        return 500

# Clean Rating
def clean_rating(val):
    try:
        if pd.isna(val) or val == "NEW" or val == "-": return 3.0
        val = str(val).split('/')[0]
        return float(val)
    except:
        return 3.0

df['costForTwo'] = df['approx_cost(for two people)'].apply(clean_cost)
df['rating'] = df['rate'].apply(clean_rating)

# Create final payload matching architecture
cleaned_data = pd.DataFrame({
    'name': df['name'].str.strip(),
    'location': df['location'].str.strip(),
    'cuisines': df['cuisines'].str.strip(),
    'costForTwo': df['costForTwo'],
    'rating': df['rating'],
    'votes': df['votes'].fillna(0).astype(int),
})

# Add search index
cleaned_data['searchIndex'] = (cleaned_data['name'] + " " + cleaned_data['location'] + " " + cleaned_data['cuisines']).str.lower()

# Sort by rating descending
cleaned_data = cleaned_data.sort_values(by='rating', ascending=False)

# Save to JSON
output_path = os.path.join(os.path.dirname(__file__), 'zomato_cleaned_full.json')
cleaned_data.to_json(output_path, orient='records', indent=4)

print(f"Phase 1 Complete: Successfully cleaned and indexed {len(cleaned_data)} restaurants.")
print(f"Data saved to: {output_path}")
