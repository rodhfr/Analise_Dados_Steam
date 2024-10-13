import requests
import json
import time
import os
from dotenv import load_dotenv


# ENTRA UM JSON COM ID DOS JOGOS E SAI O JSON COM AS INFO

load_dotenv()

client_id = os.getenv('CLIENT_ID')
access_token = os.getenv('CLIENT_SECRET')
api_url = 'https://api.igdb.com/v4/'

HEADERS = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {access_token}'
}

input_json_path = '2_game_ids.json'  
with open(input_json_path, 'r', encoding='utf-8') as f:
    game_names = json.load(f)

output_json_path = '3_game_info.json'
if os.path.exists(output_json_path):
    with open(output_json_path, 'r', encoding='utf-8') as f:
        games_all_info = json.load(f)  
else:
    games_all_info = {}  

for name, details in game_names.items():  
    game_id = details["id"]
    print(f"Fetching data for game ID: {game_id}")

    data = f'''
            fields id, aggregated_rating, aggregated_rating_count, category, cover, first_release_date, game_engines, game_localizations, game_modes,
            involved_companies, multiplayer_modes, platforms, player_perspectives, remakes, remasters, slug, status, storyline, summary, url; 
            where id = {game_id};
            '''

    retries = 3
    success = False
    failed = ''
    for attempt in range(retries):
        response = requests.post(api_url + 'games', headers=HEADERS, data=data)

        if response.status_code == 200:
            game_info = response.json()
            if game_info:  
                games_all_info[name] = {
                    "id": game_id,
                    "info": game_info  
                }
                print(f"Data fetched for {name}: {games_all_info[name]}")
                success = True
                break  
            else:
                print(f"No data found for game ID: {game_id}.")
                success = True  
                break
        else:
            print(f"Error fetching data for {name}: {response.status_code} (Attempt {attempt + 1})")
            time.sleep(1)  

    if not success:
        print(f"Failed to fetch data for {name} after {retries} attempts.")
        failed += f'{name}\n'
    time.sleep(0.26)  # esse e o limite de chamadas da api (nao alterar)

print(failed)
with open('2_failed.txt', 'w', encoding='utf-8') as file: # nao ta funcionando esse negocio do failed 
    file.write(failed)

with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(games_all_info, f, ensure_ascii=False, indent=4)

print(f"Game information saved to {output_json_path}.")
