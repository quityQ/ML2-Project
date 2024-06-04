# Dota 2 Buddy
This is a school project to familiarize myself with different Machine Learning tools

## Problem description
Dota 2 is an incredibly complex game. Improving is difficult, mainly since it's not immediately obvious to oneself where one needs to improve, since there are dozens of skills one might be lacking in.
I'm wondering if a LLM would be able to parse over a number of games and give some basic feedback on what you're doing good and what you need to work on.
If so, this might be a decent tool for beginners to get feedback for their playstyle and start improving from there.

As Plato and Socrates would discuss the allegory of the cave; The shadows in Dota become the players reality. Getting freed of the cave should lead to new insight, even if from a fool. 

## About Dota 2
Dota 2 is a "multiplayer online battle arena" (MOBA) where you play in a team of 5 against another team of 5 players. Each player controls a character ("Hero"). There are over 120 Heroes to choose from, each with their own unique abilities.
The goal of the game is to destroy the enemy "Ancient", a structure that's located deeply on the enemy side of the map. In order to reach that goal, the players must defeat enemy players, creeps and/or strucutres to gain gold and experience. The gold earned can be spent to buy from the selection of over 100 items, which also might have certain abilities. Dota 2 also has a popular eSports scene where some tournaments manage to hosts prize pool in the millions, with the winning team becoming millionaires in the process.

[Here](https://www.youtube.com/playlist?list=PLwL7E8fRVEdc0tFJlm2AWYhu4ccMk_vDD) is a playlist covering the very basics of Dota 2. 

# Basic project setup
## Data
### Player data
Game data is being pulled using [OpenDota](https://docs.opendota.com/)'s API. The data is is in JSON format which is parsed over to transform the enums into strings, to make it understandable for the LLM.
With the predefined recentMatches endpoint, we're able to receive information about the last 20 games of a given player. This will be the main way to get an insight into the player.

### Information about the game
In order to feed the LLM with good information about the game we're using different sources.
We're scraping ["How do I play?"](howdoiplay.com), a website that hosts practical information about each hero in Dota2, for detailed information about the heroes and their playstyles.
We're are also pulling information of professional players from the OpenDota API, which we feed the LLM as examples of good performance. 


## Backend/LLM
With a prompt that seeks specific feedback from the data the LLM should be able to decipher a number things:
- Successful hero choices
- Unsuccessful hero choices
- Heores you've been good against
- Heroes you've been bad against
- Your most successful position/role
- Your least successful position/role
- Point out specific game elements such as your last hits and warding and commenting on it

## Frontend
The frontend should be like a chat environment. Once the player provides their PlayerID a larger prompt will return with the information as detailed above.
After that the user is able to chat about specific things. Since the LLM has access to decent information about Dota, it might be able to give decent advice, especially to a very new player.


# Project setup
Following external tools are required in order to recreate this project:
- [Ollama](https://ollama.com/)
- [OpenDota API key](https://www.opendota.com/)
