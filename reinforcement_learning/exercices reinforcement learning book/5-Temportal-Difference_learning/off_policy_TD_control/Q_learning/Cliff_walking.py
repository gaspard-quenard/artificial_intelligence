import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table

class Gridworld():
    def __init__(self):
        self.world = np.zeros((4, 12), dtype=np.int32)
        self.Cliff = 1
        self.world[3, 1:11] = self.Cliff
        self.dict_world_to_color = {0: 'white', self.Cliff: 'red'}
        self.starting_point = (3, 0)
        self.ending_point = (3, 11)

    def display(self, agent):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_axis_off()
        tb = Table(ax)

        nrows, ncols = self.world.shape
        width, height = 1.0 / ncols, 1.0 / ncols

        for (i, j), val in np.ndenumerate(self.world):
            if (i, j) == (agent.pos_y, agent.pos_x):
                tb.add_cell(row=i, col=j, width=width, height=height, facecolor=agent.color)
            if (i, j) == self.starting_point:
                tb.add_cell(row=i, col=j, width=width, height=height, text="Start", facecolor="b")
            elif (i, j) == self.ending_point:
                tb.add_cell(row=i, col=j, width=width, height=height, text="End", facecolor="g")
            else:
                tb.add_cell(row=i, col=j, width=width, height=height, facecolor=self.dict_world_to_color[val], loc="center")
        ax.add_table(tb)
        plt.title("The cliff gridworld")

        plt.plot()
        plt.show()

    def step(self, agent, action):
        episode_finsished = False
        reward = -1
        new_state = [agent.pos_y + action[0], agent.pos_x + action[1]]
        new_state = tuple([0 if val < 0 else val-1 if val >= self.world.shape[index] else val for index, val in enumerate(new_state)]) # manage the boundaries

        if (self.world[new_state] == self.Cliff):
            reward = -100
            new_state = self.starting_point

        elif (new_state == self.ending_point):
            episode_finsished= True
        return new_state, reward, episode_finsished



class Agent():
    def __init__(self):
        self.pos_x = self.pos_y = 0, 0
        self.actions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # left, right, down, up
        self.Q = np.zeros((4, 12, len(self.actions))) # state: width and height, and action (4 actions)
        self.policy = np.zeros((4, 12), dtype=np.int32) # e greedy policy
        self.epsilon = .1
        self.alpha = 0.5
        self.discount_factor = 1
        self.color = "black"

    def get_state(self):
        return self.pos_y, self.pos_x

    def choose_action(self, state):
        if (np.random.random() < self.epsilon):
            return self.actions[np.random.randint(len(self.actions))]
        else:
            return self.actions[self.policy[state]]

    def update_policy(self, state):
        self.policy[state] = np.argmax(self.Q[state])







def generate_episode(agent, gridwold, display=False):
    agent.pos_y, agent.pos_x = gridwold.starting_point
    if (display):
        gridwold.display(agent)

    sum_reward = 0
    episode_finsished = False
    while (not episode_finsished):
        state = agent.get_state()
        action = agent.choose_action(state)
        new_state, reward, episode_finsished = gridwold.step(agent, action) # Take action, observe R, S'

        sum_reward += reward
        index = state + (agent.actions.index(action), )
        #print("State: {}, action: {}, new state: {}, reward: {}".format(state, action, new_state, reward))
        agent.Q[index] = agent.Q[index] + agent.alpha * (reward + agent.discount_factor * np.max(agent.Q[new_state]) - agent.Q[index])
        agent.update_policy(state)

        agent.pos_y, agent.pos_x = new_state # S <- S'
        if (display):
            gridwold.display(agent)
    return sum_reward





if __name__ == '__main__':
    gridworld = Gridworld()

    #gridworld.display(agent)
    number_episodes = 500


    arr_reward = np.zeros((number_episodes))
    for i in range(500):
        print("{} / {}".format(i, 500))
        agent = Agent()
        for episode in range(number_episodes):
            arr_reward[episode] += generate_episode(agent, gridworld)

    plt.plot(arr_reward / 500)
    plt.title("Q learning")
    plt.xlabel("Episodes")
    plt.ylim(ymin=-100, ymax=-25)
    plt.ylabel("Sum of reward during episode")
    plt.show()
