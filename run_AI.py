import gym_2048
import gym
import time

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

env = gym.make("2048-v0")
env.seed(42)
env.reset()
moves = 0

env = DummyVecEnv([lambda: env])

model = PPO2.load("player_2048")
obs = env.reset()
for i in range(10000):
    action,_states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    moves += 1
    print(rewards)
    print("Next Action: {}\nReward: {}".format(
         gym_2048.Base2048Env.ACTION_STRING[action[0]], rewards[0]))
    
    env.render()
    print("\n Total Moves: {}".format(moves))
    if dones[0]:
        time.sleep(5)
