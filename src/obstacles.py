import pygame
import os

class ObstacleGroup:
    def __init__(self, screen, image_file):
        self.screen = screen
        self.obstacle_map = pygame.sprite.Sprite()
        self.obstacle_map.image = pygame.image.load(os.path.join('assets', image_file)).convert_alpha()
        self.obstacle_map.rect = self.obstacle_map.image.get_rect()
        self.obstacle_map.mask = pygame.mask.from_surface(self.obstacle_map.image)

    def update(self):
        pass

    def draw(self, offset_x, offset_y):
        self.screen.blit(self.obstacle_map.image, (self.obstacle_map.rect.x + offset_x, self.obstacle_map.rect.y + offset_y))
