import pandas as pd
import json




with open ('dataframe.json', 'r', encoding='utf-8') as f:
    games_data = json.load(f)


df = pd.DataFrame(games_data)


pd.set_option('display.max_rows', None)


# Assuming df is your DataFrame and 'name' is the column you want to print
max_length = df['name'].str.len().max()  # Find the maximum length of names
aligned_names = df['name'].str.ljust(max_length)  # Left-align names

# Print each name without truncation and without the index
for name in aligned_names:
    print(name)