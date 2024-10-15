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
    endpoint='age_ratings',
    query='fields *; offset 0; where id = 17000;'
)

# Decodifica o array de bytes em uma string
decoded_byte_array = byte_array.decode('utf-8')
print(decoded_byte_array)

# Converte a string JSON para um objeto Python (dicionário, lista, etc.)
json_data = json.loads(decoded_byte_array)  # Corrigido para json.loads

# Grava o objeto JSON em um arquivo
with open('saida_simples_wrapper.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)
