# utils/debug.py
import pygame
from settings import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
from utils.drawing import draw_collision_volume

from utils.transform import w_to_s


# 按下CTRL显示所有控件坐标
def display_coordinates(screen: pygame.Surface, small_font: pygame.font.Font,
                        keys: list, mouse_pos: tuple, player_pos: tuple,
                        targets: list, arrows: list, world_offset: int):
    """
    在按下 Ctrl 键时显示鼠标、玩家、靶子和箭矢的坐标。
    :param screen: Pygame 的 Surface 对象，用于绘制文本。
    :param small_font: Pygame 的 Font 对象，用于渲染文本。
    :param keys: 按键状态列表，通过 pygame.key.get_pressed() 获取。
    :param mouse_pos: 鼠标位置，通过 pygame.mouse.get_pos() 获取。
    :param player_pos: 玩家的位置，通常是一个 (x, y) 元组。
    :param targets: 靶子对象列表。
    :param arrows: 箭矢对象列表。
    :param world_offset: 背景偏移量。
    """
    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:  # 检测 Ctrl 键是否被按下

        # 格式化坐标显示函数
        def format_coordinate(pos: object) -> str:
            x, y = pos
            x_int, y_int = int(x), int(y)
            x_str = f"{x_int}x" if x != x_int else str(x_int)
            y_str = f"{y_int}x" if y != y_int else str(y_int)
            return f"({x_str}, {y_str})"

        # 显示鼠标位置
        formatted_mouse_pos = format_coordinate(mouse_pos)
        mouse_coord_text = small_font.render(f"光标: {formatted_mouse_pos}", True, COLORS['black'])
        screen.blit(mouse_coord_text, w_to_s(mouse_pos,world_offset))

        # 显示所有靶子的坐标及碰撞体积
        for target in targets:
            target_pos = target.get_position()  # 假设 Target 类有一个 get_position 方法返回其位置
            formatted_target_pos = format_coordinate(target_pos)
            target_coord_text = small_font.render(f"靶子: {formatted_target_pos}", True, COLORS['black'])
            screen.blit(target_coord_text, (w_to_s(target_pos,world_offset)))
            # 假设每个靶子的碰撞体积为矩形，大小为 target.rect.size
            draw_collision_volume(screen, (w_to_s(target_pos,world_offset)), "rect",
                                  target.rect.size)

        # 显示所有箭矢的坐标及碰撞体积
        for arrow in arrows:
            arrow_pos = arrow.get_position()  # 假设 Arrow 类有一个 get_position 方法返回其位置
            formatted_arrow_pos = format_coordinate(arrow_pos)
            arrow_coord_text = small_font.render(f"箭矢: {formatted_arrow_pos}", True, COLORS['black'])
            screen.blit(arrow_coord_text, (w_to_s(arrow_pos,world_offset)))
            # 假设每个箭矢的碰撞体积为矩形，大小为 arrow.rect.size
            draw_collision_volume(screen, w_to_s(arrow_pos,world_offset), "circle",15)

        # 显示玩家坐标及碰撞体积
        formatted_player_pos = format_coordinate(player_pos)
        player_coord_text = small_font.render(f"玩家: {formatted_player_pos}", True, COLORS['black'])
        screen.blit(player_coord_text, (10, SCREEN_HEIGHT - 20))  # 显示在左下方
        # 玩家的碰撞体积为圆形，半径为 8
        draw_collision_volume(screen,w_to_s((0,530),world_offset), "circle", 10)

        # 显示屏幕宽高信息
        bottom_right_coord_text = small_font.render(
            f"宽高: ({SCREEN_WIDTH}, {SCREEN_HEIGHT})", True, COLORS['black']
        )
        screen.blit(bottom_right_coord_text, (SCREEN_WIDTH - 135, SCREEN_HEIGHT - 20))  # 显示在屏幕右下角

        #显示偏移量
        offset_text = small_font.render(f"偏移量: {world_offset}", True, COLORS['black'])
        screen.blit(offset_text, (10, 40))