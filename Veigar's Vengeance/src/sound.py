import pygame


class SoundManager:

    def __init__(self):
        self.sound = {
            "music": pygame.mixer.music.load("sound/minecraft-lava-ambience-sound.mp3"),
            "damage": pygame.mixer.Sound("sound/minecraft_hit.mp3"),
            "running": pygame.mixer.Sound("sound/running.mp3"),
            "auto_attack":pygame.mixer.Sound("sound/auto_attack.mp3")
        }

    def play_sound(self, name):
        """

        :rtype: object
        """
        self.sound[name].play()

    def change_music(self, name, volume):
        pygame.mixer.music.unload()
        pygame.mixer.music.load(name)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1, 0.0)

