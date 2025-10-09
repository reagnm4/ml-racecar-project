import pygame
import sys
pygame.init()

info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((144, 238, 144))
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))
    
    pygame.display.flip()
    
    clock.tick(60)

    