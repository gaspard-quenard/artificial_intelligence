import numpy as np
import matplotlib.pyplot as plt
from policies import *


class k_armed_bandit():
    def __init__(self, k):
        self.value_action = np.random.normal(loc=np.random.normal(), scale=1, size=k) # expected reward of each actions
        self.best_action = np.argmax(self.value_action)
        self.number_action = k
        #print("Real value action: {}".format(self.value_action))

    def print_reward_distribution(self):
        fig = plt.figure()
        fig.suptitle("Reward distribution for each actions")
        ax1 = fig.add_subplot(self.number_action, 1, 1)
        plt.hist(np.random.normal(loc=self.value_action[0], scale=1, size=100))
        for action in range(1, self.number_action):
            fig.add_subplot(self.number_action, 1, action+1, sharex=ax1)
            plt.hist(np.random.normal(loc=self.value_action[action], scale=1, size=100))
        plt.show()

    def get_reward_optimal_action(self):
        return np.random.normal(loc=max(self.value_action))

    def get_reward(self, action):
        return np.random.normal(loc=self.value_action[action])

    def is_optimal_action(self, action):
        return action == self.best_action



def run(policy, number_run=300, number_steps=1000):
    mean_reward_each_step = np.zeros(number_steps)
    percent_opt_action = np.zeros(number_steps)
    loss_policy = np.zeros(number_steps)
    for run in range(number_run):
        if (run % 100 == 0):
            print("run: {} / {}".format(run, number_run))
        env = k_armed_bandit(policy.number_actions)
        policy.initialize()
        for step in range(number_steps):
            action = policy.choose_action()
            reward = env.get_reward(action)
            policy.update_estimate_values(reward)
            loss_policy[step] += abs(env.value_action - policy.estimate_values).mean()
            mean_reward_each_step[step] += reward
            percent_opt_action[step] += env.is_optimal_action(action)

    loss_policy = loss_policy / number_run
    percent_opt_action = percent_opt_action / number_run
    mean_reward_each_step = mean_reward_each_step / number_run
    return loss_policy, percent_opt_action, mean_reward_each_step


def plot_result(policies_dict):
    for dict in policies_dict:
        plt.plot(dict["loss"], label=dict["name"])
    plt.title("Loss (how far away the policy is from the optimal policy)")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left')
    plt.xlabel("Steps")
    plt.ylabel("Loss")
    plt.show()
    for dict in policies_dict:
        plt.plot(dict["percent_opt_action"], label=dict["name"])
    plt.title("Percentage policy choose optimal action")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left')
    plt.xlabel("Steps")
    plt.ylabel("% optimal action")
    plt.show()
    for dict in policies_dict:
        plt.plot(dict["mean_reward_each_step"], label=dict["name"])
    plt.title("Average reward")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left')
    plt.xlabel("Steps")
    plt.ylabel("Average reward")
    plt.show()


if __name__ == '__main__':
    policies = []
    policies_dict = []
    #policies.append(e_greedy_policy(epsilon=0, number_actions=10)) # greedy policy
    policies.append(e_greedy_policy(epsilon=0.1, number_actions=10))
    policies.append(e_greedy_policy(epsilon=0, number_actions=10, optimic_initalization=True, step_size=0.1))
    #policies.append(UCB_policy(c=2, number_actions=10))

    for i, policy in enumerate(policies):
        print("Policy {} / {}".format(i+1, len(policies)))
        loss, percent_opt_action, mean_reward_each_step = run(policy, number_run=300, number_steps=1000)
        dictionary = {}
        dictionary["name"] = policy.name
        dictionary["loss"] = loss
        dictionary["percent_opt_action"] = percent_opt_action
        dictionary["mean_reward_each_step"] = mean_reward_each_step
        policies_dict.append(dictionary)
    plot_result(policies_dict)
