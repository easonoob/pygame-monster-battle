import pygame
from src.player import Player
from src.weapons import WeaponGroup
from src.obstacles import ObstacleGroup

# Initialize the game
pygame.init()

# Screen dimensions
screen_width, screen_height = 1600, 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Battle Royale")

def main():
    running = True
    clock = pygame.time.Clock()
    
    # Initialize game components
    player = Player(screen, 50, 50, 'player.png')
    weapons = WeaponGroup(screen)
    obstacles = ObstacleGroup(screen, 'obstacles.png')

    # Game loop
    while running:
        screen.fill((150, 100, 50))  # Fill the screen with black
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game components
        player.update(pygame.key.get_pressed(), obstacles)
        weapons.update()
        obstacles.update()

        # Calculate the offset to keep the player in the center of the screen
        offset_x = screen_width // 2 - player.rect.centerx
        offset_y = screen_height // 2 - player.rect.centery

        # Draw everything relative to the offset
        obstacles.draw(offset_x, offset_y)
        player.draw(offset_x, offset_y)
        weapons.draw(offset_x, offset_y)

        pygame.display.flip()
        clock.tick(100)

    pygame.quit()

if __name__ == "__main__":
    main()
