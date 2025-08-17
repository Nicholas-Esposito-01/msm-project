import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# --- Setup Selenium in headless mode ---
options = Options()
options.add_argument("--headless")            # run in background
options.add_argument("--no-sandbox")          # required for some Linux/WSL setups
options.add_argument("--disable-dev-shm-usage") # prevent resource issues
options.add_argument("--disable-gpu")         # optional, good for headless
options.add_argument("--window-size=1920,1080") # optional, ensures full page render
driver = webdriver.Chrome(options=options)

# --- Base URL and monster list ---
base_url = "https://www.msmpokegamer.com/monsters/"
monsters = [
    "Noggin",
    "Mammott",
    "Toe Jammer",
    "Potbelly",
    "Tweedle"
]

# Dictionary to store results
monster_data = {}

# --- Loop through monsters ---
for monster in monsters:
    monster_url = base_url + monster.lower().replace(" ", "-")
    driver.get(monster_url)
    
    try:
        # Wait up to 10 seconds for the span with monster name
        name_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//span[text()='{monster}']"))
        )
        monster_data[monster] = {"name": name_elem.text, "url": monster_url}
        print(f"Found: {monster}")
        
    except Exception as e:
        print(f"{monster}: Not found ({e})")
        monster_data[monster] = {"name": None, "url": monster_url}

# --- Close the browser ---
driver.quit()


