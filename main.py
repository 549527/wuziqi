from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
import numpy as np
import time

from game import Game
from ai import AI

# 设置窗口大小
Window.size = (800, 600)

class GomokuBoard(Widget):
    def __init__(self, **kwargs):
        super(GomokuBoard, self).__init__(**kwargs)
        self.board_size = 15
        self.grid_size = dp(30)
        self.board_margin = dp(50)
        self.game = Game(self.board_size)
        self.ai = AI(self.game, difficulty=3)  # 难度级别3（最高）
        self.player_turn = True  # True表示玩家回合，False表示AI回合
        self.game_over = False
        self.winner = None
        self.last_move = None
        
        # 绘制棋盘
        self.draw_board()
        
        # 设置定时器检查AI回合
        Clock.schedule_interval(self.check_ai_turn, 0.1)
    
    def draw_board(self):
        self.canvas.clear()
        with self.canvas:
            # 绘制棋盘背景
            Color(0.86, 0.71, 0.27)  # 棋盘颜色
            Rectangle(pos=(self.board_margin, self.board_margin), 
                     size=(self.grid_size * (self.board_size - 1), 
                           self.grid_size * (self.board_size - 1)))
            
            # 绘制网格线
            Color(0, 0, 0)  # 黑色线
            for i in range(self.board_size):
                # 横线
                Line(points=[self.board_margin, self.board_margin + i * self.grid_size, 
                            self.board_margin + (self.board_size - 1) * self.grid_size, 
                            self.board_margin + i * self.grid_size],
                    width=1.5 if i == 0 or i == self.board_size - 1 else 1)
                # 竖线
                Line(points=[self.board_margin + i * self.grid_size, self.board_margin,
                            self.board_margin + i * self.grid_size, 
                            self.board_margin + (self.board_size - 1) * self.grid_size],
                    width=1.5 if i == 0 or i == self.board_size - 1 else 1)
            
            # 绘制天元和星位
            star_points = [3, 7, 11] if self.board_size == 15 else [3, 5, 7]
            for x in star_points:
                for y in star_points:
                    Color(0, 0, 0)  # 黑色
                    Ellipse(pos=(self.board_margin + x * self.grid_size - dp(3),
                                self.board_margin + y * self.grid_size - dp(3)),
                            size=(dp(6), dp(6)))
            
            # 绘制棋子
            for y in range(self.board_size):
                for x in range(self.board_size):
                    piece = self.game.board[y][x]
                    if piece != 0:
                        if piece == 1:  # 黑棋
                            Color(0, 0, 0)
                        else:  # 白棋
                            Color(1, 1, 1)
                        
                        pos_x = self.board_margin + x * self.grid_size
                        pos_y = self.board_margin + y * self.grid_size
                        
                        # 绘制棋子
                        Ellipse(pos=(pos_x - dp(13), pos_y - dp(13)),
                                size=(dp(26), dp(26)))
                        
                        # 如果是白棋，添加黑色边框
                        if piece == 2:
                            Color(0, 0, 0)
                            Line(circle=(pos_x, pos_y, dp(13)), width=1)
                        
                        # 标记最后一步
                        if self.last_move and self.last_move[0] == x and self.last_move[1] == y:
                            if piece == 1:  # 黑棋上标白点
                                Color(1, 1, 1)
                            else:  # 白棋上标黑点
                                Color(0, 0, 0)
                            Ellipse(pos=(pos_x - dp(3), pos_y - dp(3)),
                                    size=(dp(6), dp(6)))
    
    def on_touch_down(self, touch):
        if self.game_over or not self.player_turn:
            return
        
        # 计算点击的棋盘坐标
        board_pos = self.get_board_position(touch.pos)
        if board_pos and self.game.is_valid_move(board_pos[0], board_pos[1]):
            # 玩家落子
            self.game.make_move(board_pos[0], board_pos[1], 1)  # 玩家使用黑子(1)
            self.last_move = (board_pos[0], board_pos[1])
            
            # 检查游戏是否结束
            if self.game.check_win(board_pos[0], board_pos[1], 1):
                self.game_over = True
                self.winner = 1
                self.parent.update_status("你赢了！")
            elif self.game.is_board_full():
                self.game_over = True
                self.winner = 0  # 平局
                self.parent.update_status("平局！")
            else:
                self.player_turn = False
                self.parent.update_status("AI思考中...")
            
            # 重绘棋盘
            self.draw_board()
    
    def check_ai_turn(self, dt):
        if not self.player_turn and not self.game_over:
            # AI落子
            ai_x, ai_y = self.ai.make_move()
            self.game.make_move(ai_x, ai_y, 2)  # AI使用白子(2)
            self.last_move = (ai_x, ai_y)
            
            # 检查游戏是否结束
            if self.game.check_win(ai_x, ai_y, 2):
                self.game_over = True
                self.winner = 2
                self.parent.update_status("AI赢了！")
            elif self.game.is_board_full():
                self.game_over = True
                self.winner = 0  # 平局
                self.parent.update_status("平局！")
            else:
                self.player_turn = True
                self.parent.update_status("你的回合")
            
            # 重绘棋盘
            self.draw_board()
    
    def get_board_position(self, pos):
        x, y = pos
        # 检查点击是否在棋盘范围内
        if (x < self.board_margin - self.grid_size/2 or 
            x > self.board_margin + self.grid_size * (self.board_size - 1) + self.grid_size/2 or
            y < self.board_margin - self.grid_size/2 or 
            y > self.board_margin + self.grid_size * (self.board_size - 1) + self.grid_size/2):
            return None
        
        # 计算棋盘坐标
        board_x = round((x - self.board_margin) / self.grid_size)
        board_y = round((y - self.board_margin) / self.grid_size)
        
        # 确保坐标在有效范围内
        if 0 <= board_x < self.board_size and 0 <= board_y < self.board_size:
            return (board_x, board_y)
        return None
    
    def reset_game(self):
        self.game.reset()
        self.player_turn = True
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.parent.update_status("你的回合")
        self.draw_board()
    
    def undo_move(self):
        if len(self.game.history) >= 2 and self.player_turn and not self.game_over:
            self.game.undo_move()  # 撤销AI的移动
            self.game.undo_move()  # 撤销玩家的移动
            if self.game.history:
                self.last_move = (self.game.history[-1][0], self.game.history[-1][1])
            else:
                self.last_move = None
            self.draw_board()
            self.parent.update_status("你的回合")

class GomokuApp(App):
    def build(self):
        # 创建主布局
        main_layout = BoxLayout(orientation='horizontal')
        
        # 创建棋盘
        self.board = GomokuBoard()
        main_layout.add_widget(self.board)
        
        # 创建右侧控制面板
        control_panel = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)
        
        # 添加标题
        title_label = Label(text='超高难度五子棋', font_size=24, size_hint=(1, 0.2))
        control_panel.add_widget(title_label)
        
        # 添加状态显示
        self.status_label = Label(text='你的回合', font_size=18, size_hint=(1, 0.2))
        control_panel.add_widget(self.status_label)
        
        # 添加说明
        info_label = Label(text='黑棋先行\n点击棋盘落子', font_size=16, size_hint=(1, 0.3))
        control_panel.add_widget(info_label)
        
        # 添加难度显示
        difficulty_label = Label(text='难度：超高', font_size=16, size_hint=(1, 0.1))
        control_panel.add_widget(difficulty_label)
        
        # 添加按钮
        buttons_layout = GridLayout(cols=1, spacing=10, size_hint=(1, 0.4))
        
        restart_button = Button(text='重新开始', font_size=18)
        restart_button.bind(on_press=self.restart_game)
        buttons_layout.add_widget(restart_button)
        
        undo_button = Button(text='悔棋', font_size=18)
        undo_button.bind(on_press=self.undo_move)
        buttons_layout.add_widget(undo_button)
        
        control_panel.add_widget(buttons_layout)
        
        # 将控制面板添加到主布局
        main_layout.add_widget(control_panel)
        
        return main_layout
    
    def update_status(self, text):
        self.status_label.text = text
    
    def restart_game(self, instance):
        self.board.reset_game()
    
    def undo_move(self, instance):
        self.board.undo_move()

if __name__ == '__main__':
    GomokuApp().run()