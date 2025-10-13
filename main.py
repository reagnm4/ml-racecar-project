import pygame
import sys
import math
pygame.init()

info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)

track_surface = pygame.image.load("assets/track.png").convert()
track_surface = pygame.transform.scale(track_surface, (info.current_w, info.current_h))

car_image = pygame.image.load("assets/car.png").convert_alpha()
car_image = pygame.transform.scale(car_image, (40, 75))

car_x = info.current_w / 2
car_y = info.current_h / 2
car_angle = 0       
car_speed = 0
acceleration = 0.2
max_speed = 8
rotation_speed = 6
friction = 0.05

def is_on_track(surface, x, y):
    if x < 0 or y < 0 or x >= surface.get_width() or y >= surface.get_height():
        return False  
    color = surface.get_at((int(x), int(y)))[:3]
    track_color = (127, 127, 127)
    tolerance = 20
    return all(abs(color[i] - track_color[i]) < tolerance for i in range(3))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    if keys[pygame.K_LEFT]:
        car_angle += rotation_speed
    if keys[pygame.K_RIGHT]:
        car_angle -= rotation_speed
    if keys[pygame.K_UP]:
        car_speed += acceleration
    elif keys[pygame.K_DOWN]:
        car_speed -= acceleration
    else:
        if car_speed > 0:
            car_speed -= friction
        elif car_speed < 0:
            car_speed += friction

    car_speed = max(-max_speed / 2, min(max_speed, car_speed))
    rad = math.radians(car_angle)
    car_x += math.cos(rad) * car_speed
    car_y -= math.sin(rad) * car_speed

    screen.blit(track_surface, (0, 0))

    rotated_car = pygame.transform.rotate(car_image, car_angle)
    car_rect = rotated_car.get_rect(center=(car_x, car_y))
    screen.blit(rotated_car, car_rect.topleft)

    on_track = is_on_track(track_surface, car_x, car_y)
    indicator_color = (0, 255, 0) if on_track else (0, 0, 255)
    pygame.draw.circle(screen, indicator_color, (int(car_x), int(car_y)), 5)

    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

    