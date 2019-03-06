import gym_2048
import gym


from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import DQN

env = gym.make("2048-v0")
env.seed(42)
env.reset()
moves = 0

env = DummyVecEnv([lambda: env])

model = DQN(MlpPolicy,env,verbose=0)
model.learn(total_timesteps=3*837209)
model.save("player_2048_dqn")
