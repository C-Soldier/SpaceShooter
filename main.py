import pygame
import sys
from game_functions import Sprites
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game_assets import BACKGROUND, PLAYER_SHIP

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load Background
background = pygame.transform.scale(pygame.image.load(BACKGROUND).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Player
player_group = pygame.sprite.Group()
def player():
    player_sprite_image = PLAYER_SHIP
    cordinates = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    speed = 300
    sprite_size = 64
    Sprites(player_group, player_sprite_image, cordinates, speed)

# Game Loop
def game_loop():
    while True:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        player()
        
        # Clock
        dt = clock.tick() / 1000
        
        # Window
        window.fill("black")
        window.blit(background)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    game_loop()