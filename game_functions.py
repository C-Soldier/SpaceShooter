import pygame
from random import randint, choice
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game_assets import *

class Sprites(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group,
                 sprite: str,
                 cordinates: pygame.math.Vector2,
                 speed: int
                 ):
        super().__init__(groups)
        self.sprite = sprite
        self.cordinates = cordinates
        self.speed = speed
        self.size = 64
        
        self.create_sprite()
    
    def create_sprite(self):
        raw_image = pygame.image.load(self.sprite)
        if self.size == None:
            self.image = raw_image.convert_alpha()
        else:
            self.image = pygame.transform.scale(raw_image, (self.size, self.size)).convert_alpha()
        self.rect = self.image.get_rect(center=(self.cordinates))