import pygame
import os

class Weapon(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load(os.path.join('assets', 'weapon.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.image, self.rect)

class WeaponGroup:
    def __init__(self, screen):
        self.weapons = [Weapon(screen, 100, 100) for _ in range(3)]

    def update(self):
        for weapon in self.weapons:
            weapon.update()

    def draw(self, offset_x, offset_y):
        for weapon in self.weapons:
            weapon.screen.blit(weapon.image, (weapon.rect.x + offset_x, weapon.rect.y + offset_y))