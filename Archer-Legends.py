# Archer-Legends.py
import pygame
import random
from sys import exit
from typing import List
from settings import *
from objects.power_bar import PowerBar
from objects.arrow import Arrow
from objects.home import Home
from objects.target import Target
from objects.player import Player
from enemys.bat import Bat
from enemys.zombie import Zombie
from utils.start_menu import show_start_menu,draw_rounded_button
from utils.game_over_menu import *
from utils.shop_menu import *
from utils.drawing import *
from utils.debug import *
from utils.pause_menu import *
from utils.transform import *
from objects.health_bar import Health_bar


# 初始化游戏
pygame.init()
pygame.mixer.init()
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
    global WORLD_OFFSET, HARD, TIME, SPAWN_TIME  # 添加 WORLD_OFFSET 的全局声明
    HARD=0
    TIME=0
    hit_sound = pygame.mixer.Sound(HIT_PATH)  # 命中靶子音效
    hit_sound.set_volume(10 * VOLUME)
    select_sound=pygame.mixer.Sound(SELECT_PATH)
    select_sound.set_volume(10 * VOLUME)

    """游戏主函数"""
    # 加载并播放背景音乐


    player=Player()
    home=Home()
     
    second=0

    arrows: List[Arrow] = []  # 箭矢列表
    targets: List[Target] = []
    bats: List[Bat] = []
    zombies: List[Zombie] = []
    font = pygame.font.Font(FONT_PATH, 28)  # 字体
    small_font = pygame.font.Font(FONT_PATH, 16)  # 小字体，用于显示坐标

    score = 0  # 得分
    spawn_timer = 0  # 靶子生成计时器

    # 蓄力系统
    power_bar = PowerBar(w_to_s(player.world_pos,WORLD_OFFSET))  # 蓄力条位置
    
    if not show_start_menu(screen, background_image):
        return
    # 初始化血量条
    health_bar = Health_bar("player", player.max_health)

    running = True
    paused = False
    shop= False
    pause_button = pygame.Rect(SCREEN_WIDTH-100, 10, 80, 50)  # 暂停按钮的位置和大小
    shop_button = pygame.Rect(SCREEN_WIDTH - 200, 10, 80, 50)  # 暂停按钮的位置和大小

    pygame.mixer.music.load(BGM_PATH)  # 替换为你的 BGM 文件路径
    pygame.mixer.music.set_volume(VOLUME / 3)  # 设置音量（0.0 到 1.0）
    pygame.mixer.music.play(-1)  # -1 表示循环播放

    while running:

        if TIME % 30 == 0 and second == 0:
            HARD += 1
            if SPAWN_TIME > 60:
                SPAWN_TIME -= 13

        second += 1
        if second == FPS:
            second = 0
            TIME += 1

        # 更新坐标与世界坐标
        mouse_pos = pygame.mouse.get_pos()
        #w_player_pos = Vector2(WORLD_OFFSET,PLAYER_START_POS[1])
        w_mouse_pos = s_to_w(pygame.mouse.get_pos(), WORLD_OFFSET)


        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.collidepoint(event.pos):  # 检测暂停按钮点击
                    select_sound.play()
                    paused = not paused
                    if paused:
                        pause_game(screen)
                        paused=False
                        break
                if shop_button.collidepoint(event.pos):  # 检测暂停按钮点击
                    select_sound.play()
                    shop = not shop
                    if shop:
                        shop_menu(screen,HARD,player,home,power_bar,zombies,bats,targets)
                        shop=False
                        break
                if event.button == 1 and not paused:  # 左键按下开始蓄力
                    player.charging = True
                    power_bar.start_charging()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and player.charging and not paused :  # 左键释放发射箭
                    player.charging = False
                    power = power_bar.stop_charging()

                    if player.arrow_count>0 and player.alive:
                        player.arrow_count -= 1
                        arrows.append(Arrow((player.world_pos.x, player.world_pos.y-30), Vector2(w_mouse_pos), WORLD_OFFSET, power))


        if paused:
            continue  # 如果游戏暂停，则跳过后续逻辑

        # 键盘控制背景和其他对象移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] :
            player.to_home+=1

        if keys[pygame.K_a] and not keys[pygame.K_d]:  # 左移背景和其他对象
            if player.alive:
                player.move = True
                WORLD_OFFSET -= player.speed
                player.go(-1)

        elif keys[pygame.K_d] and not keys[pygame.K_a]:  # 右移背景和其他对象
            if player.alive:
                player.move = True
                WORLD_OFFSET += player.speed
                player.go(1)

        elif not keys[pygame.K_d] and not keys[pygame.K_a]:
            player.move = False

        if player.to_home>=player.to_home_max:
            player.to_home=0
            player.world_pos=Vector2(PLAYER_START_POS)
            WORLD_OFFSET=0
        """ 更新游戏状态 """

        # 在主循环中更新血量条
        player.update()
        health_bar.update(player.health,player.max_health)
        home.update()

        power_bar.update(Vector2(w_to_s(player.world_pos,WORLD_OFFSET)))  # 更新蓄力条

        for target in targets[:]:
            target.update()  # 更新靶子位置

        for bat in bats[:]:
            bat.update()  # 更新bat状态
            if bat.attack and not bat.attack_cooldown:
                if home.tenacity<bat.attack_power:
                    hit_sound.play()
                    home.health -= (bat.attack_power-home.tenacity)
                bat.health -= home.return_power
                if bat.health <= 0:
                    bat.death(screen, WORLD_OFFSET)
                    player.exp += bat.exp_value
                    player.money += bat.money
                bat.attack_cooldown=True

            if not bat.alive:
                bats.remove(bat)

        for zombie in zombies[:]:
            zombie.update(player.world_pos)  # 更新bat状态
            if zombie.attack and not zombie.attack_cooldown and zombie.atk=="home":
                if home.tenacity<zombie.attack_power:
                    home.health -= (zombie.attack_power-home.tenacity)
                zombie.health-=home.return_power
                if zombie.health <= 0:
                    zombie.death(screen, WORLD_OFFSET)
                    player.exp += zombie.exp_value
                    player.money += zombie.money
                hit_sound.play()
                zombie.attack_cooldown=True
            elif zombie.attack and not zombie.attack_cooldown and zombie.atk=="player":
                if player.tenacity < zombie.attack_power:
                    player.health -= (zombie.attack_power - player.tenacity)
                zombie.health -= home.return_power
                if zombie.health <= 0:
                    zombie.death(screen, WORLD_OFFSET)
                    player.exp += zombie.exp_value
                    player.money += zombie.money
                hit_sound.play()
                zombie.attack_cooldown=True

            if not zombie.alive:
                zombies.remove(zombie)

        for arrow in arrows[:]:
            arrow.update()  # 更新箭矢位置
            remove_arrow = False  # 标记是否需要移除箭矢

            # 检测箭矢与所有靶子的碰撞
            for target in targets[:]:
                if target.check_hit(arrow.world_pos):  # 检测碰撞
                    score += target.score_value * HARD
                    targets.remove(target)
                    player.exp+=HARD
                    hit_sound.play()
                    remove_arrow = True
                    break

            for bat in bats[:]:
                if bat.death_lock:

                    if bat.check_hit(arrow.world_pos):  # 检测碰撞
                        score += bat.score_value
                        hit_sound.play()
                        bat.health-=player.attack_power
                        if bat.health<=0:
                            bat.death(screen, WORLD_OFFSET)
                            player.exp += bat.exp_value
                            player.money += bat.money
                        remove_arrow = True
                        break

            for zombie in zombies[:]:
                if zombie.death_lock:
                    if zombie.check_hit(arrow.world_pos):  # 检测碰撞
                        score += zombie.score_value
                        hit_sound.play()
                        zombie.health -= player.attack_power
                        if zombie.health <= 0:
                            zombie.death(screen, WORLD_OFFSET)
                            player.exp += zombie.exp_value
                            player.money += zombie.money
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
        len_all=len(targets)+len(zombies)+len(bats)
        if spawn_timer >= SPAWN_TIME and len_all < (40+HARD*3):  # 每3秒且
            random_opponent=random.choice(["target","zombie","zombie","bat","bat","bat"])
            if random_opponent=="target":
                targets.append(Target())
            elif random_opponent=="zombie":
                bats.append(Bat(HARD))
            elif random_opponent == "bat":
                zombies.append(Zombie(HARD))


            spawn_timer = 0



        if home.health<=0:
            if not show_game_over_menu(screen,background_image,score,TIME):
                break
            else:
                main()







        """ 渲染 """

        # 绘制背景，考虑偏移量
        screen.blit(background_image, (-WORLD_OFFSET % SCREEN_WIDTH - SCREEN_WIDTH, 0))
        screen.blit(background_image, (-WORLD_OFFSET % SCREEN_WIDTH, 0))
        screen.blit(background_image, (-WORLD_OFFSET % SCREEN_WIDTH + SCREEN_WIDTH, 0))

        #screen.blit(grass_image, (-WORLD_OFFSET % SCREEN_WIDTH - SCREEN_WIDTH, 0))
        #screen.blit(grass_image, (-WORLD_OFFSET % SCREEN_WIDTH, 0))
        #screen.blit(grass_image, (-WORLD_OFFSET % SCREEN_WIDTH + SCREEN_WIDTH, 0))



        home.draw(screen, WORLD_OFFSET)
        home.health_bar.draw(screen,Vector2(0,0),WORLD_OFFSET,True)
        # 绘制玩家
        player.draw(screen, WORLD_OFFSET)

        # 绘制，考虑偏移量
        for target in targets:
            if check(target.world_pos,WORLD_OFFSET):
                target.draw(screen, WORLD_OFFSET)
        for bat in bats:
            if check(bat.world_pos, WORLD_OFFSET):
                bat.draw(screen, WORLD_OFFSET)
                bat.health_bar.draw(screen,Vector2(bat.world_pos.x,bat.world_pos.y-30), WORLD_OFFSET)
        for zombie in zombies:
            if check(zombie.world_pos, WORLD_OFFSET):
                zombie.draw(screen, WORLD_OFFSET)
                zombie.health_bar.draw(screen,Vector2(zombie.world_pos.x,zombie.world_pos.y-30), WORLD_OFFSET)
        for arrow in arrows:
            if check(arrow.world_pos, WORLD_OFFSET):
                arrow.draw(screen, WORLD_OFFSET)

        # 绘制方向指示器和轨迹预测
        if player.charging:
            player_spos=Vector2(w_to_s((player.world_pos.x,player.world_pos.y-25),WORLD_OFFSET))
            #draw_direction_indicator(screen,player_spos , mouse_pos)
            draw_trajectory(screen,player_spos, Vector2(mouse_pos), power_bar.current_power)

        # 绘制UI
        score_text = font.render(f"分数: {score}", True, COLORS['white'])
        screen.blit(score_text, (10, 10))
        score_text = font.render(f"金钱: {player.money}", True, COLORS['white'])
        screen.blit(score_text, (10, 40))
        score_text = font.render(f"时间: {TIME}", True, COLORS['white'])
        screen.blit(score_text, (10, 70))
        score_text = font.render(f"箭矢: {player.arrow_count}", True, COLORS['white'])
        screen.blit(score_text, (10,100))


        if TIME<20:
            score_text = font.render(f"AD键移动", True, COLORS['white'])
            screen.blit(score_text, (10, 150))
            score_text = font.render(f"鼠标左键蓄力射箭", True, COLORS['white'])
            screen.blit(score_text, (10, 180))
            score_text = font.render(f"长按空格回城", True, COLORS['white'])
            screen.blit(score_text, (10, 210))
            score_text = font.render(f"保护好主城免受敌人入侵！", True, COLORS['white'])
            screen.blit(score_text, (10, 240))




        # 绘制暂停按钮
        draw_rounded_button(screen,pause_button,COLORS['black'], COLORS['gold'],border_radius=15,
                                border_width=3)
        # 绘制商店按钮
        draw_rounded_button(screen, shop_button, COLORS['black'], COLORS['gold'], border_radius=15,
                            border_width=3)


        pause_text = font.render("暂停", True, COLORS['white'])
        screen.blit(pause_text, (pause_button.x + 10, pause_button.y + 10))

        shop_text = font.render("商店", True, COLORS['white'])
        screen.blit(shop_text, (shop_button.x + 10, shop_button.y + 10))


        # 绘制蓄力条
        power_bar.draw(screen)

        # 绘制玩家血量条
        health_bar.draw(screen,player.world_pos,WORLD_OFFSET)

        # 调用 display_coordinates() 时递 WORLD_OFFSET 参数
        display_coordinates(screen, small_font, keys, w_mouse_pos, tuple(player.world_pos), targets, arrows,bats, WORLD_OFFSET)

        pygame.display.flip()  # 更新显示
        clock.tick(FPS)


if __name__ == "__main__":
    main()