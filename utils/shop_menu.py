# utils/shop_menu.py
import pygame
from sys import exit
from settings import *
from utils.start_menu import show_start_menu, draw_rounded_button

clock = pygame.time.Clock()


def shop_menu(screen: pygame.Surface,HARD,player,home,power_bar,zombies,bats,targets):
    select_sound = pygame.mixer.Sound(SELECT_PATH)
    select_sound.set_volume(10 * VOLUME)
    """显示商店菜单"""
    global WORLD_OFFSET
    shopping = True
    font = pygame.font.Font(FONT_PATH, 36)
    small_font = pygame.font.Font(FONT_PATH, 20)  # 提示文字字体
    shop_text = font.render("欢迎来到商店", True, COLORS['black'])
    exit_button = pygame.Rect(10, SCREEN_HEIGHT - 60, 100, 50)

    # 商品信息：名称和价格
    items = [
        {"name": "箭矢+30", "price": 50+(HARD*20)},
        {"name": "攻击+5", "price": 200+(HARD*20)},
        {"name": "主城血量+100", "price": 80+(HARD*20)},
        {"name": "蓄力速度+20%", "price": 200+(HARD*20)},
        {"name": "主城反伤+10", "price": 250+(HARD*20)},
        {"name": "韧性+10", "price": 250+(HARD*20)},
        {"name": "速度+10%", "price": 200+(HARD*20)},
        {"name": "所有属性上升", "price": 600+(HARD*20)},
        {"name": "回血能力上升", "price": 400+(HARD*20)},
        {"name": "核弹", "price": 800+(HARD*20)},
    ]

    # 创建10个商店窗口按钮，两行，每行5个
    shop_buttons = []
    button_width, button_height = 150, 80
    padding_x, padding_y = 20, 20
    for row in range(2):
        for col in range(5):
            x = col * (button_width + padding_x) + 100
            y = row * (button_height + padding_y) + 100
            button_rect = pygame.Rect(x, y, button_width, button_height)
            shop_buttons.append(button_rect)

    message = None
    message_timer = 0


    while shopping:


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
        screen.blit(shop_text, (SCREEN_WIDTH // 2 - shop_text.get_width() // 2, 10))

        # 显示玩家当前金钱
        money_text = font.render(f"金钱: ${player.money}", True, COLORS['black'])
        screen.blit(money_text, (SCREEN_WIDTH - money_text.get_width() - 10, 10))

        # 绘制10个商店窗口按钮
        for i, button_rect in enumerate(shop_buttons):
            item_price = items[i]["price"]
            if player.money >= item_price:
                button_color = COLORS['green']
                text_color = COLORS['black']
            else:
                button_color = COLORS['dark_gray']
                text_color = COLORS['red']

            draw_rounded_button(screen, button_rect, button_color, COLORS['white'], border_radius=15, border_width=3)

            # 第一行：商品名称
            name_text = small_font.render(items[i]["name"], True, text_color)
            name_text_rect = name_text.get_rect(center=(button_rect.centerx, button_rect.top + 20))
            screen.blit(name_text, name_text_rect.topleft)

            # 第二行：所需金钱
            price_text = small_font.render(f"${items[i]['price']}", True, text_color)
            price_text_rect = price_text.get_rect(center=(button_rect.centerx, button_rect.bottom - 20))
            screen.blit(price_text, price_text_rect.topleft)

        # 绘制退出按钮
        draw_rounded_button(screen, exit_button, COLORS['white'], COLORS['red'], border_radius=15,
                            border_width=3)
        exit_text = font.render("退出", True, COLORS['black'])
        screen.blit(exit_text, (exit_button.x + 15, exit_button.y + 5))

        # 显示消息（如果有）
        if message and pygame.time.get_ticks() - message_timer < 1000:
            screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT - message.get_height()-15))
        else:
            message = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    select_sound.play()
                    shopping = False
                else:
                    # 检查是否点击了商店按钮
                    for i, button_rect in enumerate(shop_buttons):
                        if button_rect.collidepoint(event.pos):
                            select_sound.play()
                            item_price = items[i]["price"]
                            if player.money >= item_price:
                                player.money -= item_price
                                if i==0:
                                    if player.arrow_up_cd>30:
                                        player.arrow_up_cd-=15
                                    player.arrow_count+=30
                                elif i==1:
                                    player.attack_power+=5
                                elif i==2:
                                    home.health+=100
                                elif i==3:
                                    power_bar.charge_speed*=1.2
                                elif i==4:
                                    home.return_power+=10
                                elif i==5:
                                    home.tenacity+=10
                                    player.tenacity+=10
                                elif i==6:
                                    player.speed*=1.1
                                elif i==7:
                                    player.max_health += 50
                                    player.health_up+=5
                                    home.health_up+=5
                                    home.return_power += 5
                                    home.tenacity += 5
                                    player.tenacity += 5
                                    home.health += 50
                                    player.arrow_count += 10
                                    player.attack_power += 5
                                elif i==8:
                                    player.health_up += 10
                                    home.health_up += 10
                                    if player.health_up_cd>60:
                                        player.health_up_cd -= 5
                                    if home.health_up_cd>60:
                                        home.health_up_cd -= 5
                                elif i==9:
                                    zombies.clear()
                                    bats.clear()
                                    targets.clear()





                                message = font.render(f"购买成功：{items[i]['name']}，剩余金钱：${player.money}",
                                                      True, COLORS['green'])
                                message_timer = pygame.time.get_ticks()
                            else:
                                message = font.render(f"金钱不足，无法购买：{items[i]['name']}", True,
                                                      COLORS['red'])
                                message_timer = pygame.time.get_ticks()

        pygame.display.flip()
        clock.tick(FPS)
