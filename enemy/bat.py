# enemy/bat.py
import random
import pygame
from pygame.math import Vector2
from settings import COLORS, SCREEN_WIDTH, WORLD_OFFSET, BAT_MOVE_PATH,BAT_ORIGIN_PATH
from utils.transform import sx_to_wx, w_to_s

class Bat:

    def __init__(self):
        # 决定靶子从左侧还是右侧进入屏幕
        if random.choice([True, False]):  # 随机选择左侧或右侧
            self.world_pos = Vector2(sx_to_wx(0, WORLD_OFFSET), random.randint(50, 300))  # 左侧屏幕外
            self.direct = 1  # 向右移动
        else:
            self.world_pos = Vector2(sx_to_wx(SCREEN_WIDTH, WORLD_OFFSET), random.randint(50, 300))  # 右侧屏幕外
            self.direct = -1  # 向左移动


        self.speed = random.uniform(1.0, 2.5)  # 随机速度
        self.score_value = 10  # 基础分值
        self.radius = 40  # 假设蝙蝠的半径为20像素
        self.rect = pygame.Rect(self.world_pos.x - self.radius, self.world_pos.y - self.radius, self.radius * 2,
                                self.radius * 2)
        self.health: int = 100  # 当前生命值
        self.max_health: int = 100  # 最大生命值
        self.money: int = 0  # 拥有的金币数量
        self.level: int = 1  # 等级
        self.alive: bool = True  # 玩家是否存活
        self.move: bool = False
        self.effects: list = []  # 当前玩家身上的效果列表
        self.attack_power: int = 10  # 攻击力
        self.hit_cooldown: bool = False  # 是否处于受伤冷却状态
        self.hit_cooldown_time: int = 60  # 受伤冷却剩余时间（帧数）
        self.attack_cooldown: int = 60  # 攻击冷却剩余时间（帧数）
        self.speed: int = 3  # 移动速度
        self.tenacity: int = 5  # 减少受到的伤害

        self.rect =  pygame.image.load(BAT_ORIGIN_PATH).convert_alpha().get_rect(center=self.world_pos)# 碰撞矩形
        # 动画相关属性

        self.current_frame = 0  # 当前帧索引
        self.frame_timer = 0  # 帧计时器
        self.frame_delay = 10 # 每帧显示的时间（毫秒）

        # 加载多帧角色图片
        sprite_sheet = pygame.image.load(BAT_MOVE_PATH).convert_alpha()

        self.moves = []
        for i in range(8):
            # 提取每一帧
            move = sprite_sheet.subsurface(pygame.Rect(i * 80,0,80,80))
            self.moves.append(move)

    def update(self):
        """更新蝙蝠的位置和动画"""
        # 更新位置
        self.world_pos.x += self.direct * self.speed

        # 更新碰撞矩形的位置
        self.rect.center = (int(self.world_pos.x), int(self.world_pos.y))

        # 更新动画帧
        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.moves)

    def draw(self,screen: pygame.Surface, world_offset: int):
        """绘制蝙蝠的当前帧"""
        screen_pos = (w_to_s(self.world_pos, world_offset))  # 计算屏幕相对位置
        screen.blit(self.moves[self.current_frame], screen_pos)

    def get_position(self):
        """获取当前位置"""
        return self.world_pos  # 返回世界坐标位置