import numpy as np
import matplotlib.pyplot as plt

STATE = ['A', 'B', 'Final_state']
ACTIONS_A = [-1, 1] # left right
ACTIONS_B = range(10) # Let's say we have ten action in B which let to END_LEFT

class Agent():
    def __init__(self):
        self.cur_state = 'A'
        self.Q = [np.zeros(len(ACTIONS_A)), np.zeros(len(ACTIONS_B)), np.zeros(1)]
        self.policy = [np.random.choice(ACTIONS_A), np.random.choice(ACTIONS_B)] # Actions to choose on state A and B
        self.epsilon = 0.1
        self.alpha = 0.1
        self.discount_factor = 1

    def choose_action(self, state):
        if (np.random.random() < self.epsilon):
            if (self.cur_state == 'A'):
                return np.random.choice(ACTIONS_A)
            else:
                return np.random.choice(ACTIONS_B)
        else:
            if (self.cur_state == 'A'):
                return self.policy[0]
            else:
                return self.policy[1]

    def update_policy(self, state):
        if (state == 'A'):
            self.policy[STATE.index(state)] = ACTIONS_A[np.random.choice([index for index, value in enumerate(self.Q[STATE.index(state)]) if value == np.max(self.Q[STATE.index(state)])])]
        else:
            self.policy[STATE.index(state)] = ACTIONS_B[np.random.choice([index for index, value in enumerate(self.Q[STATE.index(state)]) if value == np.max(self.Q[STATE.index(state)])])]



def generate_episode(agent):
    agent.cur_state = 'A'
    number_left_action = 0
    episode_finsished = False
    while (not episode_finsished):
        state = agent.cur_state
        agent.update_policy(state)
        action = agent.choose_action(state)
        if (state == 'A'):
            idx_action = ACTIONS_A.index(action)
            reward = 0
            if (action == -1):
                number_left_action += 1
                new_state = 'B'
            else:
                new_state = 'Final_state'
                episode_finsished = True

        else:
            idx_action = ACTIONS_B.index(action)
            reward = np.random.normal(loc=-0.1, scale=1.0)
            new_state = 'Final_state'
            episode_finsished = True

        #print("State: {}, action: {}, new state: {}, reward: {}".format(state, action, new_state, reward))
        idx_state = STATE.index(state)
        agent.Q[idx_state][idx_action] = agent.Q[idx_state][idx_action] + agent.alpha * (reward + agent.discount_factor * np.max(agent.Q[STATE.index(new_state)]) - agent.Q[idx_state][idx_action])
        agent.update_policy(state)
        agent.cur_state = new_state

    return number_left_action


if __name__ == '__main__':
    number_episodes = 300
    number_runs = 5000
    left_actions = np.zeros(number_episodes)
    for run in range(number_runs):
        agent = Agent() # We initialize the agent
        print("{} / {}".format(run, number_runs))
        for episode in range(number_episodes):
            left_actions[episode] += generate_episode(agent)

    plt.plot((left_actions / number_runs) * 100)
    plt.yticks([5, 25, 50, 75, 100], labels=['5%', '25%', '50%', '75%', '100%'])
    plt.xlabel("Episodes")
    plt.ylabel("% left actions from A")
    plt.show()

    #print(left_actions[:100] / number_runs)
