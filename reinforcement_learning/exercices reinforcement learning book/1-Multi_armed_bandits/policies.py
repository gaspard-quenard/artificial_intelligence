import numpy as np



class e_greedy_policy():
    def __init__(self, epsilon, number_actions, optimic_initalization=False, step_size=None):
        self.epsilon = epsilon
        self.number_actions = number_actions
        self.optimic_initalization = optimic_initalization
        self.step_size = step_size
        self.initialize()
        if (optimic_initalization):
            self.name = "e greedy optimic init (epsilon = " + str(self.epsilon) + ")"
        else:
            self.name = "e greedy (epsilon = " + str(self.epsilon) + ")"

    def initialize(self):
        if (self.optimic_initalization):
            self.estimate_values = np.ones(self.number_actions)*5  #Qt(a) for each actions
        else:
            self.estimate_values = np.zeros(self.number_actions)
        self.number_each_actions = np.zeros(self.number_actions)
        #self.cumul_reward_each_actions = np.zeros(self.number_actions)
        self.last_action_choosen = -1

    def choose_action(self):
        if (np.random.random() > self.epsilon):
            self.last_action_choosen = np.argmax(self.estimate_values)
        else:
            self.last_action_choosen = np.random.randint(0, self.number_actions)
        self.number_each_actions[self.last_action_choosen] += 1
        return self.last_action_choosen


    def update_estimate_values(self, reward_got):
        #self.cumul_reward_each_actions[self.last_action_choosen] += reward_got
        #self.estimate_values[self.last_action_choosen] = self.cumul_reward_each_actions[self.last_action_choosen] / self.number_each_actions[self.last_action_choosen]
        if self.step_size != None:
            self.estimate_values[self.last_action_choosen] = self.estimate_values[self.last_action_choosen] + (reward_got - self.estimate_values[self.last_action_choosen]) * self.step_size
        else:
            self.estimate_values[self.last_action_choosen] = self.estimate_values[self.last_action_choosen] + (reward_got - self.estimate_values[self.last_action_choosen]) / self.number_each_actions[self.last_action_choosen]



class UCB_policy():
    def __init__(self, c, number_actions):
        self.number_actions = number_actions
        self.epsilon = c
        self.t = 0
        self.name = "UCB (c = " + str(c) + ")"

    def initialize(self):
        self.estimate_values = np.zeros(self.number_actions)  #Qt(a) for each actions
        self.number_each_actions = np.zeros(self.number_actions)
        self.last_action_choosen = -1

    def choose_action(self):
        self.t += 1
        add_term =  (self.number_each_actions == 0) * (max(self.estimate_values) + 1) + (self.number_each_actions > 0) * (self.epsilon * np.sqrt(np.log(self.t) / (self.number_each_actions + ((self.number_each_actions  == 0) + 1))))
        self.last_action_choosen = np.argmax(self.estimate_values + add_term)
        self.number_each_actions[self.last_action_choosen] += 1
        return self.last_action_choosen

    def update_estimate_values(self, reward_got):
        self.estimate_values[self.last_action_choosen] = self.estimate_values[self.last_action_choosen] + (reward_got - self.estimate_values[self.last_action_choosen]) / self.number_each_actions[self.last_action_choosen]
