# pacman.py - Pac-Man class implementation

import pygame
from character import Character
from config import YELLOW, DOTS_COLOR, CELL_SIZE, MAZE_WIDTH, MAZE_HEIGHT, MAZE_LAYOUT

class PacMan(Character):
    def __init__(self, x, y):
        super().__init__(x, y, YELLOW)
        self.score = 0
        self.dots = set()
        self.initialize_dots()
    
    def initialize_dots(self):
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if MAZE_LAYOUT[y][x] == 0:
                    self.dots.add((x, y))
    
    def draw(self, screen):
        # Draw all dots
        for dot in self.dots:
            center_x = dot[0] * CELL_SIZE + CELL_SIZE // 2
            center_y = dot[1] * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, DOTS_COLOR, (center_x, center_y), 3)
        
        # Draw Pac-Man
        super().draw(screen)
    
    def collect_dot(self):
        pos = (self.x, self.y)
        if pos in self.dots:
            self.dots.remove(pos)
            self.score += 10
            return True
        return False
    

