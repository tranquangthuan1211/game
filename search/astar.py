# search/astar.py - A* Search implementation for Red Ghost

import heapq
from ghost import Ghost
from config import RED

class RedGhost(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, RED, "Red")
    
    def heuristic(self, pos, target):
        # Manhattan distance
        return abs(pos[0] - target[0]) + abs(pos[1] - target[1])
    
    def find_path(self):
        # A* algorithm implementation
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
        
        # A*
        open_set = []
        heapq.heappush(open_set, (0, start_pos, []))  # (f_score, position, path)
        
        g_score = {start_pos: 0}  # Cost from start to current node
        f_score = {start_pos: self.heuristic(start_pos, target_pos)}  # Estimated total cost
        
        closed_set = set()
        
        while open_set:
            _, (curr_x, curr_y), path = heapq.heappop(open_set)
            current = (curr_x, curr_y)
            self.metrics.increment_expanded_nodes()
            
            if current == target_pos:
                # Found target
                self.path = path
                self.metrics.end_tracking()
                return self.path
            
            closed_set.add(current)
            
            # Check neighbors
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # Up, Right, Down, Left
                next_x, next_y = curr_x + dx, curr_y + dy
                neighbor = (next_x, next_y)
                
                if not self.is_valid_move(next_x, next_y) or neighbor in closed_set:
                    continue
                
                tentative_g_score = g_score[current] + 1  # Move cost is 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, target_pos)
                    new_path = path + [neighbor]
                    heapq.heappush(open_set, (f_score[neighbor], neighbor, new_path))
        
        # No path found
        self.path = []
        self.metrics.end_tracking()
        return []