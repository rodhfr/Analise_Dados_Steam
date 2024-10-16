from bs4 import BeautifulSoup  
import json

html_file_path = 'steamdb.htm'

with open(html_file_path, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')  
all_games_data = []

rows = soup.select('tr.app')  

# iterar para pegar todas as informações
for i in range(1000):
    if i < len(rows):
        row = rows[i]  

        rank_number = row.select_one('td.dt-type-numeric').text
        game_name = row.select_one('td:nth-child(3) > a:nth-child(1)').text
        positive_ratings = row.select_one('td:nth-child(4)').text
        negative_ratings = row.select_one('td:nth-child(5)').text
        total_reviews = row.select_one('td:nth-child(6)').text
        rating_percentage = row.select_one('td:nth-child(7)').text

        # Entrada de dicionario para escrever no json
        new_entry = {
            'rank': rank_number,
            'name': game_name,
            'positive ratings': positive_ratings,
            'negative ratings': negative_ratings,
            'total reviews': total_reviews,
            'rating percentage': rating_percentage
        }

        all_games_data.append(new_entry)

json_file_path = '../3_game_ratings.json'

# importante usar encoding utf-8 e ensure_ascii para não quebrar com os jogos em japonês/chinês escritos com kanji
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_games_data, json_file, ensure_ascii=False, indent=4)  

print(f"Data written to {json_file_path}: {all_games_data}")
