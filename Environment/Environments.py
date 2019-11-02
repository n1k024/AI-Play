from abc import ABC, abstractmethod

import numpy as np


class Twoplayerenv(ABC):
    def __init__(self, player1, player2, episodes=1):

        self.player1 = player1

        self.player2 = player2

        self.legal_action = False

        self.bot_names = ["QPlayer", "DbQPlayer", "NStepDouble", "NStepQ", "SARSA"]

        self.episodes = episodes

        self.state = None
        self.illegal_action = True

        for x in range(episodes):
            ## reset the environment to inital state
            self.reset_env()

            #### print state

            self.display_state(self.state)
            ## Let's a play game !!!
            self.playepisode(self.player1, self.player2)

            self.display_state(self.state)

        print(player1.name, "'s Record ", player1.record[0], "-", player1.record[1], "-", player1.record[2])

        print(player2.name, "'s record ", player2.record[0], "-", player2.record[1], "-", player2.record[2])


    @abstractmethod
    def reset_env(self):
        pass

    def reset_players_and_agents(self):

        if self.player1.name in self.bot_names:
            self.player1.set_state(self.state)
            self.player1.new_state = None

        if self.player2.name in self.bot_names:
            self.player2.set_state(self.state)
            self.player2.new_state = None

            ### console should display an empty respresentation of the environment at time step t for human player

    @abstractmethod
    def update_env(self, action, player):
        pass

    @abstractmethod
    def isgameover(self, player):
        pass

    @abstractmethod
    def iswinner(self, player):
        pass

    @abstractmethod
    def display_state(self, state):
        pass

    def directional_search(self, player, board, bound_x, bound_y, depth):

        ## depth parameter is specifies how many times we must get get a match before we can declare success

        ### This function searches a game board in a direction until it finds the piece if
        ## immeately if we fail to find the piece we are looking for or hit an edge then we go to our orginal position

        directions = [0, 1, 1, 0, 1, 1]

        ##### TEST for functionality in diagonal

        ## each row is now a direction
        directions = np.array(directions).reshape(3, 2)

        np.random.shuffle(directions)

        for z in range(len(directions)):

            Y, X = self.convert_point(a=int(player.action), bound_x=bound_x, bound_y=bound_y)

            count_piece = 0

            if Y + directions[z][0] < bound_y and X + directions[z][1] < bound_x:

                for x in range(depth):

                    Y = Y + directions[z][0]
                    X = X + directions[z][1]

                    # NOTE: TO SELF check if Y and X represent an actual point on the board before checking if the piece
                    ### If we fall off the edge no reason in continuing to search

                    if Y > bound_y - 1 or X > bound_x - 1:
                        break

                    if not board[Y][X] == player.piece:
                        break
                    else:
                        count_piece = count_piece + 1

                    if count_piece == depth:
                        return 1

            #### Searching in the opposite drection
            Y, X = self.convert_point(a=int(player.action), bound_x=bound_x, bound_y=bound_y)

            if Y - directions[z][0] > -1 and X - directions[z][1] > -1:

                for x in range(depth):
                    Y = Y - directions[z][0]
                    X = X - directions[z][1]

                    if Y < -1 or X < -1:
                        break

                    if not board[Y][X] == player.piece:
                        break
                    else:
                        count_piece = count_piece + 1

                    if count_piece == depth:
                        return 1

        return 0

    @abstractmethod
    def convert_point(self, a, bound_x, bound_y):
        pass

    def determine_outcome(self, player1, player2):

        if self.iswinner(player1):

            print("Winner is ", player1.name)

            player1.record[0] += 1
            player2.record[1] += 1

            if player1.name in self.bot_names:

                player1.set_state(self.state)

                player1.set_next_state(player1.state)
                if player1.name == 'SARSA':
                    player1.value_update(state=player1.state, new_state=player1.new_state, action=player1.action,
                                         reward=1,
                                         done=1, action2=player1.action2)
                else:
                    player1.value_update(state=player1.state, new_state=player1.new_state, action=player1.action,
                                         reward=1,
                                         done=1)

                if player2.name in self.bot_names:
                    player2.set_state(player2.state)
                    player2.set_next_state(self.state)

                    player2.value_update(state=player2.state, new_state=player2.new_state, action=player2.action,
                                         reward=-1, done=1)

        elif self.iswinner(player2):

            player2.record[0] += 1
            player1.record[1] += 1

            print("Winner is", player2.name)

            if player2.name in self.bot_names:
                player2.set_state(player2.state)
                player2.set_next_state(self.state)

                player2.value_update(state=player2.state, new_state=player2.new_state, action=int(player2.action),
                                     reward=1, done=1)

            if player1.name in self.bot_names:
                player1.set_state(player1.new_state)
                player1.set_next_state(self.state)

                if player1.name == 'SARSA':
                    player1.value_update(state=player1.state, new_state=player1.new_state, action=player1.action,
                                         reward=-1,
                                         done=1, action2=player1.action2)
                else:
                    player1.value_update(state=player1.state, new_state=player1.new_state, action=player1.action,
                                         reward=-1,
                                         done=1)



        else:
            print("TIE !!!")

            player2.record[2] += 1
            player1.record[2] += 1

            if player1.name in self.bot_names:
                player1.set_state(player1.new_state)
                player1.set_next_state(self.state)

                if player1.name == 'SARSA':
                    player1.value_update(state=player1.state, new_state=player1.new_state, reward=0,
                                         action=player1.action,
                                         done=1, action2=player1.action2)
                else:
                    player1.value_update(state=player1.state, new_state=player1.new_state, reward=0,
                                         action=player1.action,
                                         done=1, action2=None)

            if player2.name in self.bot_names:
                player2.set_state(player2.new_state)
                player2.set_next_state(self.state)

                if player2.name == 'SARSA':
                    player2.value_update(state=player2.state, new_state=player2.new_state, reward=0,
                                         action=player2.action,
                                         done=1, action2=player2.action2)
                else:
                    player2.value_update(state=player2.state, new_state=player2.new_state, reward=0,
                                         action=player2.action,
                                         done=1, action2=None)


    @abstractmethod
    def islegal_action(self, a):
        pass

    def playepisode(self, player1, player2):

        ## Do NOT override this method !!!!!!

        ### We only need one state variable for the environment describing its own representation after an action from a given agent

        while True:

            self.legal_action = False
            a = None

            while not self.legal_action:
                a = player1.executeaction()
                if type(a) is str:
                    a = int(a)

                self.legal_action = self.islegal_action(a)

            self.update_env(action=a, player=player1)

            if self.isgameover(player=player1):
                break

            if player2.name in self.bot_names:

                player2.set_next_state(self.state)

                if player2.name == "SARSA":
                    player2.value_update(state=player2.state, new_state=player2.new_state, action=player2.action,
                                         action2=player2.action2, reward=0)
                else:
                    player2.value_update(state=player2.state, new_state=player2.new_state, action=player2.action,
                                         action2=None, reward=0)

                player2.set_state(player2.new_state)
            else:
                self.display_state(self.state)

            self.legal_action = False

            while not self.legal_action:
                a = player2.executeaction()
                if type(a) is str:
                    a = int(a)
                self.legal_action = self.islegal_action(a)

            ## update our environment after executing actions onto it
            self.update_env(player2.action, player2)

            ## if the game is over we get out of the loop
            if self.isgameover(player=player2):
                break

            if player1.name in self.bot_names:

                player1.set_next_state(self.state)

                if player1.name == 'SARSA':
                    player1.value_update(player1.state, player1.new_state, player1.action, action2=player1.action2,
                                         reward=0)
                else:
                    player1.value_update(player1.state, player1.new_state, player1.action, action2=None, reward=0)

                player1.set_state(player1.new_state)

            else:
                ## Display the current state of the environment for  our human player
                self.display_state(self.state)

        ## By leaving the loop this game that we have been playing has terminated for some reason

        self.determine_outcome(player1, player2)


class TicTacToe(Twoplayerenv):
    def __init__(self, player1, player2, episodes=1):

        self.player1 = player1

        self.player2 = player2

        self.player1.piece = "X"

        self.player2.piece = "O"

        Twoplayerenv.__init__(self, player1=player1, player2=player2, episodes=episodes)

    def reset_env(self):

        self.state = np.zeros((3, 3), dtype=str)

        for y in range(len(self.state)):
            for x in range(len(self.state)):
                self.state[y][x] = ""

        ### Upon reseting the environment the agents representation of state is equal to that of Env

        self.reset_players_and_agents()

        return self.state

    def islegal_action(self, a):

        if a is None or a < 0 or a > 8:
            return False

        y, x = self.convert_point(bound_x=3, a=a)

        if not self.state[y][x] == "":
            return False

        return True

    def convert_point(self, a, bound_x, bound_y=None):

        pos_x = -1
        pos_y = 0

        if a == 0:
            return 0, 0

        for x in range(9):

            pos_x = pos_x + 1

            if x == a:
                return pos_y, pos_x

            if pos_x == bound_x - 1:
                pos_x = -1
                pos_y = pos_y + 1

    def isgameover(self, player):

        ## use directional search here

        board = np.array(self.state).reshape(3, 3)

        ## determine if game terminates due to a winner
        winner = self.directional_search(player=player, board=board, bound_x=board.shape[1], bound_y=board.shape[0],
                                         depth=2)

        ####### Hard coded fixing of directional search so the environment will terminate

        if player.piece == board[2][0] and player.piece == board[1][1] and player.piece == board[0][2]:
            winner = 1

        if player.piece == board[2][0] and player.piece == board[1][1] and player.piece == board[0][1]:
            winner = 0

        if player.piece == board[2][0] and player.piece == board[1][1] and player.piece == board[0][0]:
            winner = 0

        if player.piece == board[2][0] and player.piece == board[1][1] and player.piece == board[2][2]:
            winner = 0

        ## Terminate this function  if we determine the inputted is the winner as a result of their last action

        ## Inspect the entire state space to see if all the spaces are filled

        ### Determine if a tie took place
        tie = 1

        for y in range(len(self.state)):
            for x in range(len(self.state[y])):

                if self.state[y][x] == '':
                    tie = 0

        return tie or winner

    ## if we arrive here then one of these

    def display_state(self, state):

        print(state)

    def update_env(self, action, player):

        ## Player applies an action using their game onto the environment

        # action = int(action)

        y, x = self.convert_point(a=action, bound_x=3)

        self.state[y][x] = player.piece

    def iswinner(self, player):

        ## search in repsect of the direction if in fact that player is a winner

        board = np.array(self.state)

        board = board.reshape(3, 3)

        winner = 0

        #### Fix to get to recognize diagonal from other direction
        if player.piece == board[2][0] and player.piece == board[1][1] and player.piece == board[0][2]:
            winner = 1

        if player.piece == board[2][0] and player.piece == board[1][1] and player.piece == board[0][1]:
            winner = 0

        if player.piece == board[2][0] and player.piece == board[1][1] and player.piece == board[0][0]:
            winner = 0

        if player.piece == board[2][0] and player.piece == board[1][1] and player.piece == board[2][2]:
            winner = 0
        return self.directional_search(board=board, player=player, bound_x=board.shape[1], bound_y=board.shape[0],
                                       depth=2) or winner


############## Connect4 ENVIRONMENT !!!

class Connect4(Twoplayerenv):
    def __init__(self, player1, player2, episodes=1):

        player1.piece = "R"

        player2.piece = "O"

        Twoplayerenv.__init__(self, player1=player1, player2=player2, episodes=episodes)

    def reset_env(self):
        self.state = np.zeros((6, 7), dtype=str)

    def islegal_action(self, a):

        if a > 6:
            return False

        if a < 0:
            return False

        if not self.column_check(a):
            return False

        return True

    def fall(self, a):

        ## This method is returns the position where the piece will be placed on the board
        ## Fall takes one parameter a which is the action

        ############ For some reason we have bizzare values of a that are out of bounds
        print("Action Selected", a)

        ## IF this column is filled then -1 returned as we
        z = None
        ##### Make while loop terninating on the condition on the conditions of if we reach a piece or column is filled
        for x in (range(6)):

            if not self.state[x][a] == "R" or not self.state[x][a] == "O":
                z = x
            else:
                z = -1
        print("POsition Value", z)
        return z

    def column_check(self, a):

        #### This function will examine a column in the array to determine if a slot exists

        result = False
        for row in range(6):
            if not self.state[row][a] == "R" or not self.state[row][a] == "O":
                result = True

        return result

    def display_state(self, state):
        print(state)

    def iswinner(self, player):

        return self.directional_search(player=player, board=self.state,
                                       bound_x=self.state.shape[1], bound_y=self.state.shape[0], depth=3)

    def isgameover(self, player):

        winner = self.directional_search(player=player, board=self.state,
                                         bound_x=self.state.shape[1], bound_y=self.state.shape[0], depth=3)
        tie = True

        if not winner:

            ### if the player we check for is not a winner let's check to see if we have a tie
            for y in range(len(self.state)):
                for x in range(len(self.state[y])):

                    if self.state[y][x] == "":
                        tie = False

        return winner or tie

    def convert_point(self, a, bound_x, bound_y):
        y_coor = self.fall(a)

        return y_coor, a

    def update_env(self, action, player):

        ##### UPDATE method for Connect4
        pos = self.fall(action)

        self.state[pos][action] = player.piece
