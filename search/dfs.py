from ghost import Ghost
from config import PINK

class PinkGhost(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, PINK, "Pink")
    
    def find_path(self):
    # Bắt đầu theo dõi hiệu suất
        self.metrics.start_tracking()
        
        if not self.target:
            self.metrics.end_tracking()
            return []
        
        target_pos = self.target.get_position()
        start_pos = (self.x, self.y)
        
        # Nếu đã ở đích, trả về đường đi trống
        if start_pos == target_pos:
            self.path = [start_pos]
            self.metrics.end_tracking()
            return self.path
        
        # Cấu hình DFS với path tracking để tránh vòng lặp
        stack = [(start_pos, [])]  # Stack lưu (vị trí, đường đi)
        visited = set()  # Sử dụng set để theo dõi các vị trí đã thăm
        visited.add(start_pos)
        
        while stack:
            (curr_x, curr_y), path = stack.pop()
            self.metrics.increment_expanded_nodes()
            
            # Kiểm tra các vị trí lân cận (Lên, Phải, Xuống, Trái)
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                next_x, next_y = curr_x + dx, curr_y + dy
                
                # Nếu đến đích, trả về đường đi
                if (next_x, next_y) == target_pos:
                    self.path = path + [(next_x, next_y)]
                    self.metrics.end_tracking()
                    return self.path
                
                # Kiểm tra xem có thể đi vào vị trí mới và nó chưa được thăm
                if self.is_valid_move(next_x, next_y) and (next_x, next_y) not in visited:
                    # Đánh dấu là đã thăm vị trí này
                    visited.add((next_x, next_y))  # Đánh dấu ngay khi thêm vào stack
                    new_path = path + [(next_x, next_y)]
                    stack.append(((next_x, next_y), new_path))
        
        # Nếu không tìm thấy đường đi, trả về danh sách trống
        self.path = []
        self.metrics.end_tracking()
        return []