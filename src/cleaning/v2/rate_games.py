import json



with open ('game_ratings.json', 'r', encoding='utf-8') as f:
    data = json.load(f)



for item in data:
    item["rank"] = int(float(item["rank"].rstrip('.')))  # Remove the dot and convert to int
    item["positive ratings"] = int(item["positive ratings"].replace(',', ''))  # Remove commas and convert to int
    item["negative ratings"] = int(item["negative ratings"].replace(',', ''))  # Remove commas and convert to int
    item["total reviews"] = int(item["total reviews"].replace(',', ''))  # Remove commas and convert to int
    # rating percentage remains as a string

# Check the converted data
for item in data:
    print(item)

with open('game_ratings_updated.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Data has been written to 'game_ratings_updated.json'.")