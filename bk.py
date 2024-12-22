import random
import math
from math import sqrt
import time
import pygame
import sys
sys.setrecursionlimit(2000) 
class StackNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, item):
        new_node = StackNode(item)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if not self.is_empty():
            value = self.top.value
            self.top = self.top.next
            return value
        else:
            raise IndexError("pop from an empty stack")

    def peek(self):
        if not self.is_empty():
            return self.top.value
        else:
            raise IndexError("peek from an empty stack")

    def is_empty(self):
        return self.top is None

    def size(self):
        count = 0
        current = self.top
        while current is not None:
            count += 1
            current = current.next
        return count

class QueueNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, item):
        new_node = QueueNode(item)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if not self.is_empty():
            value = self.front.value
            self.front = self.front.next
            if self.front is None:
                self.rear = None
            return value
        else:
            raise IndexError("dequeue from an empty queue")

    def peek(self):
        if not self.is_empty():
            return self.front.value
        else:
            raise IndexError("peek from an empty queue")

    def is_empty(self):
        return self.front is None

    def size(self):
        count = 0
        current = self.front
        while current is not None:
            count += 1
            current = current.next
        return count

class Maze:
    def __init__(self, width, height):
        self.V = width * height 
        self.width = width
        self.height = height
        self.adj = [[] for _ in range(self.V)]    
        self.visited = [False] * self.V   
        self.generate_dfs_maze(width,height)
        self.hurdles = Hurdles(self.adj, width, height)  
        self.player = Player(0, 0)   
    def add_edge(self, v, w):
        self.adj[v].append(w)
        self.adj[w].append(v)   
    def reset_player(self, position):  
        self.player.x, self.player.y = position 
    def get_player_position(self): return (self.player.x, self.player.y)
    def generate_dfs_maze(self, width, height):
        random.seed()
        stack = [0]   
        self.visited[0] = True
        while stack:
            v = stack[-1]
            x, y = v % width, v // width   
            neighbors = []
            if x < width - 1 and not self.visited[v + 1]:  
                neighbors.append(v + 1)
            if y < height - 1 and not self.visited[v + width]:   
                neighbors.append(v + width)
            if x > 0 and not self.visited[v - 1]:  # Left
                neighbors.append(v - 1)
            if y > 0 and not self.visited[v - width]:  # Up
                neighbors.append(v - width)
            random.shuffle(neighbors)
            if neighbors:
                next_cell = neighbors[0]
                stack.append(next_cell)
                self.add_edge(v, next_cell)   
                self.visited[next_cell] = True
            else:
                stack.pop() 
    def get_dynamic_objects_positions(self):
        """
        Dynamically find the nearest enemies, then treasures, and finally the win door,
        adjusting the player's position after each visit.
        """
        dynamic_objects = []  
        player_pos = self.get_player_position()

        enemies = []
        treasures = []
        win_door = None
        
        for node_value, object_type in self.hurdles.items.items():
            x = node_value % self.width
            y = node_value // self.width
            index = (x, y)   
            if object_type == 'enemy':
                enemies.append((index, node_value))  
            elif object_type == 'treasure':
                treasures.append((index, node_value))  
            elif object_type == 'win':
                win_door = (index, node_value)  

        
        all_objects = [('enemy', enemies), ('treasure', treasures)]
        for obj_type, obj_list in all_objects:
            while obj_list:
                
                obj_list = sorted(obj_list, key=lambda obj: self.calculate_distance(player_pos, obj[0]))                
 
                nearest_pos, nearest_index = obj_list.pop(0)
                path = self.find_path(player_pos, nearest_pos)
 
                dynamic_objects.append({'type': obj_type, 'position': nearest_pos, 'path': path, 'index': nearest_index})
     
                player_pos = nearest_pos

        
        if win_door and player_pos != win_door[0]:
            path = self.find_path(player_pos, win_door[0])
            dynamic_objects.append({'type': 'win', 'position': win_door[0], 'path': path, 'index': win_door[1]})

        return dynamic_objects

    def calculate_distance(self, pos1, pos2):
        """Calculate Euclidean distance between two positions (x1, y1) and (x2, y2)."""
        x1, y1 = pos1
        x2, y2 = pos2
        return sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def find_path(self, start, goal):
        """
        Find a valid path from the start to the goal using BFS.
        This function returns a list of valid positions from start to goal.
        """
        from collections import deque
 
        start_node = self.xy_to_node(start)
        goal_node = self.xy_to_node(goal)
 
        queue = deque([start_node])
        came_from = {start_node: None}
        visited = set()  
        
        visited.add(start_node)
        
        while queue:
            current_node = queue.popleft()
            
            
            if current_node == goal_node:
                break
 
            x, y = current_node % self.width, current_node // self.width
            neighbors = self.get_neighbors(x, y)
            
            for neighbor in neighbors:
               
                neighbor_node = self.xy_to_node(neighbor)
                 
                if neighbor_node not in visited and neighbor_node in self.adj[current_node]:
                    queue.append(neighbor_node)
                    visited.add(neighbor_node)
                    came_from[neighbor_node] = current_node
     
        path = []
        current_node = goal_node
        while current_node is not None:
            x, y = current_node % self.width, current_node // self.width
            path.append((x, y))
            current_node = came_from[current_node]
        
        path.reverse()  
        return path

    def xy_to_node(self, position):
        """Convert (x, y) coordinates to node index."""
        return position[1] * self.width + position[0]
    def get_neighbors(self, x, y):
        """Get neighbors of a cell (x, y)."""
        neighbors = []
        if x < self.width - 1: neighbors.append((x + 1, y))
        if y < self.height - 1: neighbors.append((x, y + 1))
        if x > 0: neighbors.append((x - 1, y))
        if y > 0: neighbors.append((x, y - 1))
        return neighbors  

class Player:
    def __init__(self, start_x, start_y):
        self.x, self.y = start_x, start_y
        self.target_x, self.target_y = start_x, start_y
        self.anim_x, self.anim_y = float(start_x), float(start_y)
        self.moving = False
        self.direction = 'right' 
        self.anim_x = 0 
        self.anim_y = 0
    def move_to(self, target_x, target_y):
        self.target_x, self.target_y = target_x, target_y
        self.moving = True
    def update_direction(self, new_direction): 
        if new_direction in ['left', 'right']: 
            self.direction = new_direction
    def update(self, delta_time, speed=7.0):
        if self.moving:
            dist_x = self.target_x - self.anim_x
            dist_y = self.target_y - self.anim_y
            distance = sqrt(dist_x**2 + dist_y**2)
            if distance < 0.5:
                self.anim_x, self.anim_y = self.target_x, self.target_y
                self.x, self.y = self.target_x, self.target_y
                self.moving = False
            else:
                self.anim_x += (dist_x / distance) * speed * delta_time
                self.anim_y += (dist_y / distance) * speed * delta_time

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.item = None
        
class Hurdles:
 
    def __init__(self, maze_adj, width, height):
        self.root = None
        self.width = width
        self.height = height
        self.items = {}   
        self.enemy_positions = {}  
        self.collected_treasures = 0
        self.total_treasures = 0
        self.defeated_enemies = 0
        self.total_enemies = 0
        self.maze_adj = maze_adj  
        self.enemy_move_delay = 0.5  
        self.enemy_move_timer = 0  
        self.enemy_shot_cooldown = 1.0  
        self.enemy_shot_timer = {}  
        self.build_tree(maze_adj)

    def assign_items_to_leaves(self, node):
        leaves = []
        self.collect_leaves(node, leaves)
    
        winning_node = random.choice(leaves)
        secondary_gate = random.choice([leaf for leaf in leaves if leaf != winning_node])
        
        winning_node.item = 'win'
        self.items[winning_node.value] = 'win'
        
        secondary_gate.item = 'false_win'
        self.items[secondary_gate.value] = 'false_win'
        print(str(self.total_treasures)+"---------;;;;")
        leaves = [leaf for leaf in leaves if leaf not in [winning_node, secondary_gate]]
   
        num_items = len(leaves)
        num_treasures = num_items // 2
        num_enemies = num_items - num_treasures
        
        random.shuffle(leaves)

        num_volcanoes = min(num_items // 4, len(leaves) // 3)  
        i = 0
        while num_volcanoes > 0 and i < len(leaves):
            neighbors = self.maze_adj[leaves[i].value]
            if len(neighbors) == 1:  
                leaves[i].item = 'volcano'
                self.items[leaves[i].value] = 'volcano'
                num_volcanoes -= 1
            i += 1
         
        leaves = [leaf for leaf in leaves if leaf.item != 'volcano']
        
        for i, leaf in enumerate(leaves):  
            if i < num_treasures:
                leaf.item = 'treasure'
                self.total_treasures += 1
                self.items[leaf.value] = 'treasure'
            else:
                leaf.item = 'enemy'
                self.enemy_positions[leaf.value] = {
                    'position': leaf.value,
                    'direction': 'forward',
                    'steps': 0,
                    'axis': 'horizontal' if random.choice([True, False]) else 'vertical',
                    'anim_x': float(leaf.value % self.width),
                    'anim_y': float(leaf.value // self.width),
                    'target_x': float(leaf.value % self.width),
                    'target_y': float(leaf.value // self.width),
                    'moving': False,
                    'halfway': False,   
                    'has_key': False,
                    'hit_count': 0
                }
                self.total_enemies += 1
                self.items[leaf.value] = 'enemy'
 
        if self.enemy_positions:
            random_enemy = random.choice(list(self.enemy_positions.keys()))
            self.enemy_positions[random_enemy]['has_key'] = True
        
    def shoot_if_player_near(self, player, bullets, distance_threshold, grid_size):
        """Make enemies shoot if the player is within a certain distance and there's no wall."""
        player_position = player.y * self.width + player.x
        for enemy, data in self.enemy_positions.items():
            enemy_position = data['position']
            if self.calculate_distance(player_position, enemy_position) <= distance_threshold and self.has_line_of_sight(enemy_position, player_position):
                current_time = pygame.time.get_ticks() / 1000.0  # Get current time in seconds
                if enemy not in self.enemy_shot_timer or current_time - self.enemy_shot_timer[enemy] >= self.enemy_shot_cooldown:
                    self.shoot_at_player(data, player, bullets, grid_size)
                    self.enemy_shot_timer[enemy] = current_time

    def calculate_distance(self, pos1, pos2):
        """Calculate the Manhattan distance between two positions."""
        x1, y1 = pos1 % self.width, pos1 // self.width
        x2, y2 = pos2 % self.width, pos2 // self.width
        return abs(x1 - x2) + abs(y1 - y2)

    def has_line_of_sight(self, start, end):
        """Check if there's a clear line of sight between two positions."""
        start_x, start_y = start % self.width, start // self.width
        end_x, end_y = end % self.width, end // self.width
 
        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)
        sx = 1 if start_x < end_x else -1
        sy = 1 if start_y < end_y else -1
        err = dx - dy

        while (start_x != end_x or start_y != end_y):
            current_index = start_y * self.width + start_x
            next_index = end_y * self.width + end_x
            if next_index not in self.maze_adj[current_index]:
                return False
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                start_x += sx
            if e2 < dx:
                err += dx
                start_y += sy

        return True

    def shoot_at_player(self, enemy, player, bullets, grid_size):
        """Handle shooting logic (e.g., create bullet)."""
        enemy_x = int(enemy['anim_x'] * grid_size + grid_size // 2)
        enemy_y = int(enemy['anim_y'] * grid_size + grid_size // 2)
        player_x = int(player.anim_x * grid_size + grid_size // 2)
        player_y = int(player.anim_y * grid_size + grid_size // 2)
        bullets.append({'start_x': enemy_x, 'start_y': enemy_y, 'target_x': player_x, 'target_y': player_y})
        
    
    def build_tree(self, maze_adj):
        visited = set()  
        self.root = self.dfs_tree(maze_adj, 0, visited)   
        self.assign_items_to_leaves(self.root) 

    def dfs_tree(self, maze_adj, node, visited):
        if node in visited:
            return None   
        visited.add(node)  
        tree_node = TreeNode(node)  
        for neighbor in maze_adj[node]:
            if neighbor not in visited:
                child_node = self.dfs_tree(maze_adj, neighbor, visited)   
                if child_node:
                    tree_node.children.append(child_node)  
        return tree_node

   
    def collect_leaves(self, node, leaves):
        if not node.children:  
            leaves.append(node)
        else:
            for child in node.children:
                self.collect_leaves(child, leaves)

    

    def move_enemies(self, delta_time, speed=3.0):
        self.enemy_move_timer += delta_time
        for enemy in self.enemy_positions.values():
            if enemy['moving']:
                dist_x = enemy['target_x'] - enemy['anim_x']
                dist_y = enemy['target_y'] - enemy['anim_y']
                distance = math.sqrt(dist_x**2 + dist_y**2)
                if distance < 0.05:
                    if enemy['halfway']:
                        enemy['anim_x'], enemy['anim_y'] = enemy['target_x'], enemy['target_y']
                        enemy['moving'] = False
                        enemy['halfway'] = False  
                    else:
                        enemy['anim_x'] += dist_x / 2
                        enemy['anim_y'] += dist_y / 2
                        enemy['halfway'] = True
                else:
                    enemy['anim_x'] += (dist_x / distance) * speed * delta_time
                    enemy['anim_y'] += (dist_y / distance) * speed * delta_time

        if self.enemy_move_timer < self.enemy_move_delay:
            return

        self.enemy_move_timer = 0   
        temp_updates = {}

        for enemy, data in self.enemy_positions.items():
            if data['moving']:
                continue

            position = data['position']
            direction = data['direction']
            axis = data['axis']

            next_position = self.get_next_position(position, direction, axis)

            if not self.is_valid_move(position, next_position) or next_position in self.items and self.items[next_position] in ['treasure', 'door', 'win', 'false_win']:
                alternative_directions = self.get_alternative_directions(direction, axis)
                move_found = False

                for new_direction, new_axis in alternative_directions:
                    alt_next_position = self.get_next_position(position, new_direction, new_axis)
                    if self.is_valid_move(position, alt_next_position) and alt_next_position not in temp_updates.values() and (alt_next_position not in self.items or self.items[alt_next_position] not in ['treasure', 'door', 'win', 'false_win']):
                        data['direction'] = new_direction
                        data['axis'] = new_axis
                        next_position = alt_next_position
                        move_found = True
                        break

                if not move_found:
                    data['direction'] = random.choice(['forward', 'backward'])
                    continue

            temp_updates[enemy] = next_position
            data['position'] = next_position
            data['target_x'] = float(next_position % self.width)
            data['target_y'] = float(next_position // self.width)
            data['moving'] = True

            if next_position % self.width < position % self.width:
                data['moving_left'] = True
                data['moving_right'] = False
            elif next_position % self.width > position % self.width:
                data['moving_left'] = False
                data['moving_right'] = True

        self.items = {k: v for k, v in self.items.items() if v != 'enemy'}
        for enemy, new_position in temp_updates.items():
            self.items[new_position] = 'enemy'

    def get_next_position(self, position, direction, axis):
        if axis == 'horizontal':
            return position + 1 if direction == 'forward' else position - 1
        elif axis == 'vertical':
            return position + self.width if direction == 'forward' else position - self.width
        return position

    
    def is_valid_move(self, position, next_position):
        
        if next_position in self.maze_adj[position] and 0 <= next_position < len(self.maze_adj):
            
            if next_position not in self.items or self.items[next_position] not in ['treasure', 'door', 'win', 'false_win']:
                return True
        return False

    
    def get_alternative_directions(self, current_direction, current_axis):
        opposite_direction = 'backward' if current_direction == 'forward' else 'forward'
        other_axis = 'vertical' if current_axis == 'horizontal' else 'horizontal'
        return [(opposite_direction, current_axis), ('forward', other_axis), ('backward', other_axis)]

class Level:
    def __init__(self, level_number, difficulty, time_limit, player_start, goal_position, width, height):
        self.level_number = level_number
        self.difficulty = difficulty
        self.time_limit = time_limit
        self.player_start_position = player_start
        self.goal_position = goal_position
        self.status = "locked"          
        self.maze = Maze(width, height)   
         
    def restart(self,game):
        """
        Reset the player position and other level-specific states.
        """
        print(f"Restarting Level {self.level_number}.")
 
        self.maze.reset_player(self.player_start_position)
  
        global bullets, player_bullets
        bullets = []
        player_bullets = []
 
        self.maze.hurdles.collected_treasures = 0
        self.maze.hurdles.total_treasures = 0
  
        self.maze.hurdles.defeated_enemies = 0
        game.player_lives = 3
        game.key_collected = False
        
        self.maze.hurdles.items.clear()
        self.maze.hurdles.enemy_positions.clear()   
        self.maze.hurdles.build_tree(self.maze.hurdles.maze_adj)
       
        game.falsewin = False
 
        self.maze.hurdles.enemy_move_timer = 0
        self.maze.hurdles.enemy_shot_timer.clear()

        
        self.status = "unlocked"   
        self.maze.visited = [False] * self.maze.V   

        print("Level has been reset successfully.")
        print(f"Total enemies-------------->: {(self.maze.hurdles.total_enemies)}")

    def update_status(self, status):
        if status in ["locked", "unlocked", "completed"]:
            self.status = status
            print(f"Level {self.level_number} status updated to {self.status}.")
        else:
            raise ValueError("Invalid status value. Use 'locked', 'unlocked', or 'completed'.")


class Game:
    def __init__(self):
        self.player = Player(0, 0)  
        self.is_running = True
        self.key_collected = False
        self.collected_treasures = []   
        self.player_dead = False   
        self.death_time = None   
        self.levels = HashTable(size=10)
        self.generate_levels()  
        self.current_level_number = 1
        self.current_level = self.get_level(self.current_level_number)
        self.player_lives=3
        self.falsewin=False
    def generate_levels(self):
        """Generate and insert levels into the hash table."""
        for i in range(1, 6):   
            
            width = 10 + i  
            height = 10 +i 
            
            player_start = (0, 0)
            goal_position = (width - 1, height - 1)
            level = Level(level_number=i, difficulty="Medium", time_limit=300, 
                        player_start=player_start, goal_position=goal_position, 
                        width=width, height=height)
            
            if i == 1: level.update_status("unlocked")
            else: level.update_status("locked")
            self.levels.insert( level)

    def get_level(self, level_number):
        """Retrieve level by number."""
        return self.levels.get(level_number)
    
    def collect_treasure(self,x, y):
        collected_time = time.time()
        self.collected_treasures.append((x, y, collected_time))
    
      
     
    def next_level(self):
        """Move to the next level."""
        self.current_level.status = "completed"
        next_level_num = self.current_level_number + 1
         
        next_level = self.get_level(next_level_num)
        if next_level:
            self.current_level_number = next_level_num
            self.current_level = next_level
            self.current_level.update_status("unlocked")
            self.save_game_state()   
        else:
            print("All levels completed!")
            self.is_running = False
            pygame.quit()  
            sys.exit()   
    
    def save_game_state(self):
        
        with open('bkgs.txt', 'w') as f:
            for _, level in self.levels:
                f.write(f'{level.level_number},{level.status}\n')

    
    def check_level_completion(self):
        if self.player_reached_goal():
            self.current_level.status = "completed"
            next_level = self.get_level(self.current_level_number + 1)
            if next_level:
                next_level.update_status("unlocked")
            self.save_game_state()   
            return True
        return False

                
    def check_for_item(self):
         
        Win = False
        current_index = self.player.y * self.current_level.maze.width + self.player.x 
        if current_index in self.current_level.maze.hurdles.items:
            item = self.current_level.maze.hurdles.items[current_index]
            print(f"Found item: {item}")
            if item == 'key': 
                self.key_collected = True 
                del self.current_level.maze.hurdles.items[current_index] 

            if item == 'treasure':
                if self.key_collected: 
                    self.treasure_found(current_index)
                    self.collected_treasures.append((self.player.x, self.player.y,time.time()))  
                    if self.check_win_condition():
                        self.change_doors_to_open()  
                else:
                    print("You need to collect the key before opening treasures!")
            elif item == 'enemy':
                self.enemy_encounter(current_index)
            elif item == 'volcano':
                self.volcano_encounter()
            elif item == 'win':
                if self.current_level.maze.hurdles.collected_treasures == self.current_level.maze.hurdles.total_treasures:
                    Win =True
                    if current_index in self.current_level.maze.hurdles.items:
                        del self.current_level.maze.hurdles.items[current_index]
                        self.win_game()
                else:
                        print("You need to collect all treasures before winning!")
                    
            elif item == 'false_win':
                if self.current_level.maze.hurdles.collected_treasures == self.current_level.maze.hurdles.total_treasures:
                    self.false_win()
                    if current_index in self.current_level.maze.hurdles.items:
                        del self.current_level.maze.hurdles.items[current_index]
        return Win
    def check_win_condition(self):
        return self.current_level.maze.hurdles.collected_treasures == self.current_level.maze.hurdles.total_treasures 
    
    def handle_player_death(self):
        self.player_lives -= 1
        if self.player_lives > 0:
            print(f"Lives remaining: {self.player_lives}")
            self.current_level.maze.reset_player(self.current_level.player_start_position)   
            self.player_dead = False   
            self.death_time = None   
        else:
            self.death_time = time.time()   
             
            self.player_dead = True
            print("Game Over! No more lives remaining.")
    def change_doors_to_open(self):
        return self.current_level.maze.hurdles.collected_treasures >= self.current_level.maze.hurdles.total_treasures
    def volcano_encounter(self):
        print("You fell into a volcano!")
        self.player_dead = True 
     

    def treasure_found(self, index):
        print("You found a treasure!")
        self.current_level.maze.hurdles.collected_treasures += 1
        if index in self.current_level.maze.hurdles.items:
            del self.current_level.maze.hurdles.items[index]

    def enemy_encounter(self, index):
        print("You encountered an enemy!")
        
        if index in self.current_level.maze.hurdles.enemy_positions:
            if self.current_level.maze.hurdles.enemy_positions[index]['has_key']:
                self.current_level.maze.hurdles.items[index] = 'key'
                print("An enemy dropped a key!")
   

 
    def load_game_state(self):
        try:
            with open('bkgs.txt', 'r') as f:
                for line in f:
                     
                    if ',' not in line:
                        continue
                    try:
                        level_number, status = line.strip().split(',')
                        level_number = int(level_number)
                        level = self.get_level(level_number)
                        if level:
                            level.status = status
                    except ValueError:
                        print(f"Skipping malformed line: {line.strip()}")
        except FileNotFoundError:
            print("Game state file not found.")
        

    def false_win(self):
        print("Oh no, it's a trap! You took the wrong gate and lost the game.")
        self.falsewin=True  

     
    def move_player(self, target_x, target_y):
        if self.is_valid_move(target_x, target_y):
            self.player.move_to(target_x, target_y)
            self.check_for_item()

    def is_valid_move(self, target_x, target_y):
        current_index = self.player.y * self.current_level.maze.width + self.player.x
        target_index = target_y * self.current_level.maze.width + target_x
 
        if target_index not in self.current_level.maze.adj[current_index]:
            return False
 
        valid_items = ['key', 'treasure', 'volcano', 'win', 'false_win']
        if target_index in self.current_level.maze.hurdles.items:
            item = self.current_level.maze.hurdles.items[target_index]
            if item in valid_items:
                return True

        

        return True
   
    def check_level_completion(self):
        if self.player_reached_goal():
            self.current_level.status = "completed"
            next_level = self.get_level(self.current_level_number + 1)
            if next_level:
                next_level.update_status("unlocked")
                
            return True
        return False

   
    def win_game(self):
        print("Congratulations! You've reached the goal!")
        self.next_level()   

class LinkedListNode:
    def __init__(self, level):
        self.level = level
        self.next = None

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size   
    def hash(self, key):
        """Hash function to map level number to a table index."""
        return key % self.size

    def insert(self, level):
        """Insert level into the hashtable."""
        index = self.hash(level.level_number)
        new_node = LinkedListNode(level)
 
        if not self.table[index]:
            self.table[index] = new_node
        else:
        
            current = self.table[index]
            while current.next:
                current = current.next
            current.next = new_node

    def get(self, key):
        """Get the level based on level number."""
        index = self.hash(key)
        current = self.table[index]
        
        while current:
            if current.level.level_number == key:
                return current.level
            current = current.next
        return None   

    def __iter__(self):
        """Iterate over all levels in the hashtable."""
        for bucket in self.table:
            current = bucket
            while current:
                yield current.level.level_number, current.level
                current = current.next
