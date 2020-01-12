from Player import players

from Environment import Environments

import argparse

### Command line arugments
parser = argparse.ArgumentParser()

parser.add_argument('--games', type=int, help="Number of games you wish to play this environment", default=1)

args = parser.parse_args()

games = args.games

#### Player objects created here

## This is a human player
hp = players.HumanPlayer()

qp = players.QPlayer()

dqp = players.DoubleQPLayer()

ndqp = players.NStepDoubleQAgent()

sarsa = players.SARSAgent()

### Creating an enviornment object with HumanPlayer and N-stepDouble Q-Player they will play 20 episodes or games together of the
#### Tic Tac Toe Evironment
#### Player

Environments.TicTacToe(player1=sarsa, player2=hp, episodes=games)
