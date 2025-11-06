import numpy as np

class Game:
    def __init__(self, board_size=15):
        self.board_size = board_size
        self.reset()
    
    def reset(self):
        """重置游戏状态"""
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.history = []  # 存储移动历史 [(x, y), ...]
    
    def is_valid_move(self, x, y):
        """检查移动是否有效"""
        if x < 0 or x >= self.board_size or y < 0 or y >= self.board_size:
            return False
        return self.board[y][x] == 0
    
    def make_move(self, x, y, player):
        """在指定位置落子"""
        if self.is_valid_move(x, y):
            self.board[y][x] = player
            self.history.append((x, y))
            return True
        return False
    
    def undo_move(self):
        """撤销最后一步移动"""
        if self.history:
            x, y = self.history.pop()
            self.board[y][x] = 0
            return True
        return False
    
    def check_win(self, x, y, player):
        """检查指定玩家是否在指定位置获胜"""
        directions = [
            [(1, 0), (-1, 0)],  # 水平
            [(0, 1), (0, -1)],  # 垂直
            [(1, 1), (-1, -1)],  # 对角线
            [(1, -1), (-1, 1)]   # 反对角线
        ]
        
        for dir_pair in directions:
            count = 1  # 当前位置已经有一个棋子
            
            # 检查两个相反的方向
            for dx, dy in dir_pair:
                temp_x, temp_y = x, y
                
                # 沿着当前方向计数连续的棋子
                for _ in range(4):  # 最多需要检查4步
                    temp_x += dx
                    temp_y += dy
                    
                    if (0 <= temp_x < self.board_size and 
                        0 <= temp_y < self.board_size and 
                        self.board[temp_y][temp_x] == player):
                        count += 1
                    else:
                        break
            
            # 如果找到5个连续的棋子，玩家获胜
            if count >= 5:
                return True
        
        return False
    
    def is_board_full(self):
        """检查棋盘是否已满"""
        return np.all(self.board != 0)
    
    def get_valid_moves(self):
        """获取所有有效的移动"""
        valid_moves = []
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.is_valid_move(x, y):
                    valid_moves.append((x, y))
        return valid_moves
    
    def get_board_state(self):
        """获取当前棋盘状态的副本"""
        return self.board.copy()
    
    def evaluate_position(self, player):
        """评估当前棋盘对指定玩家的有利程度"""
        opponent = 3 - player  # 1->2, 2->1
        
        # 初始化分数
        score = 0
        
        # 检查所有可能的五连线
        for y in range(self.board_size):
            for x in range(self.board_size):
                # 水平方向
                if x <= self.board_size - 5:
                    line = self.board[y, x:x+5]
                    score += self._evaluate_line(line, player, opponent)
                
                # 垂直方向
                if y <= self.board_size - 5:
                    line = self.board[y:y+5, x]
                    score += self._evaluate_line(line, player, opponent)
                
                # 对角线方向
                if x <= self.board_size - 5 and y <= self.board_size - 5:
                    line = [self.board[y+i, x+i] for i in range(5)]
                    score += self._evaluate_line(line, player, opponent)
                
                # 反对角线方向
                if x <= self.board_size - 5 and y >= 4:
                    line = [self.board[y-i, x+i] for i in range(5)]
                    score += self._evaluate_line(line, player, opponent)
        
        return score
    
    def _evaluate_line(self, line, player, opponent):
        """评估一条线的分数"""
        # 计算玩家和对手的棋子数
        player_count = np.sum(line == player)
        opponent_count = np.sum(line == opponent)
        empty_count = np.sum(line == 0)
        
        # 如果同时有玩家和对手的棋子，这条线不可能形成五连
        if player_count > 0 and opponent_count > 0:
            return 0
        
        # 根据棋子数量评分
        if player_count == 5:
            return 100000  # 五连
        elif player_count == 4 and empty_count == 1:
            return 10000   # 活四
        elif player_count == 3 and empty_count == 2:
            return 1000    # 活三
        elif player_count == 2 and empty_count == 3:
            return 100     # 活二
        elif player_count == 1 and empty_count == 4:
            return 10      # 活一
        
        # 对手的威胁
        if opponent_count == 4 and empty_count == 1:
            return -8000   # 对手活四
        elif opponent_count == 3 and empty_count == 2:
            return -800    # 对手活三
        
        return 0