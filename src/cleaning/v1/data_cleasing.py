import pandas as pd
import json
import numpy as np


with open ('input_df.json', 'r', encoding='utf-8') as f:
    games_data = json.load(f)


df = pd.DataFrame(games_data)


print(df['name'])

df.replace(['n/a', 'N/A', 'NaN', 'NA', 'n /a'], np.nan, inplace=True)

# substituindo valores numericos com virgula para .
colunas = ["positive ratings", "negative ratings", "total reviews"]
for column in colunas:
    df[column] = df[column].str.replace(',', '.', regex=False)


# converter strings para valores numericos
colunas = ["positive ratings", "negative ratings", "total reviews", "aggregated_rating"]
for column in colunas:
    df[column] = pd.to_numeric(df[column])


# display
pd.set_option('display.max_rows', None) 
print(df)


# write
df.to_json('output_df.json', orient='records', force_ascii=False)





#high_rated_games = df[df["aggregated_rating"] > 9]
#print("High Rated Games:")
#print(high_rated_games)