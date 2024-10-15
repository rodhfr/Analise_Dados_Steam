import requests
import json
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


game_name = "Bunny E-shop"

# Configure here the endpoint and the desired data
#url_endpoint = 'games'
url_endpoint = 'games'
current_request_url = api_url + url_endpoint
# --------
# sort the data
#data = 'fields name,category,platforms; limit 20;'
#data = 'fields name,rating; sort rating desc; limit 20;'
data = f'search "{game_name}"; fields name;'

# Request
response = requests.post(current_request_url, headers=HEADERS, data=data)


# Printing the response to stdout
if response.status_code == 200:
    print("Request Sucess")
    print(response.text)
  #  with open(games_json, 'w') as json_file:
  #      json.dump(response.json(), json_file, indent=4)
else:
    print(f"Request Error: {response.status_code}")
    print(response.text)