import pygame
import sys
from bk import Game
import bklevel

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

font = pygame.font.SysFont(None, 55)

game = Game()

# Background Images
bg_image = pygame.image.load("bg_1.png").convert()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_text(text, font, color, surface, x, y):
    """Draw text on the screen."""
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

def rules_page():
    """Display the rules page."""
    while True:
        screen.fill((0, 0, 0))

        draw_text('Game Rules', font, (255, 255, 255), screen, 300, 50)
        draw_text('1. Kill enemy to get key', font, (255, 255, 255), screen, 50, 150)
        draw_text('2. Use key to get treasure', font, (255, 255, 255), screen, 50, 200)
        draw_text('3. Collect all treasures to open gate', font, (255, 255, 255), screen, 50, 250)
        draw_text('4. Avoid volcanoes - they will kill you', font, (255, 255, 255), screen, 50, 300)
        draw_text('5. You have 3 lives', font, (255, 255, 255), screen, 50, 350)
        draw_text('Click here to return to main menu', font, (255, 255, 255), screen, 150, 500)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(150, 500, 500, 50).collidepoint(pygame.mouse.get_pos()):
                    main_menu()

        pygame.display.update()

def main_menu():
    """Display the main menu."""
    while True:
        screen.blit(bg_image, (0, 0))
        draw_text('Welcome to the Game', font, (255, 255, 255), screen, 250, 50)
        draw_text('Play', font, (255, 255, 255), screen, 350, 200)
        draw_text('Rules', font, (255, 255, 255), screen, 350, 300)
        draw_text('Exit', font, (255, 255, 255), screen, 350, 400)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Handle Play Button
                if pygame.Rect(350, 200, 100, 50).collidepoint((mouse_x, mouse_y)):
                    # Load game state and go to level selection
                    game.load_game_state()
                    selected_level = bklevel.main()  # Call the bklevel's main function
                    if selected_level:  # If a level is selected
                        import bkmaze
                        bkmaze.start_game_with_level(selected_level)  # Start the selected level

                # Handle Rules Button
                if pygame.Rect(350, 300, 100, 50).collidepoint((mouse_x, mouse_y)):
                    rules_page()

                # Handle Exit Button
                if pygame.Rect(350, 400, 100, 50).collidepoint((mouse_x, mouse_y)):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main_menu()
