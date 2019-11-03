import numpy as np
import matplotlib.pyplot as plt


actions_dict = {"Hit": 0, "Stick": 1}
returns = {} # a dictionary which link each state to a list of expected return for this state
DISCOUNT_RATE = 1

def draw_card():
    return min(np.random.randint(1, 14), 10)

def initialize_game(debug = False):
    debug_print("-----------INITALIZE GAME------------------", debug)
    dealer_card = draw_card()
    player_card = 0
    player_got_ace = False
    while (player_card <= 11):
        player_card, player_got_ace = update_hand(player_card, player_got_ace)

    debug_print("-----------END INITIALIZE GAME ---------------\n", debug)
    return (player_card, player_got_ace, dealer_card)


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

def generate_episode(inital_state, policy, debug=False):
    state = inital_state
    #state = inital_state
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


def update_returns(episode, debug=False):
    episode = episode[::-1]
    G = 0
    while (episode != []):
        reward, action, state, *episode = episode
        G = DISCOUNT_RATE * G + reward
        if (not state in returns):
            returns[state] = []
        returns[state].append(G)
    debug_print(returns, debug)


def update_value_function(value_function):
    for state in returns:
        value_function[state[0] - 12, int(state[1]), state[2]-1] = np.round(sum(returns[state]) / len(returns[state]), decimals=2)
    return value_function


if __name__ == '__main__':
    value_function = np.zeros((10, 2, 10)) # Current sum (from 12 to 21),  usable ace, value of dealer one showing card (ace to 10)
    policy = np.zeros((10, 2, 10))
    policy[8:, :, :] = actions_dict["Stick"]
    number_episodes = int(3e5)
    for index_episode in range(number_episodes):
        print("{} / {}".format(index_episode, number_episodes))
        init_state = initialize_game(debug=False)
        episode = generate_episode(init_state, policy, debug=False)
        update_returns(episode)
    value_function = update_value_function(value_function)
    #print(value_function)

    fig, (ax1, ax2) = plt.subplots(figsize=(21, 21), ncols=2)
    pos = ax1.imshow(np.flip(value_function[:, 0, :], axis=0))
    ax1.set_xticks(np.arange(0, 10, 1));
    ax1.set_yticks(np.arange(0, 10, 1));
    ax1.set_xticklabels(np.arange(1, 11, 1));
    ax1.set_yticklabels(np.arange(21, 11, -1));
    ax1.set_title("Appoximation of state-value function after {} episodes\n without an usable ace".format(number_episodes))
    ax1.set_xlabel("Dealer showing")
    ax1.set_ylabel("Player sum")
    fig.colorbar(pos, ax=ax1)


    pos = ax2.imshow(np.flip(value_function[:, 1, :], axis=0))
    ax2.set_title("Appoximation of state-value function after {} episodes\n with an usable ace".format(number_episodes))
    ax2.set_xlabel("Dealer showing")
    ax2.set_ylabel("Player sum")
    ax2.set_xticks(np.arange(0, 10, 1));
    ax2.set_yticks(np.arange(0, 10, 1));
    ax2.set_xticklabels(np.arange(1, 11, 1));
    ax2.set_yticklabels(np.arange(21, 11, -1));
    fig.colorbar(pos, ax=ax2)
    plt.show()
