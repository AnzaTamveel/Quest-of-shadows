import pygame
import sys
from bk import Game
import time
pygame.init()
from PIL import Image

BLACK = (0, 0, 0)
BULLET_COLOR = (0, 0, 0)
GREY=(87, 88, 93)
GRID_SIZE = 59  
FPS = 60
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()
game = Game() 
SCREEN_WIDTH = game.current_level.maze.width * GRID_SIZE
SCREEN_HEIGHT = game.current_level.maze.height * GRID_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pause_button_image = pygame.image.load('pb.png')

pause_button_image = pygame.transform.scale(pause_button_image, (44, 44))   
pause_button_rect = pause_button_image.get_rect(topleft=(10, 5))  
bullets = []
bullet_image = pygame.image.load('bullet.png')
bullet_image = pygame.transform.scale(bullet_image, (15, 15)) 
player_bullets = []
visited_positions = set()

def draw_pause_button(screen):
    screen.blit(pause_button_image, pause_button_rect)

def draw_pause_menu(screen):
    font = pygame.font.SysFont(None, 75)
    menu_text = font.render("Paused", True, (255, 255, 255))
    resume_text = font.render("Resume", True, (255, 255, 255))
    restart_text = font.render("Restart", True, (255, 255, 255))
    quit_text = font.render("Quit", True, (255, 255, 255))
 
    screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
    screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 150))

def check_pause_menu_click(mouse_pos):
    print(f"Mouse position: {mouse_pos}")
    resume_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
    restart_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2+ 50, 200, 50)
    quit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50)

    if resume_rect.collidepoint(mouse_pos):
        print("Resume button clicked.")
        return "resume"
    elif restart_rect.collidepoint(mouse_pos):
        print("Restart button clicked.")
        return "restart"
    elif quit_rect.collidepoint(mouse_pos):
        print("Quit button clicked.")
        return "quit"
    return None

def handle_pause_button_click(mouse_pos):
    if pause_button_rect.collidepoint(mouse_pos):
        return True
    return False

def draw_lives(screen, lives):
    heart_img = pygame.image.load("live.png").convert_alpha()
    heart_img = pygame.transform.scale(heart_img, (30, 30))  
    x_offset = 60   
    y_offset = 10   

    for _ in range(lives):
        screen.blit(heart_img, (x_offset, y_offset))
        x_offset += 40   
def auto_win():
    """Automatically moves the player to the target location and ends the game."""
    
    print("Traversed Path before removal: ", game.current_level.maze.get_dynamic_objects_positions())
    print("Items before removal: \n", game.current_level.maze.hurdles.items)
    
    traversed_path = game.current_level.maze.get_dynamic_objects_positions()
 
    for target in traversed_path:
        path = target['path']   
        item_type = target['type']
        target_position = target['position']   
        target_index = target['index']   
        draw_maze()

        
        for (x, y) in path:
            game.current_level.maze.player.move_to(x, y)
            delta_time = clock.get_time() / 1000.0   
            while game.current_level.maze.player.moving:
                delta_time = clock.get_time() / 1000.0   
                game.current_level.maze.player.update(delta_time)
                screen.blit(background_image, (0, 0))
                draw_maze()
                draw_maze()
                frame = player_idle_gif_frames[0]   
                screen.blit(frame, (game.current_level.maze.player.x * GRID_SIZE, game.current_level.maze.player.y * GRID_SIZE))  # Draw player
                pygame.display.update()
                clock.tick(FPS)

             
            if (x, y) == target_position:
                if item_type == 'enemy':
                    for ind, data in list(game.current_level.maze.hurdles.items.items()):  
                        print("ind", ind, "data", data)
                        if ind == target_index:
                            
                            del game.current_level.maze.hurdles.items[ind]
                            if ind in game.current_level.maze.hurdles.enemy_positions:
                                del game.current_level.maze.hurdles.enemy_positions[ind]
                            print(f"Enemy at {(x, y)} removed from the items list.")
                            draw_maze()
                            break
                elif item_type == 'treasure':
                    for ind, data in game.current_level.maze.hurdles.items.items():
                        print("ind", ind, "data", data)
                        if ind == target_index:
                             
                            del game.current_level.maze.hurdles.items[ind]
                            print(f"Collected treasure at ({x}, {y})")
                            draw_maze()
                            break
                elif item_type == 'win':
                    print(f"Reached winning door at ({x}, {y})")

    
   
    print("Auto win completed!")
    next_screen()

def next_screen():
    """Display the next screen with a button to go back to the level selection."""
    next_button_image = pygame.image.load('c.png')
    next_button_image = pygame.transform.scale(next_button_image, (200, 100))
    next_button_rect = next_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    
    font = pygame.font.Font(None, 36)  
    running = True

    while running:
        
        screen.blit(background_image, (0, 0))   
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  
        overlay.set_alpha(150) 
        overlay.fill((0, 0, 245)) 
        screen.blit(overlay, (0, 0)) 
        won_text = font.render("Player Won!", True, (255, 255, 255))   
        screen.blit(won_text, (SCREEN_WIDTH // 2 - won_text.get_width() // 2, SCREEN_HEIGHT // 3 - 50))
        note_text = font.render("The next level will only be unlocked if", True, (255, 255, 255))  
        screen.blit(note_text, (SCREEN_WIDTH // 2 - note_text.get_width() // 2, SCREEN_HEIGHT // 3))
        
        note_text_2 = font.render("the player won the game manually.", True, (255, 255, 255))  
        screen.blit(note_text_2, (SCREEN_WIDTH // 2 - note_text_2.get_width() // 2, SCREEN_HEIGHT // 3 + 30))
        screen.blit(next_button_image, next_button_rect)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button_rect.collidepoint(event.pos):
                    running = False

def draw_darkness_effect(player_x, player_y):
    """Overlay a darkness effect with a visible area around the player."""
    global visited_positions
    darkness_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    darkness_surface.fill((0, 0, 0, 245))  
    
 
    visited_positions.add((player_x, player_y))
     
    square_size = 90   
    for pos in visited_positions:
        rect = pygame.Rect(pos[0] - square_size // 2, pos[1] - square_size // 2, square_size, square_size)
        pygame.draw.rect(darkness_surface, (0, 0, 0, 0), rect)
 
    screen.blit(darkness_surface, (0, 0))

def update_visited_positions():
    player_x = int(game.player.anim_x * GRID_SIZE + GRID_SIZE // 2)
    player_y = int(game.player.anim_y * GRID_SIZE + GRID_SIZE // 2)
    visited_positions.add((player_x, player_y))

def initailize_enemy():
    for enemy in game.current_level.maze.hurdles.enemy_positions.values():
        enemy['direction'] = 'right'  
        enemy['moving_left'] = False
        enemy['moving_right'] = True

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

def reinitialize_resources(level_number):
    global player_idle_gif_frames,player_walk_gif_frames,enemy_image, death_frames, lava_frames, treasure_frames, open_door_image, key_image, door_image, background_image, treasure_image, wall, wall1, e_bullet_image
    e_bullet_image = pygame.image.load(f'bullet_{level_number}.png')
    e_bullet_image = pygame.transform.scale(e_bullet_image, (20, 20))   
    player_idle_gif_frames = load_and_resize_gif('idle.gif', (GRID_SIZE -5, GRID_SIZE -3))
    player_walk_gif_frames = load_and_resize_gif('walk.gif', (GRID_SIZE - 5, GRID_SIZE - 3))

    enemy_image = load_and_resize_gif(f'bhoot_{level_number}.gif', (GRID_SIZE + 8, GRID_SIZE))
    death_frames = load_and_resize_gif(f'dead_{level_number}.gif', (SCREEN_WIDTH+300, SCREEN_HEIGHT+300))
    lava_frames = load_and_resize_gif(f'lava_{level_number}.gif', (GRID_SIZE+15, GRID_SIZE-10))
    treasure_frames = load_and_resize_gif('treasureopen.gif', (GRID_SIZE + 8, GRID_SIZE + 8))
    open_door_image = pygame.image.load(f'open_{level_number}.png')
    open_door_image = pygame.transform.scale(open_door_image, ((GRID_SIZE / 2) + 25, GRID_SIZE - 10))
    key_image = pygame.image.load(f'key_{level_number}.png')
    key_image = pygame.transform.scale(key_image, ((GRID_SIZE) - 10, GRID_SIZE - 10))
    door_image = pygame.image.load(f'door_{level_number}.png')
    door_image = pygame.transform.scale(door_image, ((GRID_SIZE / 2) + 15, GRID_SIZE - 10))
    background_image = pygame.image.load(f'bg_{level_number}.png')
    background_image = pygame.transform.scale(background_image, (game.current_level.maze.width * GRID_SIZE, game.current_level.maze.height * GRID_SIZE))
    treasure_image = pygame.image.load(f'box_{level_number}.png')
    treasure_image = pygame.transform.scale(treasure_image, (GRID_SIZE - 5, GRID_SIZE - 5))
    wall = pygame.image.load(f'walls_{level_number}.png')
    wall = pygame.transform.scale(wall, (12, GRID_SIZE + 16))
    wall1 = pygame.image.load(f'walls_{level_number}.png')
    wall1 = pygame.transform.scale(wall, (GRID_SIZE, 16))
       
def draw_enemies(game):
    try:
        enemy_frame_index = int(pygame.time.get_ticks() / 100) % len(enemy_image)  
        for enemy in game.current_level.maze.hurdles.enemy_positions.values():
            enemy_x = int(enemy['anim_x'] * GRID_SIZE + GRID_SIZE // 2 - 12)
            enemy_y = int(enemy['anim_y'] * GRID_SIZE + GRID_SIZE // 2 -10)
            if enemy['moving_left']:
                flipped_enemy_image = pygame.transform.flip(enemy_image[enemy_frame_index], True, False)
                screen.blit(flipped_enemy_image, (enemy_x - GRID_SIZE // 4, enemy_y - GRID_SIZE // 4))
            else:
                screen.blit(enemy_image[enemy_frame_index], (enemy_x - GRID_SIZE // 4, enemy_y - GRID_SIZE // 4))
    except Exception as e:
        print(f"Error in draw_enemies: {e}")
def draw_auto_btn(screen):
    global auto_win_btn_rect
    auto_win_btn = pygame.image.load('c.png')   
    auto_win_btn = pygame.transform.scale(auto_win_btn, (90, 50))  
    auto_win_btn_rect = auto_win_btn.get_rect(topleft=(500, 0))   
    screen.blit(auto_win_btn, auto_win_btn_rect)
    
def draw_maze():
    """Draw the maze grid based on the adjacency list."""
    current_time = time.time()
    lava_frame_index = int(pygame.time.get_ticks() / 100) % len(lava_frames)  
    treasure_frame_index = int(pygame.time.get_ticks() / 100) % len(treasure_frames)  
    
    for y in range(game.current_level.maze.height):
        for x in range(game.current_level.maze.width):
            cell_index = y * game.current_level.maze.width + x
             
            if x < game.current_level.maze.width - 1:  
                if (cell_index + 1) not in game.current_level.maze.adj[cell_index]:
                    screen.blit(wall, (x * GRID_SIZE + GRID_SIZE - 2, y * GRID_SIZE))
           
            if y < game.current_level.maze.height - 1:  
                if (cell_index + game.current_level.maze.width) not in game.current_level.maze.adj[cell_index]:
                    screen.blit(wall1, (x * GRID_SIZE, y * GRID_SIZE + GRID_SIZE))
            
            if cell_index in game.current_level.maze.hurdles.items:
                item = game.current_level.maze.hurdles.items[cell_index]
                if item == 'treasure':
                    screen.blit(treasure_image, ((x * GRID_SIZE + GRID_SIZE // 4) - 10, (y * GRID_SIZE + GRID_SIZE // 4) - 7))
                elif item == 'enemy' or item == 'enemy_with_key':
                    draw_enemies(game)
                elif item == 'volcano':
                 
                    screen.blit(lava_frames[lava_frame_index], (x * GRID_SIZE-2, y * GRID_SIZE+8))
                elif item == 'key':
                    screen.blit(key_image, ((x * GRID_SIZE + GRID_SIZE // 4)-5, (y * GRID_SIZE + GRID_SIZE // 4)))  # Draw key image
                elif item == 'win' or item == 'false_win':
                    if game.change_doors_to_open():
                        
                        screen.blit(open_door_image, ((x * GRID_SIZE + GRID_SIZE // 4), (y * GRID_SIZE + GRID_SIZE // 4)))
                    else:
                    
                        screen.blit(door_image, ((x * GRID_SIZE + GRID_SIZE // 4), (y * GRID_SIZE + GRID_SIZE // 4)))

            
            for (collected_x, collected_y, collected_time) in game.collected_treasures:
                if current_time - collected_time < 1:   
                    screen.blit(treasure_frames[treasure_frame_index], ((collected_x * GRID_SIZE + GRID_SIZE // 4) - 15, (collected_y * GRID_SIZE + GRID_SIZE // 4) - 10))

 
player_image = pygame.image.load('idl.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (GRID_SIZE, GRID_SIZE))
def draw_player():
    """Draw the player at their current position with GIF animation based on movement."""
    if game.player.moving:
        player_frames = player_walk_gif_frames
    else:
        player_frames = player_idle_gif_frames

    player_frame_index = int(pygame.time.get_ticks() / 100) % len(player_frames)
    player_image = player_frames[player_frame_index]

    player_x = int(game.player.anim_x * GRID_SIZE + GRID_SIZE // 2 - (player_image.get_width() // 2))
    player_y = int(game.player.anim_y * GRID_SIZE + GRID_SIZE // 2 - (player_image.get_height() // 2))

    if game.player.direction == 'right':
        flipped_player_image = pygame.transform.flip(player_image, True, False)
        screen.blit(flipped_player_image, (player_x, player_y))
    else:
        screen.blit(player_image, (player_x, player_y))

def handle_player_shooting():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:   
        player_x = game.player.x * GRID_SIZE + GRID_SIZE // 2
        player_y = game.player.y * GRID_SIZE + GRID_SIZE // 2
         
        nearest_enemy = None
        nearest_distance = float('inf')
        for enemy in game.current_level.maze.hurdles.enemy_positions.values():
            enemy_x = int(enemy['anim_x'] * GRID_SIZE + GRID_SIZE // 2)
            enemy_y = int(enemy['anim_y'] * GRID_SIZE + GRID_SIZE // 2)
            distance_to_enemy = ((player_x - enemy_x) ** 2 + (player_y - enemy_y) ** 2) ** 0.5
            if distance_to_enemy < nearest_distance:
                nearest_enemy = (enemy_x, enemy_y)
                nearest_distance = distance_to_enemy
         
        if nearest_enemy:
            target_x, target_y = nearest_enemy
            player_bullet = Bullet(player_x, player_y, target_x, target_y, bullet_image)
            player_bullets.append(player_bullet)
        else:
            target_x = player_x + GRID_SIZE * 2
            player_bullet = Bullet(player_x, player_y, target_x, player_y, bullet_image)
            player_bullets.append(player_bullet)

def draw():
    
    screen.blit(background_image, (0, 0))
    draw_maze()
    draw_player()
    draw_enemies(game)
 
    for bullet in bullets:
        bullet.draw(screen)
    for bullet in player_bullets:
        bullet.draw(screen)
 
    update_visited_positions()
     
    player_x = int(game.player.anim_x * GRID_SIZE + GRID_SIZE // 2)
    player_y = int(game.player.anim_y * GRID_SIZE + GRID_SIZE // 2)
 
    draw_darkness_effect(player_x, player_y)


def start_game_with_level(level_number):
    global game, key_direction, previous_level, is_paused, showing_death_screen, bullets, player_bullets, visited_positions, screen
    x = game.check_for_item()
    game.current_level_number = level_number
    game.current_level = game.get_level(level_number)
    game.current_level.restart(game)   
    SCREEN_WIDTH = game.current_level.maze.width * GRID_SIZE
    SCREEN_HEIGHT = game.current_level.maze.height * GRID_SIZE
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
     
    reinitialize_resources(level_number)
    initailize_enemy()
    blast = pygame.mixer.Sound('blast.wav')
    is_paused = False
    showing_death_screen = False
    key_direction = None
    previous_level = game.current_level_number
    visited_positions = set()
    bullets = []
    player_bullets = []

    while game.is_running or showing_death_screen:
        delta_time = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting game.")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    is_paused = not is_paused
                    print("Pause toggled. Paused:", is_paused)
                elif event.key == pygame.K_m:
                    print("Returning to level selection.")
                    return  
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    key_direction = event.key
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    if key_direction == event.key:
                        key_direction = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if auto_win_btn_rect.collidepoint(mouse_pos):
                    auto_win()
                    return
                if handle_pause_button_click(mouse_pos):
                    is_paused = not is_paused
                    print("Pause button clicked. Paused:", is_paused)
                elif is_paused:
                    action = check_pause_menu_click(mouse_pos)
                    if action == "resume":
                        is_paused = False
                        print("Resume selected.")
                    elif action == "restart":
                        print("Restart selected.")
                        start_game_with_level(game.current_level_number)
                        initailize_enemy()
                        is_paused = False
                    elif action == "quit":
                        print("Quit selected.")
                        print("Returning to level selection.")
                        return 

        if is_paused:
            draw_pause_menu(screen)
        else:
            if game.player_dead:
                blast.play()
                if game.death_time is None:
                    game.death_time = time.time()
                frame_index = int(pygame.time.get_ticks() / 100) % len(death_frames)
                screen.blit(death_frames[frame_index], (0, 0))
                font = pygame.font.SysFont(None, 75)
                text = font.render("You Die", True, BLACK)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(text, text_rect)
                if time.time() - game.death_time > 2:
                    print("Player died. Exiting game.")
                    showing_death_screen = False
                    game.player_dead = False
                    blast.stop()
                    return
            else:
                if key_direction is not None and not game.player.moving:
                    target_x, target_y = game.player.x, game.player.y
                    if key_direction == pygame.K_UP:
                        target_y -= 1
                    elif key_direction == pygame.K_DOWN:
                        target_y += 1
                    elif key_direction == pygame.K_LEFT:
                        target_x -= 1
                        game.player.update_direction('right')
                    elif key_direction == pygame.K_RIGHT:
                        target_x += 1
                        game.player.update_direction('left')

                    if game.is_valid_move(target_x, target_y):
                        game.move_player(target_x, target_y)
                    

                handle_player_shooting()
                game.player.update(delta_time)
                if not game.player.moving:
                    x = game.check_for_item()
                if x:
                    if game.current_level_number > previous_level:
                        start_game_with_level(game.current_level_number)
                        previous_level = game.current_level_number
                        
                        visited_positions.clear()

                game.current_level.maze.hurdles.move_enemies(delta_time)
                bullets_to_create = []
                game.current_level.maze.hurdles.shoot_if_player_near(game.player, bullets_to_create, 5, GRID_SIZE)

                for bullet_data in bullets_to_create:
                    bullet = Bullet(bullet_data['start_x'], bullet_data['start_y'], bullet_data['target_x'], bullet_data['target_y'], e_bullet_image)
                    bullets.append(bullet)

                for bullet in bullets:
                    bullet.update(delta_time)
                    if bullet.check_collision_with_wall(game) or bullet.check_collision_with_player(game.player, game):
                        bullets.remove(bullet)

                for bullet in player_bullets:
                    bullet.update(delta_time)
                    enemy_hit_key = bullet.check_collision_with_enemy(game.current_level.maze.hurdles.enemy_positions)
                    if enemy_hit_key is not None:
                        game.enemy_encounter(enemy_hit_key)
                        del game.current_level.maze.hurdles.enemy_positions[enemy_hit_key]
                        
                        player_bullets.remove(bullet)
                    elif bullet.check_collision_with_wall(game) or not (0 <= bullet.x < SCREEN_WIDTH and 0 <= bullet.y < SCREEN_HEIGHT):
                        player_bullets.remove(bullet)
                
                screen.fill(GREY)
                draw()
                draw_pause_button(screen)
                draw_lives(screen, game.player_lives)
                draw_auto_btn(screen)
            
                if game.falsewin == True:
                    print("----------after trap------??????.....")
                    return
           
        pygame.display.flip()
class Bullet:
    def __init__(self, x, y, target_x, target_y, bullet_image):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 60.0
        self.distance = ((target_x - x) ** 2 + (target_y - y) ** 2) ** 0.5
        if self.distance == 0:
            self.distance = 1e-6
        self.has_reached_target = False
        self.image = bullet_image   

    def update(self, delta_time):
        if self.has_reached_target:
            return 
        direction_x = (self.target_x - self.x) / self.distance
        direction_y = (self.target_y - self.y) / self.distance
        self.x += direction_x * self.speed * delta_time
        self.y += direction_y * self.speed * delta_time
        if abs(self.x - self.target_x) < 3 and abs(self.y - self.target_y) < 3:
            self.has_reached_target = True
            
    def draw(self, screen):
        if not self.has_reached_target:   
            screen.blit(self.image, (int(self.x), int(self.y)))

    def check_collision_with_wall(self, game):
        cell_x = int(self.x // GRID_SIZE)
        cell_y = int(self.y // GRID_SIZE)
        if cell_x < 0 or cell_y < 0 or cell_x >= game.current_level.maze.width or cell_y >= game.current_level.maze.height:
            return True
        cell_index = cell_y * game.current_level.maze.width + cell_x
        if self.x % GRID_SIZE < 1 or self.x % GRID_SIZE > GRID_SIZE - 1:
            if (cell_index + 1) not in game.current_level.maze.adj[cell_index]:
                return True
        if self.y % GRID_SIZE < 1 or self.y % GRID_SIZE > GRID_SIZE - 1:
            if (cell_index + game.current_level.maze.width) not in game.current_level.maze.adj[cell_index]:
                return True
        return False

   
    def check_collision_with_player(self, player, game):
        player_x = int(player.anim_x * GRID_SIZE + GRID_SIZE // 2)
        player_y = int(player.anim_y * GRID_SIZE + GRID_SIZE // 2)
        distance_to_player = ((self.x - player_x) ** 2 + (self.y - player_y) ** 2) ** 0.5
        if distance_to_player < GRID_SIZE // 4:
            game.handle_player_death()  
            return True
        return False


    def check_collision_with_enemy(self, enemies):
        for key, enemy in enemies.items():
            enemy_x = int(enemy['anim_x'] * GRID_SIZE + GRID_SIZE // 2)
            enemy_y = int(enemy['anim_y'] * GRID_SIZE + GRID_SIZE // 2)
            distance_to_enemy = ((self.x - enemy_x) ** 2 + (self.y - enemy_y) ** 2) ** 0.5
            if distance_to_enemy < GRID_SIZE // 59:
                print(enemy['hit_count'])
                enemy['hit_count'] += 1
                if enemy['hit_count'] >= 5:   
                    return key
        return None
