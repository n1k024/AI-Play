# AI-Play

Allowing Humans and AI play together, unlike other environments such as gym. AI-Play allows the huamn or AI to play witn one another.

The structure is as follows

root/

Players/ 
 
 Here we find the player.py script which defines players abstract players and AI agents. 
 
 A human player is prompted for a unique name whereas the AI-player is not.
 
 
 Environments
 
 the constructor of each environment takes two player objects and an integer for the number of episodes or games in which you wish to play
 
 Currently there's only one environment available being TicTacToe, we plan to include other board-like games.
 
 To use AI-Play simply create your player objects and then pass them into the contrete TwoPlayerEnv class.
  
