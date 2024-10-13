import requests
import json
import os
import time
import pandas as pd
from dotenv import load_dotenv


def fetch_game_endpoint_name(req_ask):

    # API ACCESS DATA
    client_id = os.getenv('CLIENT_ID')
    access_token = os.getenv('CLIENT_SECRET')
    api_url = 'https://api.igdb.com/v4/'

    HEADERS = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}'
    }

    # Load your existing JSON data
    with open('overwrite.json', 'r', encoding='utf-8') as json_file:
        games_data = json.load(json_file)

    #limited_games_data = dict(list(games_data.items())[:10])

    for game_name, details in games_data.items():
    #for game_name, details in games_data.items():
        print(f"Fetching details for: {game_name}")

        # Step 1: Query the games endpoint to get game details
        url_endpoint = 'games'
        current_request_url = api_url + url_endpoint

        data = f'search "{game_name}"; fields name, {req_ask};'

        # Request to get game details
        response = requests.post(current_request_url, headers=HEADERS, data=data)

        # Checking response for game details
        if response.status_code == 200:
            print("Game Request Success")
            games_data_response = response.json()
            if games_data_response:
                # Step 2: Extract platform IDs from the game details
                platform_ids = games_data_response[0].get(f'{req_ask}', [])
                print(f"Platform IDs for {game_name}: {platform_ids}")
            
                # Step 3: Query the platforms endpoint to get platform names
                if platform_ids:
                    platform_ids_str = ','.join(map(str, platform_ids))
                    platform_url_endpoint = f'{req_ask}'  # This endpoint fetches platform details
                    platform_request_url = api_url + platform_url_endpoint

                    platform_data = f'fields id, name; where id = ({platform_ids_str});'

                    # Retry mechanism for platform requests
                    max_retries = 10  # Maximum number of retries
                    retry_delay = 2  # Delay in seconds between retries
                    platform_response = None

                    for attempt in range(max_retries):
                        platform_response = requests.post(platform_request_url, headers=HEADERS, data=platform_data)
                        if platform_response.status_code == 200:
                            print("Request Success")
                            break  # Exit the loop if the request was successful
                        else:
                            print(f"Request Error on attempt {attempt + 1}: {platform_response.status_code}")
                            time.sleep(retry_delay)  # Wait before retrying

                    # Check if the platform response was successful
                    if platform_response and platform_response.status_code == 200:
                        platforms_data = platform_response.json()
                        platform_names = [platform['name'] for platform in platforms_data]
                        print("Request:")
                        for name in platform_names:
                            print(f"- {name}")
                    
                        # Update the platforms field in the original JSON data
                        games_data[game_name][f'{req_ask}'] = platform_names
                    else:
                        print("Failed to retrieve request asked names after multiple attempts.")
            else:
                print("No games found.")
        else:
            print(f"Game Request Error: {response.status_code}")
            print(response.text)
    time.sleep(0.60)

    return games_data


def write_data_to_file(data, filename='overwrite.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Updated game data for '{filename}' has been saved successfully.")
    except Exception as e:
        print(f"Error saving data to {filename}: {e}")

def main():
    load_dotenv()

    a = 4 

    if a == 1:
        genres_data = fetch_game_endpoint_name(req_ask='genres')
        write_data_to_file(genres_data)

        print("genres_data done")
# deu ruim esse 2
    if a == 2:
        localizations_data = fetch_game_endpoint_name(req_ask='game_localizations')
        write_data_to_file(localizations_data)
        print("genres_data done")

    if a == 3:
        game_mode_data = fetch_game_endpoint_name(req_ask='game_modes')
        write_data_to_file(game_mode_data)
        print("game_mode done")

    if a == 4:
        involved_companies_data = fetch_game_endpoint_name(req_ask='involved_companies')
        write_data_to_file(involved_companies_data)
        print("involved_companies done")

    if a == 5:
        multiplayer_modes_data = fetch_game_endpoint_name(req_ask='multiplayer_modes')
        write_data_to_file(multiplayer_modes_data)
        print("Multiplayer Modes Done")






if __name__ == "__main__":
    main()