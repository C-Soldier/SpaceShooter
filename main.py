import pygame
import sys
from random import randint, choice
from game_functions import Player, Particles, Projectile
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_PROJECTILE_SIZE
from game_assets import BACKGROUND, PLAYER_SHIP, PLAYER_PROJECTILE

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load Background
background = pygame.transform.scale(pygame.image.load(BACKGROUND).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Player
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

def ship_rocket():
    pos = pygame.math.Vector2(
        player.rect.centerx + randint(-5, 5), 
        player.rect.bottom
    )
    color = choice(("#CFFF04", "#F6F3E8"))
    direction = pygame.math.Vector2(0, 1)
    speed = randint(40, 50)
    Particles(player_group, pos, color, direction, speed)

# Game Loop
def game_loop():
    while True:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                Projectile(player_group,
                           PLAYER_PROJECTILE, 
                           (player.rect.centerx, player.rect.top),
                           300,
                           PLAYER_PROJECTILE_SIZE
                           )
                
        ship_rocket()
        
        # Clock
        dt = clock.tick(60) / 1000
        
        # Window
        window.fill("black")
        window.blit(background)
        
        # Display
        player_group.draw(window)
        
        # Updates
        player_group.update(dt)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    game_loop()