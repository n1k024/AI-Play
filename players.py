from abc import ABC, abstractmethod

import collections


class Player(ABC):
    def __init__(self, name):
        self.name = name

        ## wins[0] loses[1] , ties[2]
        self.record = [0] * 3

        ## game piece to execute actions with
        self.piece = ""

    @abstractmethod
    def executeaction(self):
        pass

    ## To compare humans and robots
    def set_score(self,reward):
        self.score += reward

class TabularRLAgent(ABC):
    def __init__(self,alpha = .1):
        self.values = collections.defaultdict(float)
        self.state = None
        self.new_state = None
        self.ALPHA = alpha
        self.reward = 0
        self.GAMMA = .9

    @abstractmethod
    def value_update(self, state, action, new_state,reward):
        pass
    def set_next_state(self,next_state):
        self.new_state = next_state

    def set_reward(self,reward):
        self.reward = reward

class HumanPlayer(Player):
    def __init__(self):

        name = input("Please Enter your name")
        Player.__init__(self,name = name)


    def executeaction(self):

        action = input("Select an action to execute ")

        return action



class QPlayer(Player, TabularRLAgent):
    def __init__(self,alpha=.01,name = "QPlayer"):

        Player.__init__(self,name = name)

        TabularRLAgent.__init__(self,alpha = alpha)

    def bestactionandvalue(self,state):
        best_value = 0.0
        best_action = None

        ### add code to compute the best action in a given state

        return best_action,best_value

    def value_update(self, state, action, new_state,reward = 0):

        prev_val = self.values[(state,action)]

        _,action_val = self.bestactionandvalue(new_state)


        self.values[(state,action)] = prev_val + self.ALPHA*( reward + self.GAMMA*action_val - prev_val)




    def executeaction(self):
        ## compute best action in a given state
        print('QPlayer Executes')

        action,_ = bestactionandvalue(self.state)
        return action
