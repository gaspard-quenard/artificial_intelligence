import numpy as np
import matplotlib.pyplot as plt

DISCOUNT_RATE = 1

def behaviour_policy(state):
    if (np.random.random() < 0.5):
        return "right"
    else:
        return "left"

def generate_episode(policy_func):
    episode = []
    episode_done = False
    while (not episode_done):
        action = policy_func("s")
        if (action == "right"):
            reward = 0
            episode_done = True
        else:
            if (np.random.random() < 0.1):
                reward = 1
                episode_done = True
            else:
                reward = 0
        episode.append(("s", action, reward))
    return episode


def value_evaluation(episodes):
    V = 0
    V_ordinary = []
    for index, episode in enumerate(episodes):
        importance_sampling_ratio = 1
        Gt = episode[-1][2]
        while (episode != []):
            #print(episode)
            (state, action, reward), *episode = episode
            if (action == "left"): # target policy always go left, and behavious policy go left with proba 1/2
                importance_sampling_ratio *= 2
            else:
                importance_sampling_ratio = 0 # pi(A|S) = 0
                break

        V += (Gt * importance_sampling_ratio)
        V_ordinary.append(V / (index+1))

    V_ordinary = np.asarray(V_ordinary)
    return V_ordinary

if __name__ == '__main__':
    number_runs = int(5*10e4)
    estimate_value_independent_run = []
    number_independent_run = 10
    for independent_run in range(number_independent_run):
        episodes = []
        print("{} / {}".format(independent_run, number_independent_run))
        for run in range(number_runs):
            episode = generate_episode(behaviour_policy)
            episodes.append(episode)
        plt.plot(value_evaluation(episodes))

    plt.xlim(1, number_runs)
    plt.ylim(0, 3)
    plt.xscale("log")
    plt.xlabel("Episodes (log scale)")

    plt.show()
