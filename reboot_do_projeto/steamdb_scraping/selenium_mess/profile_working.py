from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# Cria o perfil do Firefox
firefox_profile = FirefoxProfile('C:\\Users\\Rod\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\jo9vrhd8.selenium')

# Instancia as opções do Firefox
options = Options()  # Corrigido: instanciando a classe
options.profile = firefox_profile  
options.headless = False  

url = "https://mail.google.com"

# Inicia o driver com as opções
driver = webdriver.Firefox(options=options)

# Acessa a URL
driver.get(url)
