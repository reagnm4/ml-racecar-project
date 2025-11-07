from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3 import PPO
from main import RaceEnv

env = RaceEnv()
env.render_mode = None 

model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    learning_rate=3e-4,
    batch_size=64,
    n_steps=1024,
    gamma=0.99,
    tensorboard_log="./ppo_race_tensorboard/"
)

checkpoint_callback = CheckpointCallback(
    save_freq=20_000,
    save_path="./checkpoints/",
    name_prefix="ppo_racecar"
)

model.learn(total_timesteps=500_000, callback=checkpoint_callback)

model.save("ppo_racecar_phase3")
env.close()