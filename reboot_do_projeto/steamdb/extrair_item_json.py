import json

input_json = 'input.json'
output_json = 'output.json'

with open(input_json, 'r', encoding='utf-8') as f:
    data = json.load(f)


nomes = [item['name'] for item in data]

for nome in nomes:
    print(nome)

with open(output_json, 'w', encoding='utf-8') as json_file:
    json.dump(nomes, json_file, ensure_ascii=False, indent=4)