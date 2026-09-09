import pygame
import sys
import game_functions
from random import randint, choice, uniform
from game_functions import Player, Particles, Projectile, Asteroids, Collisions, draw_score
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_PROJECTILE_SIZE, HIGH_SCORE_FILE
from game_assets import BACKGROUND, PLAYER_PROJECTILE, ASTEROIDS, HP

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load Background
background = pygame.transform.scale(pygame.image.load(BACKGROUND).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Player
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)
player_projectile_group = pygame.sprite.Group()

# Health
health_group = pygame.sprite.Group()

# Asteroids
asteroid_group = pygame.sprite.Group()

# Effects
particles_group = pygame.sprite.Group()

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
    Particles(particles_group, pos, color, direction, speed)

def player_health(lives_num: int):
    health_group.empty()
    cordinates = pygame.math.Vector2(20, 20)
    for _ in range(lives_num):
        Player.Health(health_group, player_group, asteroid_group, HP, cordinates)
        cordinates.x += 35

def spawn_asteroids():
    cordinates = pygame.math.Vector2(uniform(10, (SCREEN_WIDTH - 10)), 0)
    speed = randint(500, 550)
    size = randint(30, 80)
    
    Asteroids(asteroid_group,
              player_projectile_group,
              particles_group,
              choice((ASTEROIDS)), 
              cordinates,
              speed,
              (size, size) 
    )   

# Game Over
def game_over():
    def show_high_score():
        with open(HIGH_SCORE_FILE, 'rb') as file:
            binary_data = file.read(4)
            
            high_score = int.from_bytes(binary_data, byteorder="big")
            
            text_font2 = pygame.font.Font(None, 32)
            
            text_surface2 = text_font2.render(f"High Score: {high_score}", False, (255, 0, 0))
            text_rect2 = text_surface2.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 45))
            
            window.blit(text_surface2, text_rect2)
            
            
    text_font1 = pygame.font.Font(None, 64)
    
    text_surface1 = text_font1.render("GAME OVER", False, (255, 0, 0))
    text_rect1 = text_surface1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    show_high_score()
    
    window.blit(text_surface1, text_rect1)
    
# Game Loop
def game_loop():
    lives_num = 3
    global game_over_flag
    while True:
        # Cycle Through Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if not game_functions.game_over_flag and event.type == pygame.MOUSEBUTTONDOWN:
                Projectile(player_projectile_group,
                           PLAYER_PROJECTILE, 
                           (player.rect.centerx, player.rect.top),
                           300,
                           PLAYER_PROJECTILE_SIZE
                           )
            
            if not game_functions.game_over_flag and event.type == asteroid_event:
                spawn_asteroids()
        
        if not game_functions.game_over_flag:
            ship_rocket()
            player_health(lives_num)
            
            # Check Player Collision with Asteroids And Lives
            player_collision = Collisions(player_group, asteroid_group, False, True)
            if player_collision.check_group_collision():    
                lives_num -= 1
            if lives_num <= 0:
                game_functions.game_over_flag = True
                player_group.empty()
                particles_group.empty()
                player_projectile_group.empty()
                asteroid_group.empty()
        
        # Clock
        dt = clock.tick(60) / 1000
        
        # Window
        window.fill("black")
        window.blit(background, (0, 0))
        
        if not game_functions.game_over_flag:
            # Display
            player_group.draw(window)
            health_group.draw(window)
            player_projectile_group.draw(window)
            asteroid_group.draw(window)
            particles_group.draw(window)
            
            # Updates
            player_group.update(dt)
            health_group.update()
            player_projectile_group.update(dt)
            asteroid_group.update(dt)
            particles_group.update(dt)
        else:
            game_over()
        draw_score(window)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    game_loop()