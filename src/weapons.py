import pygame
import os
import random
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, start_x, start_y, target_pos):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((5, 5))  # Small bullet
        self.image.fill((255, 255, 255))  # White color
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.speed = 10  # Pixels per frame

        # Calculate trajectory
        x_diff = target_pos[0] - start_x
        y_diff = target_pos[1] - start_y
        distance = math.hypot(x_diff, y_diff)
        self.dx = self.speed * x_diff / distance
        self.dy = self.speed * y_diff / distance

    def update(self):
        # Move bullet
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Remove bullet if it goes off screen
        if (self.rect.x < 0 or self.rect.x > self.screen.get_width() or
                self.rect.y < 0 or self.rect.y > self.screen.get_height()):
            self.kill()

    def draw(self, offset_x, offset_y):
        self.screen.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))

class Weapon(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load(os.path.join('assets', 'weapon.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.shooting = False
        self.last_shot_time = 0

    def update(self, player_pos, mouse_pos):
        # Calculate angle to point towards the mouse
        x_diff = mouse_pos[0] - player_pos[0]
        y_diff = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-y_diff, x_diff))
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Position the weapon in front of the player
        distance_from_player = 40  # adjust this value as needed
        self.rect.centerx = player_pos[0] + distance_from_player * math.cos(math.radians(angle))
        self.rect.centery = player_pos[1] - distance_from_player * math.sin(math.radians(angle))

    def draw(self, offset_x, offset_y):
        self.screen.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))

    def shoot(self, bullets, mouse_pos):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > 500:  # 500 ms between shots
            self.last_shot_time = now
            # Create a bullet heading towards the mouse position
            bullets.add(Bullet(self.screen, self.rect.centerx, self.rect.centery, mouse_pos))

class WeaponGroup:
    def __init__(self, screen, map_width, map_height, num_weapons=5):
        self.weapons = pygame.sprite.Group()
        for _ in range(num_weapons):
            x = random.randint(0, map_width - 20)
            y = random.randint(0, map_height - 20)
            self.weapons.add(Weapon(screen, x, y))

    def update(self):
        pass

    def draw(self, offset_x, offset_y):
        for weapon in self.weapons:
            weapon.screen.blit(weapon.image, (weapon.rect.x + offset_x, weapon.rect.y + offset_y))