# objects/health_bar.py
import pygame
from pygame.math import Vector2
from settings import COLORS

from utils.transform import wx_to_sx


class Health_bar:
    """血量条类，用于显示玩家的生命值"""

    def __init__(self, owner, max_health: int):
        self.owner = owner  # 新增属性：所属生物
        self.max_health = max_health  # 最大生命值
        self.current_health = max_health  # 当前生命值
        self.width = self.max_health * 0.6  # 根据最大生命值自动调整宽度
        self.height = 10  # 调整血量条高度
        self.color = COLORS['red']  # 血量条颜色

    def update(self, current_health: int):
        self.current_health = current_health

    def draw(self,surface: pygame.Surface, pos: Vector2,offset):
        """绘制血量条"""
        # 计算血量条位置（在下方）
        bar_x = wx_to_sx((pos.x - self.width // 2),offset)
        bar_y = pos.y + 50  # 假设下方偏移 50

        # 背景框
        pygame.draw.rect(surface, COLORS['gray'],
                         (bar_x, bar_y, self.width, self.height))
        # 血量条
        health_width = min((self.current_health / self.max_health) * self.width, self.width)  # 确保不超过边框
        pygame.draw.rect(surface, self.color,
                         (bar_x, bar_y, health_width, self.height))
        # 边框
        pygame.draw.rect(surface, COLORS['white'],
                         (bar_x, bar_y, self.width, self.height), 2)