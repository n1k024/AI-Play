from abc import ABC, abstractmethod

import collections

import random


class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.action = int(-1)

        ## wins[0] loses[1] , ties[2]
        self.record = [0] * 3

        ## game piece to execute actions with
        self.piece = ""

    @abstractmethod
    def executeaction(self):
        pass


class TabularRLAgent(ABC):
    def __init__(self, alpha=.1, gamma=.9):
        self.values = collections.defaultdict(float)
        self.state = ""
        self.new_state = ""
        self.ALPHA = alpha
        self.reward = 0
        self.GAMMA = gamma

    @abstractmethod
    def value_update(self, state, action, new_state, reward, done=0):
        pass

    def set_next_state(self, next_state):

        self.new_state = self.stringify(next_state)

    def set_reward(self, reward):
        self.reward = reward

    def set_state(self, state):
        self.state = self.stringify(state)

    def stringify(self, state):
        string_state = ""

        for y in range(len(state)):
            for x in range(len(state[y])):
                string_state = string_state + ',' + state[y][x]

        return string_state


class HumanPlayer(Player):
    def __init__(self):

        name = input("Please Enter your name ")
        Player.__init__(self, name=name)

    def executeaction(self):

        action = input("Select an action to execute ")

        if str.isdigit(action):

            action = int(action)
            self.action = action
        else:
            self.executeaction()

        print(action)

        return action


class QPlayer(Player, TabularRLAgent):
    def __init__(self, alpha=.01, name="QPlayer", gamma=.9):

        Player.__init__(self, name=name)

        TabularRLAgent.__init__(self, alpha=alpha, gamma=gamma)

    def bestactionandvalue(self, state):
        switch = 1
        best_value, best_action = None, None

        # state = self.stringify(state)

        for action in range(10):

            action_value = self.values[(state, action)]

            if best_value is None or best_value < action_value:
                best_value = action_value
                best_action = action
            if best_value != action_value:
                switch = 0

        if best_value == 0:
            switch = 1

        if switch:
            best_action = random.uniform(0, 10)

        return best_value, best_action

    def value_update(self, state, action, new_state, reward=0, done=0):

        prev_val = self.values[(state, action)]

        _, action_val = self.bestactionandvalue(new_state)

        self.values[(state, action)] = prev_val + self.ALPHA * (reward + (self.GAMMA * action_val - prev_val))

    def executeaction(self):
        ## compute best action in a given state
        print('QPlayer Executes')

        _, action = self.bestactionandvalue(self.state)

        self.action = action

        return action


### This RL agent uses a technique known as Double Learning ,it can be applied to almost any TD method such as SARSA and Q-Learning
## This Agent will use double learning to avoid maximization bias obtained from the max operation in Q-Learning
class DoubleQPLayer(TabularRLAgent, Player):
    def __init__(self, alpha=.1, name="DbQPlayer", gamma=.9):
        self.v2 = collections.defaultdict(float)

        Player.__init__(self, name=name)

        TabularRLAgent.__init__(self, alpha=alpha, gamma=gamma)

    def value_update(self, state, action, new_state, reward=0, done=0):

        Z = random.uniform(0, 1)

        ### Updating of Q-values occurs here notice we are using two lookup table here, we basically flip a coin to determine which table we will update

        if Z > .5:
            action = self.best_action(self.values, new_state)

            self.values[(state, action)] = self.values[(state, action)] + self.ALPHA \
                                           * (reward + (
                    self.GAMMA * self.v2[(state, action)] - self.values[(state, action)]))
        elif Z < .5:

            action = self.best_action(self.v2, new_state)

            self.v2[(state, action)] = self.v2[(state, action)] + self.ALPHA \
                                       * (reward + (
                    self.GAMMA * self.values[(state, action)] - self.v2[(state, action)]))
        else:
            self.value_update(state, action, new_state, reward)

    def best_action(self, values, state):
        best_value = -1
        best_action = 0
        switch = 1

        for action in range(10):
            if values[(state, action)] > best_value:
                best_value = values[(state, action)]

                best_action = action

        if best_value != 0:
            switch = 0
        elif best_value == 0:
            switch = 1

        if switch:
            best_action = random.uniform(0, 10)

        return best_action

    def executeaction(self):

        #### Here half the time we will execute actions using one looks up table and the rest of the time we will use the other table for our table to make its choice of action

        Z = random.uniform(0, 1)
        if Z > .5:
            self.action = self.best_action(self.values, self.state)
        elif Z < .5:
            self.action = self.best_action(self.v2, self.state)
        else:
            ## If there are ties at which it is .5 we call the executeaction again
            self.executeaction()

        return self.action


class NStepQAgent(Player, TabularRLAgent):
    def __init__(self, N, name, gamma=.9, alpha=.1):

        #### N step Boostrapping agent that performs Q-Learning updates using partial returns consisting of N steps

        self.N = N

        self.r = []

        self.actions = []

        self.states = []

        Player.__init__(self, name=name)
        TabularRLAgent.__init__(self, alpha=alpha, gamma=gamma)

    def value_update(self, state, action, new_state, reward, done=0):

        if not self.r:
            self.r.append(reward)
            self.actions.append(action)
            self.states.append(state)

        ## Store the trasition (s',a,r) in lists
        self.r.append(reward)
        self.states.append(new_state)
        self.actions.append(action)

        if len(self.r) == self.N + 1 or done:

            Gt = 0

            for x in range(self.N):
                br = self.r.pop()
                ba = self.actions.pop()
                bs = self.states.pop()

                ### Compute the N-step return sum of future discounted reward
                Gt = br + (self.GAMMA ** x) * Gt

            s = self.states.pop()
            a = self.actions.pop()

            ####### Update our lookup table of Q-values using the N-step return that we just computed (Gt)
            self.values[(s, a)] = self.values[(s, a)] + self.ALPHA * (Gt - self.values[(s, a)])

    def executeaction(self):

        ### Semi-Greedy Action Selection
        action = self.best_action(self.state)

        #### Epsilon Greedy Action Selection

        self.action = action

        return action
