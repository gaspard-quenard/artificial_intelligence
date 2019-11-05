import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.table import Table




class racetrack():
    def __init__(self):
        self.NO_TRACK = 0
        self.STRATING_LINE = 2
        self.FINISH_LINE = 3
        self.TRACK = 1
        self.color_dict = {}
        self.color_dict[self.STRATING_LINE] = "g"
        self.color_dict[self.FINISH_LINE] = "r"
        self.color_dict[self.TRACK] = "w"
        self.dict_new_pos_each_step = {}
        self.dict_new_pos_each_step[(0, 0)] = [(0, 0)]
        self.track = self.generate_track()
        self.starting_positions = [index for index, value in np.ndenumerate(self.track) if value == self.STRATING_LINE]
        self.ending_positions = [index for index, value in np.ndenumerate(self.track) if value == self.FINISH_LINE]



    def generate_track(self):
        track = np.ones((10, 10), dtype=np.int32)
        track[5:, 0:4] = self.NO_TRACK
        track[0:2, 7:] = self.NO_TRACK
        track[5, 4:8] = self.NO_TRACK
        track[0:3, 4] = self.NO_TRACK
        track[4:6, 6] = self.NO_TRACK
        track[2:4:, 8:] = self.NO_TRACK
        track[0, :3] = self.STRATING_LINE
        track[-1, -3:] = self.FINISH_LINE
        return track

    def get_random_starting_line(self):
        random_index = np.random.randint(0, len(self.starting_positions))
        return self.starting_positions[random_index]

    def cross_finish_line(self, car):
        for i in range(car.vel_y + 1):
            for j in range(car.vel_x + 1):
                if ((car.pos_y + i, car.pos_x + j) in self.ending_positions):
                    return True
        return False


    def is_in_track(self, position_car):
        new_pos_y, new_pos_x = position_car
        pos_y_max, pos_x_max = self.track.shape
        if (new_pos_y < pos_y_max and new_pos_x < pos_x_max):
            return self.track[new_pos_y, new_pos_x]
        return self.NO_TRACK


    def go_to_dest(self, car):
        max_both_pos = max(abs(car.vel_x), abs(car.vel_y))
        min_both_pos = min(abs(car.vel_x), abs(car.vel_y))
        if ((max_both_pos, min_both_pos) not in self.dict_new_pos_each_step):
            self.add_in_pos_dict(car)
        for a, b in self.dict_new_pos_each_step[(max_both_pos, min_both_pos)]:
            if (abs(car.vel_y) >= abs(car.vel_x)):
                new_pos = car.pos_y + np.sign(car.vel_y)*a, car.pos_x + np.sign(car.vel_x)*b
            else:
                new_pos = car.pos_y +  np.sign(car.vel_y)*b, car.pos_x +  np.sign(car.vel_x)*a
            if (self.is_in_track(new_pos) == self.NO_TRACK):
                car.vel_x, car.vel_y = 0, 0
                car.pos_y, car.pos_x = self.get_random_starting_line()
                return -1
            elif (self.is_in_track(new_pos) == self.FINISH_LINE):
                return 0

        car.pos_y, car.pos_x = new_pos
        return -1


    def add_in_pos_dict(self, car):
        max_both_pos = max(abs(car.vel_x), abs(car.vel_y))
        min_both_pos = min(abs(car.vel_x), abs(car.vel_y))
        theta = math.atan(abs(min_both_pos / max_both_pos))
        new_pos_each_step = []
        for i in range(1, abs(max_both_pos) + 1):
            new_pos_each_step.append((i, int(((np.round(i*math.tan(theta), 0)) + 0.5) // 1)))
        self.dict_new_pos_each_step[(abs(max_both_pos), abs(min_both_pos))] = new_pos_each_step
        #print(self.dict_new_pos_each_step)




    def display(self, car):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_axis_off()
        tb = Table(ax)

        nrows, ncols = self.track.shape
        width, height = 1.0 / ncols, 1.0 / nrows

        for (i, j), val in np.ndenumerate(self.track):
            if (val != self.NO_TRACK):
                if ((i, j) != (car.pos_y, car.pos_x)):
                    tb.add_cell(row=i, col=j, width=width, height=height, facecolor=self.color_dict[val])
                else:
                    tb.add_cell(row=i, col=j, width=width, height=height, facecolor=car.color)
        ax.add_table(tb)

        plt.plot()
        plt.show()




class car():
    def __init__(self):
        self.pos_x, self.pos_y, self.vel_x, self.vel_y = 0, 0, 0, 0
        self.max_velocity = 3
        self.Q = np.ones((10, 10, self.max_velocity, self.max_velocity, 9))*(-10000) # pos y, pos x, vel y, vel x, action
        self.C = np.zeros((10, 10, self.max_velocity, self.max_velocity, 9)) # pos y, pos x, vel y, vel x, action
        self.target_policy = np.ones((10, 10, self.max_velocity, self.max_velocity), dtype=np.int32)*8
        self.actions = [(y, x) for y in range(-1, 2) for x in range(-1, 2)]
        self.color = "black"


    def behaviour_policy(self):
        """
        Choose randomly an action among those authorized
        """
        random_x = -self.vel_x
        random_y = -self.vel_y

        while (self.vel_x + random_x == 0 and self.vel_y + random_y == 0):
            if (self.vel_x == 0):
                random_x = np.random.randint(0, 2)
            elif (self.vel_x == self.max_velocity - 1):
                random_x = np.random.randint(-1, 1)
            else:
                random_x = np.random.randint(-1, 2)
            if (self.vel_y == 0):
                random_y = np.random.randint(0, 2)
            elif (self.vel_y == self.max_velocity - 1):
                random_y = np.random.randint(-1, 1)
            else:
                random_y = np.random.randint(-1, 2)

        return (random_y, random_x)

    def get_state(self):
        return (self.pos_y, self.pos_x, self.vel_y, self.vel_x)


def generate_episode(car, track):
    episode = []
    car.vel_x, car.vel_y = 0, 0
    car.pos_y, car.pos_x = track.get_random_starting_line()
    reward = -1
    counter = 0
    while (reward == -1):
        counter += 1
        state = car.get_state()
        action = car.behaviour_policy()
        car.vel_y += action[0]
        car.vel_x += action[1]
        reward = track.go_to_dest(car)

        if (reward == 0):
            episode.append((state, action, -1))
            break
        else:
            episode.append((state, action, -1))
    return episode

def policy_eval_improvement(episode, car):
    discount_factor = 1
    importance_sampling_ratio = 1
    episode = episode[::-1]
    G = 0
    while (episode != []):
        (state, action, reward), *episode = episode
        G = discount_factor * G + reward
        action_index = car.actions.index(action)
        index = state + (action_index, )
        car.C[index] += importance_sampling_ratio
        car.Q[index] += ((importance_sampling_ratio / car.C[index]) * (G - car.Q[index]))
        car.target_policy[state] = np.argmax(car.Q[state])
        if (action_index != car.target_policy[state]):
            return
        importance_sampling_ratio *= 9 # b(A | S) = 1 / 9



def try_policy(car, track):
    car.vel_y, car.vel_x = 0, 0
    car.pos_y, car.pos_x = track.get_random_starting_line()
    reward = -1
    secure_counter_bound = 20
    secure_counter = 0
    while (reward != 0 and secure_counter < secure_counter_bound):
        secure_counter += 1
        state = car.get_state()
        action = car.actions[car.target_policy[state]]
        car.vel_y += action[0]
        car.vel_x += action[1]

        reward = track.go_to_dest(car)
        print("State: {}, action: {}, reward: {}".format(state, action, reward))
        episode.append((state, action, reward))
        track.display(car)
        if (reward == 0):
            print("SUCCESS ! ")
            break



if __name__ == '__main__':
    track = racetrack()
    vehicle = car()
    number_episodes = 50
    for episode_index in range(number_episodes):
        print("episode: {} / {}".format(episode_index, number_episodes))
        episode = generate_episode(vehicle, track)
        policy_eval_improvement(episode, vehicle)

    try_policy(vehicle, track)
