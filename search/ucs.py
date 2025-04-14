# search/ucs.py - Uniform-Cost Search implementation for Orange Ghost

import heapq
from ghost import Ghost
from config import ORANGE

class OrangeGhost(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, ORANGE, "Orange")
    
    def find_path(self):
        # UCS algorithm implementation
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
        
        # UCS
        priority_queue = [(0, start_pos, [])]  # (cost, position, path)
        visited = {start_pos: 0}
        
        while priority_queue:
            cost, (curr_x, curr_y), path = heapq.heappop(priority_queue)
            self.metrics.increment_expanded_nodes()
            
            if (curr_x, curr_y) == target_pos:
                # Found target
                self.path = path
                self.metrics.end_tracking()
                return self.path
            
            # Check neighbors
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # Up, Right, Down, Left
                next_x, next_y = curr_x + dx, curr_y + dy
                
                # Calculate cost for this move (all moves cost 1 in this simple example)
                new_cost = cost + 1
                
                if self.is_valid_move(next_x, next_y) and ((next_x, next_y) not in visited or new_cost < visited[(next_x, next_y)]):
                    visited[(next_x, next_y)] = new_cost
                    new_path = path + [(next_x, next_y)]
                    heapq.heappush(priority_queue, (new_cost, (next_x, next_y), new_path))
        
        # No path found
        self.path = []
        self.metrics.end_tracking()
        return []