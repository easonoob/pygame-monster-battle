import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, image_file):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load(os.path.join('assets', image_file)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 60))  # Scale down the image
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.x += 100
        self.rect.y += 100
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask for the player
        self.alive = True

    def update(self, keys, obstacles):
        original_rect = self.rect.copy()  # Store the original position
        speed = 5
        if keys[pygame.K_w]:
            self.rect.y -= speed
            original_rect = self.check_collision(obstacles, original_rect)
        if keys[pygame.K_s]:
            self.rect.y += speed
            original_rect = self.check_collision(obstacles, original_rect)
        if keys[pygame.K_a]:
            self.rect.x -= speed
            original_rect = self.check_collision(obstacles, original_rect)
        if keys[pygame.K_d]:
            self.rect.x += speed
            original_rect = self.check_collision(obstacles, original_rect)
    
    def check_collision(self, obstacles, original_rect):
        if pygame.sprite.collide_mask(self, obstacles.obstacle_map):
            self.rect = original_rect
        return self.rect.copy()

    def draw(self, offset_x, offset_y):
        self.screen.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))