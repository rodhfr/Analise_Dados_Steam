import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

# json filename
games_json = 'data.json'

# API ACESS DATA
client_id = os.getenv('CLIENT_ID')
acess_token = os.getenv('CLIENT_SECRET')
api_url = 'https://api.igdb.com/v4/'

HEADERS = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {acess_token}'
}


# Configure here the endpoint and the desired data
url_endpoint = 'games'
#url_endpoint = 'search'
#url_endpoint = 'release_dates'
current_request_url = api_url + url_endpoint
# --------
# sort the data
#data = 'fields name,rating; sort rating desc; limit 20;'
#data = 'search "Halo"; fields name,game,published_at,description;'
#data = 'search "21828429" fields game,category,date,human,region,y,m;'

json_file_path = 'game_names.json'
with open(json_file_path, 'r', encoding='utf-8') as f:
    game_names = json.load(f) 


games_all_info = {}

for name in game_names:
    data = f'fields *; search "{name}";'
    response = requests.post(current_request_url, headers=HEADERS, data=data)
    
    if response.status_code == 200:
        response_data = response.json()
        
        # Verifica se a resposta é uma lista e pega o primeiro item
        if isinstance(response_data, list) and len(response_data) > 0:
            first_item = response_data[0]  # Pega o primeiro item da lista
            first_key = next(iter(first_item))  # Obtém a primeira chave do primeiro item
            
            games_all_info[name] = {first_key: first_item[first_key]}  # Armazena apenas a primeira chave e seu valor
        else:
            print(f"Nenhum resultado encontrado para {name}.")
    else:
        print(f"Erro ao buscar dados para {name}: {response.status_code}")
    time.sleep(0.26)
    print(f"alo. Posicao do Loop: {name}")

# Salva as informações atualizadas em um novo arquivo JSON
with open('games_info_updated.json', 'w', encoding='utf-8') as f:
    json.dump(games_all_info, f, ensure_ascii=False, indent=4)