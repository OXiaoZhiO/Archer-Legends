# objects/arrow.py
import math
import pygame
from pygame.math import Vector2
from settings import *

from utils.transform import s_to_w, w_to_s


class Arrow:
    """箭矢类，处理箭的物理运动、渲染以及边界检测"""

    def __init__(self, start_pos: tuple, target_pos: tuple, WORLD_OFFSET: int, power: float = 50):
        """
        初始化箭矢对象。
        :param start_pos: 箭矢的起始位置 (x, y)
        :param target_pos: 箭矢的目标位置 (x, y)
        :param WORLD_OFFSET: 当前世界的偏移量
        :param power: 射箭的力量，默认值为50
        """
        self.world_pos = start_pos  # 使用绝对世界坐标
        self.original_image = self.create_arrow_image()  # 原始箭头图像
        self.rect = self.original_image.get_rect(center=(start_pos[0], start_pos[1]))  # 碰撞矩形

        # 计算箭矢的初始速度方向和大小
        direction =  target_pos-start_pos
        speed_multiplier = 0.5 + (power / 100)  # 根据力量调整速度倍率
        self.velocity = direction.normalize() * min(15, direction.length() / 15) * speed_multiplier

        self.gravity = Vector2(0, 0.21)  # 重力加速度
        self.angle = 0  # 当前旋转角度
        self.active = True  # 箭矢是否处于活跃状态

    def create_arrow_image(self) -> pygame.Surface:
        """创建箭头图像"""
        try:
            # 加载箭头图像并调整大小
            surf = pygame.image.load(ARROW_IMAGE_PATH).convert_alpha()
            surf = pygame.transform.scale(surf, (45, 10))  # 调整箭头图像大小

        except pygame.error as e:
            # 如果加载失败，使用默认的简单箭头图形
            print(f"无法加载图像 {ARROW_IMAGE_PATH}: {e}")
            surf = pygame.Surface((30, 8), pygame.SRCALPHA)
            pygame.draw.polygon(surf, (0, 0, 0), [(0, 0), (25, 4), (0, 8)])

        return surf

    def update(self):
        """更新箭矢的物理状态"""
        self.velocity += self.gravity  # 应用重力影响
        self.world_pos += self.velocity  # 更新箭矢的世界坐标位置

        # 根据速度向量计算箭头的旋转角度（弧度转角度）
        self.angle = math.degrees(math.atan2(-self.velocity.y, self.velocity.x))

        # 更新碰撞矩形的位置
        self.rect.center = (int(self.world_pos.x), int(self.world_pos.y))

    def draw(self, surface: pygame.Surface, WORLD_OFFSET: int):
        """绘制旋转后的箭头，并考虑背景偏移"""
        # 根据当前角度旋转箭头图像
        rotated = pygame.transform.rotate(self.original_image, self.angle)

        # 计算箭头在屏幕上的相对位置
        screen_pos=w_to_s(self.world_pos,WORLD_OFFSET)
        rect = rotated.get_rect(center=screen_pos)

        # 绘制箭头到指定表面
        surface.blit(rotated, rect)

    def get_position(self):
        """获取箭矢的当前位置"""
        return self.world_pos  # 返回箭矢的世界坐标位置

    def is_out_of_bounds(self, world_width: int, world_height: int) -> bool:
        """
        检查箭矢是否超出世界边界。
        :param world_width: 世界的宽度
        :param world_height: 世界的高度
        :return: 如果箭矢超出边界则返回 True，否则返回 False
        """
        return (self.world_pos.x < 0 or self.world_pos.x > world_width or
                self.world_pos.y < 0 or self.world_pos.y > world_height)
