import requests
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

api_key = os.getenv("API_KEY")

class Data:
    def get_heroes():
        if os.path.exists("heroes.json"):
            print("heroes.json already exists")
        else:
            url = "https://api.opendota.com/api/heroes"
            response = requests.get(url)
            data = response.json()
            file_path = "heroes.json"
            with open(file_path, "w") as file:
                json.dump(data, file)
            print("heroes.json created")
            
    def get_recent_games(player_id):
        url = f"https://api.opendota.com/api/players/{player_id}/recentMatches?api_key={api_key}"
        response = requests.get(url)
        data = response.json()
        return data
    
    #use get recent games then turn the enums in the json to the hero names
    def parse_recent_games(player_id):
        data = Data.get_recent_games(player_id)    
        with open("heroes.json") as file:
            heroes = json.load(file)
        hero_dict = {}
        for hero in heroes:
            hero_dict[hero["id"]] = hero["localized_name"]
        for game in data:
            game["hero_name"] = hero_dict[game["hero_id"]]
        with open("recent_games.json", "w") as file:
            json.dump(data, file)

    #remove not needed datapoints
    def clean_up_recent_games():
        json_file = "recent_games.json"
        with open(json_file) as file:
            data = json.load(file)
        for game in data:
            del game["match_id"]
            del game["game_mode"]
            del game["lobby_type"]
            del game["version"]
            del game["lane"] #lane information currently broken 26.05.
            del game["lane_role"]
            del game["is_roaming"]
            del game["leaver_status"]
            del game["party_size"]
        with open(json_file, "w") as file:
            json.dump(data, file)

    #get hero guides from howdoiplay.com for each hero
    def get_hero_guides():
        url = "https://howdoiplay.com/"
        driver = webdriver.Chrome()
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

        with open("database\hero_guides.json", "w") as file:
            json.dump(guide_list, file)



            