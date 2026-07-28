import pygame
import random


pygame.init()

# Variables for the game assets
screen_width = 1280
screen_height = 720
background = "Assets/background.png"

player_pos = pygame.Vector2(screen_width / 2, screen_height / 2)
player_ship = "Assets/player_ship.png"

asteroids = ("Assets/Asteroids/big_asteroid.png", "Assets/Asteroids/asteroid_01.png", "Assets/Asteroids/asteroid_02.png", "Assets/Asteroids/asteroid_03.png", "Assets/Asteroids/asteroid_04.png")
asteroids_group = pygame.sprite.Group()
asteroid_event = pygame.USEREVENT + 1
pygame.time.set_timer(asteroid_event, 1000)
max_asteroids = 5

# Varibles for the game itself
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0

# Functions
class Sprites(pygame.sprite.Sprite):
    def __init__(self, sprite, x_cord: int=0, y_cord: int=0, size: tuple=None, speed_x: int=0, speed_y: int=0):
        super().__init__()
        raw_sprite = pygame.image.load(sprite).convert_alpha()
        if size == None:
            self.image = raw_sprite
        elif size != None:
            self.image = pygame.transform.scale(raw_sprite, (size, size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_cord, y_cord)
        
        self.speed_x = speed_x
        self.speed_y = speed_y

class Player(Sprites):
    def __init__(self, sprite, x_cord = 0, y_cord = 0, size = None, speed_x = 0, speed_y = 0):
        super().__init__(sprite, x_cord, y_cord, size, speed_x, speed_y)

class Asteroids(Sprites): 
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.rect.top > screen_height:
            self.kill()


# Load background and player ship images
background = pygame.transform.scale(pygame.image.load(background).convert(), (screen_width, screen_height)) # Load and scale the background image to fit the screen size
player = pygame.transform.scale(pygame.image.load(player_ship).convert_alpha(), (64, 64))


while running:
    asteroid_size = random.randint(30,80)
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == asteroid_event:
            if len(asteroids_group) < max_asteroids:
                asteroid = Asteroids(random.choice(asteroids), x_cord=random.randint(0, 1270), y_cord=0, size=asteroid_size, speed_y=random.choices((2, 6), weights=(75, 25), k=1)[0])
                asteroids_group.add(asteroid)

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

    # incoming_asteroids(asteroids, screen)
    
    asteroids_group.update()
    asteroids_group.draw(screen)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000  # Limit the game to 60 frames per second and store the elapsed time in seconds

pygame.quit()