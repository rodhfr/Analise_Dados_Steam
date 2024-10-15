import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
# JSON filename
games_json = 'data.json'

# API ACCESS DATA
client_id = os.getenv('CLIENT_ID')
access_token = os.getenv('CLIENT_SECRET')
api_url = 'https://api.igdb.com/v4/'

HEADERS = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {access_token}'
}

game_name = "Vampire Survivors"

# Step 1: Query the games endpoint to get game details
url_endpoint = 'games'
current_request_url = api_url + url_endpoint

data = f'search "{game_name}"; fields name, platforms;'

# Request to get game details
response = requests.post(current_request_url, headers=HEADERS, data=data)

# Checking response for game details
if response.status_code == 200:
    print("Game Request Success")
    games_data = response.json()
    if games_data:
        # Step 2: Extract platform IDs from the game details
        platform_ids = games_data[0].get('platforms', [])
        print(f"Platform IDs for {game_name}: {platform_ids}")
        
        # Step 3: Query the platforms endpoint to get platform names
        if platform_ids:
            platform_ids_str = ','.join(map(str, platform_ids))
            platform_url_endpoint = 'platforms'  # This endpoint fetches platform details
            platform_request_url = api_url + platform_url_endpoint

            platform_data = f'fields name; where id = ({platform_ids_str});'
            platform_response = requests.post(platform_request_url, headers=HEADERS, data=platform_data)

            # Checking response for platform details
            if platform_response.status_code == 200:
                print("Platform Request Success")
                platforms_data = platform_response.json()
                print("Platforms:")
                for platform in platforms_data:
                    print(f"- {platform['name']}")
            else:
                print(f"Platform Request Error: {platform_response.status_code}")
                print(platform_response.text)
    else:
        print("No games found.")
else:
    print(f"Game Request Error: {response.status_code}")
    print(response.text)
