import requests
import json
import os
import time
from dotenv import load_dotenv
import datetime


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

        all_games_tmp_file = read_file_path 
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
        all_games_tmp_file = self.all_games_tmp_file 
        if os.path.isfile(all_games_tmp_file):
            print(f" {all_games_tmp_file} exists. \nGetting Platform Names")
            games_data = self.load_games_data(all_games_tmp_file)
            return games_data
        else:
            print("else")
            return False
        
    def fetch_company_for_all_games(self, read_file_path, initial_limit=0, end_limit=0, write_file_path=''):
        # Load game data from the specified file
        all_games_data = self.load_games_data(read_file_path)

        # Determine the range of games to process based on the limits
        game_names = list(all_games_data.keys())
        if end_limit > 0:
            game_names = game_names[initial_limit:end_limit]
        else:
            game_names = game_names[initial_limit:]  # Process all games from the initial limit onward

        platforms_names = {}
        platforms = {}

        # Iterate over each game in the determined range
        for game_name in game_names:
            print(f"Processing game: {game_name}")
        
            # Access the actual game data using the game_name key
            game_data = all_games_data[game_name]
            # Use 'involved_companies' to access the platform IDs
            platform_ids = game_data.get('involved_companies', [])
            platform_ids_str = ', '.join(map(str, platform_ids))

            # Request platform names using the platform IDs
            req_ask = f'fields id, name; where id = ({platform_ids_str});'
            platforms_data = self._make_request(endpoint='companies', data=req_ask)

            # Extract only the names of the platforms from the requested info, with error handling
            platform_names = [platform['name'] for platform in platforms_data if 'name' in platform]
            platforms[game_name] = platforms_data
            platforms_names[game_name] = platform_names

        # Replace the old platform IDs with platform name strings in all_games_data
        for game_name in all_games_data:
            all_games_data[game_name]['involved_companies'] = platforms_names.get(game_name, [])

        # Write the updated game data to a JSON file
        self.write_data_to_file(data=all_games_data, output='fetch_platform_for_all_games.json')
        if write_file_path:
            self.write_data_to_file(data=all_games_data, output=write_file_path)

        return platforms_names

    def release_unix_to_commom(self, read_file_path, initial_limit=0, end_limit=0, write_file_path=''):
        all_games_data = self.load_games_data(read_file_path) 
        # Determine the range of games to process based on the limits
        game_names = list(all_games_data.keys())
        if end_limit > 0:
            game_names = game_names[initial_limit:end_limit]
        else:
            game_names = game_names[initial_limit:]  # Process all games from the initial limit onward

        for game in game_names:
            details = all_games_data[game]
            if 'first_release_date' in details:
                details['first_release_date'] = datetime.datetime.fromtimestamp(details['first_release_date']).strftime('%Y-%m-%d')

        if write_file_path:
            self.write_data_to_file(data=all_games_data, output=write_file_path)
        self.write_data_to_file()


    def replace_category_numbers(self, read_file_path, write_file_path=''):
        all_games_data = self.load_games_data(read_file_path)

        # Define the category mapping
        category_mapping = {
            0: "main_game",
            1: "dlc_addon",
            2: "expansion",
            3: "bundle",
            4: "standalone_expansion",
            5: "mod",
            6: "episode",
            7: "season",
            8: "remake",
            9: "remaster",
            10: "expanded_game",
            11: "port",
            12: "fork",
            13: "pack",
            14: "update"
        }

        # Replace category numbers with their corresponding names
        for game, details in all_games_data.items():
            if 'category' in details and details['category'] in category_mapping:
                details['category'] = category_mapping[details['category']]

        # Write the modified data to the specified file
        if write_file_path:
            self.write_data_to_file(all_games_data, write_file_path)


    def remove_item_from_key(self, read_file_path, write_file_path='', item=''):
        all_games_data = self.load_games_data(read_file_path)

        # Remove the "cover" item from each game's details
        for game, details in all_games_data.items():
            if item in details:
                del details[item]

        # Write the modified data to the specified file
        if write_file_path:
            self.write_data_to_file(all_games_data, write_file_path)

    def fetch_time_beats_for_all_games(self, file_path, initial_limit = 0, end_limit = 0):


        all_games_data = self.load_games_data(file_path)

        beats_names = {}
        beats = {}
        req_field = 'normally'
        for game_name in all_games_data.keys():
            print(game_name)
            # Access the actual game data using the game_name key
            game_data = all_games_data[game_name]
            game_ids = game_data['id']

            if isinstance(game_ids, int):   
               game_ids_str = str(game_ids) 
            else:
                game_ids_str = ', '.join(map(str, game_ids))

            # requesting platforms names 
            req_ask = f'fields normally; where game_id = ({game_ids_str});'
            time_to_beats_data = self._make_request(endpoint='game_time_to_beats', data=req_ask) 

            if not time_to_beats_data:
                print(f"No time to beat data returned for game: {game_name}")
                beats_names[game_name] = []
            else:
                time_in_hours = []
                for beats in time_to_beats_data:
                    time_in_seconds = beats[req_field]
                    hours = time_in_seconds / 3600
                    time_in_hours.append(hours)
                beats[game_name] = time_to_beats_data
                beats_names[game_name] = time_in_hours

        # replacing the old platform ids with platform_names strings
        for game_name in all_games_data:
            all_games_data[game_name][req_field] = beats_names.get(game_name, [])

        self.write_data_to_file(data=all_games_data, output='fetch_time_beats_for_all_games.json')
        self.write_data_to_file(data=all_games_data, output=file_path)

        return beats_names  

    def fetch_genre_for_all_games(self, file_path, initial_limit=0, end_limit=0):
        games_data = 'fetch_details_for_all_games.json'
        tmp_file_exists = self.check_baseline_info()

        # checar se o arquivo com os ids das categorias dos endpoints esta disponivel
        if tmp_file_exists:
            games_data = tmp_file_exists 
        else:
            print("Baseline info not present. Getting from API...")
            games_data = self.fetch_details_for_all_games(file_path, initial_limit, end_limit)

        all_games_data = self.load_games_data(games_data)

        genres_names = {}
        genres = {}
        for game_name in games_data.keys():
            print(game_name)
            game_data = games_data[game_name]

            # Verificar se a chave 'genres' existe antes de acessar
            if 'genres' in game_data:
                id_genres = game_data['genres']
                id_genres_str = ', '.join(map(str, id_genres))

                # Solicitar nomes dos gêneros
                req_ask = f'fields id, name; where id = ({id_genres_str});'
                genres_data = self._make_request(endpoint='genres', data=req_ask)

                # Obter apenas os nomes dos gêneros retornados
                genre_names = [genre['name'] for genre in genres_data]
            else:
                genre_names = []  # Definir lista vazia se a chave 'genres' não estiver presente

            genres[game_name] = genres_data if 'genres' in game_data else []
            genres_names[game_name] = genre_names

        # Substituir os ids antigos dos gêneros pelos nomes dos gêneros
        for game_name in all_games_data:
            all_games_data[game_name]['genres'] = genres_names.get(game_name, [])

        self.write_data_to_file(data=all_games_data, output='fetch_genre_for_all_games.json')

        return genres_names


def main():



    api_wrapper = IGDBApiWrapper()


#    resultado_time_beat = api_wrapper.fetch_time_beats_for_all_games(read_file_path='input.json', end_limit=15, write_file_path='input.json')

 #   print(resultado_time_beat)

    #response = api_wrapper.fetch_time_beats_for_all_games(read_file_path='overwrite2.json', write_file_path='overwrite2.json')
    #
    #involved = api_wrapper.fetch_company_for_all_games(read_file_path='input.json.', write_file_path='input.json')

   # response = api_wrapper.fetch_multiplayer_modes_for_games(read_file_path='overwrite2.json', end_limit=15,write_file_path='overwrite2.json')
    #response = api_wrapper.release_unix_to_commom(read_file_path='overwrite2.json', write_file_path='overwrite2.json')
   # response = api_wrapper.replace_category_numbers(read_file_path='overwrite2.json', write_file_path='overwrite2.json')
    #response = api_wrapper.remove_cover_item(read_file_path='overwrite2.json', write_file_path='overwrite2.json', item='cover')
    #api_wrapper.remove_cover_item(read_file_path='overwrite2.json', write_file_path='overwrite2.json', item= 'multiplayer_modes')
    #api_wrapper.remove_cover_item(read_file_path='overwrite2.json', write_file_path='overwrite2.json', item= 'remasters')
    api_wrapper.fetch_genre_for_all_games(read_file_path='overwrite2.json', write_file_path='overwrite2.json')

    #print(response)
if __name__ == "__main__":
    main()