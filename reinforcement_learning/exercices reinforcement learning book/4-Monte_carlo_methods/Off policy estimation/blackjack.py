import numpy as np
import matplotlib.pyplot as plt


actions_dict = {"Hit": 0, "Stick": 1}
DISCOUNT_RATE = 1

def draw_card():
    return min(np.random.randint(1, 14), 10)


def update_hand(current_hand, got_activate_ace, debug=False):
    card = draw_card()
    debug_print("cart drawn: {}".format(card), debug=debug)
    if (card == 1):
        if (current_hand + 11 > 21):
            current_hand += 1
        else:
            got_activate_ace = True
            current_hand += 11

    else:
        current_hand += card
        if (current_hand > 21 and got_activate_ace):
            current_hand -= 10
            got_activate_ace = False

    return (current_hand, got_activate_ace)

def debug_print(message, debug=False):
    if (debug):
        print(message)


def generate_episode(policy, debug=False):
    #state = inital_state
    state = (13, True, 2)
    #print("INIT STATE: {}".format(state))
    episode = []
    debug_print("-------------INITIALIZE DEALER GAME-----------------", debug)
    dealer_card = state[2]
    dealer_got_ace = False
    if (dealer_card == 1):
        dealer_got_ace = True
        dealer_card = 11
    dealer_card, dealer_got_ace = update_hand(current_hand=dealer_card, got_activate_ace=dealer_got_ace)
    debug_print("------------END INITIALIZE DEALER GAME-----------------\n", debug)
    episode_done = False
    exploring_start_done = False
    reward = 0
    turn_player_done = False
    while (not turn_player_done):
        episode.append(state)

        if (np.random.random() < 0.5):
            action = actions_dict["Stick"]
        else:
            action = actions_dict["Hit"]


        episode.append(action)
        reward = 0
        if (action == actions_dict["Stick"]):
            turn_player_done = True
        else:
            new_hand, new_active_ace = update_hand(current_hand=state[0], got_activate_ace=state[1])
            state = (new_hand, new_active_ace, state[2])
            if (new_hand > 21):
                reward = -1
                episode.append(reward)
                return episode
            else:
                episode.append(0)

    # dealer turn
    while (dealer_card < 17):
        debug_print("Dealer draw a card",  debug)
        dealer_card, dealer_got_ace = update_hand(current_hand=dealer_card, got_activate_ace=dealer_got_ace)
        if (dealer_card > 21):
            reward = 1
            episode.append(reward)
            return episode

    if (state[0] > dealer_card):
        reward = 1
    elif (state[0] == dealer_card):
        reward = 0
    else:
        reward = -1
    episode.append(reward)
    #debug_print("Episode: {}".format(episode), True)
    return episode



def policy_evaluation(episodes, weight_importante_sampling=False):
    """
    We estimate V(s) for state: (13, True, 2)
    """
    V = 0
    V_ordinary = []
    V_weight = []
    cumul_importance_sampling_ratio = 0
    for index, episode in enumerate(episodes):
        importance_sampling_ratio = 1
        Gt = episode[-1]
        while (episode != []):
            state, action, reward, *episode = episode
            if ((state[0] < 20 and action == actions_dict["Hit"]) or (state[0] >=20 and action == actions_dict["Stick"])):
                importance_sampling_ratio *= 2
            else:
                importance_sampling_ratio = 0 # pi(A|S) = 0
                break

        V += (Gt * importance_sampling_ratio)
        V_ordinary.append(V / (index+1))
        cumul_importance_sampling_ratio += importance_sampling_ratio
        if (cumul_importance_sampling_ratio == 0):
            V_weight.append(0)
        else:
            V_weight.append(V / cumul_importance_sampling_ratio)

    V_ordinary = np.asarray(V_ordinary)
    V_weight = np.asarray(V_weight)

    return (V_ordinary + 0.2767774)**2, (V_weight + 0.2767774)**2

if __name__ == '__main__':
    action_value_function = np.ones((10, 2, 10, 2)) # Current sum (from 12 to 21),  usable ace, value of dealer one showing card (ace to 10), action (stick or hit)
    policy = np.zeros((10, 2, 10))
    policy[8:, :, :] = actions_dict["Stick"]
    number_episodes = int(10e3) # -0.2767774
    V_mean1 = np.zeros(number_episodes)
    V_mean2 = np.zeros(number_episodes)
    number_runs = 100
    for i in range(number_runs):
        print("Run: {} / {}".format(i, number_runs))
        total_reward = 0
        episodes = []
        for index_episode in range(number_episodes):
            episode = generate_episode(policy, debug=False)
            total_reward += episode[-1]
            episodes.append(episode)
            #action_value_function, policy = update_policy(action_value_function, policy, episode)

        (V1, V2) = policy_evaluation(episodes, weight_importante_sampling=False)
        V_mean1 += V1
        V_mean2 += V2
        #V_mean2 += V2

    V_mean1 /= number_runs
    V_mean2 /= number_runs
    #mean_square_error_ordinary_sampling_ratio = (V_mean - (-0.2767774))**2
    plt.title("Estimation of the value of a single blackjack state from off-policy episodes")
    plt.ylim(0, 5)
    plt.xscale("log")
    plt.xlabel("Episodes (log scale)")
    plt.ylabel("Mean square error (average over 100 runs)")
    plt.plot(V_mean1, label='Ordinary importance sampling')
    plt.plot(V_mean2, label="Weight importance sampling")
    plt.legend()
    plt.show()
