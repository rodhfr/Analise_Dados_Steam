import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Credenciais
client_id = os.getenv('CLIENT_ID')
acess_token = os.getenv('CLIENT_SECRET')
api_url = 'https://api.igdb.com/v4/'

HEADERS = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {acess_token}'
}

game_name = "LEGO Star Wars: The Complete Saga"

url_endpoint = 'games'
current_request_url = api_url + url_endpoint
# examples:
#   data = 'fields name,category,platforms; limit 20;'
#   data = 'fields name,rating; sort rating desc; limit 20;'
data = f'search "{game_name}"; fields name;'

# Requisição
response = requests.post(current_request_url, headers=HEADERS, data=data)

if response.status_code == 200:
    print("Request Sucess")
    print(response.text)
    with open('data.json', 'w') as json_file:
        json.dump(response.json(), json_file, indent=4)
else:
    print(f"Request Error: {response.status_code}")
    print(response.text)