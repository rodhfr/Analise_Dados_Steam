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
    element_rank_number = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'td.dt-type-numeric'))
    )
    inner_element_rank_number = element_rank_number.text
    print(inner_element_rank_number)

    # find name of the game
    element_name = driver.find_element(By.CSS_SELECTOR,'tr.app:nth-child(1) > td:nth-child(3) > a:nth-child(1)')
    inner_element_name = element_name.text
    print(inner_element_name)

    # find positive ratings
    element_positive = driver.find_element(By.CSS_SELECTOR,'tr.app:nth-child(1) > td:nth-child(4)')
    inner_element_positive = element_positive.text
    print(inner_element_positive)

    # negative ratings
    element_negative = driver.find_element(By.CSS_SELECTOR,'tr.app:nth-child(1) > td:nth-child(5)')
    inner_element_negative = element_negative.text
    print(inner_element_negative)

    # total ratings
    element_total = driver.find_element(By.CSS_SELECTOR,'tr.app:nth-child(1) > td:nth-child(6)')
    inner_element_total = element_total.text
    print(inner_element_total)

    # rating percentage
    element_rating_percentage = driver.find_element(By.CSS_SELECTOR,'tr.app:nth-child(1) > td:nth-child(7)')
    inner_element_rating_percentage = element_rating_percentage.text
    print(inner_element_rating_percentage)

    # create new dictionary entry for the json file
    new_entry = {
        'name': inner_element_name,
        'rank': inner_element_rank_number,
        'positive': inner_element_positive,
        'negative': inner_element_negative,
        'total': inner_element_total,
        'rating percentage': inner_element_rating_percentage
    }

    json_file_path = 'game_ratings.json'

    # Check if the JSON file exists
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    else:
        # If the file doesn't exist, create a new list
        data = []

    # Append the new entry to the data list
    data.append(new_entry)

    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4) 

    print(f"Data appended to {json_file_path}: {new_entry}")

except Exception as e:
    print(f"Error: {e}")


driver.quit()