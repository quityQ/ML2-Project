import requests
import json
import os

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
            