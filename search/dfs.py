# search/dfs.py - Depth-First Search implementation for Pink Ghost

from ghost import Ghost
from config import PINK

class PinkGhost(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, PINK, "Pink")
    
    def find_path(self):
        # DFS algorithm implementation
        self.metrics.start_tracking()
        
        if not self.target:
            self.metrics.end_tracking()
            return []
        
        target_pos = self.target.get_position()
        start_pos = (self.x, self.y)
        
        # If already at target
        if start_pos == target_pos:
            self.path = []
            self.metrics.end_tracking()
            return []
        
        # DFS
        stack = [(start_pos, [])]  # (position, path)
        visited = {start_pos}
        
        while stack:
            (curr_x, curr_y), path = stack.pop()
            self.metrics.increment_expanded_nodes()
            
            # Check neighbors
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # Up, Right, Down, Left
                next_x, next_y = curr_x + dx, curr_y + dy
                
                if (next_x, next_y) == target_pos:
                    # Found target
                    self.path = path + [(next_x, next_y)]
                    self.metrics.end_tracking()
                    return self.path
                
                if self.is_valid_move(next_x, next_y) and (next_x, next_y) not in visited:
                    visited.add((next_x, next_y))
                    new_path = path + [(next_x, next_y)]
                    stack.append(((next_x, next_y), new_path))
        
        # No path found
        self.path = []
        self.metrics.end_tracking()
        return []