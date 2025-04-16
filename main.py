# main.py - Main game file for Pac-Man Search Project

import pygame
import sys
import random

from config import (
    BLACK, WHITE, WALL_COLOR, PATH_COLOR, 
    SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE,
    MAZE_WIDTH, MAZE_HEIGHT, MAZE_LAYOUT,
    GAME_SPEED
)

from pacman import PacMan
from search import BlueGhost, PinkGhost, OrangeGhost, RedGhost

class PacManGame:
    def __init__(self, level=6):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man Search Project")
        self.clock = pygame.time.Clock()
        self.level = level
        self.running = True
        self.font = pygame.font.SysFont('Arial', 24)
        
        # Initialize characters
        self.initialize_game()
    
    def initialize_game(self):
        # Place Pac-Man and ghosts at valid positions
        valid_positions = self.get_valid_positions()
        random.shuffle(valid_positions)
        
        pacman_pos = valid_positions.pop()
        self.pacman = PacMan(pacman_pos[0], pacman_pos[1])
        
        # Initialize ghosts based on level
        self.ghosts = []
        
        if self.level >= 1:
            blue_pos = valid_positions.pop()
            self.blue_ghost = BlueGhost(blue_pos[0], blue_pos[1])
            self.blue_ghost.set_target(self.pacman)
            self.ghosts.append(self.blue_ghost)
        
        if self.level >= 2:
            pink_pos = valid_positions.pop()
            self.pink_ghost = PinkGhost(pink_pos[0], pink_pos[1])
            self.pink_ghost.set_target(self.pacman)
            self.ghosts.append(self.pink_ghost)
        
        if self.level >= 3:
            orange_pos = valid_positions.pop()
            self.orange_ghost = OrangeGhost(orange_pos[0], orange_pos[1])
            self.orange_ghost.set_target(self.pacman)
            self.ghosts.append(self.orange_ghost)
        
        if self.level >= 4:
            red_pos = valid_positions.pop()
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
            text_surface = self.font.render(text, True, WHITE)
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 30
    
    def draw_characters(self):
        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
    
    def handle_events(self):
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
                        self.running = False
    
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
                print(f"{ghost.name} Ghost caught Pac-Man!")
                self.initialize_game()  # Reset the game
                break
    
    def run(self):
        while self.running:
            self.handle_events()
            
            # Update game state
            self.pacman.collect_dot()
            
            # Update ghosts
            self.update_ghosts()
            
            # Draw everything
            self.screen.fill(BLACK)
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
    level = 6
    
    # Regular game mode
    game = PacManGame(level=level)
    game.run()
    
    # Uncomment to run specific test cases