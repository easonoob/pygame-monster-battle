import pygame
import os
import math

class HealthBar:
    def __init__(self, screen, x, y, width, height, color, background_color, font_size=36, font_color=(0, 0, 0)):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.background_color = background_color
        self.current_health = 100
        self.max_health = 100
        self.font_size = font_size
        self.font_color = font_color
        
        self.font = pygame.font.Font(None, self.font_size)

    def set_health(self, health):
        self.current_health = max(0, min(health, self.max_health))

    def draw(self):
        pygame.draw.rect(self.screen, self.background_color, (self.x, self.y, self.width, self.height))
        
        fill_width = self.width * (self.current_health / self.max_health)
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, fill_width, self.height))

        health_text = f"{round(self.current_health, 1)}"
        text_surface = self.font.render(health_text, True, self.font_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        self.screen.blit(text_surface, text_rect)

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
        self.mask = pygame.mask.from_surface(self.image)
        self.weapon = None
        self.center_offset = 20

        self.health = 100
        w, h = pygame.display.get_surface().get_size()
        self.health_bar = HealthBar(screen, 100, h-100, 500, 50, (0, 255, 0), (255, 0, 0))

    def update(self, keys, obstacles, weapons, monsters):

        collided = pygame.sprite.spritecollide(self, monsters.monsters, False)
        if collided:
            self.health -= 0.1 * len(collided)
            self.health_bar.set_health(self.health)

        original_rect = self.rect.copy()
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
        original_rect = self.rect.copy()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.rect.centerx - offset_x
        dy = mouse_y - self.rect.centery - offset_y
        angle = math.degrees(math.atan2(-dy, dx)) - 90

        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        original_rect = self.check_collision(obstacles, original_rect)
        self.mask = pygame.mask.from_surface(self.image)
        
        # self.rect.centery += self.center_offset if self.weapon is not None else 0
    
    def check_collision(self, obstacles, original_rect):
        if pygame.sprite.collide_mask(self, obstacles.obstacle_map):
            self.rect = original_rect
        return self.rect.copy()

    def draw(self, offset_x, offset_y):
        self.screen.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))
        self.health_bar.draw()