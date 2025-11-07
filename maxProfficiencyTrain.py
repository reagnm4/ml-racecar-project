from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3 import PPO
from main import RaceEnv

env = RaceEnv()
env.render_mode = None 

model = PPO.load("ppo_racecar_phase3", env=env)

checkpoint_callback = CheckpointCallback(
    save_freq=100_000,
    save_path="./checkpoints/",
    name_prefix="ppo_racecar"
)

model.learn(total_timesteps=500_000, callback=checkpoint_callback)

model.save("ppo_racecar_phase3")
env.close()