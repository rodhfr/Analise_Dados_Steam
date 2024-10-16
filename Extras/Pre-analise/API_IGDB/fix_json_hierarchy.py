import json


with open ("dataframe.json", "r", encoding='utf-8') as f:
    data = json.load(f)


# Iterate through each game in the dictionary
for game_name, game_data in data.items():
    # Check if the 'info' key exists and is a list
    if "info" in game_data and isinstance(game_data["info"], list):
        # Extract the first (and only) element from the 'info' array and merge it with the main dictionary
        info_data = game_data.pop("info")[0]
        # Merging 'info' data with the main game dictionary
        game_data.update(info_data)

keys_to_remove = ["summary", "slug", "url", "storyline"]
# Iterate through each game in the dictionary
for game_name, game_data in data.items():
    # Remove the specified keys if they exist in the game data
    for key in keys_to_remove:
        if key in game_data:
            del game_data[key]


with open("output_dataframe_fixed.json", 'w', encoding='utf-8') as z:
    json.dump(data, z, indent=4)

# Optional: Print the modified dictionary to verify the change
print(json.dumps(data, indent=4))