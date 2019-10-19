from abc import ABC, abstractmethod

import collections

import random

import pickle


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
    def __init__(self, alpha=.1, gamma=.9, epsilon=.05, decay=.99):
        self.values = collections.defaultdict(float)
        self.state = ""
        self.new_state = ""
        self.ALPHA = alpha
        self.reward = 0
        self.GAMMA = gamma
        self.EPSILON = epsilon
        self.DECAY = decay

        if epsilon < 0 or epsilon > 1:
            self.EPSILON = .05

        if alpha < 0 or alpha > 1:
            self.ALPHA = .1

        if gamma < 0 or gamma > 1:
            self.GAMMA = .9

    @abstractmethod
    def value_update(self, state, action, new_state, reward, done=0):
        pass

    def load(self):
        pass

    def save(self):
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

    def adjust_learning_rate(self, alpha, decay, done=0):
        if done:
            alpha = alpha * decay
        return alpha

    def epsilon_greedy_action_selection(self, action, epsilon):

        a = action

        if random.random() < epsilon:
            a = random.uniform(0, 10)

        ### return epsilon greedy action selection
        return a


class HumanPlayer(Player):
    def __init__(self):

        name = input("Please Enter your name ")
        Player.__init__(self, name=name)

    def executeaction(self):
        """

        :rtype: int
        """
        action = input("Select an action to execute ")

        if str.isdigit(action):

            action = int(action)
            self.action = action
        else:
            self.executeaction()

        print(type(action))

        return action


class QPlayer(Player, TabularRLAgent):
    def __init__(self, alpha=.1, name="QPlayer", gamma=.9, epsilon=.05):

        Player.__init__(self, name=name)

        TabularRLAgent.__init__(self, alpha=alpha, gamma=gamma, epsilon=epsilon)

    def bestactionandvalue(self, state):
        switch = 1
        best_value, best_action = None, None

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

        self.ALPHA = self.adjust_learning_rate(self.ALPHA, self.DECAY, done)

    def executeaction(self):
        ## compute best action in a given state
        _, action = self.bestactionandvalue(self.state)

        action = self.epsilon_greedy_action_selection(action, self.EPSILON)

        self.action = int(action)

        return int(action)


### This RL agent uses a technique known as Double Learning ,it can be applied to almost any TD method such as SARSA and Q-Learning
## This Agent will use double learning to avoid maximization bias obtained from the max operation in Q-Learning
class DoubleQPLayer(TabularRLAgent, Player):
    def __init__(self, alpha=.1, name="DbQPlayer", gamma=.9, epsilon=.05):
        self.v2 = collections.defaultdict(float)

        Player.__init__(self, name=name)

        TabularRLAgent.__init__(self, alpha=alpha, gamma=gamma, epsilon=epsilon)

    def value_update(self, state, action, new_state, reward=0, done=0):

        Z = random.uniform(0, 1)

        ### Updating of Q-values occurs here notice we are using two lookup table here, we basically flip a coin to determine which table we will update

        if Z > .5:
            a = self.best_action(self.values, new_state)

            self.values[(state, action)] = self.values[(state, action)] + self.ALPHA \
                                           * (reward + (
                    self.GAMMA * self.v2[(state, a)] - self.values[(state, action)]))
        elif Z < .5:

            a = self.best_action(self.v2, new_state)

            self.v2[(state, action)] = self.v2[(state, action)] + self.ALPHA \
                                       * (reward + (
                    self.GAMMA * self.values[(state, a)] - self.v2[(state, action)]))
        else:
            self.value_update(state, action, new_state, reward)

            self.ALPHA = self.adjust_learning_rate(self.ALPHA, self.DECAY, done)

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

        self.action = self.epsilon_greedy_action_selection(action=self.action, epsilon=self.EPSILON)

        return self.action


class NStepQAgent(Player, TabularRLAgent):
    def __init__(self, N, name="NStepQ", gamma=.9, alpha=.1, epsilon=.05):

        #### N step Boostrapping agent that performs Q-Learning updates using partial returns consisting of N steps

        self.N = N

        self.r = []

        self.actions = []

        self.states = []

        Player.__init__(self, name=name)
        TabularRLAgent.__init__(self, alpha=alpha, gamma=gamma, epsilon=epsilon)

    def value_update(self, state, action, new_state, reward, done=0):

        if not self.r:
            self.r.append(reward)
            self.actions.append(action)
            self.states.append(state)
        else:
            self.r.append(reward)
            self.actions.append(action)
            self.states.append(state)

        ## Store the trasition (s',a,r) in lists
        self.r.append(reward)
        self.states.append(new_state)
        self.actions.append(action)

        if len(self.r) == self.N + 1 or done:

            Gt = 0
            k = 0

            while not len(self.r) == 1:
                br = self.r.pop()
                ba = self.actions.pop()
                bs = self.states.pop()

                ### Compute the N-step return sum of future discounted reward
                Gt = br + (self.GAMMA ** k) * Gt

                k += 1

            s = self.states.pop()
            a = self.actions.pop()

            ####### Update our lookup table of Q-values using the N-step return that we just computed (Gt)
            self.values[(s, a)] = self.values[(s, a)] + self.ALPHA * (Gt - self.values[(s, a)])

            self.ALPHA = self.adjust_learning_rate(self.ALPHA, self.DECAY, done)

    def best_action(self, state):
        best_value = -1
        best_action = 0
        switch = 1

        for action in range(10):
            if self.values[(state, action)] > best_value:
                best_value = self.values[(state, action)]

                best_action = action

        if best_value != 0:
            switch = 0
        elif best_value == 0:
            switch = 1

        if switch:
            best_action = random.uniform(0, 10)

        return best_action

    def executeaction(self):

        ### Semi-Greedy Action Selection
        action = int(self.best_action(self.state))

        #### Epsilon Greedy Action Selection
        action = self.epsilon_greedy_action_selection(action, self.EPSILON)

        self.action = action

        return action


### This is an agent that theoretically aims decreasing bias to less than the Double or N-step agent
## This agent uses both N-step returns and Double Learning
#### Theoretical decrease in bias comes from taking N-step return and Double Learning
class NStepDoubleQAgent(Player, TabularRLAgent):
    def __init__(self, gamma=.9, alpha=.1, N=2, name="NStepDouble", epsilon=.05):

        Player.__init__(self, name=name)
        TabularRLAgent.__init__(self, alpha=alpha, gamma=gamma, epsilon=epsilon)

        self.N = N
        self.v2 = collections.defaultdict(float)

        self.r = []
        self.actions = []
        self.states = []


    def value_update(self, state, action, new_state, reward=0, done=0):

        if not self.r:
            self.r.append(reward)
            self.actions.append(action)
            self.states.append(state)
        else:
            self.states.append(state)
            self.actions.append(action)
            self.r.append(reward)

        if len(self.r) == self.N + 1 or done:

            Gt = 0
            k = 0

            while not len(self.states) > 1:
                br = self.r.pop()
                self.actions.pop()
                self.states.pop()

                ### Compute the N-step return sum of future discounted reward
                Gt = br + (self.GAMMA ** k) * Gt

                k += 1

            s = self.states.pop()
            a = self.actions.pop()

            Z = random.uniform(0, 1)

            ### Updating of Q-values occurs here notice we are using two lookup table here, we basically flip a coin to determine which table we will update
            #### Perform update using n-step partial return Gt
            if Z > .5:

                self.values[(s, a)] = self.values[(s, a)] + self.ALPHA \
                                      * (reward + (
                        Gt - self.values[(s, a)]))
            elif Z < .5:

                self.v2[(s, a)] = self.v2[(s, a)] + self.ALPHA \
                                  * (reward + (
                        Gt - self.v2[(s, a)]))
            else:
                self.value_update(state, action, new_state, reward, done)

            self.ALPHA = self.adjust_learning_rate(self.ALPHA, self.DECAY, done)

    def executeaction(self):
        Z = random.uniform(0, 1)
        if Z > .5:
            self.action = int(self.best_action(self.values, self.state))
        elif Z < .5:
            self.action = int(self.best_action(self.v2, self.state))
        else:
            ## If there are ties at which it is .5 we call the executeaction again
            self.executeaction()

            self.action = self.epsilon_greedy_action_selection(self.action, self.EPSILON)

        return self.action

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

        return int(best_action)
