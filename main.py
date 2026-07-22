import pygame
import random
import time

# Variables for the game assets
screen_width = 1280
screen_height = 720
background = "Assets/background.png"

player_pos = pygame.Vector2(screen_width / 2, screen_height / 2)
player_ship = "Assets/player_ship.png"

asteroids = ("Assets/big_asteroid.png", "Assets/asteroid_01.png", "Assets/asteroid_02.png", "Assets/asteroid_03.png", "Assets/asteroid_04.png")

pygame.init()

# Varibles for the game itself
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0

# Functions
def incoming_asteroids(asteroids, screen):
    asteroid = random.choice(asteroids)
    asteroid_size = random.randint(30, 80)
    
    asteroid = pygame.transform.scale(pygame.image.load(asteroid).convert_alpha(), (asteroid_size, asteroid_size))
    
    time.sleep(2)
    
    return screen.blit(asteroid, (random.randint(1, 1279), 0))

# Load background and player ship images
background = pygame.transform.scale(pygame.image.load(background).convert(), (screen_width, screen_height)) # Load and scale the background image to fit the screen size
player = pygame.transform.scale(pygame.image.load(player_ship).convert_alpha(), (64, 64))

        

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    screen.blit(background)
    
    screen.blit(player, player_pos)
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    incoming_asteroids(asteroids, screen)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000  # Limit the game to 60 frames per second and store the elapsed time in seconds

pygame.quit()