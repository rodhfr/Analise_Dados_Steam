import requests
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JSON filename
games_json = 'input.json'

# API ACCESS DATA
client_id = os.getenv('CLIENT_ID')
access_token = os.getenv('CLIENT_SECRET')
api_url = 'https://api.igdb.com/v4/'

HEADERS = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {access_token}'
}

# Load your existing JSON data
with open(games_json, 'r') as json_file:
    games_data = json.load(json_file)

# Limit to the first 10 entries
for idx, (game_name, details) in enumerate(games_data.items()):
    if idx >= 10:  # Stop after 10 entries
        break

    print(f"Fetching details for: {game_name}")

    # Step 1: Query the games endpoint to get game details
    url_endpoint = 'games'
    current_request_url = api_url + url_endpoint

    data = f'search "{game_name}"; fields name, platforms;'

    # Request to get game details
    response = requests.post(current_request_url, headers=HEADERS, data=data)

    # Checking response for game details
    if response.status_code == 200:
        print("Game Request Success")
        games_data_response = response.json()
        if games_data_response:
            # Step 2: Extract platform IDs from the game details
            platform_ids = games_data_response[0].get('platforms', [])
            print(f"Platform IDs for {game_name}: {platform_ids}")
            
            # Step 3: Query the platforms endpoint to get platform names
            if platform_ids:
                platform_ids_str = ','.join(map(str, platform_ids))
                platform_url_endpoint = 'platforms'  # This endpoint fetches platform details
                platform_request_url = api_url + platform_url_endpoint

                platform_data = f'fields id, name; where id = ({platform_ids_str});'

                # Retry mechanism for platform requests
                max_retries = 5  # Maximum number of retries
                retry_delay = 1  # Delay in seconds between retries
                platform_response = None

                for attempt in range(max_retries):
                    platform_response = requests.post(platform_request_url, headers=HEADERS, data=platform_data)
                    if platform_response.status_code == 200:
                        print("Platform Request Success")
                        break  # Exit the loop if the request was successful
                    else:
                        print(f"Platform Request Error on attempt {attempt + 1}: {platform_response.status_code}")
                        time.sleep(retry_delay)  # Wait before retrying

                # Check if the platform response was successful
                if platform_response and platform_response.status_code == 200:
                    platforms_data = platform_response.json()
                    platform_names = [platform['name'] for platform in platforms_data]
                    print("Platforms:")
                    for name in platform_names:
                        print(f"- {name}")
                    
                    # Update the platforms field in the original JSON data
                    games_data[game_name]['platforms'] = platform_names
                else:
                    print("Failed to retrieve platform names after multiple attempts.")
        else:
            print("No games found.")
    else:
        print(f"Game Request Error: {response.status_code}")
        print(response.text)

# Save the updated JSON data back to the file, overwriting the existing data
with open(games_json, 'w') as json_file:
    json.dump(games_data, json_file, indent=4)

print("Updated game data has been saved successfully.")
