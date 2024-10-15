import json
from igdb.wrapper import IGDBWrapper
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('CLIENT_ID')
acess_token = os.getenv('CLIENT_SECRET')

'''
Esse codigo aqui estava quase funcionando mas estava tendo muito problema com esse evelopador porque ele retorna esse
byte array que ainda nao sei usar e acaba dando um montede problema para parsear com o json vou recorrer as calls de api normais 
que elas retornam strings
'''

game_id_json_file = 'games_ids2.json'
game_info_output_file = 'second_iteration.json'

# variavel para salvar o envelope do igdb
wrapper = IGDBWrapper(client_id, acess_token)

# abrindo o json com os ids dos jogos e carregando o json para dicionario python
with open(game_id_json_file, 'r', encoding='utf-8') as r:
    game_ids = json.load(r)

# inicializr o dicionario para salvar game data
game_data = {}
for game_name, game_info in list(game_ids.items())[:5]:
    # faz a requisição para a API usando o envelope
    game_id = game_info['id']
    byte_array = wrapper.api_request(
        endpoint='games',
        query=
        f'''
                fields id, aggregated_rating, aggregated_rating_count, category, cover, first_release_date, game_engines, game_localizations, game_modes,
                involved_companies, multiplayer_modes, platforms, player_perspectives, remakes, remasters, slug, status, storyline, summary, url; 
                offset 0; 
                where id = {game_id};
        '''
    )
    print(f"Game: {game_name}. ID: {game_id}. Processing...")

    # esse decode aqui e porque esse wrapper retorna um byte_array que eu nao faco ideia de como parseia entao eu sotransformei em uma string formatada em json 
    decoded_byte_array = byte_array.decode('utf-8')

    print(decoded_byte_array)

    # convertendo a string formatada em json para dicionario do python
    json_game_data = json.loads(decoded_byte_array)  

    game_data.update(json_game_data)
    sleep(1)


# escrevendo json
with open(game_info_output_file, 'w', encoding='utf-8') as f:
    json.dump(game_data, f, ensure_ascii=False, indent=4)
