import pygame
import os
import math
import random

class Monster(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, image_file):
        super().__init__()
        self.screen = screen
        self.base_image = pygame.image.load(os.path.join('assets', image_file)).convert_alpha()
        self.base_image = pygame.transform.scale(self.base_image, (80, 80))  # Scale down the image
        self.image = self.base_image
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask for the player
        self.health = 100
        self.speed = 5

    def update(self, bullets, player_rect, obstacles, offset_x, offset_y):

        if pygame.sprite.spritecollide(self, bullets, False):
            self.health -= 10

        if self.health <= 0:
            self.kill()
            return

        x_diff = player_rect.centerx - self.rect.centerx - offset_x
        y_diff = player_rect.centerx - self.rect.centerx - offset_y
        distance = math.hypot(x_diff, y_diff)
        dx = self.speed * x_diff / (distance + 5)
        dy = self.speed * y_diff / (distance + 5)

        original_rect = self.rect.copy()  # Store the original position

        self.rect.x += dx + random.randint(-10, 10)
        original_rect = self.check_collision(obstacles, original_rect)
        self.rect.y += dy + random.randint(-10, 10)
        original_rect = self.check_collision(obstacles, original_rect)

    def check_collision(self, obstacles, original_rect):
        if pygame.sprite.collide_mask(self, obstacles.obstacle_map):
            self.rect = original_rect
        return self.rect.copy()

    def draw(self, offset_x, offset_y):
        self.screen.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))

class MonsterGroup:
    def __init__(self, screen, map_width, map_height, num_monsters=50, obstacles=None):
        self.monsters = pygame.sprite.Group()
        self.screen = screen
        for _ in range(num_monsters):
            monster = self.create(map_width, map_height)
            monster.mask = pygame.mask.from_surface(monster.image)
            while pygame.sprite.collide_mask(monster, obstacles.obstacle_map):
                monster = self.create(map_width, map_height)
                monster.mask = pygame.mask.from_surface(monster.image)
            self.monsters.add(monster)
    
    def create(self, map_width, map_height):
        x = random.randint(map_width//2, map_width)
        y = random.randint(map_height//2, map_height)
        return Monster(self.screen, x, y, 'monster.png')

    def update(self, *args):
        self.monsters.update(*args)

    def draw(self, offset_x, offset_y):
        for weapon in self.monsters:
            weapon.screen.blit(weapon.image, (weapon.rect.x + offset_x, weapon.rect.y + offset_y))