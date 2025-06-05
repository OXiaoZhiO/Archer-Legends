# settings.py
import os
from pygame.math import Vector2

# 资源路径配置

BASE_DIR = os.path.dirname(os.path.abspath(__file__))# 获取项目根目录，并拼接相对路径
BACKGROUND_IMAGE_PATH = os.path.join(BASE_DIR, "pictures", "background.png") # 背景图片路径
FONT_PATH = os.path.join( BASE_DIR, "fonts", "font.ttf")  # 字体文件路径
ARROW_IMAGE_PATH = os.path.join(BASE_DIR, "pictures", "arrow.png") # 箭矢文件路径
PLAYER_IMAGE_PATH = os.path.join(BASE_DIR, "pictures", "player.png")# 玩家文件路径
HOME_IMAGE_PATH=os.path.join(BASE_DIR, "pictures", "home.png")# 大本营文件路径
if True:
    BAT_MOVE_PATH = os.path.join(BASE_DIR, "pictures", "bat","move.png")  # 路径
    BAT_DEATH_PATH = os.path.join(BASE_DIR, "pictures", "bat", "death.png")  # 路径
    BAT_ORIGIN_PATH = os.path.join(BASE_DIR, "pictures", "bat", "origin.png")  # 路径

# 游戏窗口配置
SCREEN_WIDTH= 1024  # 屏幕宽度
SCREEN_HEIGHT= 600  # 屏幕高度
FPS= 60  # 帧率


#世界难度
HARD=1


# 颜色定义
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'gold': (255, 215, 0),
    'yellow': (255, 255, 0),
    'gray': (150,150,150)
}

# 玩家配置
PLAYER_SPEED= 5  # 玩家移动速度
PLAYER_START_POS = Vector2(0, 530)  # 玩家初始位置
WORLD_OFFSET = 0# 绝对世界坐标偏移量，用于背景滚动
HALF_SCREEN=SCREEN_WIDTH//2