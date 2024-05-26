import requests
import json
import os

api_key = os.getenv("API_KEY")


def get_heroes():
    url = "https://api.opendota.com/api/heroes"
    response = requests.get(url)
    data = response.json()
    file_path = "heroes.json"
    with open(file_path, "w") as file:
        json.dump(data, file)

def get_recent_games(player_id):
    url = f"https://api.opendota.com/api/players/{player_id}/recentMatches?api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

#use get recent games then turn the enums in the json to the hero names
def parse_recent_games(player_id):
    data = get_recent_games(player_id)    
    with open("heroes.json") as file:
        heroes = json.load(file)
    hero_dict = {}
    for hero in heroes:
        hero_dict[hero["id"]] = hero["localized_name"]
    for game in data:
        game["hero_name"] = hero_dict[game["hero_id"]]
    with open("recent_games.json", "w") as file:
        json.dump(data, file)

parse_recent_games(153086719)
