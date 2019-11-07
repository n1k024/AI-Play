from Player import players

from Environment import Environments

#### Player objects created here


## This is a human player
hp = players.HumanPlayer()

qp = players.QPlayer()

dqp = players.DoubleQPLayer()

ndqp = players.NStepDoubleQAgent()

### Creating an enviornment object with Qplayer and N-stepDouble Q-Player they will play 20 episodes or games together of the
#### Tic Tac Toe Evironment
Environments.TicTacToe(player1=qp, player2=ndqp, episodes=20)
