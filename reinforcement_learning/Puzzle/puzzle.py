import numpy as np
import matplotlib.pyplot as plt
import itertools
from p5 import *



class Board():
    def __init__(self, width, height, width_square):
        self.width = width
        self.height = height
        self.width_square = width_square
        self.ending_point = (3, 1)
        self.counter = 0
        self.initialize()
        self.initialize_array()

    def initialize(self):
        self.pieces = []
        self.pieces.append(Piece(0, 1, self.width_square, 2, 2))
        self.pieces.append(Piece(0, 0, self.width_square, 1, 2))
        self.pieces.append(Piece(0, 3, self.width_square, 1, 2))
        #self.pieces.append(Piece(0, 0, self.width_square, 1, 2))
        #self.pieces.append(Piece(0, 3, self.width_square, 1, 2))
        self.pieces.append(Piece(2, 1, self.width_square, 2, 1))
        #self.pieces.append(Piece(3, 1, self.width_square, 1, 1))
        self.pieces.append(Piece(3, 2, self.width_square, 1, 1))
        self.pieces.append(Piece(4, 1, self.width_square, 1, 1))
        self.pieces.append(Piece(4, 2, self.width_square, 1, 1))


    def initialize_array(self):
        self.all_pos_pieces1 = []
        self.all_pos_pieces3 = []

        for i in range(self.height - self.pieces[0].height + 1):
            for j in range(self.width - self.pieces[0].width + 1):
                self.all_pos_pieces1.append((i, j))
        print(len(self.all_pos_pieces1))


        self.all_pos_pieces2 = self.get_all_pos_piece2(self.pieces[2])
        print(len(self.all_pos_pieces2))

        for i in range(self.height - self.pieces[3].height + 1):
            for j in range(self.width - self.pieces[3].width + 1):
                self.all_pos_pieces3.append((i, j))
        print(len(self.all_pos_pieces3))


        self.all_pos_pieces4 = self.get_all_pos_piece4(self.pieces[4])
        print(len(self.all_pos_pieces4))


    def get_all_pos_piece2(self, piece):
        pos = []
        pos_1_piece = []
        for i in range(self.height - piece.height + 1):
            for j in range(self.width - piece.width + 1):
                pos_1_piece.append((i, j))
        for piece1 in pos_1_piece:
            controlled_squares_piece1 = [(piece1[0] + h, piece1[1] + w) for h in range(piece.height) for w in range(piece.width)]
            for piece2 in pos_1_piece:
                controlled_squares_piece2 = [(piece2[0] + h, piece2[1] + w) for h in range(piece.height) for w in range(piece.width)]
                if (len(set(controlled_squares_piece1) & set(controlled_squares_piece2)) == 0 and (piece2 + piece1) not in pos):
                    pos.append(piece1 + piece2)

        return pos

    def get_all_pos_piece4(self, piece):
        pos = list(itertools.combinations_with_replacement(range(20), 3))
        pos_2 = []
        for elemt in pos: # remove state with elements if same position
            if (elemt[0] in elemt[1:] or elemt[1] == elemt[2]):
                pass
            else:
                pos_2.append(elemt)
        pos_3 = [(val1 // self.width, val1 % self.width) + (val2 // self.width, val2 % self.width) + (val3 // self.width, val3 % self.width) for val1, val2, val3 in pos_2]
        return pos_3



    def get_state(self):
        state1 = self.all_pos_pieces1.index(self.pieces[0].get_pos()) # piece with width = 2 and height = 2
        a = sorted((self.pieces[1].get_pos(), self.pieces[2].get_pos()), key=lambda tup: (tup[0], tup[1]))
        state2 =  self.all_pos_pieces2.index(a[0] + a[1]) # piece with width = 1 and height = 2
        state3 = self.all_pos_pieces3.index(self.pieces[3].get_pos())
        b = sorted((self.pieces[4].get_pos(), self.pieces[5].get_pos(), self.pieces[6].get_pos()), key=lambda tup: (tup[0], tup[1]))
        #state4 =  self.all_pos_pieces4.index(b[0] + b[1] + b[2] + b[3])
        state4 =  self.all_pos_pieces4.index(b[0] + b[1] + b[2])
        state = (state1,) + (state2,) + (state3,) + (state4,)
        return state

    def step(self, action):
        reward = -1
        episode_finsished = False
        piece_choosen_index = action[0]
        new_state = tuple([self.pieces[piece_choosen_index].pos_y + action[1], self.pieces[piece_choosen_index].pos_x + action[2]])

        # First manage the boundaries
        if (new_state[0] < 0 or \
            new_state[1] < 0 or \
            new_state[0] + self.pieces[piece_choosen_index].height > self.height or \
            new_state[1] + self.pieces[piece_choosen_index].width > self.width):
            return self.get_state(), reward, episode_finsished


        controlled_squares = [(self.pieces[piece_choosen_index].pos_y + action[1] + h, self.pieces[piece_choosen_index].pos_x + action[2]  + w) for h in range(self.pieces[piece_choosen_index].height) for w in range(self.pieces[piece_choosen_index].width)]
        #print(controlled_squares)

        for index, piece in enumerate(self.pieces):
            if (index != piece_choosen_index):
                if (len(set(controlled_squares) & set(piece.controlled_squares)) > 0):
                    return self.get_state(), reward, episode_finsished


        self.pieces[piece_choosen_index].move_to((action[1], action[2]))
        if (piece_choosen_index == 0 and new_state == self.ending_point):
            #print("BRAVO")
            reward = 80
            episode_finsished = True

        return self.get_state(), reward, episode_finsished



    def draw(self):
        fill(100, 0, 0);
        rect((0, 0), self.width*self.width_square, self.height*self.width_square, mode='CORNER')

        for i in range(self.height):
          line((0, i*self.width_square),  (self.width_square*self.height, i*self.width_square))

        for i in range(self.width):
          line((i*self.width_square, 0), (i*self.width_square, self.width_square*self.height))

        for piece in self.pieces:
            piece.draw()

class Piece():
    def __init__(self, pos_y, pos_x, width_square, width, height):
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.controlled_squares = [(self.pos_y + h, self.pos_x + w) for h in range(self.height) for w in range(self.width)]
        self.width_square = width_square
        if (width * height == 1):
            self.color = Color(255, 0, 0)
        elif (width * height == 2):
            self.color = Color(0, 0, 255)
        else:
            self.color = Color(0, 255, 0)

    def move_to(self, new_pos):
        self.pos_y += new_pos[0]
        self.pos_x += new_pos[1]
        self.controlled_squares = [(self.pos_y + h, self.pos_x + w) for h in range(self.height) for w in range(self.width)]

    def draw(self):
        fill(0, 100, 0)
        stroke(0);
        rect((self.pos_x*self.width_square, self.pos_y*self.width_square), self.width*self.width_square, self.height*self.width_square, mode='CORNER')
        fill(self.color);
        circle(((self.pos_x + self.width/2 ) * self.width_square, (self.pos_y + self.height/2 ) * self.width_square), self.width_square/2);

    def get_pos(self):
        return (self.pos_y, self.pos_x)



class Agent():
    def __init__(self, number_pieces):
        self.actions = []
        for i in range(number_pieces): # left, right, down, up for each pieces
            self.actions.append((i, 0, 1))
            self.actions.append((i, 0, -1))
            self.actions.append((i, 1, 0))
            self.actions.append((i, -1, 0))
        self.Q = np.zeros((12, 108, 15, 1140, len(self.actions)))
        self.policy = np.zeros((12, 108, 15, 1140), dtype=np.int32) # e greedy policy
        self.initial_epsilon = 0.2
        self.epsilon = self.initial_epsilon
        self.alpha = 0.5
        self.discount_factor = 1

    def choose_action(self, state):
        if (np.random.random() < self.epsilon):
            return self.actions[np.random.randint(len(self.actions))]
        else:
            return self.actions[self.policy[state]]

    def update_policy(self, state):
        self.policy[state] = np.argmax(self.Q[state])



def setup():
    size(width_board*width_square, height_board*width_square)
    background(0)


def draw():
    board.draw()

def key_pressed(event):
    state = board.get_state()
    agent.update_policy(state)
    action = agent.choose_action(state)
    new_state, reward, episode_finsished = board.step(action) # Take action, observe R, S'
    index = state + (agent.actions.index(action), )
    #print("State: {}, action: {}, new state: {}, reward: {}".format(state, action, new_state, reward))
    agent.Q[index] = agent.Q[index] + agent.alpha * (reward + agent.discount_factor * np.max(agent.Q[new_state]) - agent.Q[index])
    save('frames_8_pieces/Frame_.jpg');
    board.counter += 1





def generate_episode_Q_learning(board, agent):
    episode = []
    safe_counter = 0
    episode_finsished = False
    board.initialize()
    while (safe_counter < 50000 and not episode_finsished):
        safe_counter += 1
        state = board.get_state()
        agent.update_policy(state)
        action = agent.choose_action(state)
        new_state, reward, episode_finsished = board.step(action) # Take action, observe R, S'
        #print("Step: {}\nState: {}\nAction: {}\nNew state: {}\nReward: {}\n".format(safe_counter, state, action, new_state, reward))
        index = state + (agent.actions.index(action), )
        agent.Q[index] = agent.Q[index] + agent.alpha * (reward + agent.discount_factor * np.max(agent.Q[new_state]) - agent.Q[index])
    return safe_counter


def generate_episode_sarsa(board, agent):
    episode = []
    safe_counter = 0
    episode_finsished = False
    state = board.get_state()
    action = agent.choose_action(state)
    board.initialize()
    while (safe_counter < 50000 and not episode_finsished):
        safe_counter += 1
        state = board.get_state()
        agent.update_policy(state)
        new_state, reward, episode_finsished = board.step(action) # Take action, observe R, S'
        new_action = agent.choose_action(new_state)
        #print("Step: {}\nState: {}\nAction: {}\nNew state: {}\nReward: {}\n".format(safe_counter, state, action, new_state, reward))
        index = state + (agent.actions.index(action), )
        new_index = new_state + (agent.actions.index(new_action),)
        agent.Q[index] = agent.Q[index] + agent.alpha * (reward + agent.discount_factor * agent.Q[new_index] - agent.Q[index])
        agent.update_policy(state)
        action = new_action
    return safe_counter







if __name__ == '__main__':
    width_board = 4
    height_board = 5
    width_square = 50

    board = Board(width_board, height_board, width_square)
    agent = Agent(len(board.pieces))

    #agent.Q = np.load("Q array_7_pieces.npy")

    counter_mean = []

    number_episodes = 30000
    for episode in range(number_episodes):
        print("{} / {}".format(episode, number_episodes))
        print(generate_episode_Q_learning(board, agent))
        if (episode % 10 == 0):
            agent.epsilon = 0
            mean = 0
            for i in range(10):
                mean += generate_episode_Q_learning(board, agent)
            counter_mean.append(mean)
            print("Episode: {} / {}, mean: {}".format(episode, number_episodes, mean / 10))
            agent.epsilon = agent.initial_epsilon - (agent.initial_epsilon / (number_episodes * 2)) * episode


    plt.plot([10 * index for index in range(len(counter_mean))], counter_mean)
    plt.ylabel("Number of step by episode")
    plt.xlabel("Episode")
    plt.show()

    np.save("Q array_7_pieces", agent.Q)

    board.initialize()
    agent.epsilon = 0
    run()
