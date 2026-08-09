import pygame
from random import randint, choice
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game_assets import *

# Particles
class Particles(pygame.sprite.Sprite):
    def __init__(self, 
                 groups: pygame.sprite.Group,
                 pos: list[int],
                 color: str,
                 direction: pygame.math.Vector2,
                 speed: int
                 ):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed
        self.size = 4
        
        self.create_surf()
        
    def create_surf(self):
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        pygame.draw.circle(surface=self.image, color=self.color, center=(self.size/2, self.size/2), radius=self.size/2)
        self.rect = self.image.get_rect(center=self.pos)
    
    def move_particles(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
    
    def update(self, dt):
        self.move_particles(dt)
    
# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprite = PLAYER_SHIP
        self.cordinates = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT/2)
        self.speed = 300
        self.size = 64
        
        self.image = pygame.transform.scale(pygame.image.load(self.sprite), (self.size, self.size)).convert_alpha()
        self.rect = self.image.get_rect(center=(self.cordinates))
        
        
    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.rect.y += self.speed * dt
        if keys[pygame.K_a]:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.rect.x += self.speed * dt
        
        # Keep player inside screen
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)

# Other Sprites
class Sprites(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group,
                 sprite: str,
                 cordinates: pygame.math.Vector2,
                 speed: int,
                 size: tuple[int] = None
                 ):
        super().__init__(groups)
        self.sprite = sprite
        self.cordinates = cordinates
        self.speed = speed
        self.size = size
        
        self.create_sprite()
    
    def create_sprite(self):
        raw_image = pygame.image.load(self.sprite)
        if self.size == None:
            self.image = raw_image.convert_alpha()
        else:
            self.image = pygame.transform.scale(raw_image, (self.size, self.size)).convert_alpha()
        self.rect = self.image.get_rect(center=(self.cordinates))
