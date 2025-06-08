# enemy/bat.py
import random
import pygame
from pygame.math import Vector2
from settings import *
from utils.transform import sx_to_wx, w_to_s
from objects.health_bar import Health_bar

class Bat:

    def __init__(self,hard):
        # 决定蝙蝠从左侧还是右侧进入屏幕
        if random.choice([True, False]):  # 随机选择左侧或右侧
            self.world_pos = Vector2(-2000, random.randint(50, 250))  # 左侧屏幕外，随机高度
            self.direct = 1  # 向右移动
        else:
            self.world_pos = Vector2(2000, random.randint(50, 250))  # 右侧屏幕外，随机高度
            self.direct = -1  # 向左移动

        # 基础属性
        self.attack=False
        self.speed = random.uniform(1.0, 2.0)  # 随机速度，控制蝙蝠的移动快慢
        self.score_value = 5 * hard  # 基础分值，击杀蝙蝠后玩家获得的分数
        self.exp_value = 2 * hard  # 经验值，击杀蝙蝠后玩家获得的经验
        self.radius = 20  # 假设蝙蝠的半径为20像素，用于碰撞检测
        self.max_health = 10 * hard  # 最大生命值，用于限制生命恢复
        self.health_bar= Health_bar("bat", self.max_health)
        self.health = self.max_health  # 当前生命值，初始为最大生命值
        self.level = hard  # 等级，影响蝙蝠的基础属性和掉落奖励
        self.money = self.level * 5  # 拥有的金币数量，击杀后掉落
        self.alive = True  # 是否存活，标记蝙蝠是否被击败
        self.move = False  # 移动状态，暂时未使用
        self.effects = []  # 当前效果列表，存储附加的状态效果（如减速、中毒等）
        self.attack_power = 5 *hard  # 攻击力，蝙蝠对玩家造成的伤害
        self.hit_cooldown = False  # 是否处于受伤冷却状态，防止频繁受伤
        self.attack_cooldown = False  # 是否处于攻击冷却状态
        self.hit_cooldown_time = 60  # 受伤冷却剩余时间（帧数），每帧更新一次
        self.attack_cooldown_time = 60  # 攻击冷却剩余时间（帧数），控制攻击频率
        self.tenacity = 5  # 减少受到的伤害，提升生存能力
        self.time_temp=self.attack_cooldown_time
        self.death_lock = True

        # 碰撞矩形
        self.rect = pygame.image.load(BAT_ORIGIN_PATH).convert_alpha().get_rect(
            center=self.world_pos)  # 加载蝙蝠的原始图片并获取其矩形区域

        # 动画相关属性
        self.current_frame = 0  # 当前帧索引，用于切换动画帧
        self.frame_timer = 0  # 帧计时器，记录当前帧显示的时间
        self.frame_delay = 10  # 每帧显示的时间（毫秒），控制动画播放速度

        # 加载多帧角色图片
        sprite_sheet = pygame.image.load(BAT_MOVE_PATH).convert_alpha()  # 加载蝙蝠的动画精灵图
        self.moves = []  # 存储每一帧的图像
        for i in range(15):  # 假设动画有8帧
            # 提取每一帧
            move = sprite_sheet.subsurface(pygame.Rect(i * 80, 0, 80, 80))  # 每帧大小为80x80像素
            self.moves.append(move)  # 将提取的帧添加到动画列表中

        sprite_sheet = pygame.image.load(BAT_DEATH_PATH).convert_alpha()  # 加载蝙蝠的动画精灵图
        self.deaths = []  # 存储每一帧的图像
        for i in range(8):  # 假设动画有8帧
            # 提取每一帧
            death = sprite_sheet.subsurface(pygame.Rect(i * 80, 0, 80, 80))  # 每帧大小为80x80像素
            self.deaths.append(death)  # 将提取的帧添加到动画列表中

    def update(self):
        """更新蝙蝠的位置和动画"""
        # 更新位置
        self.world_pos.x += self.direct * self.speed
        self.health_bar.update(self.health)

        # 更新碰撞矩形的位置
        self.rect.center = (int(self.world_pos.x), int(self.world_pos.y))
        if 100 > self.world_pos.x > -100:
            self.speed=0
            self.attack=True
        # 更新动画帧
        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.moves)
        if self.current_frame==7 and len(self.moves)==8:
            self.alive = False
        if self.attack_cooldown:
            self.time_temp-=1
            if self.time_temp <= 0:
                self.attack_cooldown=False
                self.time_temp=self.attack_cooldown_time

    def draw(self, screen: pygame.Surface, world_offset: int):
        """绘制蝙蝠的当前帧"""
        # 计算屏幕相对位置
        screen_pos = Vector2(w_to_s(self.world_pos, world_offset))  # 转换为屏幕坐标

        # 获取当前帧图片
        current_image = self.moves[self.current_frame]

        # 调整绘制位置，使图片中心对齐到 screen_pos
        image_rect = current_image.get_rect(center=screen_pos)

        # 绘制图片
        screen.blit(current_image, image_rect.topleft)

    def get_position(self):
        """获取当前位置"""
        return Vector2(self.world_pos.x,self.world_pos.y)  # 返回世界坐标位置

    def check_hit(self, arrow_pos: Vector2) -> bool:
        """
        检测箭是否命中
        :param arrow_pos: 箭矢的当前位置(Vector2)
        :return: 如果命中返回True，否则返回False
        """
        return self.world_pos.distance_to(arrow_pos) <= (self.radius + 15)  # 判断箭与靶子中心的距离是否小于命中范围

    def death(self,screen: pygame.Surface,offset):
        self.death_lock = False
        self.current_frame = 0  # 重置当前帧为死亡动画的第一帧
        self.frame_timer = 0  # 重置帧计时器
        self.moves = self.deaths  # 切换到死亡动画帧
        self.speed = 0
        self.draw(screen,offset)
        self.frame_delay = 5  # 调整死亡动画的播放速度



