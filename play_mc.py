import gym_2048
import gym
import copy
import random
import numpy as np

moves = [i for i in range(4)]
gamma = 0.9

def max_val(board):
    return np.asarray(board).max()

# return the discounted value of the Monte Carlo play
def play_randomly(env,num_steps=10):
    score = 0
    for i in range(num_steps):
        obs, rewards, done, info = env.step(random.choice(moves))
        score += (gamma**(i+i))*rewards
        if done:
            break
    return score
# returns the best movement based in the Monte Carlo search
# make copies of the board and play then
def mc_search(env, num_search=100):
    move_score = [0 for i in range(len(moves))]
    for i in range(len(moves)):
        envi = copy.deepcopy(env)
        obs, rewards, done, info = envi.step(i)
        games = [copy.deepcopy(envi) for i in range(num_search)]
        #Pick different seed than the game being played
        games = [games[i].seed(np.random.randint(0,10000)) for i in range(num_search)]
        scores= [rewards + play_randomly(games[i]) for i in range(num_search)]
        move_score[i] = np.mean(scores)
    return np.argmax(move_score)



# MAIN

env = gym.make("2048-v0")

max_tile = []
obs_ant = None
env.seed(42)
env.reset()    
while True:
    next_move = mc_search(env,200)
    obs, rewards, done, info = env.step(next_move)
    
    # uncomment to see board
    # env.render()
    # print("\n")
    
    if done:
        break
    obs_ant = obs
max_tile.append(max_val(obs_ant))
print(max_tile)