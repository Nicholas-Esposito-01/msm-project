import requests
from bs4 import BeautifulSoup
import time
from data_structures import categories, natural_monsters, natural_rare_monsters, natural_epic_monsters, excluded_islands

base_url = 'https://mysingingmonsters.fandom.com/wiki/'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/113.0.0.0 Safari/537.36"
}

for monster in natural_monsters:

    monster_url = base_url + monster
    response = requests.get(monster_url, headers=headers)

    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    monster_name = soup.find("h2", {"data-source": "title"})
    monster_img = soup.find("img", {"alt": "Current Design"})

    islands_div = soup.find("div", {"data-source": "island(s)"})

    island_names = [a.text.strip() 
                    for a in islands_div.find_all('a')
                    if a.text.strip() and a.text.strip() not in excluded_islands
    ]
        
    

    print("Found Monster: ", monster_name.text)
    #print(monster_img)
    time.sleep(1)
