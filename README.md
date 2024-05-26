# Dota 2 Buddy
This is a school project to familiarize myself with different Machine Learnin tools

## Problem description
Dota 2 is an incredibly complex game. Improving is difficult, mainly since it's not immediately obvious to oneself where one needs to imrpove.
I'm wondering if a LLM would be able to parse over a number of games and give some basic feedback on what you're doing good and what you need to work on.


# Basic project setup
## Data
Valve (developers behind Dota 2) provides a powerful API where I can get game data given I have a PlayerID. The response is in JSON, which should be parsable by an LLM.

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
