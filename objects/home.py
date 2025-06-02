# objects/home.py
import pygame
from pygame import Vector2
from settings import *
from utils.transform import *
from objects.health_bar import Health_bar

class Home:

    def __init__(self):
        self.world_pos=Vector2(0, 530)
        self.image = pygame.transform.scale(pygame.image.load(HOME_IMAGE_PATH).convert_alpha(), (350, 350))
        self.max_health = 500  # 最大生命值，用于限制生命恢复
        self.health_bar = Health_bar("home", self.max_health)
        self.health = self.max_health  # 当前生命值，初始为最大生命值
        self.rect = self.image.get_rect(center=self.world_pos)  # 加载原始图片并获取其矩形区域

    def update(self):
        self.health_bar.update(self.health)

    def draw(self,screen: pygame.Surface, world_offset: int):

        screen_pos = (w_to_s((self.world_pos.x-175,self.world_pos.y-300), world_offset))  # 计算屏幕相对位置
        screen.blit(self.image,screen_pos)
