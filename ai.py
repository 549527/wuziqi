import numpy as np
import random
import time

class AI:
    def __init__(self, game, difficulty=3):
        self.game = game
        self.difficulty = difficulty  # 1-3，3为最高难度
        self.max_depth = {1: 2, 2: 4, 3: 6}[difficulty]  # 根据难度设置搜索深度
        self.time_limit = {1: 0.5, 2: 1.5, 3: 3}[difficulty]  # 思考时间限制(秒)
    
    def make_move(self):
        """AI决策并返回最佳移动"""
        start_time = time.time()
        
        # 获取有效移动
        valid_moves = self._get_heuristic_moves()
        
        if not valid_moves:
            # 如果没有启发式移动，则获取所有有效移动
            valid_moves = self.game.get_valid_moves()
        
        # 如果是第一步，选择靠近中心的位置
        if len(self.game.history) == 0:
            center = self.game.board_size // 2
            return (center, center)
        
        # 如果是第二步，选择靠近玩家棋子的位置
        if len(self.game.history) == 1:
            px, py = self.game.history[0]
            # 在玩家棋子周围2格范围内随机选择一个位置
            candidates = []
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    nx, ny = px + dx, py + dy
                    if (0 <= nx < self.game.board_size and 
                        0 <= ny < self.game.board_size and 
                        self.game.is_valid_move(nx, ny)):
                        candidates.append((nx, ny))
            
            if candidates:
                return random.choice(candidates)
        
        # 初始化最佳移动和分数
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        # 对每个可能的移动进行评估
        for move in valid_moves:
            x, y = move
            
            # 模拟移动
            self.game.make_move(x, y, 2)  # AI使用白子(2)
            
            # 使用极小极大算法评估移动
            score = self._minimax(self.max_depth, False, alpha, beta, start_time)
            
            # 撤销移动
            self.game.undo_move()
            
            # 更新最佳移动
            if score > best_score:
                best_score = score
                best_move = move
            
            # Alpha-Beta剪枝
            alpha = max(alpha, best_score)
            
            # 如果超过时间限制，提前结束
            if time.time() - start_time > self.time_limit:
                break
        
        # 如果没有找到最佳移动，随机选择一个有效移动
        if best_move is None and valid_moves:
            best_move = random.choice(valid_moves)
        
        return best_move
    
    def _minimax(self, depth, is_maximizing, alpha, beta, start_time):
        """极小极大算法与Alpha-Beta剪枝"""
        # 检查是否达到搜索深度或游戏结束
        if depth == 0 or self.game.is_board_full():
            return self._evaluate_board()
        
        # 检查是否有玩家获胜
        last_move = self.game.history[-1] if self.game.history else None
        if last_move:
            x, y = last_move
            player = self.game.board[y][x]
            if self.game.check_win(x, y, player):
                return float('inf') if player == 2 else float('-inf')
        
        # 检查是否超时
        if time.time() - start_time > self.time_limit:
            return self._evaluate_board()
        
        # 获取有效移动
        valid_moves = self._get_heuristic_moves()
        
        if not valid_moves:
            valid_moves = self.game.get_valid_moves()
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                x, y = move
                self.game.make_move(x, y, 2)  # AI使用白子(2)
                eval = self._minimax(depth - 1, False, alpha, beta, start_time)
                self.game.undo_move()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta剪枝
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                x, y = move
                self.game.make_move(x, y, 1)  # 玩家使用黑子(1)
                eval = self._minimax(depth - 1, True, alpha, beta, start_time)
                self.game.undo_move()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha剪枝
            return min_eval
    
    def _evaluate_board(self):
        """评估当前棋盘状态"""
        # 使用游戏类的评估函数
        ai_score = self.game.evaluate_position(2)  # AI评分
        player_score = self.game.evaluate_position(1)  # 玩家评分
        
        # 在高难度下，更重视防守
        if self.difficulty == 3:
            return ai_score - 1.2 * player_score
        else:
            return ai_score - player_score
    
    def _get_heuristic_moves(self):
        """获取启发式移动（靠近现有棋子的空位）"""
        board = self.game.board
        moves = []
        
        # 只考虑现有棋子周围2格范围内的空位
        for y in range(self.game.board_size):
            for x in range(self.game.board_size):
                if board[y][x] != 0:  # 如果有棋子
                    # 检查周围的空位
                    for dy in range(-2, 3):
                        for dx in range(-2, 3):
                            nx, ny = x + dx, y + dy
                            if (0 <= nx < self.game.board_size and 
                                0 <= ny < self.game.board_size and 
                                board[ny][nx] == 0 and
                                (nx, ny) not in moves):
                                moves.append((nx, ny))
        
        # 对移动进行评分和排序
        scored_moves = []
        for move in moves:
            x, y = move
            # 模拟AI移动
            self.game.make_move(x, y, 2)
            ai_score = self.game.evaluate_position(2)
            self.game.undo_move()
            
            # 模拟玩家移动
            self.game.make_move(x, y, 1)
            player_score = self.game.evaluate_position(1)
            self.game.undo_move()
            
            # 综合评分（防守与进攻的平衡）
            score = ai_score + player_score * 0.8
            scored_moves.append((move, score))
        
        # 按评分降序排序
        scored_moves.sort(key=lambda x: x[1], reverse=True)
        
        # 根据难度级别选择不同数量的移动
        num_moves = {1: 5, 2: 8, 3: 12}[self.difficulty]
        return [move for move, _ in scored_moves[:num_moves]]