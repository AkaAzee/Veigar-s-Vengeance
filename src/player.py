import pygame
import math

from animation import AnimateSprite
from sound import SoundManager


class Player(AnimateSprite, SoundManager):

    def __init__(self, x, y):
        super().__init__()
        self.image = self.get_image(0, 0, self.sprite_sheet_surplace, 33, 37)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.diagspeed = 2
        self.attack = 10
        self.current_health = 800
        self.target_health = 800
        self.max_health = 800
        self.health_bar_length = 680
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 5
        self.sound_manager = SoundManager()

    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health <= 0:
            self.target_health = 0
        self.sound_manager.play_sound("damage")

    def get_health(self, amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health >= self.max_health:
            self.target_health = self.max_health

    def basic_health(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (20, 20, self.target_health / self.health_ratio, 25))
        pygame.draw.rect(surface, (255, 255, 255), (20, 20, self.health_bar_length, 25), 4)

    def advanced_health(self, surface):
        transition_width = 0
        transition_color = (191, 10, 27)
        health_bar_width = int(self.current_health / self.health_ratio)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (160, 160, 0)
            health_bar_width = int(self.current_health / self.health_ratio)

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.current_health - self.target_health) / self.health_ratio)
            transition_color = (209, 161, 2)
            health_bar_width = int(self.target_health / self.health_ratio)

        health_bar = pygame.Rect(30, 1041, health_bar_width, 20)
        transition_bar = pygame.Rect(health_bar.right, 1041, transition_width, 20)

        pygame.draw.rect(surface, (191, 10, 27), health_bar)
        pygame.draw.rect(surface, transition_color, transition_bar)
        pygame.draw.rect(surface, (255, 255, 255), (30, 1041, self.health_bar_length, 20), 3)

    def save_location(self):
        self.old_position = self.position.copy()

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] += self.speed

    def move_diag_right_up(self):
        self.position[0] += self.diagspeed
        self.position[1] -= self.diagspeed

    def move_diag_left_up(self):
        self.position[0] -= self.diagspeed
        self.position[1] -= self.diagspeed

    def move_diag_right_down(self):
        self.position[1] += self.diagspeed
        self.position[0] += self.diagspeed

    def move_diag_left_down(self):
        self.position[1] += self.diagspeed
        self.position[0] -= self.diagspeed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


class Boss(AnimateSprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = self.get_image(0, 0, self.sprite_boss, 128, 153)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.position = [x, y]
        self.current_health = 10000
        self.target_health = 10000
        self.max_health = 10000
        self.health_bar_length = 1400
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 20
        self.sound_manager = SoundManager()
        self.hit_auto_cd = 300
        self.last96 = pygame.time.get_ticks()

    def update(self):
        self.rect.topleft = self.position

    def get_damage(self, amount):
        now = pygame.time.get_ticks()
        if now - self.last96 >= self.hit_auto_cd:
            self.last96 = now
            if self.target_health > 0:
                self.target_health -= amount
            if self.target_health <= 0:
                self.target_health = 0
            self.sound_manager.play_sound("damage")

    def get_health(self, amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health >= self.max_health:
            self.target_health = self.max_health

    def basic_health(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (20, 20, self.target_health / self.health_ratio, 25))
        pygame.draw.rect(surface, (255, 255, 255), (20, 20, self.health_bar_length, 25), 4)

    def advanced_health(self, surface):
        transition_width = 0
        transition_color = (191, 10, 27)
        health_bar_width = int(self.current_health / self.health_ratio)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (160, 160, 0)
            health_bar_width = int(self.current_health / self.health_ratio)

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.current_health - self.target_health) / self.health_ratio)
            transition_color = (209, 161, 2)
            health_bar_width = int(self.target_health / self.health_ratio)

        health_bar = pygame.Rect(240, 60, health_bar_width, 15)
        transition_bar = pygame.Rect(health_bar.right, 60, transition_width, 15)

        pygame.draw.rect(surface, (191, 10, 27), health_bar)
        pygame.draw.rect(surface, transition_color, transition_bar)
        pygame.draw.rect(surface, (255, 255, 255), (240, 60, self.health_bar_length, 15), 2)


class Heal(AnimateSprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = self.get_image(0, 0, self.sprite_sheet_surplace, 33, 37)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.change_animation("heal", 8, 8)
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.value = 400
        self.cooldown = 20000

    def update(self):
        self.rect.topleft = self.position
        self.change_animation("heal", 8, 10)
