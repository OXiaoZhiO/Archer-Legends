# utils/transform.py
import pygame
from settings import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT


def w_to_s(w_pos,offset):
    return (SCREEN_WIDTH // 2) - (offset - w_pos[0]),w_pos[1]

def s_to_w(s_pos, offset):
    return + offset + s_pos[0]-(SCREEN_WIDTH // 2) , s_pos[1]

def wx_to_sx(wx,offset):
    return (SCREEN_WIDTH // 2) - (offset - wx)

def sx_to_wx(sx, offset):
    return + offset + sx-(SCREEN_WIDTH // 2)

def check(w_pos,offset) ->bool:
    check_x=wx_to_sx(w_pos.x,offset)
    if check_x>SCREEN_WIDTH or  check_x<0:
        return False
    else:
        return True

