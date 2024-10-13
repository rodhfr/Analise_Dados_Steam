import requests
import json
import os
import time
from dotenv import load_dotenv


class IGDBApiWrapper:

    all_games_tmp_file = 'fetch_details_for_all_games.json'

    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('CLIENT_ID')
        self.access_token = os.getenv('CLIENT_SECRET')
        self.api_url = 'https://api.igdb.com/v4/'
        self.headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}'
        }

    def _make_request(self, endpoint, data):
        """Private method to make a POST request to the IGDB API."""
        url = f"{self.api_url}{endpoint}"
        response = requests.post(url, headers=self.headers, data=data)
        
        return response.json()
    
    def search_game_details(self, game_name, search_query=0):
        req_ask = f'search "{game_name}"; fields *;'
        game_data = self._make_request('games', data=req_ask)
    
        return game_data[search_query]


    def load_games_data(self, file_path):
        """Load existing games data from a JSON file."""
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)


    def fetch_details_for_all_games(self, read_file_path, initial_limit=0, end_limit=0):
        """Fetch details for all games listed in the provided JSON file."""
        print("also here")
        games_data = self.load_games_data(read_file_path)

        results = {}
        request_limit_per_second = 4  # Limit set by IGDB
        delay_between_requests = 1 / request_limit_per_second  # Time to wait between each request

        if initial_limit != 0 or end_limit != 0:  
            games_data = dict(list(games_data.items())[initial_limit:end_limit])
        
        for game_name, details in games_data.items():
            print(f"Fetching details for: {game_name}")
            try:
                game_details = self.search_game_details(game_name)
                results[game_name] = game_details
            except requests.HTTPError as e:
                print(f"Error fetching details for {game_name}: {e}")
            time.sleep(delay_between_requests)

        
        self.write_data_to_file(results, output='fetch_details_for_all_games.json')

        #self.write_data_to_file(results, output=write_file_path)

        return results
    
    def fetch_game_platform(self, game_name):
        """Return values from the id from the platform."""
    
        game_data = self.search_game_details(game_name)
        id_platforms = game_data['platforms']
        id_platforms_str = ', '.join(map(str, id_platforms))

        # print(id_platforms)    
     
        req_ask = f'fields id, name; where id = ({id_platforms_str});'
        platforms_names = self._make_request(endpoint='platforms', data=req_ask)

        return platforms_names
    
    def fetch_platform_for_all_games(self, read_file_path, initial_limit = 0, end_limit = 0, write_file_path=''):

        all_games_tmp_file = self.all_games_tmp_file  
        tmp_file_exists = self.check_baseline_info()

        if (tmp_file_exists):
            games_data = tmp_file_exists 
        else:
            print("baseline info not present getting from api...")
            games_data = self.fetch_details_for_all_games(read_file_path, initial_limit, end_limit)

        # loading all_games_tmp_file to a dictionary
        all_games_data = self.load_games_data(all_games_tmp_file)

        platforms_names = {}
        platforms = {}
        for game_name in games_data.keys():
            print(game_name)
            # Access the actual game data using the game_name key
            game_data = games_data[game_name]
            id_platforms = game_data['platforms']  # Use game_data to access platforms
            id_platforms_str = ', '.join(map(str, id_platforms))

            # requesting platforms names 
            req_ask = f'fields id, name; where id = ({id_platforms_str});'
            platforms_data = self._make_request(endpoint='platforms', data=req_ask) 

            # getting only the string from the platforms requested info
            platform_names = [platforms['name'] for platforms in platforms_data]
            platforms[game_name] = platforms_data
            platforms_names[game_name] = platform_names

        # replacing the old platform ids with platform_names strings
        for game_name in all_games_data:
            all_games_data[game_name]['platforms'] = platforms_names.get(game_name, [])

        self.write_data_to_file(data=all_games_data, output='fetch_platform_for_all_games.json')
        if write_file_path != '':
            self.write_data_to_file(data=all_games_data, output=write_file_path)

        return platforms_names 
        
        

    def write_data_to_file(self, data, output):

        with open(output, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Updated game data for '{output}' has been saved successfully.")


    def check_baseline_info(self):

        self.all_games_tmp_file 
        if os.path.isfile(self.all_games_tmp_file):
            print(f" {self.all_games_tmp_file} exists. \nGetting Platform Names")
            games_data = self.load_games_data(self.all_games_tmp_file)
            return games_data
        else:
            print("else")
            return False

    #def fetch_game_time_to_beat(self, read_file_path, initial_limit=0, end_limit=0):

        #all_games_tmp_file = self.all_games_tmp_file  
        #tmp_file_exists = self.check_baseline_info()

        #if (tmp_file_exists):
            #games_data = tmp_file_exists 
        #else:
            #print("baseline info not present getting from api...")
            #games_data = self.fetch_details_for_all_games(read_file_path, initial_limit, end_limit)

        #self.load_games_data(all_games_tmp_file)



 
def main():

    api_wrapper = IGDBApiWrapper()

    resultado = api_wrapper.fetch_platform_for_all_games(read_file_path='input.json', end_limit=5, write_file_path='furicasso.json')


    print(resultado)    


if __name__ == "__main__":
    main()