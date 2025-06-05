#utils/pause_menu.py
import pygame
from sys import exit
from settings import *
from utils.start_menu import show_start_menu,draw_rounded_button

clock = pygame.time.Clock()
# 加载背景图，添加错误处理逻辑


def pause_game(screen: pygame.Surface):
    """暂停游戏并显示暂停菜单"""

    paused = True
    font = pygame.font.Font(FONT_PATH, 36)
    pause_text = font.render("游戏已暂停", True, COLORS['white'])
    resume_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 100, 50)

    while paused:
        global WORLD_OFFSET, HARD
        screen.fill(COLORS['black'])

        try:
            background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()  # 加载背景图
            background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # 调整背景图大小
        except pygame.error as e:
            print(f"无法加载背景图像: {e}")
            background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            background_image.fill(COLORS['black'])
        # 绘制背景，考虑偏移量
        screen.blit(background_image, (-WORLD_OFFSET % SCREEN_WIDTH - SCREEN_WIDTH, 0))
        screen.blit(background_image, (-WORLD_OFFSET % SCREEN_WIDTH, 0))
        screen.blit(background_image, (-WORLD_OFFSET % SCREEN_WIDTH + SCREEN_WIDTH, 0))
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        # 绘制继续按钮
        draw_rounded_button(screen, resume_button, COLORS['white'], COLORS['gold'], border_radius=15,
                            border_width=3)
        resume_text = font.render("继续", True, COLORS['black'])
        screen.blit(resume_text, (resume_button.x + 13, resume_button.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(event.pos):
                    paused = False

        pygame.display.flip()
        clock.tick(FPS)
