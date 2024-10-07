from bs4 import BeautifulSoup  # Import BeautifulSoup
import json

# Define the path to your HTML file
html_file_path = r'C:/Users/Rod/Code/IGDB-API/steamdb/Selenium-Model/steamdb.htm'

# Read the HTML file
with open(html_file_path, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')  # Parse the HTML content

all_games_data = []

# Find all rows in the ranking list
rows = soup.select('tr.app')  # Select all rows with class 'app'

# Iterate through the desired range of rows
for i in range(1000):
    if i < len(rows):
        row = rows[i]  # Get the row

        # Extract the relevant data from each cell
        rank_number = row.select_one('td.dt-type-numeric').text
        game_name = row.select_one('td:nth-child(3) > a:nth-child(1)').text
        positive_ratings = row.select_one('td:nth-child(4)').text
        negative_ratings = row.select_one('td:nth-child(5)').text
        total_reviews = row.select_one('td:nth-child(6)').text
        rating_percentage = row.select_one('td:nth-child(7)').text

        # Create new dictionary entry for the JSON file
        new_entry = {
            'rank': rank_number,
            'name': game_name,
            'positive ratings': positive_ratings,
            'negative ratings': negative_ratings,
            'total reviews': total_reviews,
            'rating percentage': rating_percentage
        }

        all_games_data.append(new_entry)

# Define JSON file path
json_file_path = 'game_ratings2.json'

# Write the JSON file with utf-8 encoding
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_games_data, json_file, ensure_ascii=False, indent=4)  # Ensure ASCII is not enforced

print(f"Data written to {json_file_path}: {all_games_data}")
