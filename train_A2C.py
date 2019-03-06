import gym_2048
import gym


from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import SubprocVecEnv
from stable_baselines import A2C

env = gym.make("2048-v0")
env.seed(42)
env.reset()
moves = 0

n_cpu = 4
env = SubprocVecEnv([lambda: gym.make("2048-v0") for i in range(n_cpu)])

model = A2C(MlpPolicy,env,verbose=0)
model.learn(total_timesteps=3600000)
# model.learn(total_timesteps=3*837209)
model.save("player_2048_A2C")
