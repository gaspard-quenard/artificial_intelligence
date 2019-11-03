import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table
import math

# Some hyper parameters
DISCOUNT_RATE = 0.9
MAX_CAR_LOC_1 = 20
MAX_CAR_LOC_2 = 20

UPPER_BOUND_POISSON = 10
ACCURACY_ESTIMATION_BOUND = 0.01

ACTIONS = np.arange(-5, 6) # -x, we move x from second location to first location
                           # +x, we move x car from first location to second location

dict_action_color = {}
dict_action_color[0] = 'white'
dict_action_color[1] = 'cyan'
dict_action_color[2] = 'green'
dict_action_color[3] = 'blue'
dict_action_color[4] = 'magenta'
dict_action_color[5] = 'red'


def poisson(_lambda, n):
    return (_lambda**n) * np.exp(-_lambda) / math.factorial(n)


def expected_return(state, action, value_function):
    # First, we get the negative reward for the number of car we have moved
    exp_return = -2 * abs(action)

    new_state = get_new_state(list(state), action)

    # Then we make the sum of proba on the expected reward : p(r|s, pi(s))
    for rental_loc_1 in range(UPPER_BOUND_POISSON):
        for rental_loc_2 in range(UPPER_BOUND_POISSON):
            number_car_loc_1 = new_state[0]
            number_car_loc_2 = new_state[1]
            proba = poisson(_lambda=3, n=rental_loc_1) * poisson(_lambda=4, n=rental_loc_2)
            reward = min(new_state[0], rental_loc_1) * 10 + min(new_state[1], rental_loc_2) * 10
            number_car_loc_1 = number_car_loc_1 -  min(new_state[0], rental_loc_1) + 3  # Let's say the clients return 3 cars each day at location one
            if (number_car_loc_1 < 0):
                number_car_loc_1 = 0
            elif (number_car_loc_1 >= MAX_CAR_LOC_1):
                number_car_loc_1 = MAX_CAR_LOC_1 - 1

            number_car_loc_2 = number_car_loc_2 - min(new_state[1], rental_loc_2) + 2
            if (number_car_loc_2 < 0):
                number_car_loc_2 = 0
            elif (number_car_loc_2 >= MAX_CAR_LOC_2):
                number_car_loc_2 = MAX_CAR_LOC_2 - 1
            exp_return += proba*(reward + DISCOUNT_RATE * value_function[number_car_loc_1, number_car_loc_2])
    return exp_return




def get_new_state(state, action):
    state[0] -= action
    state[1] += action
    return state

def policy_evaluation(policy, value_function):
    accuracy_estimation = 10
    while (accuracy_estimation > ACCURACY_ESTIMATION_BOUND):
        new_value_function = np.zeros((MAX_CAR_LOC_1, MAX_CAR_LOC_2))
        for i in range(MAX_CAR_LOC_1):
            for j in range(MAX_CAR_LOC_2):
                action = int(policy[i, j])
                new_value_function[i, j] = expected_return((i, j), action, value_function)
        accuracy_estimation = np.max(abs(value_function - new_value_function))
        print("accuracy_estimation: {}".format(accuracy_estimation))
        value_function = new_value_function.copy()
    return value_function


def allowed_action(state, action): # zero if the action is not possible, 1 otherwise
    new_state = get_new_state(state, action)
    if (new_state[0] < 0 or new_state[0] >= MAX_CAR_LOC_1 or new_state[1] < 0 or new_state[1] >= MAX_CAR_LOC_2):
        return False
    return True


def policy_improvement(policy, value_function):
    new_policy = np.zeros((MAX_CAR_LOC_1, MAX_CAR_LOC_2), dtype=np.int32)
    for i in range(MAX_CAR_LOC_1):
        for j in range(MAX_CAR_LOC_2):
            max_value = -np.inf
            best_action = -1
            for action in ACTIONS:
                if (allowed_action(list((i, j)), action)):
                    Gt = expected_return((i, j), action, value_function)
                    if (Gt > max_value):
                        max_value = Gt
                        best_action = action
            new_policy[i, j] = best_action
    return new_policy


def print_policy(policy, i):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.ylim(MAX_CAR_LOC_1, 0)
    plt.yticks(np.arange(MAX_CAR_LOC_1, -1, step=-5))
    plt.xticks(np.arange(0, MAX_CAR_LOC_2 + 1, step=5))
    tb = Table(ax)
    plt.title(r"$π_" + str(i) + "$")

    nrows, ncols = policy.shape
    width, height = 1.0 / ncols, 1.0 / nrows

    policy = np.flip(policy, axis=0)

    for (i, j), val in np.ndenumerate(policy):
        tb.add_cell(row=i, col=j, width=width, height=height, text=str(policy[i,j]), loc='center', facecolor=dict_action_color[abs(policy[i, j])])

    ax.set_xlabel("Number car at second location", fontsize=12)
    ax.set_ylabel("Number car at first location", fontsize=12)
    ax.add_table(tb)
    plt.draw()
    while True:
        if plt.waitforbuttonpress(0):
            break
    plt.close(fig)




if __name__ == '__main__':
    value_function = np.zeros((MAX_CAR_LOC_1, MAX_CAR_LOC_2))
    policy = np.zeros((MAX_CAR_LOC_1, MAX_CAR_LOC_2), dtype=np.int32)
    i = 0

    while True:
        i += 1
        value_function = policy_evaluation(policy, value_function)
        new_policy = policy_improvement(policy, value_function)
        print("Enter a key to exit the display")
        print_policy(new_policy, i)
        if (np.array_equal(policy, new_policy)):
            print("Optimal policy reached !!")
            break
        else:
            print("Non optimal policy")
            policy = new_policy
