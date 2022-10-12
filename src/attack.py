import pygame
import math

from animation import AnimateSprite
from mouse import Mouse


class AutoPlayer(AnimateSprite, Mouse):

    def __init__(self, player_x, player_y):
        super().__init__()
        self.image = self.get_image(0, 0, self.sprite_auto_attack, 11, 11)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [player_x, player_y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.ratio = 0.25
        self.speed = 7
        map_mouse_x, map_mouse_y = self.mouse_position(player_x, player_y)
        self.dir = (map_mouse_x - player_x, map_mouse_y - player_y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)

    def update(self):
        self.rect.topleft = self.position
        self.position = (self.position[0] + self.dir[0] * self.speed,
                         self.position[1] + self.dir[1] * self.speed)
        self.change_animation("auto_attack", 8, 5)


class AutoBoss(AnimateSprite):

    def __init__(self, boss_x, boss_y, player_x, player_y):
        super().__init__()
        self.image = self.get_image(0, 0, self.sprite_auto_attack, 11, 11)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [boss_x, boss_y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.ratio = 0.25
        self.speed = 7
        self.dir = (player_x - boss_x, player_y - boss_y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)

    def update(self):
        self.rect.topleft = self.position
        self.position = (self.position[0] + self.dir[0] * self.speed,
                         self.position[1] + self.dir[1] * self.speed)
        self.change_animation("auto_attack", 8, 5)

    def zob(self):
        print("caca")