import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

# API Access Data
client_id = os.getenv('CLIENT_ID')
acess_token = os.getenv('CLIENT_SECRET')
api_url = 'https://api.igdb.com/v4/'

HEADERS = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {acess_token}'
}

# Load game names and IDs from a JSON file
input_json_path = 'input.json'  # Change this to your input JSON filename
with open(input_json_path, 'r', encoding='utf-8') as f:
    game_names = json.load(f)

# Check if the output JSON file exists and load existing data
output_json_path = 'output.json'
if os.path.exists(output_json_path):
    with open(output_json_path, 'r', encoding='utf-8') as f:
        games_all_info = json.load(f)  # Load existing data
else:
    games_all_info = {}  # Initialize an empty dict if file doesn't exist

for name, details in game_names.items():  # Process all game names
    game_id = details["id"]
    print(f"Fetching data for game ID: {game_id}")

    data = f'''
            fields id, aggregated_rating, aggregated_rating_count, category, cover, first_release_date, game_engines, game_localizations, game_modes,
            involved_companies, multiplayer_modes, platforms, player_perspectives, remakes, remasters, slug, status, storyline, summary, url; 
            where id = {game_id};
            '''
    response = requests.post(api_url + 'games', headers=HEADERS, data=data)

    if response.status_code == 200:
        game_info = response.json()
        if game_info:  # Check if there's any information returned
            # Update the existing dictionary structure with name at a higher level
            games_all_info[name] = {
                "id": game_id,
                "info": game_info  # Add game information under 'info'
            }
            print(f"Data fetched for {name}: {games_all_info[name]}")
        else:
            print(f"No data found for game ID: {game_id}")
    else:
        print(f"Error fetching data for {name}: {response.status_code}")

    time.sleep(0.26)  # Respect the rate limit

# Save the collected game information to the same JSON file
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(games_all_info, f, ensure_ascii=False, indent=4)

print(f"Game information saved to {output_json_path}.")
