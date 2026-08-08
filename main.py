import pygame
import sys
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game_assets import BACKGROUND

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load Background
background = pygame.transform.scale(pygame.image.load(BACKGROUND).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Game Loop
def game_loop():
    while True:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Clock
        dt = clock.tick() / 1000
        
        # Window
        window.fill("black")
        window.blit(background)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    game_loop()