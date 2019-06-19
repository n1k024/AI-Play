
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

            #### print state

            print(self.state)

            ## Let's a play game !!!
            self.playepisode(self.player1,self.player2)



        print("Player1's Record ",player1.record[0],"-",player1.record[1],"-",player1.record[2])

        print("Player2's record ",player2.record[0],"-",player2.record[1],"-",player2.record[2])


    @abstractmethod
    def reset_env(self):
        pass
    def reset_players_and_agents(self):


        if self.player1.name == "QPlayer":

            self.player1.state = self.state
            self.player1.new_state = None

        if self.player2.state == "QPlayer":

            self.player2.state = self.state
            self.player2.new_state = None


            ### console should display an empty respresentation of the environment at time step t for human player


    @abstractmethod
    def update_env(self,action,player):
        pass

    @abstractmethod
    def isgameover(self,player):
        pass

    @abstractmethod
    def iswinner(self,player):
        pass
    @abstractmethod
    def display_state(self,state):
        pass


    def directional_search(self,player,board,bound_x,bound_y,depth):

        ## depth parameter is specifies how many times we must get get a match before we can declare success

        ### This function searches a game board in a direction until it finds the piece if
        ## immeately if we fail to find the piece we are looking for or hit an edge then we go to our orginal position


        directions= [0,1,1,0,1,1]



        ##### TEST for functionality in diagonal

        #directions = [1,1]


        ## each row is now a direction
        directions = np.array(directions).reshape(3,2)

        np.random.shuffle(directions)

        #print(directions)



        for z in range(len(directions)):

            Y, X = self.convert_point(a=int(player.action),bound=bound_x)



            count_piece = 0
            
            if Y + directions[z][0] < bound_y   and X + directions[z][1] < bound_x:

                for x in range(depth):

                    Y = Y + directions[z][0]
                    X = X + directions[z][1]


                    #NOTE: TO SELF check if Y and X represent an actual point on the board before checking if the piece
                    ### If we fall off the edge no reason in continuing to search

                    if Y > bound_y - 1 or X > bound_x - 1:
                        break

                    if not board[Y][X] == player.piece:
                        break
                    else:
                        count_piece = count_piece + 1

                    if count_piece == depth:
                        return 1

            print("Number of pieces",count_piece)

            #### Searching in the opposite drection
            Y, X = self.convert_point(a=int(player.action),bound=bound_x)


            if Y - directions[z][0] > -1 and X - directions[z][1] > -1:


                for x in range(depth):
                    Y = Y - directions[z][0]
                    X = X - directions[z][1]


                    if  Y < -1 or X < -1:
                        break

                    if not board[Y][X] == player.piece:
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

            if x == a:
                return pos_y, pos_x




            if pos_x == bound -1:
                pos_x = -1
                pos_y = pos_y + 1






    def determine_outcome(self,player1,player2):

        if self.iswinner(player1):

            print("Winner is ",player1.name)

            player1.record[0] += 1
            player2.record[1] += 1

            if player1.name == "QPlayer":
                player1.value_update(player1.state, player1.new_state,1)

                if player2.name == "QPlayer":
                    player2.value_update(player2.state, player2.new_state,-1)

        elif self.iswinner(player2):

                player2.record[0] += 1
                player1.record[1] += 1

                print("Winner is", player2.name)

                if player2.name == "QPlayer":
                    player2.value_update(player2.state,player2.new_state,1)

                if player1.name == "QPlayer":
                    player1.value_update(player1.state, player1.new_state,-1)

        else:

                print("TIE !!!")

                player2.record[2] += 1
                player1.record[2] += 1

                if player1.name == "QPlayer":
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



                    while not self.islegal_action(player1.action):


                         player1.executeaction()


                    self.update_env(action=player1.action,player=player1)

                    if self.isgameover(player=player1):
                        break


                    if player2.name == 'QPlayer':
                        player2.set_state(player2.state)

                        player2.set_next_state(self.state)

                        player2.value_update(state=player2.state, new_state=player2.new_state, action=player2.action)

                        player2.set_state(player2.new_state)
                    else:
                        self.display_state(self.state)




                    while not self.islegal_action(player2.action):


                             player2.executeaction()


                    ## update our environment after executing actions onto it
                    self.update_env(player2.action,player2)

                ## if the game is over we get out of the loop
                    if self.isgameover(player=player2):
                        break


                    if player1.name =="QPlayer":

                        player1.set_next_state(self.state)

                        player1.value_update(player1.state, player1.new_state,action=player1.action)

                        player1.state = player1.new_state
                    else:
                        ## Display the current state of the environment for  our human player
                        self.display_state(self.state)




        ## By leaving the loop this game that we have been playing has terminated for some reason

             self.determine_outcome(player1, player2)


class TicTacToe(Twoplayerenv):
    def __init__(self,player1,player2,episodes = 1):

        self.player1 = player1

        self.player2 = player2

        self.player1.piece = "X"

        self.player2.piece = "O"



        Twoplayerenv.__init__(self, player1=player1,player2 = player2,episodes=episodes)





    def reset_env(self):
        self.state = ["-"] * 9



    ### Upon reseting the environment the agents representation of state is equal to that of Env

        self.reset_players_and_agents()


        return self.state

    def islegal_action(self,a):

        switch = True


        a = int(a)


        if  a < 0 or  a > 8:
            return False

        if not self.state[a]== "-":
            return  False


        return switch


    def isgameover(self,player):

        ## use directional search here

        board = np.array(self.state).reshape(3, 3)

        ## determine if game terminates due to a winner
        winner = self.directional_search(player=player, board=board, bound_x=board.shape[1], bound_y=board.shape[0],
                                         depth=2)

        ## Terminate this function  if we determine the inputted is the winner as a result of their last action

        if winner:
            print("Terminating due to winner")
            return winner


    ## Inspect the entire state space to see if all the spaces are filled

        ### Determine if a tie took place
        tie = 1

        for x in range(len(self.state)):

            if self.state[x] =='-':
                tie = 0

        return tie or winner


## if we arrive here then one of these


    def display_state(self,state):

        board = np.array(state).reshape(3,3)

        print(board)




    def update_env(self, action,player):

        ## Player applies an action using their game onto the environment

        action = int(action)

        self.state[action] = player.piece

    def iswinner(self,player):

        ## search in repsect of the direction if in fact that player is a winner

        board = np.array(self.state)

        board = board.reshape(3,3)


        return self.directional_search(board=board,player=player,bound_x=board.shape[1],bound_y=board.shape[0],depth=2)






