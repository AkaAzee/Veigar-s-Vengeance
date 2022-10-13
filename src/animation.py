import pygame

from sound import SoundManager


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.sprite_sheet_deplacement = pygame.image.load("sprites/deplacement.png")
        self.sprite_sheet_surplace = pygame.image.load("sprites/surplace.png")
        self.sprite_auto_attack = pygame.image.load("sprites/auto_attack.png")
        self.sprite_sheet_surplace_auto = pygame.image.load("sprites/auto_surplace.png")
        self.sprite_boss = pygame.image.load("sprites/boss.png")
        self.sprite_sheet_mvt_auto = pygame.image.load("sprites/deplacement_attack.png")
        self.animation_index = 0
        self.clock = 0
        self.images = {
            "right": self.get_images(0, self.sprite_sheet_deplacement, 33, 37, 4),
            "left": self.get_images(37, self.sprite_sheet_deplacement, 33, 37, 4),
            "no_mvt_right": self.get_images(0, self.sprite_sheet_surplace, 34, 37, 4),
            "no_mvt_left": self.get_images(37, self.sprite_sheet_surplace, 34, 37, 4),
            "auto_attack": self.get_images(0, self.sprite_auto_attack, 11, 11, 4),
            "surplace_auto_right": self.get_images(0, self.sprite_sheet_surplace_auto, 33, 37, 4),
            "surplace_auto_left": self.get_images(37, self.sprite_sheet_surplace_auto, 33, 37, 4),
            "boss": self.get_images(0, self.sprite_boss, 128, 153, 1),
            "deplacement_auto_right": self.get_images(0, self.sprite_sheet_mvt_auto, 33, 39, 4),
            "deplacement_auto_left": self.get_images(39, self.sprite_sheet_mvt_auto, 33, 39, 4)
        }
        self.speed = 3

    def get_images(self, y, name, d, d2, g):
        images = []

        for i in range(0, g):
            x = i * d
            image = self.get_image(x, y, name, d, d2)
            images.append(image)

        return images

    def change_animation(self, name, time, index):
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey((0, 0, 0))
        self.clock += self.speed * time

        if self.clock >= 100:

            self.animation_index += 1

            if self.animation_index >= (index - 1):
                self.animation_index = 0

            self.clock = 0

    def get_image(self, x, y, name, d1, d2):
        image = pygame.Surface([d1, d2])
        image.blit(name, (0, 0), (x, y, d1, d2))
        return image

    def blit_alpha(self, target, source, location, opacity):
        x, y = location[0], location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)


class you_died:

    def __init__(self, x, y):
        self.position = x, y
        self.image = pygame.image.load("image/you_died.png")
        self.ds_you_died = pygame.transform.scale(self.image, (1920, 270))
