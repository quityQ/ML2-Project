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
With the predefined recentMatches endpoint, we're able to receive information about the last 20 games of a given player.
This list is broken down to just the Hero names and is fed to the LLM in an initial prompt

### Information about the game
In order to feed the LLM with good information about the game we're using different sources.
We're scraping ["How do I play?"](howdoiplay.com), a website that hosts practical information about each hero in Dota2, for detailed information about the heroes and their playstyles.
It's unstructured Data which is ideal for the RAG.

## Backend/LLM
The initial prompt sends the recent 20 hero choices of the player, and asks for some tips.
Over this prompt the RAG attempts to find information within the data that was scraped.
Chat history is preserved, meaning that the chatbot should not lose context over the conversation.

## Frontend
The frontend is a chat environment created with streamlit
The user is asked to provide playerID (preferably their own)
Once provided the site loads for a bit and the initial answer is generated. In the ideal case it be relevant to the players past few heroes.


# Project setup
Following external tools are required in order to recreate this project:
- [Ollama](https://ollama.com/)
- [OpenDota API key](https://www.opendota.com/)

## Running the project
Follow the steps in Setup notebook to setup the project to run locally
