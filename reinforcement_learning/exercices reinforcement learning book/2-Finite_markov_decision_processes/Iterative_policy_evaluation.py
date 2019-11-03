import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table

WIDTH_WORLD = 4
LENGTH_WORLD = 4

ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, down , left, right

TERMINAL_STATE = [(0, 0), (LENGTH_WORLD-1, WIDTH_WORLD-1)]


def random_policy(state):
    return 1 / len(ACTIONS)


def show_grids(value_function, time_step):
    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1)
    ax.set_axis_off()
    tb = Table(ax)
    plt.title(r"$V_" + str(time_step+1) + "$ for the random policy")

    nrows, ncols = value_function.shape
    width, height = 1.0 / ncols, 1.0 / nrows

    for (i, j), val in np.ndenumerate(value_function):
        tb.add_cell(row=i, col=j, width=width, height=height, text=val, loc='center')

    ax.add_table(tb)

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_axis_off()
    tb2 = Table(ax2)
    plt.title(r"Greedy policy on $V_" + str(time_step+1) + "$")


    for (i, j), val in np.ndenumerate(value_function):
        if (i, j) in TERMINAL_STATE:
            text = ""
        else:  # Compute the greedy policy by using the value function
            max_action = -np.inf
            max_action_index = []
            for index, action in enumerate(ACTIONS):
                new_pos = manage_boundaries((i + action[0], j + action[1]))
                if (value_function[new_pos] == max_action): # There are multiple optimal actions
                    max_action_index.append(index)
                elif (value_function[new_pos] > max_action):
                    max_action = value_function[new_pos]
                    max_action_index = [index]
            text = "{} {} {} {}".format((0 in max_action_index)*"↑", (2 in max_action_index)*"←", (3 in max_action_index)*"→", (1 in max_action_index)*"↓")
        tb2.add_cell(row=i, col=j, width=width, height=height, text=text, loc='center')
    ax2.add_table(tb2)
    print("Use q to close the figure")
    plt.draw()
    plt.show()


def manage_boundaries(position):
    new_pos = list(position)
    if (position[0] < 0):
        new_pos[0] = 0
    elif (position[0] >= LENGTH_WORLD):
        new_pos[0] = LENGTH_WORLD - 1

    if (position[1] < 0):
        new_pos[1] = 0
    elif (position[1] >= WIDTH_WORLD):
        new_pos[1] = WIDTH_WORLD - 1
    return tuple(new_pos)


def update_value_function(value_function, grid_world_reward):
    new_value_function = np.zeros(value_function.shape)
    for (i, j), val in np.ndenumerate(value_function):
        if (i, j) in TERMINAL_STATE:
            new_value_function[(i, j)] = 0 # For all pol(a|s), we have r = 0 + gamma * V(s') with s' = s, and V(s) = 0
        else:
            for action in ACTIONS:
                new_pos = manage_boundaries((i + action[0], j + action[1]))
                new_value_function[(i, j)] += random_policy(state=(i, j)) * (grid_world_reward[new_pos] + value_function[new_pos])

    return np.around(new_value_function, decimals=1)


if __name__ == '__main__':
    grid_world_reward = np.ones((LENGTH_WORLD, WIDTH_WORLD)) * -1
    value_function = np.zeros((LENGTH_WORLD, WIDTH_WORLD))
    show_grids(value_function, 0)
    total_time_step = 5

    for time_step in range(total_time_step):
        print("Time step: {}/{}".format(time_step+1, total_time_step))
        value_function = update_value_function(value_function, grid_world_reward)
        show_grids(value_function, time_step)
