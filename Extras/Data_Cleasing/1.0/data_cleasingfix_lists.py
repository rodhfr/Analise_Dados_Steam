import json
import ast

# Load the JSON data from the input file
with open('input_remove_list.json', 'r', encoding='utf-8') as infile:
    data = json.load(infile)

ignore_values = ['n/a', 'N/A', 'NaN', 'NA', 'n /a']

# Modify the platforms and other relevant fields
for line_number, item in enumerate(data, start=1):  # Start line numbers at 1
    for key in ['platforms', 'genres', 'game_engines', 'game_modes', 'player_perspectives']:
        if key in item and isinstance(item[key], str):
            # Ignore specified values
            if item[key].strip() in ignore_values:
                continue
            
            # Remove any forward slashes
            item[key] = item[key].replace('/', '')

            # Replace specific genres
            item[key] = item[key].replace("Hack and slash/Beat 'em up", "hack_and_slash_beat_em_up")

            # Clean up the string by replacing single quotes with double quotes
            item[key] = item[key].replace("'", '"')

            # Remove any backslashes entirely
            item[key] = item[key].replace('\\', '')

            try:
                # Safely evaluate the string representation of the list
                item[key] = ast.literal_eval(item[key])
            except (ValueError, SyntaxError):
                # Print the line number when there's a parsing error
                print(f"Could not parse {key} on line {line_number}: {item[key]}")

# Save the modified data to the output file
with open('output_remove_list.json', 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)
