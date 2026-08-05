import pygame
import sys
import random


pygame.init()

# Variables for the game
screen_width = 400
screen_height = 720
background = "Assets/background.png"
sprites = pygame.sprite.Group()

player_pos = pygame.Vector2(screen_width / 2, screen_height / 2)
player_ship = "Assets/Player/player_ship.png"
player_ship_size = (64, 64)

player_projectile_sprite = "Assets\Player\player_projectile_1.png"
player_projectile_size = (player_ship_size[0] / 8, player_ship_size[1] / 2)
projectile_group = pygame.sprite.Group()

asteroids = ("Assets/Asteroids/big_asteroid.png", "Assets/Asteroids/asteroid_01.png", "Assets/Asteroids/asteroid_02.png", "Assets/Asteroids/asteroid_03.png", "Assets/Asteroids/asteroid_04.png")
asteroid_group = pygame.sprite.Group()

asteroid_event = pygame.USEREVENT + 1
pygame.time.set_timer(asteroid_event, 1000)
max_asteroids = 10

# Varibles for the game itself
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0

# Functions
class Sprites(pygame.sprite.Sprite):
    def __init__(self, sprite, x_cord: int=0, y_cord: int=0, size: tuple=None, speed_x: int=0, speed_y: int=0, angle: float=0):
        super().__init__()
        raw_sprite = pygame.image.load(sprite).convert_alpha()
        if size == None:
            self.image = raw_sprite
        elif size != None:
            self.image = pygame.transform.scale(raw_sprite, size)
        self.rect = self.image.get_rect(center=(x_cord, y_cord))
        
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.angle = angle

class Player(Sprites):
    def __init__(self, sprite, x_cord=0, y_cord=0, size=None, speed_x=0, speed_y=0, angle=0):
        super().__init__(sprite, x_cord, y_cord, size, speed_x, speed_y, angle)
        self.original_image = self.image.copy()
        
    def update(self):
        keys = pygame.key.get_pressed()

        # Player's Mechanics
        if keys[pygame.K_w]:
            self.rect.y -= self.speed_y * dt
        if keys[pygame.K_s]:
            self.rect.y += self.speed_y * dt
        if keys[pygame.K_a]:
            self.rect.x -= self.speed_x * dt
        if keys[pygame.K_d]:
            self.rect.x += self.speed_x * dt
        
        # Keep the player inside the screen bounds
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(screen_width, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(screen_height, self.rect.bottom)
        
class PlayerProjectile(Sprites):       
    def update(self):
        # Move the projectile each frame.
        self.rect.y -= self.speed_y
        
        # Remove the projectile once it leaves top side of the screen.
        if self.rect.bottom < 0:
            self.kill()
    
def shoot_player_projectile():
    mouse = pygame.mouse.get_just_pressed()
    
    if mouse[0]:
        player_projectile = PlayerProjectile(
            player_projectile_sprite,
            x_cord=player.rect.centerx,
            y_cord=player.rect.top,
            size=player_projectile_size,
            speed_x=0,
            speed_y=10,
        )
        projectile_group.add(player_projectile)
        sprites.add(player_projectile)

class Asteroids(Sprites):
    def __init__(self, sprite, x_cord=0, y_cord=0, size=None, speed_x=0, speed_y=0, angle=0):
        super().__init__(sprite, x_cord, y_cord, size, speed_x, speed_y, angle)
        self.original_image = self.image.copy()
        self.rotation_speed = random.uniform(-2, 2)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if (self.rect.top > screen_height
            or self.rect.right < -screen_width
            or self.rect.left > screen_width):
            self.kill()


# Load background and player ship
background = pygame.transform.scale(pygame.image.load(background).convert(), (screen_width, screen_height)) # Load and scale the background image to fit the screen size

player = Player(player_ship, 
                x_cord=player_pos.x, 
                y_cord=player_pos.y, 
                size=player_ship_size, 
                speed_x=300, 
                speed_y=300
                )
sprites.add(player)

while running:
    mouse = pygame.mouse.get_just_pressed()
    asteroid_size = random.randint(30,80)
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == asteroid_event:
            if len(asteroid_group) < max_asteroids:
                asteroid = Asteroids(
                    random.choice(asteroids),
                    x_cord=random.randint(0, (screen_width - 10)),
                    y_cord=0,
                    size=(asteroid_size, asteroid_size),
                    speed_x=random.choice((-1, 0, 1)),
                    speed_y=random.choices((2, 6), weights=(75, 25), k=1)[0],
                    angle=-1
                )
                asteroid_group.add(asteroid)
                sprites.add(asteroid)
                

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    screen.blit(background)

    shoot_player_projectile()

    # Destroy asteroids when a player projectile hits them.
    pygame.sprite.groupcollide(projectile_group, asteroid_group, True, True)

    if pygame.sprite.spritecollide(player, asteroid_group, True):
        print("got hit")

    sprites.update()

    sprites.draw(screen)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000  # Limit the game to 60 frames per second and store the elapsed time in seconds

pygame.quit()
sys.exit()