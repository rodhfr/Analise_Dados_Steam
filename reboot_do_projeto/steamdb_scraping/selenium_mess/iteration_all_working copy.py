from selenium import webdriver # import webdriver
from selenium.webdriver.common.by import By  # Import the By class
import os # geckodriver was not opening so this was the hotfix
from selenium.webdriver.support.ui import WebDriverWait # wait library
from selenium.webdriver.support import expected_conditions as EC # conditions library
from selenium.webdriver.support.ui import Select # select dropdown menus
from selenium.webdriver.firefox.options import Options # make firefox hidden
import json

# Set the path to GeckoDriver
PATH_TO_GECKODRIVER = 'gecko/geckodriver'  # Replace with the actual path

# Set GeckoDriver path as an environment variable
os.environ['PATH'] += ':' + PATH_TO_GECKODRIVER

# enable my profile
options = Options()

# Use your Firefox profile where you're already logged in
profile_path = r'C:\Users\Rod\AppData\Roaming\Mozilla\Firefox\Profiles\nk66yd47.default-release'
options.set_preference('profile', profile_path)


driver = webdriver.Firefox(options=options)


#acess webpage
driver.get("https://steamdb.info/stats/gameratings/")


try:
    # wait page to load and find number in the ranking list
    rows = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'tr.app, tr.owned'))
    )

    all_games_data = []

    for i in range(100):
        row = driver.find_element(By.CSS_SELECTOR,f'tr.app:nth-child({i + 1})')
        rank_number = row.find_element(By.CSS_SELECTOR, 'td.dt-type-numeric').text
        game_name = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3) > a:nth-child(1)').text
        positive_ratings = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text
        negative_ratings = row.find_element(By.CSS_SELECTOR, 'td:nth-child(5)').text
        total_reviews = row.find_element(By.CSS_SELECTOR, 'td:nth-child(6)').text
        rating_percentage = row.find_element(By.CSS_SELECTOR, 'td:nth-child(7)').text

        # create new dictionary entry for the json file
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
    json_file_path = 'game_ratings.json'

    # Overwrite the JSON file with new data
    with open(json_file_path, 'w') as json_file:
        json.dump(all_games_data, json_file, indent=4)  # Directly writing the new data

    print(f"Data written to {json_file_path}: {all_games_data}")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()