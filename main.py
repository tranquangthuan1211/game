import pygame
import sys
import random
import time

from config import (
    BLACK, WHITE, WALL_COLOR, PATH_COLOR, 
    SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE,
    MAZE_WIDTH, MAZE_HEIGHT, MAZE_LAYOUT,
    GAME_SPEED
)

from pacman import PacMan
from search import BlueGhost, PinkGhost, OrangeGhost, RedGhost

class MenuButton:
    def __init__(self, x, y, width, height, text, color=(100, 100, 100), hover_color=(150, 150, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.SysFont('Arial', 20)
        
    def draw(self, screen):
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)  # Border
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class PacManGame:
    def __init__(self, level=6):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man Search Project")
        self.clock = pygame.time.Clock()
        self.level = level
        self.running = True
        self.in_menu = True
        self.selecting_position = False
        self.positioning_character = None  # Will hold the character being positioned
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)
        
        # Timer variables
        self.start_time = None
        
        # Custom positions
        self.custom_positions = {
            'pacman': None,
            'blue': None,
            'pink': None,
            'orange': None,
            'red': None
        }
        
        # Create menu buttons
        self.create_menu_buttons()
        
        # Initialize characters with default positions
        self.initialize_game(use_custom_positions=False)
    
    def create_menu_buttons(self):
        btn_width = 250
        btn_height = 40
        spacing = 60
        col_spacing = 80

        total_width = btn_width * 2 + col_spacing
        start_x = (SCREEN_WIDTH - total_width) // 2  # Cột trái
        start_x_right = start_x + btn_width + col_spacing  # Cột phải



 
        self.buttons = {
            'start_game': MenuButton(start_x, 100, btn_width, btn_height, "Start Game"),
            'position_pacman': MenuButton(start_x, 160, btn_width, btn_height, "Set Pacman Position"),
            'position_blue': MenuButton(start_x, 220, btn_width, btn_height, "Set Blue Ghost Position"),
            'position_pink': MenuButton(start_x, 280, btn_width, btn_height, "Set Pink Ghost Position"),
            'position_orange': MenuButton(start_x, 340, btn_width, btn_height, "Set Orange Ghost Position"),
            'position_red': MenuButton(start_x, 400, btn_width, btn_height, "Set Red Ghost Position"),
            'random_positions': MenuButton(start_x, 460, btn_width, btn_height, "Use Random Positions")
        }
        # Bên phải: các nút level nằm ngang tại y = 480
        # Cột phải: các nút Level 1 đến 6
        for i in range(6):
            level_y = 100 + i * spacing
            self.buttons[f'level_{i+1}'] = MenuButton(start_x_right, level_y, btn_width, btn_height, f"Level {i+1}")
    
    def initialize_game(self, use_custom_positions=True):
        # Reset timer when starting a new game
        self.start_time = time.time()
        
        # Place Pac-Man and ghosts at valid positions
        valid_positions = self.get_valid_positions()
        random.shuffle(valid_positions)
        
        # Initialize Pac-Man
        if use_custom_positions and self.custom_positions['pacman']:
            pacman_pos = self.custom_positions['pacman']
        else:
            pacman_pos = valid_positions.pop()
            self.custom_positions['pacman'] = pacman_pos
        
        self.pacman = PacMan(pacman_pos[0], pacman_pos[1])
        
        # Initialize ghosts based on level
        self.ghosts = []
        
        if self.level == 1:
            if use_custom_positions and self.custom_positions['blue']:
                blue_pos = self.custom_positions['blue']
            else:
                blue_pos = valid_positions.pop()
                self.custom_positions['blue'] = blue_pos
                
            self.blue_ghost = BlueGhost(blue_pos[0], blue_pos[1])
            self.blue_ghost.set_target(self.pacman)
            self.ghosts.append(self.blue_ghost)

        elif self.level == 2:
            if use_custom_positions and self.custom_positions['pink']:
                pink_pos = self.custom_positions['pink']
            else:
                pink_pos = valid_positions.pop()
                self.custom_positions['pink'] = pink_pos
                
            self.pink_ghost = PinkGhost(pink_pos[0], pink_pos[1])
            self.pink_ghost.set_target(self.pacman)
            self.ghosts.append(self.pink_ghost)

        elif self.level == 3:
            if use_custom_positions and self.custom_positions['orange']:
                orange_pos = self.custom_positions['orange']
            else:
                orange_pos = valid_positions.pop()
                self.custom_positions['orange'] = orange_pos
                
            self.orange_ghost = OrangeGhost(orange_pos[0], orange_pos[1])
            self.orange_ghost.set_target(self.pacman)
            self.ghosts.append(self.orange_ghost)

        elif self.level == 4:
            if use_custom_positions and self.custom_positions['red']:
                red_pos = self.custom_positions['red']
            else:
                red_pos = valid_positions.pop()
                self.custom_positions['red'] = red_pos
                
            self.red_ghost = RedGhost(red_pos[0], red_pos[1])
            self.red_ghost.set_target(self.pacman)
            self.ghosts.append(self.red_ghost)

        elif self.level >= 5:
            if use_custom_positions and self.custom_positions['blue']:
                blue_pos = self.custom_positions['blue']
            else:
                blue_pos = valid_positions.pop()
                self.custom_positions['blue'] = blue_pos
                
            self.blue_ghost = BlueGhost(blue_pos[0], blue_pos[1])
            self.blue_ghost.set_target(self.pacman)
            self.ghosts.append(self.blue_ghost)

            if use_custom_positions and self.custom_positions['pink']:
                pink_pos = self.custom_positions['pink']
            else:
                pink_pos = valid_positions.pop()
                self.custom_positions['pink'] = pink_pos
                
            self.pink_ghost = PinkGhost(pink_pos[0], pink_pos[1])
            self.pink_ghost.set_target(self.pacman)
            self.ghosts.append(self.pink_ghost)

            if use_custom_positions and self.custom_positions['orange']:
                orange_pos = self.custom_positions['orange']
            else:
                orange_pos = valid_positions.pop()
                self.custom_positions['orange'] = orange_pos
                
            self.orange_ghost = OrangeGhost(orange_pos[0], orange_pos[1])
            self.orange_ghost.set_target(self.pacman)
            self.ghosts.append(self.orange_ghost)

            if use_custom_positions and self.custom_positions['red']:
                red_pos = self.custom_positions['red']
            else:
                red_pos = valid_positions.pop()
                self.custom_positions['red'] = red_pos
                
            self.red_ghost = RedGhost(red_pos[0], red_pos[1])
            self.red_ghost.set_target(self.pacman)
            self.ghosts.append(self.red_ghost)
    
    def get_valid_positions(self):
        valid = []
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if MAZE_LAYOUT[y][x] == 0:
                    valid.append((x, y))
        return valid
    
    def draw_maze(self):
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if MAZE_LAYOUT[y][x] == 1:
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                else:
                    pygame.draw.rect(self.screen, PATH_COLOR, rect)
    
    def draw_metrics(self):
        y_offset = 10
        for ghost in self.ghosts:
            metrics = ghost.metrics.get_results()
            text = f"{ghost.name}: Time: {metrics['search_time']:.4f}s, Nodes: {metrics['expanded_nodes']}, Memory: {metrics['memory_used']:.2f}KB"
            print(text)  
            text_surface = self.font.render(text, True, WHITE)
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 30
    
    def draw_characters(self):
        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
    
    def draw_menu(self):
        # Thay font cho chữ để nhìn đẹp hơn và thêm hiệu ứng shadow
        title_font = pygame.font.SysFont('Arial', 50, bold=True)  # Đổi size và bật bold
        title_text = title_font.render("Game Pac-Man", True, (255, 215, 0))  # Màu vàng

        # Shadow effect (bóng mờ)
        shadow_text = title_font.render("Game Pac-Man", True, (50, 50, 50))  # Màu đen cho bóng mờ
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 3, 50 + 3))  # Di chuyển bóng mờ 3 pixel

        # Vẽ bóng mờ trước
        self.screen.blit(shadow_text, shadow_rect)

        # Vẽ chữ chính
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)

        # Vẽ các button level
        for level in range(1, 7):
            self.buttons[f'level_{level}'].draw(self.screen)

        
        if self.level == 1:
            self.buttons['start_game'].draw(self.screen)
            self.buttons['position_pacman'].draw(self.screen)
            self.buttons['position_blue'].draw(self.screen)
        elif self.level == 2:
            self.buttons['start_game'].draw(self.screen)
            self.buttons['position_pacman'].draw(self.screen)
            self.buttons['position_pink'].draw(self.screen)
        elif self.level == 3:
            self.buttons['start_game'].draw(self.screen)
            self.buttons['position_pacman'].draw(self.screen)
            self.buttons['position_orange'].draw(self.screen)
        elif self.level == 4:
            self.buttons['start_game'].draw(self.screen)
            self.buttons['position_pacman'].draw(self.screen)
            self.buttons['position_red'].draw(self.screen)
        elif self.level >= 5:
            self.buttons['start_game'].draw(self.screen)
            self.buttons['position_pacman'].draw(self.screen)
            self.buttons['position_blue'].draw(self.screen)
            self.buttons['position_pink'].draw(self.screen)
            self.buttons['position_orange'].draw(self.screen)
            self.buttons['position_red'].draw(self.screen)
        # Draw buttons
        # for button in self.buttons.values():
        #     if self.level < 2 and button == self.buttons['position_pink']:
        #         continue
        #     if self.level < 3 and button == self.buttons['position_orange']:
        #         continue
        #     if self.level < 4 and button == self.buttons['position_red']:
        #         continue
        #     button.draw(self.screen)
        
        # Draw position information
        position_text = self.small_font.render("Current Positions:", True, WHITE)
        self.screen.blit(position_text, (50, 520))
        
        y_offset = 550
        positions = [
            ("Pacman", self.custom_positions['pacman'], (255, 255, 0)),
            ("Blue Ghost", self.custom_positions['blue'], (0, 0, 255)),
        ]
        
        if self.level >= 2:
            positions.append(("Pink Ghost", self.custom_positions['pink'], (255, 182, 193)))
        if self.level >= 3:
            positions.append(("Orange Ghost", self.custom_positions['orange'], (255, 165, 0)))
        if self.level >= 4:
            positions.append(("Red Ghost", self.custom_positions['red'], (255, 0, 0)))
        
        for name, pos, color in positions:
            if pos:
                pos_text = self.small_font.render(f"{name}: ({pos[0]}, {pos[1]})", True, color)
                self.screen.blit(pos_text, (50, y_offset))
                y_offset += 25
    
    def draw_position_selector(self):
        # Draw maze for position selection
        self.draw_maze()
        
        # Draw existing characters for reference
        if self.positioning_character != 'pacman':
            self.pacman.draw(self.screen)
        
        for ghost in self.ghosts:
            if (self.positioning_character != 'blue' or ghost != self.blue_ghost) and \
               (self.positioning_character != 'pink' or ghost != self.pink_ghost) and \
               (self.positioning_character != 'orange' or ghost != self.orange_ghost) and \
               (self.positioning_character != 'red' or ghost != self.red_ghost):
                ghost.draw(self.screen)
        
        # Draw hover indicator for valid positions
        mouse_pos = pygame.mouse.get_pos()
        cell_x = mouse_pos[0] // CELL_SIZE
        cell_y = mouse_pos[1] // CELL_SIZE
        
        if 0 <= cell_x < MAZE_WIDTH and 0 <= cell_y < MAZE_HEIGHT and MAZE_LAYOUT[cell_y][cell_x] == 0:
            hover_rect = pygame.Rect(cell_x * CELL_SIZE, cell_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            # Use appropriate color based on character being positioned
            if self.positioning_character == 'pacman':
                hover_color = (255, 255, 0, 128)  # Yellow for Pacman
            elif self.positioning_character == 'blue':
                hover_color = (0, 0, 255, 128)    # Blue
            elif self.positioning_character == 'pink':
                hover_color = (255, 182, 193, 128)  # Pink
            elif self.positioning_character == 'orange':
                hover_color = (255, 165, 0, 128)  # Orange
            elif self.positioning_character == 'red':
                hover_color = (255, 0, 0, 128)    # Red
            
            pygame.draw.rect(self.screen, hover_color, hover_rect)
        
        # Display instructions
        instruction_text = self.font.render(f"Click to place {self.positioning_character.capitalize()}. ESC to cancel.", True, WHITE)
        self.screen.blit(instruction_text, (10, 10))
    
    def handle_menu_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.selecting_position:
                    self.selecting_position = False
                else:
                    self.running = False
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
        # Xử lý sự kiện khi nhấn vào các button level
        for level in range(1, 7):
            if self.buttons[f'level_{level}'].is_clicked(mouse_pos, mouse_click):
                self.level = level
                self.initialize_game(use_custom_positions=False)

        if self.selecting_position:
            self.handle_position_selection(mouse_pos, mouse_click)
        else:
            # Update button hover states
            for button in self.buttons.values():
                button.check_hover(mouse_pos)
            
            # Check button clicks
            if mouse_click:
                if self.buttons['start_game'].is_clicked(mouse_pos, mouse_click):
                    self.in_menu = False
                    # Start the timer when the game begins
                    self.start_time = time.time()
                elif self.buttons['position_pacman'].is_clicked(mouse_pos, mouse_click):
                    self.selecting_position = True
                    self.positioning_character = 'pacman'
                elif self.buttons['position_blue'].is_clicked(mouse_pos, mouse_click):
                    self.selecting_position = True
                    self.positioning_character = 'blue'
                elif self.level >= 2 and self.buttons['position_pink'].is_clicked(mouse_pos, mouse_click):
                    self.selecting_position = True
                    self.positioning_character = 'pink'
                elif self.level >= 3 and self.buttons['position_orange'].is_clicked(mouse_pos, mouse_click):
                    self.selecting_position = True
                    self.positioning_character = 'orange'
                elif self.level >= 4 and self.buttons['position_red'].is_clicked(mouse_pos, mouse_click):
                    self.selecting_position = True
                    self.positioning_character = 'red'
                elif self.buttons['random_positions'].is_clicked(mouse_pos, mouse_click):
                    # Reset custom positions to None to generate new random ones
                    for key in self.custom_positions:
                        self.custom_positions[key] = None
                    self.initialize_game(use_custom_positions=False)
    
    def handle_position_selection(self, mouse_pos, mouse_click):
        if mouse_click:
            cell_x = mouse_pos[0] // CELL_SIZE
            cell_y = mouse_pos[1] // CELL_SIZE
            
            # Check if clicked on a valid path cell
            if 0 <= cell_x < MAZE_WIDTH and 0 <= cell_y < MAZE_HEIGHT and MAZE_LAYOUT[cell_y][cell_x] == 0:
                # Update position
                self.custom_positions[self.positioning_character] = (cell_x, cell_y)
                
                # Reinitialize game with updated positions
                self.initialize_game(use_custom_positions=True)
                
                # Exit position selection mode
                self.selecting_position = False
    
    def handle_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Level 6: User-controlled Pac-Man
            if self.level >= 6:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.pacman.move("up")
                    elif event.key == pygame.K_DOWN:
                        self.pacman.move("down")
                    elif event.key == pygame.K_LEFT:
                        self.pacman.move("left")
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.move("right")
                    elif event.key == pygame.K_ESCAPE:
                        self.in_menu = True  # Return to menu
                        return
    
    def update_ghosts(self):
        ghost_positions = set()
        
        for ghost in self.ghosts:
            # If ghost has no path or reached the end, find a new path
            if not ghost.path:
                ghost.find_path()
            
            # If the ghost has a path to follow
            if ghost.path:
                next_pos = ghost.path[0]
                
                # Check if next position is already occupied by another ghost (Level 5+)
                if self.level >= 5 and next_pos in ghost_positions:
                    # Skip this move
                    continue
                
                ghost.follow_path()
                ghost_positions.add(ghost.get_position())
            
            # Check if ghost caught Pac-Man
            if ghost.get_position() == self.pacman.get_position():
                # Calculate and print the time it took to catch Pacman
                end_time = time.time()
                elapsed_time = end_time - self.start_time
                
                print(f"\n{ghost.name} Ghost caught Pac-Man!")
                print(f"Time taken to catch Pacman: {elapsed_time:.2f} seconds")
                print(f"Pacman started at: {self.custom_positions['pacman']}")
                
                # Print starting positions of all ghosts
                ghost_positions_str = []
                if self.level == 1:
                    ghost_positions_str.append(f"Blue Ghost: {self.custom_positions['blue']}")
                if self.level == 2:
                    ghost_positions_str.append(f"Pink Ghost: {self.custom_positions['pink']}")
                if self.level == 3:
                    ghost_positions_str.append(f"Orange Ghost: {self.custom_positions['orange']}")
                if self.level == 4:
                    ghost_positions_str.append(f"Red Ghost: {self.custom_positions['red']}")
                if self.level >= 5:
                    ghost_positions_str.append(f"Blue Ghost: {self.custom_positions['blue']}")
                    ghost_positions_str.append(f"Pink Ghost: {self.custom_positions['pink']}")
                    ghost_positions_str.append(f"Orange Ghost: {self.custom_positions['orange']}")
                    ghost_positions_str.append(f"Red Ghost: {self.custom_positions['red']}")
                print("Ghost starting positions:")
                for pos in ghost_positions_str:
                    print(f"  {pos}")
                
                # Print a separator for clarity
                print("-" * 50)
                
                self.in_menu = True  # Return to menu after being caught
                break
    
    def run(self):
        while self.running:
            self.screen.fill(BLACK)
            
            if self.in_menu:
                if self.selecting_position:
                    self.draw_position_selector()
                else:
                    self.draw_menu()
                self.handle_menu_events()
            else:
                self.handle_game_events()
                
                # Update game state
                self.pacman.collect_dot()
                
                self.update_ghosts()
                
                # Draw everything
                self.draw_maze()
                self.draw_characters()
                self.draw_metrics()
            
            pygame.display.flip()
            self.clock.tick(GAME_SPEED)  # Slower speed for better visualization
        
        pygame.quit()
        sys.exit()

# Test specific scenarios
def run_test_case(test_number, pacman_pos, ghost_positions, level=4):
    game = PacManGame(level=level)
    
    # Override random positions with test case positions
    game.pacman.set_position(pacman_pos[0], pacman_pos[1])
    
    if level >= 1 and 0 < len(ghost_positions):
        game.blue_ghost.set_position(ghost_positions[0][0], ghost_positions[0][1])
    
    if level >= 2 and 1 < len(ghost_positions):
        game.pink_ghost.set_position(ghost_positions[1][0], ghost_positions[1][1])
    
    if level >= 3 and 2 < len(ghost_positions):
        game.orange_ghost.set_position(ghost_positions[2][0], ghost_positions[2][1])
    
    if level >= 4 and 3 < len(ghost_positions):
        game.red_ghost.set_position(ghost_positions[3][0], ghost_positions[3][1])
    
    print(f"Running Test Case #{test_number}")
    print(f"Pac-Man position: {pacman_pos}")
    print(f"Ghost positions: {ghost_positions}")
    
    game.run()

# Main entry point
if __name__ == "__main__":
    # Change the level number (1-6) based on what you want to test
    level = 6  # Set to 4 to enable all ghosts with position selection
    
    # Regular game mode
    game = PacManGame(level=level)
    game.run()
    