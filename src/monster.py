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
        self.max_health = 100
        self.speed = 1

        self.health_bar_width = 60
        self.health_bar_height = 10
        self.health_bar_color = (0, 255, 0)
        self.background_bar_color = (255, 0, 0)

    def update(self, bullets, player_rect, obstacles, offset_x, offset_y):
        if pygame.sprite.spritecollide(self, bullets, False):
            self.health -= 5

        if self.health <= 0:
            self.kill()
            return

        x_diff = player_rect.centerx - self.rect.centerx
        y_diff = player_rect.centery - self.rect.centery
        distance = math.hypot(x_diff, y_diff)
        dx = self.speed * x_diff / (distance + 5)
        dy = self.speed * y_diff / (distance + 5)

        original_rect = self.rect.copy()

        self.rect.x += dx + random.randint(-2, 2)
        original_rect = self.check_collision(obstacles, original_rect)
        self.rect.y += dy + random.randint(-2, 2)
        original_rect = self.check_collision(obstacles, original_rect)

        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - 90

        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def check_collision(self, obstacles, original_rect):
        if pygame.sprite.collide_mask(self, obstacles.obstacle_map):
            self.rect = original_rect
        return self.rect.copy()

    def draw(self, offset_x, offset_y):
        self.screen.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))
        self.draw_health_bar(offset_x, offset_y)

    def draw_health_bar(self, offset_x, offset_y):
        health_bar_rect = pygame.Rect(
            self.rect.x + offset_x + (self.rect.width - self.health_bar_width) // 2,
            self.rect.y + offset_y - self.health_bar_height - 5,
            self.health_bar_width,
            self.health_bar_height
        )
        pygame.draw.rect(self.screen, self.background_bar_color, health_bar_rect)
        health_fill_rect = pygame.Rect(
            health_bar_rect.left,
            health_bar_rect.top,
            self.health_bar_width * (self.health / self.max_health),
            self.health_bar_height
        )
        pygame.draw.rect(self.screen, self.health_bar_color, health_fill_rect)

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
        x = random.randint(int(map_width//1.5), map_width)
        y = random.randint(int(map_height//1.5), map_height)
        return Monster(self.screen, x, y, 'monster.png')

    def update(self, *args):
        self.monsters.update(*args)

    def draw(self, offset_x, offset_y):
        for monster in self.monsters:
            # weapon.screen.blit(weapon.image, (weapon.rect.x + offset_x, weapon.rect.y + offset_y))
            monster.draw(offset_x, offset_y)