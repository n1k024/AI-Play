# AI-Play

Allowing Humans and AI play together, unlike other environments such as gym. AI-Play allows the huamn or AI to play witn one another. AI-Play is an educational ,research framework for experimenting with AI agents. 

Requirements

Python 3.x

root/

Players/ 
 
 Here we find the player.py script which defines players abstract players and AI agents. 
 
 A human player is prompted for a unique name whereas the AI-player is not.
 
 RLAgents
 
 QPlayer: RL agent that uses tabular Q-Learning to perform updates, Inherits RLtabularagent and Player classes
 
 DoubleQPlayer: RL agent that uses two Q functions to avoid over estimation of the Q-values (each Q function is chosen by probability .5)
 
 NstepQAgent: RL agent that computes an N-step return (Gt) to compute the expected reward for Q(s,a) = Q(s,a) + alpha(Gt - Q(s,a))
 Inherits: RLTabularAgent and Player
 
 
 NstepDoubleAgent: RL agent that uses both N-step returns and Double Learning to update the Q-values 
 
 Inherits : RLTabularAgent and Player

 SARSAgent: implmentation of SARSA algorithm
 SARSA is an on-policy TD method that uses Q-values for to compute the policy
 Inherits: RLTabularAgent and Player
 
 
 Environments
 the constructor of each environment takes two player objects and an integer for the number of episodes or games in which you wish to play
 
 Currently  only  environment available are TicTacToe and Connect4 we plan to include other board-like games.


 The Play script (Play.py) allows you (Human) to play with a QPlayer agent upon cloning this repository

 To use AI-Play simply create your player objects and then pass them into the contrete TwoPlayerEnv class. Please keep in mind you will need to create a Python script to call the environment and the two player objects you wish to use for that environment.

  You can change the types of players in each game by altering parameters for the environment



Credits
Works Cited on the research conducted to create this project can be found at WorksCited.txt


Parameter Setting

If you wish to change the parameters of the agents consult the parameter guide (Parameter_Guide.txt) to understand the various settings and how they work