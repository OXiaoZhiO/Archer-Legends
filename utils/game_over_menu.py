import pygame
from sys import exit
from pygame.locals import *
from settings import *


def draw_rounded_button(screen, rect, color, border_color, border_radius=15, border_width=3):
    """
    绘制带圆角的按钮
    :param screen: 屏幕对象
    :param rect: 按钮的矩形区域
    :param color: 按钮的填充颜色
    :param border_color: 按钮边框的颜色
    :param border_radius: 圆角半径，默认为 15
    :param border_width: 边框宽度，默认为 3
    """
    # 绘制按钮的填充颜色
    pygame.draw.rect(screen, color, rect, border_radius=border_radius)
    # 绘制按钮的边框
    pygame.draw.rect(screen, border_color, rect, width=border_width, border_radius=border_radius)


def draw_options(screen, font):
    """
    绘制 Restart 和 Quit 选项按钮及文本
    :param screen: 屏幕对象
    :param font: 字体对象
    :return: 返回两个按钮的矩形区域 (restart_rect, quit_rect)
    """
    # 渲染“重新再来”文本
    restart_text = font.render("重新再来", True, COLORS['black'])
    # 渲染“退出游戏”文本
    quit_text = font.render("退出游戏", True, COLORS['black'])

    # 定义“重新再来”按钮的矩形区域
    restart_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - restart_text.get_width() // 2 - 10,
        240,
        restart_text.get_width() + 20,
        restart_text.get_height() + 20
    )
    # 绘制“重新再来”按钮
    draw_rounded_button(screen, restart_rect, COLORS['green'], COLORS['black'], border_radius=15)
    # 将“重新再来”文本绘制到屏幕上
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 250))

    # 定义“退出游戏”按钮的矩形区域
    quit_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - quit_text.get_width() // 2 - 10,
        340,
        quit_text.get_width() + 20,
        quit_text.get_height() + 20
    )
    # 绘制“退出游戏”按钮
    draw_rounded_button(screen, quit_rect, COLORS['red'], COLORS['black'], border_radius=15)
    # 将“退出游戏”文本绘制到屏幕上
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 350))

    # 返回两个按钮的矩形区域，用于事件检测
    return restart_rect, quit_rect


def show_game_over_menu(screen, background_image, score, play_time):
    """
    显示游戏结束菜单
    :param screen: 屏幕对象
    :param background_image: 背景图像
    :param score: 玩家得分
    :param play_time: 游戏时间
    :return: 如果玩家选择“重新再来”，返回 True；如果选择“退出游戏”，返回 False
    """
    # 加载选择音效
    select_sound = pygame.mixer.Sound(SELECT_PATH)
    select_sound.set_volume(10 * VOLUME)  # 设置音效音量
    clock = pygame.time.Clock()  # 创建时钟对象以控制帧率

    # 加载字体
    font = pygame.font.Font(FONT_PATH, 48)
    small_font = pygame.font.Font(FONT_PATH, 36)

    running = True  # 控制菜单循环的标志

    # 加载并播放背景音乐
    pygame.mixer.music.load(END_PATH)  # 替换为你的 BGM 文件路径
    pygame.mixer.music.set_volume(VOLUME / 2)  # 设置音量（0.0 到 1.0）
    pygame.mixer.music.play(-1)  # -1 表示循环播放

    while running:
        # 绘制背景图像
        screen.blit(background_image, (0, 0))

        # 绘制标题
        title = font.render("游戏结束", True, COLORS['red'])
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # 显示分数
        score_text = small_font.render(f"分数: {score}", True, COLORS['black'])
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 160))

        # 显示游戏时间
        time_text = small_font.render(f"时间: {play_time}", True, COLORS['black'])
        screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, 200))

        # 绘制选项按钮
        restart_rect, quit_rect = draw_options(screen, font)

        # 更新屏幕显示
        pygame.display.flip()
        clock.tick(60)  # 控制帧率为 60 FPS

        # 事件处理
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()  # 如果用户关闭窗口，退出程序

            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # 获取鼠标点击位置
                if restart_rect.collidepoint(mouse_pos):
                    select_sound.play()  # 播放选择音效
                    return True  # 用户点击“重新再来”，重启游戏
                elif quit_rect.collidepoint(mouse_pos):
                    return False  # 用户点击“退出游戏”，退出游戏

    return None


def check_home_health_and_trigger_menu(home_health, screen, background_image, score, play_time):
    """
    检查大本营生命值并在必要时触发游戏结束菜单
    :param home_health: 大本营的生命值
    :param screen: 屏幕对象
    :param background_image: 背景图像
    :param score: 玩家得分
    :param play_time: 游戏时间
    :return: 如果大本营生命值小于等于 0，则显示游戏结束菜单；否则返回 True
    """
    if home_health <= 0:  # 如果大本营生命值小于等于 0
        return show_game_over_menu(screen, background_image, score, play_time)  # 显示游戏结束菜单
    return True  # 否则继续游戏