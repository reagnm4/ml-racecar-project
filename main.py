import pygame
import sys
import math

class RaceEnv:
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

        self.reset()

    def reset(self):
        self.car_x = self.info.current_w / 2
        self.car_y = self.info.current_h / 2
        self.car_angle = 0       
        self.car_speed = 0
        state = self.get_state(on_track=True)
        return state

    def is_on_track(self, x, y):
        if x < 0 or y < 0 or x >= self.track_surface.get_width() or y >= self.track_surface.get_height():
            return False  
        color = self.track_surface.get_at((int(x), int(y)))[:3]
        track_color = (127, 127, 127)
        tolerance = 20
        return all(abs(color[i] - track_color[i]) < tolerance for i in range(3))
    
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

        on_track = self.is_on_track(self.car_x, self.car_y)
        reward = 1 if on_track else -1
        done = False 

        state = self.get_state(on_track)
        return state, reward, done
    
    def get_state(self, on_track):
        return {
            "x": self.car_x,
            "y": self.car_y,
            "angle": self.car_angle,
            "speed": self.car_speed,
            "on_track": on_track
        }
    
    def render(self):
        self.screen.blit(self.track_surface, (0, 0))
        rotated_car = pygame.transform.rotate(self.car_image, self.car_angle)
        car_rect = rotated_car.get_rect(center=(self.car_x, self.car_y))
        self.screen.blit(rotated_car, car_rect.topleft)
        
        indicator_color = (0, 255, 0) if self.is_on_track(self.car_x, self.car_y) else (0, 0, 255)
        pygame.draw.circle(self.screen, indicator_color, (int(self.car_x), int(self.car_y)), 4)

        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        speed_text = self.font.render(f"Speed: {self.car_speed:.2f}", True, (255, 255, 255))
        angle_text = self.font.render(f"Angle: {self.car_angle:.1f}°", True, (255, 255, 255))
        on_track_text = self.font.render(f"On Track: {self.is_on_track(self.car_x, self.car_y)}", True, (255, 255, 255))

        self.screen.blit(fps_text, (10, 10))
        self.screen.blit(speed_text, (10, 35))
        self.screen.blit(angle_text, (10, 55))
        self.screen.blit(on_track_text, (10, 75))

        pygame.display.flip()
        self.clock.tick(60)

if __name__ == "__main__":
    env = RaceEnv()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            env.car_speed += env.acceleration
        if keys[pygame.K_DOWN]:
            env.car_speed -= env.acceleration
        if keys[pygame.K_LEFT]:
            env.car_angle += env.rotation_speed
        if keys[pygame.K_RIGHT]:
            env.car_angle -= env.rotation_speed

        env.car_angle %= 360
        env.step(0)
        env.render()

    pygame.quit()
    sys.exit()
    