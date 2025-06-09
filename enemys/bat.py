# enemys/bat.py
import random
import pygame
from pygame.math import Vector2
from settings import *
from utils.transform import sx_to_wx, w_to_s
from objects.health_bar import Health_bar


class Bat:

    def __init__(self, hard):
        # 初始化蝙蝠的进入方向和位置
        if random.choice([True, False]):  # 随机选择左侧或右侧进入屏幕
            self.world_pos = Vector2(-2000, random.randint(50, 250))  # 左侧屏幕外，随机高度
            self.direct = 1  # 向右移动
        else:
            self.world_pos = Vector2(2000, random.randint(50, 250))  # 右侧屏幕外，随机高度
            self.direct = -1  # 向左移动

        # 基础属性初始化
        self.attack = False
        self.speed = random.uniform(0.5, 2.0) + (HARD / 3)  # 随机速度，控制蝙蝠的移动快慢
        if self.speed > 5:
            self.speed = 5 - random.uniform(1, 2.0)
        self.score_value = 5 * hard + random.randint(1, HARD + 1)  # 击杀蝙蝠后玩家获得的基础分值
        self.exp_value = 2 * hard + random.randint(1, HARD + 1)  # 击杀蝙蝠后玩家获得的经验值
        self.radius = 20  # 假设蝙蝠的半径为20像素，用于碰撞检测
        self.max_health = 10 * hard  # 最大生命值
        self.health_bar = Health_bar("bat", self.max_health)  # 生命条对象
        self.health = self.max_health  # 当前生命值，初始为最大生命值
        self.level = hard  # 等级，影响蝙蝠的基础属性和掉落奖励
        self.money = self.level * 5 + random.randint(0, 10)  # 拥有的金币数量，击杀后掉落
        self.alive = True  # 是否存活，标记蝙蝠是否被击败
        self.move = False  # 移动状态，暂时未使用
        self.effects = []  # 当前效果列表，存储附加的状态效果（如减速、中毒等）
        self.attack_power = 5 * hard + random.randint(0, 2 * HARD)# 攻击力，蝙蝠对玩家造成的伤害
        self.hit_cooldown = False  # 是否处于受伤冷却状态，防止频繁受伤
        self.attack_cooldown = False  # 是否处于攻击冷却状态
        self.hit_cooldown_time = 60  # 受伤冷却剩余时间（帧数），每帧更新一次
        self.attack_cooldown_time = 60  # 攻击冷却剩余时间（帧数），控制攻击频率
        self.tenacity = 5  # 减少受到的伤害，提升生存能力
        self.time_temp = self.attack_cooldown_time
        self.death_lock = True

        # 碰撞矩形初始化
        self.rect = pygame.image.load(BAT_ORIGIN_PATH).convert_alpha().get_rect(center=self.world_pos)

        # 动画相关属性初始化
        self.current_frame = 0  # 当前帧索引，用于切换动画帧
        self.frame_timer = 0  # 帧计时器，记录当前帧显示的时间
        self.frame_delay = 10  # 每帧显示的时间（毫秒），控制动画播放速度
        self.moves = []  # 存储蝙蝠移动动画的每一帧图像
        self.deaths = []  # 存储蝙蝠死亡动画的每一帧图像

        # 加载蝙蝠的移动动画帧
        sprite_sheet = pygame.image.load(BAT_MOVE_PATH).convert_alpha()
        for i in range(15):  # 假设动画有15帧
            move = sprite_sheet.subsurface(pygame.Rect(i * 80, 0, 80, 80))  # 每帧大小为80x80像素
            self.moves.append(move)

        # 加载蝙蝠的死亡动画帧
        sprite_sheet = pygame.image.load(BAT_DEATH_PATH).convert_alpha()
        for i in range(8):  # 假设动画有8帧
            death = sprite_sheet.subsurface(pygame.Rect(i * 80, 0, 80, 80))  # 每帧大小为80x80像素
            self.deaths.append(death)

    def update(self):
        """更新蝙蝠的位置、动画和状态"""
        # 更新蝙蝠的位置
        self.world_pos.x += self.direct * self.speed
        self.health_bar.update(self.health)  # 更新生命条

        # 更新碰撞矩形的位置
        self.rect.center = (int(self.world_pos.x), int(self.world_pos.y))

        # 检测是否进入攻击范围
        if -100 < self.world_pos.x < 100:
            self.speed = 0
            self.attack = True

        # 更新动画帧
        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.moves)

        # 检测死亡条件
        if self.current_frame == 7 and len(self.moves) == 8:
            self.alive = False

        # 更新攻击冷却时间
        if self.attack_cooldown:
            self.time_temp -= 1
            if self.time_temp <= 0:
                self.attack_cooldown = False
                self.time_temp = self.attack_cooldown_time

    def draw(self, screen: pygame.Surface, world_offset: int):
        """绘制蝙蝠的当前帧"""
        screen_pos = Vector2(w_to_s(self.world_pos, world_offset))  # 转换为屏幕坐标
        current_image = self.moves[self.current_frame]  # 获取当前帧图片
        image_rect = current_image.get_rect(center=screen_pos)  # 调整绘制位置
        screen.blit(current_image, image_rect.topleft)  # 绘制图片

    def get_position(self):
        """获取蝙蝠的当前位置"""
        return Vector2(self.world_pos.x, self.world_pos.y)

    def check_hit(self, arrow_pos: Vector2) -> bool:
        """
        检测箭是否命中
        :param arrow_pos: 箭矢的当前位置(Vector2)
        :return: 如果命中返回True，否则返回False
        """
        return self.world_pos.distance_to(arrow_pos) <= (self.radius + 15)  # 判断箭与靶子中心的距离是否小于命中范围

    def death(self, screen: pygame.Surface, offset):
        """处理蝙蝠的死亡动画"""
        self.death_lock = False
        self.current_frame = 0  # 重置当前帧为死亡动画的第一帧
        self.frame_timer = 0  # 重置帧计时器
        self.moves = self.deaths  # 切换到死亡动画帧
        self.speed = 0  # 停止移动
        self.draw(screen, offset)  # 绘制死亡动画
        self.frame_delay = 5  # 调整死亡动画的播放速度
