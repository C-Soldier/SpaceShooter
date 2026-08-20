import pygame
from random import randint, choice, uniform
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SHIP_SIZE
from game_assets import PLAYER_SHIP

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
        self.alpha = 255
        self.fade_speed = 200
        
        self.create_surf()
        
    def create_surf(self):
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        # pygame.draw.circle(surface=self.image, color=self.color, center=(self.size/2, self.size/2), radius=self.size/2)
        pygame.draw.rect(surface=self.image, color=self.color, rect=(self.direction.x, self.direction.y, self.size, self.size))
        self.rect = self.image.get_rect(center=self.pos)
    
    def move_particles(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
    
    def fade_particles(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)
        
        if self.alpha <= 0:
            self.kill()
    
    def update(self, dt):
        self.move_particles(dt)
        self.fade_particles(dt)

# Sprites
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
            self.image = pygame.transform.scale(raw_image, (self.size)).convert_alpha()
        self.rect = self.image.get_rect(center=(self.cordinates))
        self.mask = pygame.mask.from_surface(self.image)

# Collisons
class Collisions():
    def __init__(self, 
                 groupa: pygame.sprite.Group, 
                 groupb: pygame.sprite.Group, 
                 kill_a: bool,
                 kill_b: bool
                 ):
        self.groupa = groupa
        self.groupb = groupb
        self.kill_a = kill_a
        self.kill_b = kill_b
        self.collision_detected = self.check_group_collision()
    
    def check_group_collision(self):
        collision_result = pygame.sprite.groupcollide(
            self.groupa, 
            self.groupb, 
            self.kill_a, 
            self.kill_b,
            pygame.sprite.collide_mask
        )
        return bool(collision_result)
    
    def check_sprite_collision(self):
            collision_result = pygame.sprite.spritecollide(
                self.groupa, 
                self.groupb, 
                self.kill_b,
                pygame.sprite.collide_mask
            )
            return bool(collision_result)
            

# Health Tracker
class Health(pygame.sprite.Sprite):
    def __init__(self, groups, health_sprite, lives_num):
        super().__init__(groups)
        self.groups = groups
        self.health_sprite = health_sprite
        self.lives_num = lives_num
        self.cordinates = pygame.math.Vector2(
            SCREEN_WIDTH - 20,
            SCREEN_HEIGHT - 20
        )
        self.size = (30, 30)
        
    def show_health(self):
        for _ in range(self.lives_num):
            Sprites(self.groups, self.health_sprite, self.cordinates, 0, self.size)
            
    
# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprite = PLAYER_SHIP
        self.cordinates = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT/2)
        self.speed = 300
        self.size = PLAYER_SHIP_SIZE
        
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

# Projectiles
class Projectile(Sprites):
    def __init__(self, groups, sprite, cordinates, speed, size = None):
        super().__init__(groups, sprite, cordinates, speed, size)
        
        self.groups = groups

    def update(self, dt):
        self.rect.y -= self.speed * dt
        
        if self.rect.bottom < 0:
            self.kill()
        
        Particles(groups=self.groups, 
                  pos=(self.rect.centerx + randint(-2, 2), 
                   self.rect.bottom
                   ), 
                  color="yellow", 
                  direction=pygame.math.Vector2(0, 1),
                  speed=randint(30, 40)
                  )

# Asteroids
class Asteroids(Sprites):
    def __init__(self, 
                 groups,
                 collide_group: pygame.sprite.Group, 
                 particles_group: pygame.sprite.Group, 
                 sprite, 
                 cordinates,
                 speed, 
                 size = None
                 ):
        super().__init__(groups, sprite, cordinates, speed, size)
        self.groups = groups
        self.angle = 0
        self.collide_group = collide_group
        self.particles_group = particles_group
        
        self.original_image = self.image.copy()
        self.rotation_speed = randint(-2, 2)
        
        if self.rotation_speed == 0:
            self.rotation_speed = choice((-1, 1))
    
    def update(self, dt):
        self.rect.y += self.speed * dt
        
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        collision = Collisions(self.groups, self.collide_group, True, True)
        if collision.collision_detected:
            for _ in range(100):
                Particles(
                    groups=self.particles_group,
                    pos=(self.rect.centerx, self.rect.centery),
                    color="white",
                    direction=pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1)),
                    speed=randint(50, 400)
                )
        
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            
        
       