import pygame
import os
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, image_file):
        super().__init__()
        self.screen = screen
        self.base_image = pygame.image.load(os.path.join('assets', image_file)).convert_alpha()
        self.base_image = pygame.transform.scale(self.base_image, (80, 80))  # Scale down the image
        self.weapon_image = pygame.image.load(os.path.join('assets', 'player_weapon.png')).convert_alpha()
        self.weapon_image = pygame.transform.scale(self.weapon_image, (80, 140))  # Scale down the image
        self.image = self.base_image
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask for the player
        self.alive = True
        self.weapon = None
        self.center_offset = 20

    def update(self, keys, obstacles, weapons):
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
        
        # Check for weapon pickup
        if keys[pygame.K_f]:
            for weapon in weapons.weapons:
                if pygame.sprite.collide_rect(self, weapon):
                    self.weapon = weapon
                    weapons.weapons.remove(weapon)
                    self.image = self.weapon_image
                    self.mask = pygame.mask.from_surface(self.image)
                    self.original_image = self.weapon_image
                    break
        
    def update_direction(self, obstacles, offset_x, offset_y):
        original_rect = self.rect.copy()  # Store the original position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate the angle to the mouse
        dx = mouse_x - self.rect.centerx - offset_x
        dy = mouse_y - self.rect.centery - offset_y
        angle = math.degrees(math.atan2(-dy, dx)) - 90  # atan2 returns angle in radians

        # Rotate the image
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        original_rect = self.check_collision(obstacles, original_rect)
        self.mask = pygame.mask.from_surface(self.image)
        
        # Adjust the center downwards
        # self.rect.centery += self.center_offset if self.weapon is not None else 0
    
    def check_collision(self, obstacles, original_rect):
        if pygame.sprite.collide_mask(self, obstacles.obstacle_map):
            self.rect = original_rect
        return self.rect.copy()

    def draw(self, offset_x, offset_y):
        self.screen.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))