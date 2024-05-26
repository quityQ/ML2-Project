from steam.client import SteamClient
from dota2.client import Dota2Client
import logging

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)

client = SteamClient()
dota = Dota2Client(client)  

@client.on('logged_on')
def start_dota():
    dota.launch()

@dota.on('ready')
def fetch_profile_card():
    dota.request_profile_card(76543359)

@dota.on('profile_card')
def print_profile_card(account_id, profile_card):
    if account_id == 76543359:
        print (profile_card)

client.cli_login()
client.run_forever()