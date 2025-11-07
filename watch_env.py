from main import RaceEnv
import time

env = RaceEnv()
env.render_mode = "human"

obs, info = env.reset()
for step in range(500):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()
    print(f"Step {step} | Reward {reward:.3f} | Terminated {terminated}")
    if terminated or truncated:
        print("Episode ended — resetting")
        obs, info = env.reset()
    time.sleep(0.02)
env.close()