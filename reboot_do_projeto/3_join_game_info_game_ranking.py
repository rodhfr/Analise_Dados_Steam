import json

# Carregar os arquivos JSON
with open('3_game_ratings.json', 'r', encoding='utf-8') as rankings_file:
    rankings_data = json.load(rankings_file)

with open('3_game_info.json', 'r', encoding='utf-8') as details_file:
    details_data = json.load(details_file)

# Juntar os dados
combined_json = {}
for ranking in rankings_data:
    game_name = ranking['name']
    
    # Encontrar o ID correspondente no details_data
    game_info = details_data.get(game_name)  # Acessa pelo nome do jogo

    if game_info:  # Se o jogo for encontrado
        # Cria a estrutura desejada
        combined_json[game_name] = {
            "id": game_info['id'],
            "positive ratings": ranking['positive ratings'],
            "negative ratings": ranking['negative ratings'],
            "total reviews": ranking['total reviews'],
            "rating percentage": ranking['rating percentage'],
            "info": game_info['info']
        }

# Salvar o resultado em um novo arquivo JSON
with open('4_combined_dataframe.json', 'w', encoding='utf-8') as combined_file:
    json.dump(combined_json, combined_file, ensure_ascii=False, indent=4)

print("Combinação concluída e salva em '4_combined_dataframe.json'.")
