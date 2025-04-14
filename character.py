# character.py - Base character class

import pygame
from config import CELL_SIZE, MAZE_WIDTH, MAZE_HEIGHT, MAZE_LAYOUT

class Character:
    def __init__(self, x, y, color, size=CELL_SIZE-10):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.direction = None
        self.path = []
        
    def draw(self, screen):
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, self.color, (center_x, center_y), self.size // 2)
    
    def move(self, direction):
        if direction == "up" and self.is_valid_move(self.x, self.y - 1):
            self.y -= 1
        elif direction == "down" and self.is_valid_move(self.x, self.y + 1):
            self.y += 1
        elif direction == "left" and self.is_valid_move(self.x - 1, self.y):
            self.x -= 1
        elif direction == "right" and self.is_valid_move(self.x + 1, self.y):
            self.x += 1
    
    def is_valid_move(self, x, y):
        # Check if the move is within boundaries and not a wall
        if 0 <= x < MAZE_WIDTH and 0 <= y < MAZE_HEIGHT:
            return MAZE_LAYOUT[y][x] == 0
        return False
    
    def get_position(self):
        return (self.x, self.y)
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
    
    def follow_path(self):
        if self.path:
            next_pos = self.path.pop(0)
            self.set_position(next_pos[0], next_pos[1])