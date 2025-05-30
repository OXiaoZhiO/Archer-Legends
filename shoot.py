# shoot.py
import pygame
from typing import List
from settings import *
from objects.power_bar import PowerBar
from objects.arrow import Arrow
from objects.target import Target
from utils.start_menu import show_start_menu
from utils.drawing import *
from utils.debug import *
from utils.transform import *

# 初始化游戏
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("弓箭手传奇")
clock = pygame.time.Clock()


# 加载背景图，添加错误处理逻辑
try:
    background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()  # 加载背景图
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # 调整背景图大小
except pygame.error as e:
    print(f"无法加载背景图像: {e}")
    background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image.fill(COLORS['black'])


def main():
    """游戏主函数"""
    global WORLD_OFFSET  # 添加 WORLD_OFFSET 的全局声明
    player_pos = Vector2(PLAYER_START_POS)  # 玩家初始位置
    player_speed = PLAYER_SPEED  # 玩家移动速度
    arrows: List[Arrow] = []  # 箭矢列表
    targets: List[Target] = []
    font = pygame.font.Font(FONT_PATH, 28)  # 字体
    small_font = pygame.font.Font(FONT_PATH, 16)  # 小字体，用于显示坐标

    score = 0  # 得分
    spawn_timer = 0  # 靶子生成计时器

    # 蓄力系统
    power_bar = PowerBar(player_pos)  # 蓄力条位置
    charging = False  # 是否正在蓄力
    if not show_start_menu(screen, background_image):
        return

    running = True
    while running:

        # 更新坐标与世界坐标
        mouse_pos = pygame.mouse.get_pos()
        w_player_pos = Vector2(WORLD_OFFSET,PLAYER_START_POS[1])
        w_mouse_pos = s_to_w(pygame.mouse.get_pos(), WORLD_OFFSET)


        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键按下开始蓄力
                    charging = True
                    power_bar.start_charging()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and charging:  # 左键释放发射箭
                    charging = False
                    power = power_bar.stop_charging()
                    arrows.append(Arrow((w_player_pos.x, w_player_pos.y), Vector2(w_mouse_pos), WORLD_OFFSET, power))

        # 键盘控制背景和其他对象移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # 左移背景和其他对象
            WORLD_OFFSET -= player_speed
        if keys[pygame.K_d]:  # 右移背景和其他对象
            WORLD_OFFSET += player_speed

        # 更新游戏状态


        power_bar.update(player_pos)  # 更新蓄力条

        for target in targets[:]:
            target.update()  # 更新靶子位置


        for arrow in arrows[:]:
            arrow.update()  # 更新箭矢位置
            remove_arrow = False  # 标记是否需要移除箭矢

            # 检测箭矢与所有靶子的碰撞
            for target in targets[:]:
                if target.check_hit(arrow.world_pos):  # 检测碰撞
                    score += target.score_value
                    targets.remove(target)
                    remove_arrow = True
                    break

            # 移除超出下表面的箭矢，考虑世界偏移
            if not ( arrow.world_pos.y <= SCREEN_HEIGHT):
                remove_arrow = True

            # 安全移除箭矢
            if remove_arrow and arrow in arrows:
                arrows.remove(arrow)

        # 随机生成新靶子
        spawn_timer += 1
        if spawn_timer >= 120 and len(targets) < 6:  # 每3秒且靶子少于5个时
            targets.append(Target())
            spawn_timer = 0

        # 绘制背景，考虑偏移量
        screen.blit(background_image, (-WORLD_OFFSET % SCREEN_WIDTH - SCREEN_WIDTH, 0))
        screen.blit(background_image, (-WORLD_OFFSET % SCREEN_WIDTH, 0))
        screen.blit(background_image, (-WORLD_OFFSET % SCREEN_WIDTH + SCREEN_WIDTH, 0))

        # 绘制玩家
        pygame.draw.circle(screen, COLORS['blue'], (int(player_pos.x), int(player_pos.y)), 8)

        # 绘制靶子和箭矢，考虑偏移量
        for target in targets:
            target.draw(screen, WORLD_OFFSET)
        for arrow in arrows:
            arrow.draw(screen, WORLD_OFFSET)

        # 绘制方向指示器和轨迹预测
        if charging:
            draw_direction_indicator(screen, player_pos, mouse_pos)
            draw_trajectory(screen, Vector2(player_pos), Vector2(mouse_pos), power_bar.current_power)

        # 绘制UI
        score_text = font.render(f"分数: {score}", True, COLORS['white'])
        screen.blit(score_text, (10, 10))

        # 绘制蓄力条
        power_bar.draw(screen)

        # 调用 display_coordinates() 时传递 WORLD_OFFSET 参数
        display_coordinates(screen, small_font, keys, w_mouse_pos, tuple(w_player_pos), targets, arrows, WORLD_OFFSET)

        pygame.display.flip()  # 更新显示
        clock.tick(FPS)  # 60FPS


if __name__ == "__main__":
    main()
