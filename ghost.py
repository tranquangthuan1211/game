# ghost.py - Base Ghost class
import random
from character import Character
from search.metrics import SearchMetrics

class Ghost(Character):
    def __init__(self, x, y, color, name):
        super().__init__(x, y, color)
        self.name = name
        self.target = None
        self.path = []
        self.metrics = SearchMetrics()
    
    def set_target(self, target):
        self.target = target
    
    def update(self):
        if self.target:
            if not self.path:  # Nếu chưa có đường đi
                self.find_path()  # Tìm đường đi mới
            if self.path:  # Nếu có đường đi, di chuyển theo đường đó
                self.follow_path()
            else:
                 pass

        
    def find_path(self):
        # To be implemented by subclasses
        pass