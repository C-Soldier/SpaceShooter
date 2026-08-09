import pygame
import sys
from random import randint
from game_functions import Player, Particles
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game_assets import BACKGROUND, PLAYER_SHIP

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load Background
background = pygame.transform.scale(pygame.image.load(BACKGROUND).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

particle_group = pygame.sprite.Group()

# Load Player
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

def ship_rocket():
    pos = player.rect.bottom + randint(-10, 10), player.rect.bottom + randint(-10, 10)
    color = "yellow"
    direction = pygame.math.Vector2(0, 1)
    speed = randint(50, 100)
    Particles(particle_group, pos, color, direction, speed)

# Game Loop
def game_loop():
    while True:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Clock
        dt = clock.tick(60) / 1000
        
        # Window
        window.fill("black")
        window.blit(background)
        
        # Display
        player_group.draw(window)
        
        # Updates
        player_group.update(dt)
        particle_group.update(dt)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    game_loop()