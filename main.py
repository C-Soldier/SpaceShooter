import pygame
import sys
from random import randint, choice, uniform
from game_functions import Player, Particles, Projectile, Asteroids
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_PROJECTILE_SIZE
from game_assets import BACKGROUND, PLAYER_PROJECTILE, ASTEROIDS

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load Background
background = pygame.transform.scale(pygame.image.load(BACKGROUND).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Player
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)
player_projectile_group = pygame.sprite.Group()

# Asteroids
asteroid_group = pygame.sprite.Group()

# Effects
particle_group = pygame.sprite.Group()

# Events
asteroid_event = pygame.USEREVENT
pygame.time.set_timer(asteroid_event, 1000)

# Functions
def ship_rocket():
    pos = pygame.math.Vector2(
        player.rect.centerx + randint(-5, 5), 
        player.rect.bottom
    )
    color = choice(("orange", "red"))
    direction = pygame.math.Vector2(0, 1)
    speed = randint(40, 50)
    Particles(particle_group, pos, color, direction, speed)

def spawn_asteroids():
    cordinates = pygame.math.Vector2(uniform(10, (SCREEN_WIDTH - 10)), 0)
    speed = randint(200, 300)
    size = randint(30, 80)
    
    Asteroids(asteroid_group, 
              choice((ASTEROIDS)), 
              cordinates,
              speed,
              (size, size) 
    )
    
def explosion(n: int):
    for _ in range(n):
        pass

# Game Loop
def game_loop():
    while True:
        # Cycle Through Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                Projectile(player_projectile_group,
                           PLAYER_PROJECTILE, 
                           (player.rect.centerx, player.rect.top),
                           300,
                           PLAYER_PROJECTILE_SIZE
                           )
            
            if event.type == asteroid_event:
                spawn_asteroids()
        
        ship_rocket()
        
        if pygame.sprite.groupcollide(player_projectile_group, asteroid_group, True, True, pygame.sprite.collide_mask):
            print("Got em")
        
        if pygame.sprite.spritecollide(player, asteroid_group, True, pygame.sprite.collide_mask):
            print("got hit")
        
            
        # Clock
        dt = clock.tick(60) / 1000
        
        # Window
        window.fill("black")
        window.blit(background)
        
        # Display
        player_group.draw(window)
        player_projectile_group.draw(window)
        asteroid_group.draw(window)
        particle_group.draw(window)
         
        # Updates
        player_group.update(dt)
        player_projectile_group.update(dt)
        asteroid_group.update(dt)
        particle_group.update(dt)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    game_loop()