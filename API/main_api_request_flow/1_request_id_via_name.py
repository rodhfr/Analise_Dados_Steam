import requests
import json
import time
import os
from dotenv import load_dotenv



# ENTRA O NOME DOS JOGO EM JSON E SAI UM JSON COM OS NOME DOS JOGO

load_dotenv()

games_json = 'data.json'

client_id = os.getenv('CLIENT_ID')
access_token = os.getenv('CLIENT_SECRET')
api_url = 'https://api.igdb.com/v4/'

HEADERS = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {access_token}'
}


url_endpoint = 'games'
current_request_url = api_url + url_endpoint

json_file_path = '1_game_names.json'
with open(json_file_path, 'r', encoding='utf-8') as f:
    game_names = json.load(f)

games_all_info = {}

for name in game_names:
    data = f'fields *; search "{name}";'
    
    
    retries = 3
    success = False
    failed = ''
    for attempt in range(retries):
        response = requests.post(current_request_url, headers=HEADERS, data=data)

        if response.status_code == 200:
            response_data = response.json()
            
            
            if isinstance(response_data, list) and len(response_data) > 0:
                first_item = response_data[0]  
                first_key = next(iter(first_item))  
                
                games_all_info[name] = {first_key: first_item[first_key]}  
                success = True
                break  
            else:
                print(f"No results found for {name}.")
                break  
        else:
            print(f"Error fetching data for {name}: {response.status_code} (Attempt {attempt + 1})")
            time.sleep(1)  

    if not success:
        print(f"Failed to fetch data for {name} after {retries} attempts.")
        failed += f'{name}\n'

    time.sleep(0.26)  # esse e o limite de chamadas da api (nao alterar)
    print(f"Current Loop Position: {name}")

print(failed)
with open('1_failed.txt', 'w', encoding='utf-8') as file: # nao ta funcionando essa parada do failed 
    file.write(failed)

with open('2_game_ids.json', 'w', encoding='utf-8') as f:
    json.dump(games_all_info, f, ensure_ascii=False, indent=4)


