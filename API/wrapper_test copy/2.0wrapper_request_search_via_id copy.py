import json
from igdb.wrapper import IGDBWrapper
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('CLIENT_ID')
access_token = os.getenv('CLIENT_SECRET')
# Initialize IGDB wrapper
wrapper = IGDBWrapper(client_id, access_token)

with open('dataframe1.2.0gamePlatforms.json', 'r', encoding='utf-8') as f:
    games_data = json.load(f)

for game_name, details in games_data.items():
    print(f'Fetching details for: {game_name}')

    ask_request = 'game_engines'

    ask_query = str(f'search {game_name}; fields name, {ask_request};')
    print("ask query is:", ask_query)
    # Make request to API
    byte_array = wrapper.api_request(endpoint='games', query=f'search {game_name}; fields name, {ask_request};')

    # Decode the byte array
    response = byte_array.decode('utf-8')
    req_ids = response[0].get(f'"{ask_request}"', [])
    print(f"'{ask_request}' IDs for {game_name}: {req_ids}")

    if req_ids:
        req_ids_str = ','.join(map(str, req_ids))

        byte_array_req = wrapper.api_request(
            endpoint=f'{ask_request}',
            query=f'fields id, name; where id = ({req_ids_str});'
        )
        
        req_response = byte_array_req.decode('utf-8')
        
        if req_response:  # Check if response is valid
            req_names = [req['name'] for req in req_response]
            print(f"{ask_request}: ")
            for name in req_names:
                print(f"- {name}")

            games_data[game_name][f'{ask_request}'] = req_names
        else:
            print(f"No platform data found for {game_name}.")
    else:
        print(f"No platform IDs found for {game_name}.")

# Save updated data to output.json
with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(games_data, json_file, ensure_ascii=False, indent=4)

print("Finished")
