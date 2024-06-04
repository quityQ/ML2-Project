import requests
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

api_key = os.getenv("API_KEY")

class Data:
    
    def __init__(self, player_id):
        self.player_id = player_id
        pass
    
    def get_heroes():
        url = "https://api.opendota.com/api/heroes"
        response = requests.get(url)
        data = response.json()
        return data

    #get recent games from opendota api
    def get_recent_games(player_id):
        url = f"https://api.opendota.com/api/players/{player_id}/recentMatches?api_key={api_key}"
        response = requests.get(url)
        data = response.json()
        return data
    
    #use get recent games then turn the enums in the json to the hero names
    def parse_recent_games(self, player_id):
        data = Data.get_recent_games(player_id)    
        heroes = Data.get_heroes()
        hero_dict = {}
        for hero in heroes:
            hero_dict[hero["id"]] = hero["localized_name"]
        for game in data:
            game["hero_name"] = hero_dict[game["hero_id"]]
        return data

    #create list of recent heroes from the parsed recent games
    def get_recent_heroes(self, player_id):
        data = self.parse_recent_games(player_id)
        heroes = []
        for game in data:
            heroes.append(game["hero_name"])
        return heroes

    #get hero guides from howdoiplay.com for each hero
    def get_hero_guides(self):
        url = "https://howdoiplay.com/"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        guide_list = []
        
        with open ("database\heroes.json") as file:
            heroes = json.load(file)
        
        for hero in heroes:
            hero_name = hero["localized_name"]
            driver.get(url + '?' + hero_name)
            driver.implicitly_wait(1)
            tips = driver.find_element(by=By.CLASS_NAME, value='tips')
            content = tips.text
            guide_dict = {"name": hero_name, "guide": content}
            guide_list.append(guide_dict)

        driver.quit()

        return guide_list
            