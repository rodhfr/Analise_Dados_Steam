import json
from igdb.wrapper import IGDBWrapper
from dotenv import load_dotenv
import os

load_dotenv()


client_id = os.getenv('CLIENT_ID')
acess_token = os.getenv('CLIENT_SECRET')
# Inicializa o wrapper da API IGDB
wrapper = IGDBWrapper(client_id, acess_token)

# Faz a requisição para a API
byte_array = wrapper.api_request(
    endpoint='games',
    query=
    '''
            fields aggregated_rating, aggregated_rating_count, category, cover, first_release_date, game_engines, game_localizations, game_modes,
            involved_companies, multiplayer_modes, platforms, player_perspectives, remakes, remasters, slug, status, storyline, summary, url; 
            offset 0; 
            where id = 134165;
    '''
)

# Decodifica o array de bytes em uma string
decoded_byte_array = byte_array.decode('utf-8')
print(decoded_byte_array)

# Converte a string JSON para um objeto Python (dicionário, lista, etc.)
json_data = json.loads(decoded_byte_array)  # Corrigido para json.loads

# Grava o objeto JSON em um arquivo
#with open('saida_simples_wrapper.json', 'w', encoding='utf-8') as f:
#    json.dump(json_data, f, ensure_ascii=False, indent=4)
