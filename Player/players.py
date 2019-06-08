from abc import ABC, abstractmethod

import collections

import random

class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.action = -1

        ## wins[0] loses[1] , ties[2]
        self.record = [0] * 3

        ## game piece to execute actions with
        self.piece = ""

    @abstractmethod
    def executeaction(self):
        pass


class TabularRLAgent(ABC):
    def __init__(self,alpha = .1):
        self.values = collections.defaultdict(float)
        self.state = None
        self.new_state = None
        self.ALPHA = alpha
        self.reward = 0
        self.GAMMA = .99

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

        self.action = action

        return action



class QPlayer(Player, TabularRLAgent):
    def __init__(self,alpha=.01,name = "QPlayer"):

        Player.__init__(self,name = name)

        TabularRLAgent.__init__(self,alpha = alpha)

    def bestactionandvalue(self,state):
        switch = 1
        best_value, best_action = None, None
        for action in range(20):

            action_value = self.values[(state, action)]

            if best_value is None or best_value < action_value:
                best_value = action_value
                best_action = action
            if best_value != action_value:
                switch = 0

        if best_value == 0:
            switch = 1

        if switch:
            best_action = random.uniform(0,20)


        return best_value, best_action



    def value_update(self, state, action, new_state,reward = 0):

        prev_val = self.values[(state,action)]

        _,action_val = self.bestactionandvalue(new_state)


        self.values[(state,action)] = prev_val + self.ALPHA*( reward + self.GAMMA * (action_val - prev_val))




    def executeaction(self):
        ## compute best action in a given state
        print('QPlayer Executes')

        _,action = self.bestactionandvalue(self.state)

        self.action = action

        return action
