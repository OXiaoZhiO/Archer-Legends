# objects/target.py
import random
import pygame
from pygame.math import Vector2
from settings import COLORS, SCREEN_WIDTH,WORLD_OFFSET,HALF_SCREEN
from utils.transform import sx_to_wx,w_to_s



class Target:
    """靶子类，处理靶子的移动、绘制和碰撞检测"""

    def __init__(self):
        """
        初始化靶子属性。
        靶子从屏幕左侧或右侧随机生成，并向相反方向移动。
        """
        # 决定靶子从左侧还是右侧进入屏幕
        if random.choice([True, False]):  # 随机选择左侧或右侧
            self.world_pos = Vector2(random.randint(-2000, -1000), random.randint(50, 300))  # 左侧屏幕外
            self.direction = 1  # 向右移动
        else:
            self.world_pos = Vector2(random.randint(1000, 2000), random.randint(50, 300))  # 右侧屏幕外
            self.direction = -1  # 向左移动

        self.radius = 20  # 靶子半径
        self.speed = random.uniform(1.0, 2.5)  # 随机速度
        self.score_value = 10  # 基础分值
        self.rect = pygame.Rect(self.world_pos.x - self.radius, self.world_pos.y - self.radius, self.radius * 2,
                                self.radius * 2)

    def update(self):

        self.world_pos.x += self.speed * self.direction  # 根据方向更新世界坐标位置

        if self.world_pos.x <=-1000: # 检查是否超出边界
            self.direction = 1
        elif self.world_pos.x >=1000:
            self.direction = -1


        # 更新碰撞矩形的位置
        self.rect.topleft = (self.world_pos.x - self.radius, self.world_pos.y - self.radius)

    def draw(self, surface: pygame.Surface, world_offset: int):
        """
        绘制靶子(同心圆)，并考虑背景偏移。
        :param surface: 绘制目标的Surface对象
        :param world_offset: 当前世界的偏移量
        """
        screen_pos = (w_to_s(self.world_pos,world_offset))  # 计算屏幕相对位置
        pygame.draw.circle(surface, COLORS['red'], screen_pos, self.radius)  # 外层红色圆
        pygame.draw.circle(surface, COLORS['white'], screen_pos, self.radius - 10)  # 中间白色圆
        pygame.draw.circle(surface, COLORS['gold'], screen_pos, 5)  # 靶心金色圆

    def check_hit(self, arrow_pos: Vector2) -> bool:
        """
        检测箭是否命中靶子。
        :param arrow_pos: 箭矢的当前位置(Vector2)
        :return: 如果命中返回True，否则返回False
        """
        return self.world_pos.distance_to(arrow_pos) <= (self.radius + 10)  # 判断箭与靶子中心的距离是否小于命中范围

    def get_position(self) -> Vector2:
        """
        获取靶子的当前位置。
        :return: 靶子的当前位置(Vector2)
        """
        return self.world_pos
