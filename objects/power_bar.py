# objects/power_bar.py
import pygame
from pygame.math import Vector2
from settings import COLORS

class PowerBar:
    """蓄力条类，用于显示和计算蓄力值"""

    def __init__(self, player_pos: Vector2):

        self.player_pos = player_pos  # 玩家位置坐标
        self.pos = player_pos  # 新增 pos 属性，与 player_pos 同步
        self.max_power = 50  # 最大蓄力值
        self.current_power = 0  # 当前蓄力值
        self.width = self.max_power * 0.6  # 根据最大蓄力值自动调整宽度
        self.height = 10  # 调整蓄力条高度 '''调小至合适大小'''
        self.charging = False  # 是否正在蓄力
        self.charge_speed = 1.5  # 蓄力速度

    def start_charging(self):
        """开始蓄力"""
        self.charging = True

    def stop_charging(self):
        """停止蓄力并返回当前蓄力值"""
        power = self.current_power
        self.current_power = 0
        self.charging = False
        return power

    def update(self, player_pos: Vector2):
        """更新蓄力值和玩家位置"""
        self.player_pos = player_pos
        self.pos = player_pos  # 同步更新 pos 属性
        if self.charging and self.current_power < self.max_power:
            self.current_power += self.charge_speed

    def draw(self, surface: pygame.Surface):
        """绘制蓄力条"""
        if not self.charging:
            return  # 未蓄力时不绘制蓄力条

        # 计算蓄力条位置（在玩家头部上方）
        bar_x = self.player_pos.x - self.width // 2
        bar_y = self.player_pos.y + 10  # 假设玩家头部在 y 方向偏移 50

        # 背景框
        pygame.draw.rect(surface, COLORS['gray'],
                         (bar_x, bar_y, self.width, self.height))
        # 蓄力条
        power_width = min((self.current_power / self.max_power) * self.width, self.width)  # 确保不超过边框 '''确保充能条不超过蓄力条边框'''
        pygame.draw.rect(surface, COLORS['yellow'],
                         (bar_x, bar_y, power_width, self.height))
        # 边框
        pygame.draw.rect(surface, COLORS['white'],
                         (bar_x, bar_y, self.width, self.height), 2)