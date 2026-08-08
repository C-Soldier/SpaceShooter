import pygame
from random import randint, choice
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game_assets import *

class Sprites(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group,
                 cordinates: pygame.math.Vector2,
                 size):
        super().__init__(groups)