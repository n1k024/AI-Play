
from abc import ABC, abstractmethod

import numpy as np



class Twoplayerenv(ABC):
    def __init__(self,player1,player2,episodes = 1):

        self.player1 = player1

        self.player2 = player2





        self.episodes = episodes

        self.state = None
        self.illegal_action = True

        for x in range(episodes):

            ## reset the environment to inital state
            self.reset_env()

            ## Let's a play game !!!
            self.playepisode(self.player1,self.player2)


    @abstractmethod
    def reset_env(self):
        pass

    @abstractmethod
    def update_env(self,action,player):
        pass

    @abstractmethod
    def isgameover(self,player):
        pass

    @abstractmethod
    def iswinner(self,player):
        pass
    def directional_search(self,player,board,bound_x,bound_y,depth):



        ### This function searches a game board in a direction until it finds the piece if
        ## immeately if we fail to find the piece we are looking for or hit an edge then we go to our orginal position


        directions= [0,1,1,0,1,1]


        ## each row is now a direction
        directions = np.array(directions).reshape(3,2)


        for direction in directions:

            Y, X = self.convert_point(a=player.action,bound=bound_x)

            count_piece = 0

            if Y + direction[0] < bound_y and X + direction[1] < bound_x:

                for x in range(depth):

                    Y = Y + direction[0]
                    X = X + direction[1]


                    if x== depth - 1:
                        result = 1
                    if not board[Y][X] == player.piece and Y > bound_y and X > bound_x:
                        break
                    else:
                        count_piece = count_piece + 1
                    if count_piece == depth:
                        return 1


            #### Searching in the opposite drection
            Y, X = self.convert_point(a=player.action,bound=bound_x)

            if Y - direction[0] > -1 and X - direction[1] > -1:
                Y = Y - direction[0]
                X = X - direction[1]

                for x in range(depth):
                    Y = Y - direction[0]
                    X = X - direction[1]


                    if not board[Y][X] == player.piece and Y < 0 and X < 0:
                        break
                    else:
                        count_piece = count_piece + 1

                    if count_piece == depth:
                        return 1


        return 0



    def convert_point(self,a,bound):
        pos_x = -1
        pos_y = 0

        for x in range(len(self.state)):

            pos_x = pos_x + 1



            if  x == a:
                return pos_y,pos_x



            if pos_x == bound:
                pos_x = 0
                pos_y = pos_y+1










    def determine_outcome(self,player1,player2):

        if self.iswinner(player1):

            player1.record[0] += 1
            player2.record[1] += 1

            if player1.name == "QPlayer":
                player1.set_reward(1)
                player1.value_update(player1.state, player1.new_state,1)

                if player2.name == "QPlayer":
                    player2.set_reward(-1)
                    player2.value_update(player2.state, player2.new_state,-1)

        if self.iswinner(player2):

            player2.record[0] +=1
            player1.record[1] +=1

            if player2.name == "QPlayer":
                player2.value_update(player2.state,player2.new_state,1)

                if player1.name == "QPlayer":
                    player1.set_reward(-1)
                    player1.value_update(player1.state, player1.new_state,-1)


        if not self.iswinner(player1) and player1.name == "QPlayer":

            player1.value_update(player1.state, player1.new_state,-1)

        if not self.iswinner(player2) and player2.name == "QPlayer":

            player2.value_update(player2.state, player2.new_state,-1)

        if not self.iswinner(player1) or self.iswinner(player2):

            player2.record[2] += 1
            player1.record[2] += 1

            if player1.name == "QPlayer":
                player1.set_reward(0)
                player1.value_update(player1.state, player1.new_state,0)

            if player2.name == "QPlayer":
                player2.value_update(player2.state, player2.new_state,0)
    @abstractmethod
    def islegal_action(self,a):
        pass

    def playepisode(self,player1,player2):

        ## Do NOT override this method !!!!!!

        ### We only need one state variable for the environment describing its own representation after an action from a given agent

             while True:

                    action = player1.executeaction()

                    while self.illegal_action:

                        if not self.islegal_action(action):


                            action = player1.executeaction()
                        else:
                            self.illegal_action = False


                    self.update_env(action,player1)

                    if self.isgameover(player=player1):
                        break

                    if player2.name == 'QPlayer':
                        player2.set_next_state(self.state)

                        player2.value_update(player1.state,player1.new_state)

                        player2.state = player2.new_state

                    self.illegal_action = True

                    action =  player2.executeaction()

                    while self.illegal_action:

                        if not self.islegal_action(action):

                            action = player2.executeaction()

                        else:

                            self.illegal_action = False

                    ## update our environment after executing actions onto it
                    self.update_env(action,player2)

                ## if the game is over we get out of the loop
                    if self.isgameover(player=player2):
                        break

                        # the enviornment needs to update its own state
                    if player2.name =="QPlayer":

                        player2.set_next_state(self.state)

                        player2.value_update(player2.state, player2.new_state)

                        player1.state = player1.new_state



        ## By leaving the loop this game that we have been playing has terminated for some reason

             self.determine_outcome(player1, player2)


class TicTacToe(Twoplayerenv):
    def __init__(self,player1,player2):

        self.player1.piece = "X"

        self.player2.piece = "O"



        Twoplayerenv.__init__(self, player1=player1,player2 = player2)


    def reset_env(self):
        self.state = ["-"] * 9



    ### Upon reseting the environment the agents representation of state is equal to that of Env

        if self.player1.name == "QPlayer":

            self.player1.state = self.state
        if self.player2.state == "QPlayer":

            self.player2.state = self.state

        return self.state

    def islegal_action(self,a):

        switch = True

        if  a < 0 and  a > 9 or not self.state[a] == "-":
            switch = False


            return switch


    def isgameover(self,player):
        gameover = 0


    ## Inspect the entire state space to see if all the spaces are filled

       ## use directional search here

        board = np.array(self.state).reshape(3,3)
        self.directional_search(player=player,board=board,bound_x=board.shape[0],bound_y=board.shape[1],depth=2)


        if gameover==1:
            return gameover






    def update_env(self, action,player):

        ## Player applies an action using their game onto the environment
        self.state[action] = player.piece






