from stable_baselines3 import PPO
from main import RaceEnv

env = RaceEnv()
env.render_mode = None

model = PPO("MlpPolicy", env, verbose=1)
total_steps = 20000

model.learn(total_timesteps=total_steps)
model.save("ppo_racecar_debug")

env.close()