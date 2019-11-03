import numpy as np
import matplotlib.pyplot as plt


actions_dict = {"Hit": 0, "Stick": 1}
returns = {} # a dictionary which link each state to a list of expected return for this state
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
    state = (np.random.randint(low=12, high=22), bool(np.random.randint(0, 2)), np.random.randint(1, 11))
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
        if (not exploring_start_done):
            if (np.random.random() < 0.5):
                action = actions_dict["Stick"]
            else:
                action = actions_dict["Hit"]
            exploring_start_done = True
        else:
            action = policy[state[0] - 12, int(state[1]), state[2] - 1]
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



def update_policy(action_value_function, policy, episode, debug=False):
    episode = episode[::-1]
    G = 0
    while (episode != []):
        reward, action, state, *episode = episode
        G = DISCOUNT_RATE * G + reward
        if (not (state, action) in returns):
            returns[state, action] = [0, 0]
        returns[state, action][1] += 1
        returns[state, action][0] = returns[state, action][0] - (returns[state, action][0] - G) / returns[state, action][1]
        action_value_function[state[0] - 12, int(state[1]), state[2]-1, int(action)] = returns[state, action][0]
        if (action_value_function[state[0] - 12, int(state[1]), state[2]-1, 0] == action_value_function[state[0] - 12, int(state[1]), state[2]-1,1]):
            policy[state[0] - 12, int(state[1]), state[2]-1] = np.random.randint(0, 2)
        else:
            policy[state[0] - 12, int(state[1]), state[2]-1] = np.argmax(action_value_function[state[0] - 12, int(state[1]), state[2]-1])
    debug_print(returns, debug)

    return action_value_function, policy


if __name__ == '__main__':
    action_value_function = np.ones((10, 2, 10, 2))*0.5 # Current sum (from 12 to 21),  usable ace, value of dealer one showing card (ace to 10), action (stick or hit)
    policy = np.zeros((10, 2, 10))
    policy[8:, :, :] = actions_dict["Stick"]
    number_episodes = int(10e5)
    for index_episode in range(number_episodes):
        if (index_episode % 1000 == 0):
            print("{} / {}".format(index_episode, number_episodes))
        episode = generate_episode(policy, debug=False)
        action_value_function, policy = update_policy(action_value_function, policy, episode)

    # plot policy
    fig, (ax1, ax2) = plt.subplots(figsize=(21, 21), ncols=2)
    im = ax1.imshow(np.flip(policy[:, 0, :], axis=0))

    #ax = plt.gca();
    ax1.set_xticks(np.arange(-.5, 10, 1));
    ax1.set_yticks(np.arange(-.5, 10, 1));
    ax1.set_xticklabels(np.arange(1, 11, 1));
    ax1.set_yticklabels(np.arange(22, 11, -1));
    ax1.grid(color='black', linestyle='-', linewidth=1)
    ax1.set_title("Appoximation of policy function after {} episodes\n without an usable ace".format(number_episodes))
    ax1.set_xlabel("Dealer showing")
    ax1.set_ylabel("Player sum")
    cbar = fig.colorbar(im, ax=ax1, ticks=range(2))
    cbar.ax.set_yticklabels(['Hit', 'Stick'])

    pos = ax2.imshow(np.flip(policy[:, 1, :], axis=0))
    ax2.set_title("Appoximation of policy function after {} episodes\n with an usable ace".format(number_episodes))
    ax2.set_xlabel("Dealer showing")
    ax2.set_ylabel("Player sum")
    ax2.set_xticks(np.arange(-.5, 10, 1));
    ax2.set_yticks(np.arange(-.5, 10, 1));
    ax2.grid(color='black', linestyle='-', linewidth=1)
    ax2.set_xticklabels(np.arange(1, 11, 1));
    ax1.set_yticklabels(np.arange(22, 11, -1));
    cbar2 = fig.colorbar(pos, ax=ax2, ticks=range(2))
    cbar2.ax.set_yticklabels(['Hit', 'Stick'])
    plt.show()
