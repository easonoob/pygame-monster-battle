import pygame
from src.player import Player
from src.weapons import WeaponGroup
from src.obstacles import ObstacleGroup
from src.monster import MonsterGroup

pygame.init()

screen_width, screen_height = 1600, 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Battle Royale")

def main():
    running = True
    clock = pygame.time.Clock()
    
    # Initialize game components
    player = Player(screen, 150, 150, 'player_fists1.png')
    weapons = WeaponGroup(screen, 1921, 1021)
    obstacles = ObstacleGroup(screen, 'obstacles.png')
    monsters = MonsterGroup(screen, 1921, 1021, 5, obstacles)

    bullets = pygame.sprite.Group()

    while running:
        screen.fill((150, 100, 50))# 150, 100, 50

        keys = pygame.key.get_pressed()
        player.update(keys, obstacles, weapons)
        
        weapons.update()
        obstacles.update()

        # Calculate the offset to keep the player in the center of the screen
        offset_x = screen_width // 2 - player.rect.centerx
        offset_y = screen_height // 2 - player.rect.centery

        monsters.update(bullets, player.rect, obstacles, offset_x, offset_y)

        # Draw everything relative to the offset
        obstacles.draw(offset_x, offset_y)
        weapons.draw(offset_x, offset_y)
        player.update_direction(obstacles, offset_x, offset_y)
        player.draw(offset_x, offset_y)
        monsters.draw(offset_x, offset_y)
        
        bullets.update(obstacles)
        for bullet in bullets:
            # if not bullet.alive:
            #     bullet.kill()
            #     bullets.remove(bullet)
            #     del bullet
            # else:
            bullet.draw(offset_x, offset_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.weapon:
                    bullet = player.weapon.shoot(player, pygame.mouse.get_pos(), offset_x, offset_y)
                    if bullet is not None: bullets.add(bullet)
                    # print(bullets)

        pygame.display.flip()
        clock.tick(100)

    pygame.quit()

if __name__ == "__main__":
    main()
