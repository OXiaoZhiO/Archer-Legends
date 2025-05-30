# utils/drawing.py
import math
import pygame
from pygame.math import Vector2
from settings import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT


def draw_dashed_line(surface: pygame.Surface, color: tuple, start_pos: Vector2, end_pos: Vector2, dash_length: int = 5):
    """
    绘制虚线。
    :param surface: Pygame 的 Surface 对象，用于绘制。
    :param color: 虚线的颜色 (R, G, B)。
    :param start_pos: 虚线起点的 Vector2 对象。
    :param end_pos: 虚线终点的 Vector2 对象。
    :param dash_length: 每段虚线的长度，默认为 5。
    """
    length = (end_pos - start_pos).length()  # 计算起点到终点的总长度
    if length == 0:
        return  # 如果长度为 0，则不绘制

    direction = (end_pos - start_pos).normalize()  # 计算方向向量
    for i in range(0, int(length), dash_length * 5):  # 每隔 dash_length * 5 绘制一段
        start = start_pos + direction * i
        end = start_pos + direction * min(i + dash_length, length)
        pygame.draw.line(surface, color, start, end, 1)  # 绘制单段虚线


def draw_trajectory(surface: pygame.Surface, start_pos: Vector2, target_pos: Vector2, power: float):
    """
    绘制抛物线轨迹预测线。
    :param surface: Pygame 的 Surface 对象，用于绘制。
    :param start_pos: 抛物线起点的 Vector2 对象。
    :param target_pos: 抛物线目标点的 Vector2 对象。
    :param power: 发射力度，影响初速度。
    """
    steps = 20  # 预测步数
    initial_velocity = (target_pos - start_pos).normalize() * min(15, (target_pos - start_pos).length() / 15)
    velocity = initial_velocity * (0.5 + (power / 100))  # 根据力度调整初速度
    gravity = Vector2(0, 0.21)  # 模拟重力
    pos = Vector2(start_pos)

    for _ in range(steps):  # 按步数模拟抛物线轨迹
        velocity += gravity  # 更新速度（受重力影响）
        next_pos = pos + velocity  # 计算下一位置
        draw_dashed_line(surface, COLORS['black'], pos, next_pos)  # 使用虚线绘制轨迹
        pos = next_pos  # 更新当前位置
        if not (0 <= pos.x <= SCREEN_WIDTH and 0 <= pos.y <= SCREEN_HEIGHT):  # 检查是否超出屏幕范围
            break


def draw_direction_indicator(surface: pygame.Surface, player_pos: Vector2, mouse_pos: tuple):
    """
    绘制方向指示箭头。
    :param surface: Pygame 的 Surface 对象，用于绘制。
    :param player_pos: 玩家位置的 Vector2 对象。
    :param mouse_pos: 鼠标位置的 (x, y) 元组。
    """
    direction = Vector2(mouse_pos) - player_pos  # 计算玩家到鼠标的向量
    if direction.length() > 0:  # 确保方向向量非零
        direction = direction.normalize()
        end_pos = player_pos + direction * 30  # 箭头长度为 30
        pygame.draw.line(surface, COLORS['white'], player_pos, end_pos, 2)  # 绘制箭头主干

        # 计算箭头三角形的两个顶点
        angle = -math.atan2(-direction.y, direction.x)  # 计算箭头方向的角度
        arrow_size = 10  # 箭头三角形的大小
        point1 = end_pos + Vector2(math.cos(angle + math.pi * 3 / 4), math.sin(angle + math.pi * 3 / 4)) * arrow_size
        point2 = end_pos + Vector2(math.cos(angle - math.pi * 3 / 4), math.sin(angle - math.pi * 3 / 4)) * arrow_size

        # 绘制箭头三角形
        pygame.draw.polygon(surface, COLORS['white'], [end_pos, point1, point2])


def draw_collision_volume(surface: pygame.Surface, position: tuple, shape: str, size):
    """
    绘制碰撞体积（矩形或圆形）。
    :param surface: Pygame 的 Surface 对象，用于绘制。
    :param position: 碰撞体积的位置 (x, y)。
    :param shape: 碰撞体积的形状，可以是 "rect" 或 "circle"。
    :param size: 碰撞体积的大小。对于矩形为 (width, height)，对于圆形为半径。
    """
    if shape == "rect":
        rect = pygame.Rect(0, 0, size[0], size[1])  # 创建矩形对象
        rect.center = position  # 设置矩形的中心坐标
        pygame.draw.rect(surface, COLORS['red'], rect, 1)  # 使用红色线条绘制矩形
    elif shape == "circle":
        pygame.draw.circle(surface, COLORS['red'], position, size, 1)  # 使用红色线条绘制圆形
