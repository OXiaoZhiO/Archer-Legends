import pygame
from  sys import  exit
from pygame.locals import *
from shoot.settings import COLORS, FONT_PATH, SCREEN_WIDTH, SCREEN_HEIGHT


def draw_rounded_button(screen, rect, color, border_color, border_radius=15, border_width=3):
    """绘制带圆角的按钮"""
    pygame.draw.rect(screen, color, rect, border_radius=border_radius)
    pygame.draw.rect(screen, border_color, rect, width=border_width, border_radius=border_radius)


def draw_options(screen, font):
    """绘制 Restart 和 Quit 选项"""
    restart_text = font.render("重新再来", True, COLORS['black'])
    quit_text = font.render("退出游戏", True, COLORS['black'])

    # 绘制 Restart 按钮
    restart_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - restart_text.get_width() // 2 - 10,
        240,
        restart_text.get_width() + 20,
        restart_text.get_height() + 20
    )
    draw_rounded_button(screen, restart_rect, COLORS['green'], COLORS['black'] , border_radius=15)

    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 250))

    # 绘制 Quit 按钮
    quit_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - quit_text.get_width() // 2 - 10,
        340,
        quit_text.get_width() + 20,
        quit_text.get_height() + 20
    )
    draw_rounded_button(screen, quit_rect, COLORS['red'], COLORS['black'] , border_radius=15)

    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 350))

    return restart_rect, quit_rect


def show_game_over_menu(screen, background_image):
    """显示游戏结束菜单"""
    clock = pygame.time.Clock()

    font = pygame.font.Font(FONT_PATH, 48)

    running = True

    while running:
        screen.blit(background_image, (0, 0))  # 绘制背景图像

        # 绘制标题
        title = font.render("游戏结束", True, COLORS['red'])
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # 绘制选项
        restart_rect, quit_rect = draw_options(screen, font)

        pygame.display.flip()
        clock.tick(60)

        # 事件处理
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()


            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_rect.collidepoint(mouse_pos):
                    return True  # 用户点击“重新再来”，重启游戏
                elif quit_rect.collidepoint(mouse_pos):
                    return False  # 用户点击“退出游戏”，退出游戏

    return None


def check_home_health_and_trigger_menu(home_health, screen, clock):
    if home_health <= 0:
        return show_game_over_menu(screen, clock)
    return True