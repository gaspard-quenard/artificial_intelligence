import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table

class Gridworld():
    def __init__(self):
        self.world = np.zeros((7, 10), dtype=np.int32)
        self.world[:, 3:6] = 1
        self.world[:, 6:8] = 2
        self.world[:, 8] = 1
        self.dict_world_to_color = {0: 'white', 1: 'b', 2: 'g'}
        self.dict_world_to_text = {0: '', 1: '↑', 2: '↑↑'}
        self.starting_point = (3, 0)
        self.ending_point = (3, 7)

    def display(self, agent):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_axis_off()
        tb = Table(ax)

        nrows, ncols = self.world.shape
        width, height = 1.0 / ncols, 1.0 / nrows

        for (i, j), val in np.ndenumerate(self.world):
            if (i, j) == (agent.pos_y, agent.pos_x):
                tb.add_cell(row=i, col=j, width=width, height=height, facecolor=agent.color)
            elif (i, j) == self.ending_point:
                tb.add_cell(row=i, col=j, width=width, height=height, facecolor="red")
            else:
                tb.add_cell(row=i, col=j, width=width, height=height, text=self.dict_world_to_text[val], facecolor=self.dict_world_to_color[val], loc="center")
        ax.add_table(tb)

        plt.plot()
        plt.show()

    def step(self, agent, action):
        episode_finsished = False
        reward = -1
        new_state = [agent.pos_y + action[0], agent.pos_x + action[1]]
        new_state[0] -= self.world[agent.pos_y, agent.pos_x]
        new_state = tuple([0 if val < 0 else val-1 if val >= self.world.shape[index] else val for index, val in enumerate(new_state)]) # manage the boundaries
        if (new_state == self.ending_point):
            episode_finsished= True
        return new_state, reward, episode_finsished



class Agent():
    def __init__(self):
        self.pos_x = self.pos_y = 0, 0
        self.actions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # left, right, down, up
        self.Q = np.zeros((7, 10, len(self.actions))) # state: width and height, and action (4 actions)
        self.policy = np.zeros((7, 10), dtype=np.int32) # e greedy policy
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







def generate_episode(agent, gridwold, display=False):
    agent.pos_y, agent.pos_x = gridwold.starting_point
    if (display):
        gridwold.display(agent)
    state = agent.get_state()
    action = agent.choose_action(state)
    episode_finsished = False
    time_step_to_end = 0
    while (not episode_finsished):
        time_step_to_end += 1
        state = agent.get_state()
        new_state, reward, episode_finsished = gridwold.step(agent, action)
        new_action = agent.choose_action(new_state)
        index = state + (agent.actions.index(action),)
        new_index = new_state + (agent.actions.index(new_action),)
        agent.Q[index] = agent.Q[index] + agent.alpha * (reward + agent.discount_factor * agent.Q[new_index] - agent.Q[index])
        agent.policy[state] = np.argmax(agent.Q[state])
        agent.pos_y, agent.pos_x = tuple(new_state)
        action = new_action
        if (display):
            gridwold.display(agent)
    return time_step_to_end




if __name__ == '__main__':
    gridworld = Gridworld()
    agent = Agent()
    number_episodes = 170
    """
    step_to_end_episode_arr = []
    for episode in range(number_episodes):
        step_to_end_episode_arr.append(generate_episode(agent, gridworld))
    print(step_to_end_episode_arr[-10:])
    plt.plot(step_to_end_episode_arr)
    plt.show()
    """
    arr = []
    time_step_total = 0
    for episode in range(number_episodes):
        time_step_total += generate_episode(agent, gridworld)
        arr.append(time_step_total)
    plt.plot(arr, range(170))
    plt.xlabel("Time steps")
    plt.ylabel("Episodes")
    plt.show()

    average_episode_length = 0
    for episode in range(100):
        average_episode_length += generate_episode(agent, gridworld)
    print("Average episode length: {}".format(average_episode_length / 100))

    agent.epsilon = 0 # turn off the exploration part
    generate_episode(agent, gridworld, display=True)
