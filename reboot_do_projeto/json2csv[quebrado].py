import pandas as pd
import json

# Load JSON data
with open('dataframe.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Convert to DataFrame
df = pd.json_normalize(data)

# Save to CSV
df.to_csv('output.csv')
