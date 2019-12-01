import numpy as np
import matplotlib.pyplot as plt


class Environment():
    def __init__(self, number_states):
        self.number_states = number_states
        self.terminal_states = [0, number_states-1]

    def get_initial_state(self):
        return self.number_states // 2

    def step(self, state):
        """
        return tuple containing new state, reward and finished
        """
        action = -1
        reward = 0
        episode_finsished = False
        if (np.random.random() < 0.5):
            action = 1

        new_state = state + action
        if (new_state in self.terminal_states):
            episode_finsished = True
            if (new_state == self.number_states-1):
                reward = 1
            else:
                reward = -1
        return (new_state, reward, episode_finsished)


class Agent():
    def __init__(self, alpha, n_step, number_states):
        self.alpha = alpha
        self.discount_factor = 1
        self.n_step = n_step
        self.V = np.zeros(number_states)
        self.V[0] = self.V[-1] = 0
        self.cache = [] # Contain state and reward associate

    def initialize(self):
        self.V = np.zeros(number_states)
        self.V[0] = self.V[-1] = 0



def n_step_TD_prediction(env, agent):
    state = env.get_initial_state()
    agent.cache = []
    agent.cache.append({"state":state, "reward": 0})
    episode_finsished = False
    time_step = 0
    number_step_episode = np.inf
    tau = 0
    while (tau < number_step_episode - 1):
        if (time_step < number_step_episode):
            new_state, reward, episode_finsished = env.step(state)
            agent.cache.append({"state":new_state, "reward": reward})
            if (episode_finsished):
                number_step_episode = time_step + 1

        tau = time_step - agent.n_step + 1
        if (tau >= 0):
            G = 0
            for i in range(tau + 1, min(tau + agent.n_step + 1, number_step_episode + 1)):
                G += (agent.discount_factor ** (i - tau)) * agent.cache[i]['reward']
            if (tau + agent.n_step < number_step_episode):
                G += (agent.discount_factor ** agent.n_step) * agent.V[agent.cache[tau + agent.n_step]['state']]
            agent.V[agent.cache[tau]['state']] += agent.alpha * (G - agent.V[agent.cache[tau]['state']])

        state = new_state
        time_step +=1






if __name__ == '__main__':
    number_states = 21 # include the two final states
    number_episodes = 10
    number_runs = 100
    true_value = np.arange(-number_states+1, number_states+1, 2) / (number_states-1)
    true_value[-1] = true_value[0] = 0
    test = 0

    alphas = np.arange(0, 1.1, 0.1)
    n_steps = [1, 2, 4, 8, 16]
    results = np.zeros((len(n_steps), len(alphas)))
    env = Environment(number_states=number_states)
    for index_n_step, n_step in enumerate(n_steps):
        for index_alpha, alpha in enumerate(alphas):
            print("n_step: {}, alpha: {}".format(n_step, np.round(alpha, 2)))
            agent = Agent(alpha=alpha, n_step=n_step, number_states=number_states)
            result = 0
            for run in range(number_runs):
                agent.initialize()
                for episode in range(number_episodes):
                    n_step_TD_prediction(env, agent)
                    result += np.sqrt(((true_value[1:-1] - agent.V[1:-1])**2).mean())
            result /= number_runs * number_episodes
            results[index_n_step, index_alpha] = result
    for i in range(results.shape[0]):
        plt.plot(alphas, results[i, :], label="n=" + str(n_steps[i]))
    plt.legend()
    plt.ylim(0.25, 0.55)
    plt.xlabel("α")
    plt.ylabel("Root mean square error")
    plt.show()
