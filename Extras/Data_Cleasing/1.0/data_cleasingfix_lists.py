import json
import ast

with open('input_remove_list.json', 'r', encoding='utf-8') as infile:
    data = json.load(infile)

ignore_values = ['n/a', 'N/A', 'NaN', 'NA', 'n /a']

for line_number, item in enumerate(data, start=1):  
    for key in ['platforms', 'genres', 'game_engines', 'game_modes', 'player_perspectives']:
        if key in item and isinstance(item[key], str):
            
            if item[key].strip() in ignore_values:
                continue
            
          
            item[key] = item[key].replace('/', '')

            item[key] = item[key].replace("Hack and slash/Beat 'em up", "hack_and_slash_beat_em_up")


            item[key] = item[key].replace("'", '"')

            item[key] = item[key].replace('\\', '')

            try:
 
                item[key] = ast.literal_eval(item[key])
            except (ValueError, SyntaxError):

                print(f"Could not parse {key} on line {line_number}: {item[key]}")

with open('output_remove_list.json', 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)
