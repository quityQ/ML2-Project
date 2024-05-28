# Dota 2 Buddy
This is a school project to familiarize myself with different Machine Learning tools

## Problem description
Dota 2 is an incredibly complex game. Improving is difficult, mainly since it's not immediately obvious to oneself where one needs to imrpove.
I'm wondering if a LLM would be able to parse over a number of games and give some basic feedback on what you're doing good and what you need to work on.
If so, this might be a decent tool for beginners to get feedback for their playstyle and start imrpoving from there.

As Plato and Socrates would discuss the allegory of the cave; The shadows in Dota become the players reality. Getting freed of the cave should lead to new insight, even if from a fool. 

# Basic project setup
## Data
### Player data
Game data is being pulled using OpenDota's API. The data is is in JSON format which is slightly formatted to transform the enums into strings. All that's needed is the players ID.
https://api.opendota.com


### Information about the game
In order to feed the LLM with good information about the game we're using different sources.
We're scraping howdoiplay.com for detailed information about the heroes and their playstyles.
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
After that the user is able to chat about specific things. If the LLM is pretrained with some sound discussion about Dota, it might be able to give decent advice, especially to a very new player.


# Project setup
Following external tools are required in order to recreate this project:
- Docker (https://www.docker.com/products/docker-desktop/)
- Ollama (https://ollama.com/)
- OpenDota API key (https://www.opendota.com/)