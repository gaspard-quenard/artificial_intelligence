import numpy as np
import matplotlib.pyplot as plt


NUM_STATES = 100
ACTIONS = np.arange(NUM_STATES)
PROBA_COIN_HEADS = 0.4
DISCOUNT_RATE = 1


def allowed_action(state, action):
    return action <= state and (action + state <= 100) # allowed if stake is inferior to capital


def expected_return(state, action, value_function):
    exp_return = PROBA_COIN_HEADS * (0 + DISCOUNT_RATE * value_function[state + action])
    exp_return += (1 - PROBA_COIN_HEADS) * (0 + DISCOUNT_RATE * value_function[state - action])
    return exp_return

def value_iteration(value_function):
    accuracy_estimation = 10
    value_function_array = []
    while (accuracy_estimation > 10e-20):
        old_value_function = value_function.copy()
        for state in range(1, NUM_STATES):
            all_expected_return = []
            for action in ACTIONS:
                if (allowed_action(state, action)):
                    all_expected_return.append(expected_return(state, action, value_function))
            value_function[state] = max(all_expected_return)
        accuracy_estimation = np.max(abs(value_function - old_value_function))
        print("accuracy_estimation: {}".format(accuracy_estimation))
        value_function_array.append(value_function.copy())
    plt.plot(value_function_array[0], label="sweep 1")
    plt.plot(value_function_array[1], label="sweep 2")
    plt.plot(value_function_array[2], label="sweep 3")
    plt.plot(value_function_array[-1], label="sweep " + str(len(value_function_array)))
    plt.legend()
    plt.xlabel("Capital")
    plt.ylabel("Value estimates")
    #plt.plot(value_function_array[1])
    plt.title("Value function")
    plt.show()
    return value_function




if __name__ == '__main__':
    value_function = np.zeros(NUM_STATES + 1)
    value_function[NUM_STATES] = 1
    value_function = value_iteration(value_function)
    policy = np.zeros(NUM_STATES)
    for state in range(1, NUM_STATES):
        all_expected_return = []
        test = []
        for action in ACTIONS[1:]:
            if (allowed_action(state, action)):
                test.append(action)
                all_expected_return.append(expected_return(state, action, value_function))
        #policy[state] = np.argmax(all_expected_return)
        policy[state] = np.argmax(np.round(all_expected_return, 6)) + 1 # Taken from # https://github.com/ShangtongZhang/reinforcement-learning-an-introduction/issues/83
    plt.plot(policy)
    plt.title("Final policy")
    plt.xlabel("Capital")
    plt.ylabel("Final policy")
    plt.show()
