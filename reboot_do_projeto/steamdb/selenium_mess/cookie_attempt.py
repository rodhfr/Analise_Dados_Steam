from selenium import webdriver
import json
import os


# Load cookies to a variable from a file
if os.path.exists('cookies.json'):
    try:
        with open('cookies.json', 'r') as file:
            cookies = json.load(file)
    except json.JSONDecodeError:
        cookies = []  # Initialize an empty list if the JSON is invalid
else:
    cookies = []  # Initialize an empty list if the file does not exist




url = "https://mail.google.com"
# Inicia o driver com as opções
driver = webdriver.Firefox()

# Acessa a URL
driver.get(url)

input("Press Enter after logging in...")  # This will pause the script until you press Enter

# Get and store cookies after login
cookies = driver.get_cookies()

for cookie in cookies:
    driver.add_cookie(cookie)
    print(f"Name: {cookie['name']}, Value: {cookie['value']}")

driver.quit()

# Store cookies in a file
with open('cookies.json', 'w') as file:
    json.dump(cookies, file) 