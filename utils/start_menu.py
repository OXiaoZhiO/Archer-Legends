# utils/start_menu.py
from settings import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH
import pygame


def show_start_menu(screen, background_image):
    """显示开始菜单，提供动态效果和用户交互"""

    # 初始化字体对象
    menu_font = pygame.font.Font(FONT_PATH, 48)  # 主菜单字体
    small_menu_font = pygame.font.Font(FONT_PATH, 20)  # 提示文字字体
    big_menu_font = pygame.font.Font(FONT_PATH, 50)  # 标题背景字体

    # 渲染菜单文本
    start_text = menu_font.render("开始游戏", True, COLORS['black'])  # 开始按钮文本
    title_text = menu_font.render("弓箭手传奇", True, COLORS['gold'])  # 主标题
    title_text_bk = big_menu_font.render("弓箭手传奇", True, COLORS['red'])  # 主标题背景
    quit_text = small_menu_font.render("退出游戏", True, COLORS['black'])  # 退出按钮文本

    # 定义按钮区域
    start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)  # 开始按钮
    quit_button_rect = pygame.Rect(10, SCREEN_HEIGHT - 40, 100, 30)  # 退出按钮调整到左下角并缩小

    # 绘制圆角带边框的按钮
    pygame.draw.rect(screen, COLORS['black'], start_button_rect, border_radius=20, width=4)  # 开始按钮边框
    pygame.draw.rect(screen, COLORS['gold'], start_button_rect, border_radius=20)  # 开始按钮背景
    pygame.draw.rect(screen, COLORS['black'], quit_button_rect, border_radius=15, width=3)  # 退出按钮边框
    pygame.draw.rect(screen, COLORS['red'], quit_button_rect, border_radius=15)  # 退出按钮背景

    # 主循环
    while True:
        screen.blit(background_image, (0, 0))  # 绘制背景图像

        # 绘制主标题及其背景
        title_x = SCREEN_WIDTH // 2 - title_text.get_width() // 2  # 计算标题水平居中位置
        title_y = SCREEN_HEIGHT // 2 - 220  # 标题垂直位置
        screen.blit(title_text_bk, (title_x, title_y))  # 绘制标题背景
        screen.blit(title_text, (title_x + 5, title_y))  # 绘制主标题（带轻微偏移）

        # 绘制按钮
        pygame.draw.rect(screen, COLORS['gold'], start_button_rect)  # 开始按钮背景
        pygame.draw.rect(screen, COLORS['red'], quit_button_rect)  # 退出按钮背景
        screen.blit(start_text, (start_button_rect.x + 10, start_button_rect.y + 10))  # 开始按钮文本
        screen.blit(quit_text, (quit_button_rect.x + 10, quit_button_rect.y + 5))  # 调整退出按钮文本位置

        pygame.display.flip()  # 更新屏幕显示

        # 处理用户事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 检测窗口关闭事件
                return False  # 返回 False 表示退出游戏
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 检测鼠标点击事件
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):  # 点击开始按钮
                    return True  # 返回 True 表示进入游戏
                elif quit_button_rect.collidepoint(mouse_pos):  # 点击退出按钮
                    return False  # 返回 False 表示退出游戏
