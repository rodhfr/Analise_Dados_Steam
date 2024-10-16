import pandas as pd
import json

with open('games_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

games_data = []

for game, details in data.items():
    details['game'] = game
    games_data.append(details)

df = pd.json_normalize(games_data)

df.to_csv('games_data.csv', index=False)

print('dados salvos no arquivo de saida')