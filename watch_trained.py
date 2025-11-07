from stable_baselines3 import PPO
from main import RaceEnv
import time

env = RaceEnv()
env.render_mode = "human"

model = PPO.load("ppo_racecar_phase3", env=env)

obs, info = env.reset()
for step in range(2000):
    action, _ = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action)
    env.render()
    time.sleep(0.02)
    if done or truncated:
        obs, info = env.reset()
env.close()