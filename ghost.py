# ghost.py - Base Ghost class

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
            if not self.path:
                self.find_path()
            if self.path:
                self.follow_path()
    
    def find_path(self):
        # To be implemented by subclasses
        pass