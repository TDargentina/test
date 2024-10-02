import pygame
import random

# Initialize Pygame
pygame.init()

# Set window dimensions
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Improved Mario-like Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Load sprites
player_img = pygame.Surface((30, 40))
player_img.fill(red)
enemy_img = pygame.Surface((30, 30))
enemy_img.fill(green)
coin_img = pygame.Surface((20, 20))
coin_img.fill(yellow)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.speed = 5
        self.jump_force = 15
        self.gravity = 0.8
        self.on_ground = True
        self.score = 0

    def update(self):
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_force
            self.on_ground = False

        self.vel_y += self.gravity
        dy += self.vel_y

        # Check for collisions with platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True
                    dy = 0
                elif self.vel_y < 0:
                    self.rect.top = platform.bottom
                    self.vel_y = 0
                    dy = 0

        # Apply movement
        self.rect.x += dx
        self.rect.y += dy

        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > window_width:
            self.rect.right = window_width

        # Collect coins
        coin_collisions = pygame.sprite.spritecollide(self, coins, True)
        for coin in coin_collisions:
            self.score += 1

        # Check for enemy collisions
        enemy_collisions = pygame.sprite.spritecollide(self, enemies, False)
        if enemy_collisions:
            global running
            running = False

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.speed = 2

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left < 0 or self.rect.right > window_width:
            self.direction *= -1

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create sprites
player = Player(100, window_height - 90)
all_sprites = pygame.sprite.Group(player)
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()

# Create enemies
for _ in range(3):
    enemy = Enemy(random.randint(0, window_width), random.randint(0, window_height - 100))
    enemies.add(enemy)
    all_sprites.add(enemy)

# Create coins
for _ in range(10):
    coin = Coin(random.randint(0, window_width), random.randint(0, window_height - 100))
    coins.add(coin)
    all_sprites.add(coin)

# Platforms
platforms = [
    pygame.Rect(200, 500, 200, 20),
    pygame.Rect(500, 400, 200, 20),
    pygame.Rect(300, 300, 100, 20),
    pygame.Rect(0, window_height - 20, window_width, 20),
]

# Font for score display
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    window.fill(black)
    for platform in platforms:
        pygame.draw.rect(window, white, platform)
    all_sprites.draw(window)

    # Display score
    score_text = font.render(f"Score: {player.score}", True, white)
    window.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

# Game over screen
window.fill(black)
game_over_text = font.render("Game Over", True, white)
final_score_text = font.render(f"Final Score: {player.score}", True, white)
window.blit(game_over_text, (window_width // 2 - 100, window_height // 2 - 50))
window.blit(final_score_text, (window_width // 2 - 100, window_height // 2 + 50))
pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.wait(3000)

pygame.quit()
