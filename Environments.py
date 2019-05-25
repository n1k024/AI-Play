
from abc import ABC, abstractmethod



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
    def isgameover(self):
        pass

    @abstractmethod
    def iswinner(self,player):
        pass


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

                    if self.isgameover():
                        break

                    if player1.name == 'QPlayer':
                        player1.set_next_state(self.state)

                        player1.value_update(player1.state,player1.new_state)

                        player1.state = player1.new_state

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
                    if self.isgameover():
                        break

                        # the enviornment needs to update its own state
                    if player2.name =="QPlayer":

                        player2.set_next_state(self.state)

                        player2.value_update(player2.state, player2.new_state)

                        player2.state = player2.new_state



        ## By leaving the loop this game that we have been playing has terminated for some reason

             self.determine_outcome(player1, player2)


class TicTacToe(Twoplayerenv):
    def __init__(self,player1,player2,episodes = 1):

        self.player1.piece = "X"

        self.player2.piece = "O"


        Twoplayerenv.__init__(self, player1=player1,player2 = player2,episodes = episodes)


    def reset_env(self):
        self.state = ["-"] * 9

        self.player1.state = self.state

        self.player2 = self.state


    ### Upon reseting the environment the agents representation of state is equal to that of Env

        if self.player1.name == "QPlayer":

            self.player1.state = self.state
        if self.player2.state == "QPlayer":

            self.player2.state = self.state

    def islegal_action(self,a):

        switch = 0

        if not a > -1 and not a < 9:
            switch = 1

        if not self.state[a] == "-":
            switch = 1

            return switch


    def isgameover(self):
        gameover = 0

        for s in self.state:


            if s =='-':
                gameover = 0

    def update_env(self, action,player):

        ## Player applies an action using their game onto the environment
        self.state[action] = player.piece






