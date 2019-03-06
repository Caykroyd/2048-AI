import gym_2048
import gym
import time
import numpy as np
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import A2C

env = gym.make("2048-v0")
env.seed(42)
env.reset()
moves = 0

env = DummyVecEnv([lambda: env])

model = A2C.load("player_2048_A2C")
obs = env.reset()
obs_ant = None
max_tile = []
sum_tiles = []

def max_val(board):
    return np.asarray(board).max()

for i in range(10000):
    action,_states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    moves += 1
    if done[0]:
        # print("\n Total Moves: {}".format(moves))
        # print(obs_ant)
        max_tile.append(max_val(obs_ant))
        moves = 0

    obs_ant = obs


x = [i for i in range(len(max_tile))]
import matplotlib.pyplot as plt
plt.plot(x,max_tile,'ro')
plt.title("A2C")
plt.xlabel("Game")
plt.ylabel("Max tile")
plt.show()

from utils import avg_value
print("64:",avg_value(64,max_tile))
print("128:",avg_value(128,max_tile))
print("256:",avg_value(256,max_tile))
