import json

# Load the rankings JSON data
with open('game_ratings_updated.json', 'r', encoding='utf-8') as f:
    rankings_data = json.load(f)

# Load the second JSON file
with open('dataframe.json', 'r', encoding='utf-8') as f:
    portal_data = json.load(f)

# Iterate over the rankings data and update the portal data
for index, ranking in enumerate(rankings_data):
    if index < len(portal_data):  # Ensure we don't exceed the portal_data list length
        portal_data[index]["positive ratings"] = ranking["positive ratings"]
        portal_data[index]["negative ratings"] = ranking["negative ratings"]
        portal_data[index]["total reviews"] = ranking["total reviews"]

# Write the updated portal data back to the JSON file
with open('serase_updated.json', 'w', encoding='utf-8') as f:
    json.dump(portal_data, f, ensure_ascii=False, indent=4)

# Optionally, print a confirmation message
print("Portal data has been updated and written to 'portal_data_updated.json'.")