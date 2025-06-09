# objects/player.py
import random

import pygame
from pygame import Vector2
from settings import *
from utils.transform import w_to_s



class Player:
    current_frame = 0  # 当前帧索引
    frame_timer = 0  # 帧计时器
    frame_delay = 100  # 每帧显示的时间（毫秒）
    def __init__(self):
        # Player attributes
        self.arrow_up =3
        self.to_home = 0
        self.to_home_max = 180
        self.health: int = 30  # 玩家当前生命值
        self.health_up=2
        self.max_health: int = self.health  # 玩家最大生命值
        self.money: int = 100  # 玩家拥有的金币数量
        self.exp:int=0
        self.level: int = 1  # 玩家的经验等级
        self.alive: bool = True  # 玩家是否存活
        self.death_time=0
        self.move: bool = False
        self.direct:int=0
        self.effects: list = []  # 当前玩家身上的效果列表
        self.attack_power: int = 10  # 玩家的攻击力
        self.world_pos: Vector2 = Vector2(PLAYER_START_POS)  # 玩家在世界中的位置
        self.hit_cooldown: bool = False  # 是否处于受伤冷却状态
        self.hit_cooldown_time: int = 60  # 受伤冷却剩余时间（帧数）
        self.attack_cooldown: int = 60  # 攻击冷却剩余时间（帧数）
        self.charging:bool=False # 玩家是否正在蓄力
        self.skills: dict = {}  # 玩家技能字典
        self.respawn_penalty: int = 300  # 玩家复活时的惩罚值
        self.speed: int = 3  # 玩家移动速度
        self.tenacity: int = 0  # 玩家韧性，减少受到的伤害
        self.arrow_count: int = 50  # 玩家拥有的箭矢数量
        self.current_frame = 0  # 当前帧索引
        self.frame_timer = 0  # 帧计时器
        self.frame_delay = 30  # 每帧显示的时间（毫秒）
        self.temp_speed=0
        self.health_up_cd=120
        self.health_up_cd_time=0
        self.arrow_up_cd = 180
        self.arrow_up_cd_time = 0
        self.level_choice = []
        for i in range(5):
            self.level_choice.append("max_health_up")
        for i in range(3):
            self.level_choice.append("attack_up")
        for i in range(2):
            self.level_choice.append("speed_up")


        # 加载多帧角色图片
        sprite_sheet = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()

        # 定义帧的大小（假设每帧宽 64 像素，高 64 像素）
        frame_width = 64
        frame_height = 64

        # 切割图片为单个帧
        self.statics = []
        for i in range(5):
            # 提取每一帧
            static = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            self.statics.append(static)

        self.chargings= []
        for i in range(8):
            # 提取每一帧
            charging = sprite_sheet.subsurface(pygame.Rect(i * frame_width,64, frame_width, frame_height))
            self.chargings.append(charging)

        self.moves = []
        for i in range(8):
            # 提取每一帧
            move = sprite_sheet.subsurface(pygame.Rect(i * frame_width,128, frame_width, frame_height))
            self.moves.append(move)




    def go(self,direct:int=0):
        if direct == -1:
            self.direct=-1
            self.world_pos.x -= self.speed
        elif direct ==1:
            self.direct = 1
            self.world_pos.x += self.speed

    def update(self):
        if self.health<=0:
            if self.alive:
                self.alive=False
            self.death_time+=1
            if self.death_time>=self.respawn_penalty:
                self.alive=True
                self.health=self.max_health
                self.death_time=0
                self.to_home_max+=20
                self.to_home =  self.to_home_max

        elif self.exp>=self.level*10+100:
            self.level+=1
            self.exp=0
            self.arrow_count +=self.level*2
            self.money += 100
            if random.choice(self.level_choice)=="max_health_up":
                self.max_health += 10
            if random.choice(self.level_choice)=="attack_up":
                self.attack_power += 5
            if random.choice(self.level_choice)=="speed_up":
                self.speed += 0.5




        self.health_up_cd_time+=1
        if self.health<self.max_health and self.health_up_cd_time >= self.health_up_cd:
            self.health += self.health_up
            self.health_up_cd_time =0

        self.arrow_up_cd_time += 1
        if self.arrow_up_cd_time >= self.arrow_up_cd:
            self.arrow_count += 1
            self.arrow_up_cd_time = 0




        if self.health>self.max_health:
            self.health = self.max_health






    def draw(self, surface: pygame.Surface, world_offset: int):
        if self.alive:
            screen_pos = (w_to_s(self.world_pos, world_offset))  # 计算屏幕相对位置
            try:
                # 更新帧计时器
                self.frame_timer += 1

                # 绘制当前帧
                if self.charging:

                    self.frame_delay = 10  # 每帧显示的时间（毫秒）
                    if self.frame_timer >= self.frame_delay:
                        self.frame_timer = 0

                        if self.current_frame < 7:
                            self.current_frame = (self.current_frame + 1)
                        else:
                            self.current_frame = 7

                    surface.blit(self.chargings[self.current_frame], (screen_pos[0]-24, screen_pos[1]-64))
                elif self.move:
                    # 当蓄力结束时，重置帧计数
                    if self.current_frame >= 5:
                        self.current_frame = 0

                    self.frame_delay = 5  # 每帧显示的时间（毫秒）
                    if self.frame_timer >= self.frame_delay:
                        self.frame_timer = 0
                        self.current_frame = (self.current_frame + 1) % len(self.moves)  # 循环播放动画

                    # 水平翻转图像
                    if self.direct==-1:
                        flipped_image = pygame.transform.flip(self.moves[self.current_frame], True, False)
                        surface.blit(flipped_image, (screen_pos[0] - 35, screen_pos[1] - 64))
                    else:
                        surface.blit(self.moves[self.current_frame], (screen_pos[0] - 24, screen_pos[1] - 64))
                else:

                # 当蓄力结束时，重置帧计数
                        if self.current_frame>=5:
                            self.current_frame = 0

                        self.frame_delay = 20  # 每帧显示的时间（毫秒）
                        if self.frame_timer >= self.frame_delay:
                            self.frame_timer = 0
                            self.current_frame = (self.current_frame + 1) % len(self.statics)  # 循环播放动画
                        surface.blit(self.statics[self.current_frame], (screen_pos[0]-24, screen_pos[1]-64))

            except pygame.error as e:
                # 绘制玩家
                pygame.draw.circle(surface, COLORS['blue'], screen_pos, 8)

    def take_damage(self, damage: int):
        # 如果不在受伤冷却中，则根据伤害值扣除生命值，并触发冷却
        if not self.hit_cooldown:
            self.health -= max(0, damage - self.tenacity)
            self.hit_cooldown = True
            self.hit_cooldown_time = 60  # 冷却时间为60帧



    def attack(self, target: Vector2):
        if self.alive:
            """触发射击行为，如果箭矢大于零且不在冷却中，则执行攻击动作并重置冷却时间"""
            if self.is_attack_ready():
                self.perform_attack(target)
                self.reset_attack_cooldown()
                self.decrease_arrow_count()

    def is_attack_ready(self) -> bool:
        """检查攻击是否准备好（冷却时间结束）"""
        return self.attack_cooldown <= 0

    def perform_attack(self, target: Vector2):
        """执行攻击动作，例如生成箭矢"""
        print(f"Attacking target at {target}")

    def decrease_arrow_count(self):
        """减少箭矢数量"""
        if self.arrows > 0:
            self.arrows -= 1
            print(f"Arrows left: {self.arrows}")
        else:
            print("No arrows left!")

    def get_position(self) -> Vector2:
        return self.world_pos