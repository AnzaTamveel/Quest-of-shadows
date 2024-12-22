import pygame
import sys
from bk import Game
import bkmaze

 
pygame.init()
game = Game() 
GRID_SIZE=59
SCREEN_WIDTH = game.current_level.maze.width * GRID_SIZE
SCREEN_HEIGHT = game.current_level.maze.height * GRID_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Level Selection")
import pygame
import sys
from PIL import Image
import time
pygame.init()
 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze of Shadows")
menu_bg_image = pygame.image.load("menu_bg.png").convert()
menu_bg_image = pygame.transform.scale(menu_bg_image, (1000, 1000))
font = pygame.font.SysFont(None, 55)

def load_and_resize_gif(gif_path, resize_to):
    gif = Image.open(gif_path)
    frames = []
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_image = gif.copy().convert('RGBA')
        frame_image = frame_image.resize(resize_to, Image.Resampling.LANCZOS)
        frame_data = pygame.image.fromstring(frame_image.tobytes(), frame_image.size, frame_image.mode)
        frames.append(frame_data)
    return frames

intro_gif_frames = load_and_resize_gif('play.gif', (SCREEN_WIDTH-30, SCREEN_HEIGHT))

def show_intro():
    """Function to display the intro with GIF animation and game title."""
 
    for frame in intro_gif_frames:
        screen.blit(frame, (0, 0))
        pygame.display.flip()
        pygame.time.wait(100)   
   
    animate_text("Quest of", SCREEN_WIDTH - 300, SCREEN_HEIGHT - 110, 100)
    animate_text("Shadows", SCREEN_WIDTH - 280, SCREEN_HEIGHT - 60, 100)

def animate_text(text, x, y, delay):
    """Function to animate text display."""
    for i in range(1, len(text) + 1):
        screen.fill((0, 0, 0))  
        screen.blit(intro_gif_frames[-1], (0, 0))  
        draw_text(text[:i], font, (255, 255, 255), screen, x, y)
        pygame.display.flip()
        pygame.time.wait(delay)

def draw_text(text, font, color, surface, x, y):
    """Helper function to draw text on the screen."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

 
 
font = pygame.font.SysFont(None, 55)
game = Game()
bg_image_level1 = pygame.image.load("bg_1.png").convert()
bg_image_level2 = pygame.image.load("bg_2.png").convert()
bg_image_level3 = pygame.image.load("bg_3.png").convert()
bg_image_level4 = pygame.image.load("bg_4.png").convert()
bg_image_level5 = pygame.image.load("bg_5.png").convert()
bg_width = 1000
bg_height = 120   
bg_height5 = 550
bg_image_level1 = pygame.transform.scale(bg_image_level1, (bg_width, bg_height))
bg_image_level2 = pygame.transform.scale(bg_image_level2, (bg_width, bg_height))
bg_image_level3 = pygame.transform.scale(bg_image_level3, (bg_width, bg_height))
bg_image_level4 = pygame.transform.scale(bg_image_level4, (bg_width, bg_height))
bg_image_level5 = pygame.transform.scale(bg_image_level5, (bg_width, bg_height5))
level_to_bg_image = {
    1: bg_image_level1,
    2: bg_image_level2,
    3: bg_image_level3,
    4: bg_image_level4,
    5: bg_image_level5
}

def draw_text(text, font, color, surface, x, y):
    """Helper function to draw text on the screen."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

qos_image = pygame.image.load('qos.png')
qos_image = pygame.transform.scale(qos_image, (300, 100))   
qos_image_rect = qos_image.get_rect(center=(SCREEN_WIDTH / 2, 100))
p = pygame.image.load('p.png')
p = pygame.transform.scale(p, (80, 50))   
pr = qos_image.get_rect(center=((SCREEN_WIDTH / 2)+100, 280))
e = pygame.image.load('e.png')
e = pygame.transform.scale(e, (80, 50))   
er = qos_image.get_rect(center=((SCREEN_WIDTH / 2)+100, 480))
r = pygame.image.load('r.png')
pygame.mixer.init()
x = pygame.mixer.Sound('gm.wav')
r= pygame.transform.scale(r, (80, 50))   
rr = qos_image.get_rect(center=((SCREEN_WIDTH / 2)+100, 380))
p_rect = pygame.Rect((SCREEN_WIDTH // 2) - 40, 240, 80, 50)
e_rect = pygame.Rect((SCREEN_WIDTH // 2) - 40, 340, 80, 50)
r_rect = pygame.Rect((SCREEN_WIDTH // 2) - 40, 440, 80, 50)

def show_menu():
    """Function to show the main menu."""
    menu_active = True
    while menu_active:
        x.play() 
        screen.blit(menu_bg_image, (0, 0))   
        screen.blit(qos_image, qos_image_rect.topleft)
        screen.blit(p, pr.topleft)
        screen.blit(e, er.topleft)
        screen.blit(r, rr.topleft)
        
       
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if p_rect.collidepoint(mouse_x, mouse_y):
                    menu_active = False   
                elif e_rect.collidepoint(mouse_x, mouse_y):
                    show_rules()
                elif r_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()
rules_bg_image = pygame.image.load('rules.png').convert()
rules_bg_image = pygame.transform.scale(rules_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def show_rules():
    """Function to display the game rules."""
    rules_active = True
    while rules_active:
        screen.blit(rules_bg_image, (0, 0))   
        draw_text('back', font, (255, 255, 255), screen, 350, 580)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 350 <= mouse_x <= 650 and 580 <= mouse_y <= 630:
                    rules_active = False   
def draw_levels():
    """Draw levels and their statuses on the screen with background images."""
    y_offset = 0   
    for level_num, level in game.levels:
        if level is not None:   
            bg_image = level_to_bg_image.get(level.level_number, bg_image_level1)  
            screen.blit(bg_image, (0, y_offset))   

            color = (255, 255, 255) if level.status == "unlocked" else (128, 128, 128)
            status_text = " (Locked)" if level.status == "locked" else " (Unlocked)" if level.status == "unlocked" else " (Completed)"
            text = font.render(f"Level {level.level_number}{status_text}", True, color)
            screen.blit(text, (50, y_offset + 25))   
        
        y_offset += bg_height   
    draw_text('Main Menu', font, (255, 255, 255), screen, 53, y_offset)
    pygame.display.flip()

def main():
    """Main function for the level selection menu."""
    while True:
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                y_offset = 25 
                for level_num in range(1, game.levels.size + 1):
                    level = game.get_level(level_num)
                    if level is not None:   
                        if 50 <= mouse_x <= 750 and y_offset <= mouse_y <= y_offset + 50:
                            if level.status != "locked":
                                print(f"Level {level.level_number} selected")
                                game.current_level_number = level.level_number
                                game.current_level = level
                                return level.level_number  
                        y_offset += bg_height   
                if 0 <= mouse_x <= 154 and y_offset-15 <= mouse_y <= y_offset + 75:
                    show_menu()
        draw_levels()

if __name__ == "__main__":
    # show_intro()
 
    show_menu()
    while True:   
        
        game = Game()   
        game.load_game_state()  
        selected_level = main()
        if selected_level:
           
            import bkmaze
            bkmaze.start_game_with_level(selected_level)
