import pygame
import sys
import math
import numpy as np
import gymnasium as gym
from gymnasium import spaces

class RaceEnv(gym.Env):
    def __init__(self):
        pygame.init()

        self.info = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.info.current_w, self.info.current_h), pygame.NOFRAME)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 25)
        
        self.track_surface = pygame.image.load("assets/track.png").convert()
        self.track_surface = pygame.transform.scale(self.track_surface, (self.info.current_w, self.info.current_h))
        self.car_image = pygame.image.load("assets/car.png").convert_alpha()
        self.car_image = pygame.transform.scale(self.car_image, (40, 75))


        self.acceleration = 0.2
        self.max_speed = 8
        self.rotation_speed = 6
        self.friction = 0.05

        self.num_sensors = 5
        self.sensor_angles = [-45, -25, 0, 25, 45]
        self.sensor_max_distance = 300

        self.observation_space = spaces.Box(low=0, high=1, shape=(7,), dtype=np.float32)
        self.action_space = spaces.Discrete(5)

        self.reset()

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.car_x = self.info.current_w * 0.5
        self.car_y = self.info.current_h * 0.1
        self.car_angle = -90       
        self.car_speed = 0

        on_track = self.is_on_track(self.car_x, self.car_y)
        state = self.get_state(on_track)
        info = {}
        return state, info

    def is_on_track(self, x, y):
        if x < 0 or y < 0 or x >= self.track_surface.get_width() or y >= self.track_surface.get_height():
            return False

        track_color = self.track_surface.get_at((int(x), int(y)))[:3]

        return (
            abs(track_color[0] - 127) < 30 and
            abs(track_color[1] - 127) < 30 and
            abs(track_color[2] - 127) < 30
        )
    
    def cast_sensor(self, angle_offset):
        angle = math.radians(self.car_angle + angle_offset)
        for dist in range(0, self.sensor_max_distance, 5):
            x = int(self.car_x + math.cos(angle) * dist)
            y = int(self.car_y - math.sin(angle) * dist)
            if not self.is_on_track(x, y):
                return dist / self.sensor_max_distance
        return 1.0
    
    def step(self, action):
        if action == 1:
            self.car_speed += self.acceleration
        elif action == 2:
            self.car_speed -= self.acceleration
        elif action == 3:
            self.car_angle += self.rotation_speed
        elif action == 4:
            self.car_angle -= self.rotation_speed

        if action not in [1, 2]:
            if self.car_speed > 0:
                self.car_speed -= self.friction
            elif self.car_speed < 0:
                self.car_speed += self.friction

        self.car_speed = max(-self.max_speed / 2, min(self.max_speed, self.car_speed))
        self.car_angle = ((self.car_angle + 180) % 360) - 180

        rad = math.radians(self.car_angle)
        self.car_x += math.cos(rad) * self.car_speed
        self.car_y -= math.sin(rad) * self.car_speed

        self.car_x = max(0, min(self.info.current_w, self.car_x))
        self.car_y = max(0, min(self.info.current_h, self.car_y))

        reward = 0.0
        on_track = self.is_on_track(self.car_x, self.car_y)

        if on_track:
            reward += 0.1 * abs(self.car_speed)
        else:
            reward -= 0.5
        # on_track = True
        # reward = 0.05 * abs(self.car_speed)
        # reward += np.random.uniform(-0.01, 0.01)

        if self.car_speed == 0:
            reward -= 0.1
        
        self.prev_angle = getattr(self, "prev_angle", self.car_angle)
        angle_change = abs(self.car_angle - self.prev_angle)
        reward -= 0.002 * angle_change
        self.prev_angle = self.car_angle

        dx = self.car_x - getattr(self, "prev_x", self.car_x)
        dy = self.car_y - getattr(self, "prev_y", self.car_y)
        self.prev_x, self.prev_y = self.car_x, self.car_y

        forward_progress = dx * math.cos(rad) - dy * math.sin(rad)
        reward += 0.1 * forward_progress

        terminated = not on_track
        truncated = False
        info = {}

        state = self.get_state(on_track)

        return state, reward, terminated, truncated, info
    
    def get_state(self, on_track):
        sensors = np.array([self.cast_sensor(a) for a in self.sensor_angles], dtype=np.float32)
        state = np.array([
            self.car_x / self.info.current_w,
            self.car_y / self.info.current_h,
            self.car_speed / self.max_speed,
            math.sin(math.radians(self.car_angle)),
            math.cos(math.radians(self.car_angle)),
            1.0 if on_track else 0.0
        ], dtype=np.float32)
        return np.concatenate((sensors, state))[:7]
    
    def render(self):
        # self.screen.blit(self.track_surface, (0, 0))
        # rotated_car = pygame.transform.rotate(self.car_image, self.car_angle)
        # car_rect = rotated_car.get_rect(center=(self.car_x, self.car_y))
        # self.screen.blit(rotated_car, car_rect.topleft)
        
        # indicator_color = (0, 255, 0) if self.is_on_track(self.car_x, self.car_y) else (0, 0, 255)
        # pygame.draw.circle(self.screen, indicator_color, (int(self.car_x), int(self.car_y)), 4)

        # fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        # speed_text = self.font.render(f"Speed: {self.car_speed:.2f}", True, (255, 255, 255))
        # angle_text = self.font.render(f"Angle: {self.car_angle:.1f}°", True, (255, 255, 255))
        # on_track_text = self.font.render(f"On Track: {self.is_on_track(self.car_x, self.car_y)}", True, (255, 255, 255))

        # self.screen.blit(fps_text, (10, 10))
        # self.screen.blit(speed_text, (10, 35))
        # self.screen.blit(angle_text, (10, 55))
        # self.screen.blit(on_track_text, (10, 75))

        # for a in self.sensor_angles:
        #     dist = self.cast_sensor(a) * self.sensor_max_distance
        #     rad = math.radians(self.car_angle + a)
        #     end_x = self.car_x + math.cos(rad) * dist
        #     end_y = self.car_y - math.sin(rad) * dist
        #     pygame.draw.line(self.screen, (255, 0, 0), (self.car_x, self.car_y), (end_x, end_y), 1)

        # pygame.display.flip()
        # self.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if getattr(self, "render_mode", "human") != "human":
            return

        self.screen.blit(self.track_surface, (0, 0))
        rotated_car = pygame.transform.rotate(self.car_image, self.car_angle)
        car_rect = rotated_car.get_rect(center=(self.car_x, self.car_y))
        self.screen.blit(rotated_car, car_rect.topleft)

        indicator_color = (0, 255, 0) if self.is_on_track(self.car_x, self.car_y) else (255, 0, 0)
        pygame.draw.circle(self.screen, indicator_color, (int(self.car_x), int(self.car_y)), 4)

        pygame.display.flip()
        self.clock.tick(60)

if __name__ == "__main__":
    env = RaceEnv()

    obs, info = env.reset()

    for _ in range(10):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        print("Obs:", obs, "Reward:", reward)

        env.render()
        if terminated or truncated:
            obs, info = env.reset()

    pygame.quit()
    sys.exit()