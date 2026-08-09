import pygame
from random import randint, choice
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game_assets import *

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
