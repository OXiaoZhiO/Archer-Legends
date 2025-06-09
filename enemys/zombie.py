# enemys/zombie.py
import random
import pygame
from pygame.math import Vector2

# 导入项目配置和工具函数
from settings import *
from utils.transform import sx_to_wx, w_to_s

# 导入资源路径和自定义模块
from settings import ZOMBIE_IMAGE_PATH
from objects.health_bar import Health_bar

class Zombie:
    def __init__(self, hard):
        # 初始化位置和方向
        if random.choice([True, False]):  # 随机选择左侧或右侧
            self.world_pos = Vector2(-2000, 490)  # 左侧屏幕外，随机高度
            self.direct = 1  # 向右移动
        else:
            self.world_pos = Vector2(2000, 490)  # 右侧屏幕外，随机高度
            self.direct = -1  # 向左移动

        # 基础属性
        self.speed = random.uniform(1, 3) + (HARD / 3)  # 随机速度，控制僵尸的移动快慢
        if self.speed > 5:
            self.speed = 5 - random.uniform(1, 2.0)
        self.score_value = 10 * hard + random.randint(1, HARD + 1)  # 基础分值，击杀僵尸后玩家获得的分数
        self.exp_value = 5 * hard + random.randint(1, HARD + 1)  # 经验值，击杀僵尸后玩家获得的经验
        self.radius = 20  # 假设僵尸的半径为20像素，用于碰撞检测
        self.max_health = 15 * hard  # 最大生命值，用于限制生命恢复
        self.health_bar = Health_bar("bat", self.max_health)
        self.health = self.max_health  # 当前生命值，初始为最大生命值
        self.level = hard  # 等级，影响僵尸的基础属性和掉落奖励
        self.money = self.level * 10 + random.randint(0, 10)  # 拥有的金币数量，击杀后掉落
        self.alive = True  # 是否存活，标记僵尸是否被击败
        self.move = False  # 移动状态，暂时未使用
        self.effects = []  # 当前效果列表，存储附加的状态效果（如减速、中毒等）
        self.attack_power = 5 * hard + random.randint(0, 2 * HARD) # 攻击力，僵尸对玩家造成的伤害
        self.hit_cooldown = False  # 是否处于受伤冷却状态，防止频繁受伤
        self.attack_cooldown = False  # 是否处于攻击冷却状态
        self.hit_cooldown_time = 60  # 受伤冷却剩余时间（帧数），每帧更新一次
        self.attack_cooldown_time = 60  # 攻击冷却剩余时间（帧数），控制攻击频率
        self.tenacity = 5  # 减少受到的伤害，提升生存能力
        self.time_temp = self.attack_cooldown_time
        self.speed_temp = 0
        self.atk = "None"
        self.death_lock = True
        self.attack = False

        # 碰撞矩形
        self.rect = pygame.image.load(BAT_ORIGIN_PATH).convert_alpha().get_rect(center=self.world_pos)

        # 动画相关属性
        self.current_frame = 0  # 当前帧索引，用于切换动画帧
        self.frame_timer = 0  # 帧计时器，记录当前帧显示的时间
        self.frame_delay = 10  # 每帧显示的时间（毫秒），控制动画播放速度

        # 加载多帧角色图片
        sprite_sheet = pygame.image.load(ZOMBIE_IMAGE_PATH).convert_alpha()
        self.moves = []
        self.deaths = []
        self.attacks = []

        # 加载移动动画
        for i in range(8):
            move = sprite_sheet.subsurface(pygame.Rect(i * 48, 48, 48, 48))
            move = pygame.transform.scale(move, (90, 90))
            self.moves.append(move)

        # 加载死亡动画
        for i in range(3):
            death_image = sprite_sheet.subsurface(pygame.Rect(i * 48, 48 * 3, 48, 48))
            death_image = pygame.transform.scale(death_image, (90, 90))
            self.deaths.append(death_image)

        # 加载攻击动画
        for i in range(3):
            attack_image = sprite_sheet.subsurface(pygame.Rect(i * 48, 48 * 4, 48, 48))
            attack_image = pygame.transform.scale(attack_image, (90, 90))
            self.attacks.append(attack_image)

    def update(self, player_pos: Vector2):
        """更新僵尸的位置和动画"""
        # 更新位置
        self.world_pos.x += self.direct * self.speed
        self.health_bar.update(self.health)

        # 更新碰撞矩形的位置
        self.rect.center = (int(self.world_pos.x), int(self.world_pos.y))

        # 检查是否接近玩家或基地
        if 100 > self.world_pos.x > -100:
            self.speed = 0
            self.attack = True
            self.atk = "home"
        if self.world_pos.distance_to(player_pos) <= (self.radius + 30) and self.speed_temp == 0:
            self.speed_temp = self.speed
            self.speed = 0
            self.attack = True
            self.atk = "player"
        elif self.world_pos.distance_to(player_pos) > (self.radius + 30) and self.speed_temp != 0:
            self.speed = self.speed_temp
            self.speed_temp = 0
            self.attack = False
            self.atk = "None"

        # 更新动画帧
        if self.atk == "None" or len(self.moves) == 3:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.moves)
            if self.current_frame == 2 and len(self.moves) == 3:
                self.alive = False
        else:
            if self.current_frame > 2:
                self.current_frame = 0
            self.frame_timer += 1
            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.attacks)
            if self.current_frame == 2 and len(self.moves) == 3:
                self.alive = False

        # 更新攻击冷却时间
        if self.attack_cooldown:
            self.time_temp -= 1
            if self.time_temp <= 0:
                self.attack_cooldown = False
                self.time_temp = self.attack_cooldown_time

    def draw(self, screen: pygame.Surface, world_offset: int):
        """绘制僵尸的当前帧"""
        screen_pos = Vector2(w_to_s(self.world_pos, world_offset))  # 转换为屏幕坐标

        # 获取当前帧图片
        if self.atk == "None":
            current_image = self.moves[self.current_frame]
        else:
            current_image = self.attacks[self.current_frame]

        # 调整绘制位置，使图片中心对齐到 screen_pos
        image_rect = current_image.get_rect(center=screen_pos)

        # 根据方向翻转图片
        if self.direct == -1:
            if self.atk == "None":
                flipped_image = pygame.transform.flip(self.moves[self.current_frame], True, False)
                screen.blit(flipped_image, image_rect.topleft)
            elif self.atk == "player" or self.atk == "home":
                flipped_image = pygame.transform.flip(self.attacks[self.current_frame], True, False)
                screen.blit(flipped_image, image_rect.topleft)
        else:
            if self.atk == "None":
                screen.blit(current_image, image_rect.topleft)
            elif self.atk == "player" or self.atk == "home":
                screen.blit(current_image, image_rect.topleft)

    def get_position(self):
        """获取当前位置"""
        return Vector2(self.world_pos.x, self.world_pos.y)

    def check_hit(self, arrow_pos: Vector2) -> bool:
        """检查是否被箭命中"""
        return self.world_pos.distance_to(arrow_pos) <= (self.radius + 15)

    def death(self, screen: pygame.Surface, offset):
        """处理死亡逻辑"""
        self.death_lock = False
        self.current_frame = 0  # 重置当前帧为死亡动画的第一帧
        self.frame_timer = 0  # 重置帧计时器
        self.moves = self.deaths  # 切换到死亡动画帧
        self.speed = 0
        self.draw(screen, offset)
        self.frame_delay = 5  # 调整死亡动画的播放速度