import numpy as np
import matplotlib.pyplot as plt

states = ['END1', 'A', 'B', 'C', 'D', 'E', 'END2']
true_value = np.arange(len(states)) / 6
true_value[-1] = 0
terminal_states = ['END1', 'END2']
DISCOUNT_FACTOR = 1

def step(state):
    """
    return tuple containing new state, reward and finished
    """
    action = -1
    reward = 0
    episode_finsished = False
    if (np.random.random() < 0.5):
        action = 1
    new_state = states[states.index(state) + action]
    if (new_state in terminal_states):
        episode_finsished = True
        if (new_state == 'END2'):
            reward = 1
    return (new_state, reward, episode_finsished)


def TD_prediction(number_episodes, alpha=0.1):
    V = np.ones(len(states)) * 0.5
    V[0] = V[-1] = 0

    for episode in range(number_episodes):
        state = 'C'
        episode_finsished = False
        while (not episode_finsished):
            new_state, reward, episode_finsished = step(state)
            V[states.index(state)] = V[states.index(state)] + alpha*(reward + DISCOUNT_FACTOR*V[states.index(new_state)] - V[states.index(state)])
            state = new_state
    return V[1:-1]



def TD_compute_rms(alphas):
    V = np.ones((len(alphas), len(states))) * 0.5
    V[:, 0] = V[:, -1] = 0
    mean_square_err = np.zeros((len(alphas), 100))

    for episode in range(100):
        state = 'C'
        episode_finsished = False
        while (not episode_finsished):
            new_state, reward, episode_finsished = step(state)
            V[:, states.index(state)] = V[:, states.index(state)] + alphas*(reward + DISCOUNT_FACTOR*V[:, states.index(new_state)] - V[:, states.index(state)])
            state = new_state
        square_error = (V - true_value)**2

        mean_square_err[:, episode] = np.mean(square_error, axis=1)
    return mean_square_err



def generate_episode():
    """
    Geneate an episode for the MC evaluation
    """
    episode = []
    state = 'C'
    episode_finsished = False
    while (not episode_finsished):
        new_state, reward, episode_finsished = step(state)
        episode.append((state, reward))
        state = new_state

    return episode


def MC_compute_rms(alphas):
    V = np.ones((len(alphas), len(states))) * 0.5
    mean_square_err = np.zeros((len(alphas), 100))
    V[:, 0] = V[:, -1] = 0
    for episode_index in range(100):
        episode = generate_episode()
        G = 0
        episode = episode[::-1]
        for state, reward in episode:
            G = reward + DISCOUNT_FACTOR * G
            V[:, states.index(state)] = V[:, states.index(state)] + alphas*(G - V[:, states.index(state)])
        square_error = (V - true_value)**2
        mean_square_err[:, episode_index] = np.mean(square_error, axis=1)
    return mean_square_err






if __name__ == '__main__':
    number_episodes_arr = [0, 1, 10, 100]
    for number_episodes in number_episodes_arr:
        plt.plot(TD_prediction(number_episodes), label=str(number_episodes) + " episode(s)")
    plt.plot(np.arange(1, 6) / 6, label="True Value")
    plt.legend()
    plt.title("Estimated value")
    plt.xlabel("State")
    plt.xticks(range(0, 5), states[1:-1])
    plt.show()


    alphas_TD = np.array([0.15, 0.1, 0.05])
    mean_square_err_values = np.zeros((len(alphas_TD), 100))

    for i in range(100): # We want to average the RMS error get over 100 run
        mean_square_err_values += TD_compute_rms(alphas_TD)

    for i in range(len(alphas_TD)):
        plt.plot(mean_square_err_values[i] / 100, label="TD α=" + str(alphas_TD[i]))
    plt.legend()
    plt.title("Empirical RMS error, averaged over states")
    plt.xlabel("Episodes")


    alphas_MC = np.array([0.01, 0.02, 0.03, 0.04])
    mean_square_err_values = np.zeros((len(alphas_MC), 100))

    for i in range(100): # We want to average the RMS error get over 100 run
        mean_square_err_values += MC_compute_rms(alphas_MC)

    for i in range(len(alphas_MC)):
        plt.plot(mean_square_err_values[i] / 100, label="MC α=" + str(alphas_MC[i]))
    plt.legend()
    plt.title("Empirical RMS error, averaged over states")
    plt.xlabel("Episodes")
    plt.show()
