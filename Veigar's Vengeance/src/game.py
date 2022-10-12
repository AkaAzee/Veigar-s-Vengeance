import pygame
import pyscroll
import pytmx

from player import Player
from player import Boss
from player import Heal
from animation import AnimateSprite
from sound import SoundManager
from attack import AutoPlayer
from attack import AutoBoss


class Game(AnimateSprite):

    def __init__(self):
        super().__init__()
        self.reinit()

    def reinit(self):
        # charger map (tmx)
        self.screen = pygame.display.set_mode((1920, 1080))
        self.tmx_data = pytmx.util_pygame.load_pygame("map/map_2.tmx")
        pygame.display.set_caption("Veigar's Vengeance")

        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3.5

        # generer joueur/boss
        player_position = self.tmx_data.get_object_by_name("player")
        boss_position = self.tmx_data.get_object_by_name("boss")
        self.player = Player(player_position.x, player_position.y)
        self.boss = Boss(boss_position.x, boss_position.y)
        self.reward = self.tmx_data.get_object_by_name("spawn_reward")

        # jeu is playing ?
        self.is_playing = False

        # son
        self.sound_manager = SoundManager()

        # collision/death (lave)
        self.walls = []
        self.lava = []
        self.arena = []
        self.collision_2 = []

        # attaques
        self.ratio_screen_x = 480 / 1920
        self.ratio_screen_y = 272 / 1080
        self.autoplayer = []

        # cooldown
        self.last = pygame.time.get_ticks()
        self.last2 = pygame.time.get_ticks()
        self.last3 = pygame.time.get_ticks()
        self.last4 = pygame.time.get_ticks()
        self.last47 = pygame.time.get_ticks()
        self.last49 = pygame.time.get_ticks()
        self.lava_cooldown = 500
        self.auto_attack_cooldown = 1000
        self.death_cooldown = 5000
        self.running_cooldown = 640
        self.death_time = 0
        self.auto_boss_cooldown = 1500
        self.heal_cooldown = 1000
        self.heal_time = 0
        self.auto_time = 0

        self.t = True
        self.arena_bool = False

        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "lava":
                self.lava.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "arena":
                self.arena.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "collision_2":
                self.collision_2.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessin groupe calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)
        self.group.add(self.player)
        self.group.add(self.boss)

        # bool anime
        self.anime = True

        self.b = True
        self.mvt = False
        self.bool_auto = False
        self.bool_mvt_auto = True
        self.bool_vie = False
        self.death_bool = True
        self.death_bool_2 = False
        self.boss_attack = False
        self.heal_bool = False
        self.auto_boss_bool = False

    def interface(self):
        sysfont = pygame.font.get_default_font()
        font1 = pygame.font.SysFont(sysfont, 40)
        font2 = pygame.font.SysFont(sysfont, 30)
        font3 = pygame.font.SysFont(sysfont, 55)
        player_name = font1.render(f'Veigar', True, (255, 255, 255))
        player_life = font2.render(f'{self.player.target_health}/{self.player.max_health}', True,
                                   (255, 255, 255))
        boss_name = font3.render("Boss très méchant", True, (255, 255, 255))

        pygame.draw.rect(self.screen, (0, 0, 0), (20, 970, 700, 100))
        pygame.draw.rect(self.screen, (255, 255, 255), (20, 970, 700, 101), 3)
        self.player.advanced_health(self.screen)
        self.screen.blit(player_name, (30, 980))
        self.screen.blit(player_life, (30, 1015))
        if self.bool_vie:
            self.boss.advanced_health(self.screen)
            self.screen.blit(boss_name, (750, 10))
        self.opacity = 255

    def handle_input(self):
        if self.death_bool:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_z] and self.bool_mvt_auto:
                if pressed[pygame.K_d]:
                    self.player.move_diag_right_up()
                    self.player.change_animation("right", 10, 5)
                    self.anime = True
                    self.mvt = True
                elif pressed[pygame.K_q]:
                    self.player.move_diag_left_up()
                    self.player.change_animation("left", 10, 5)
                    self.anime = False
                    self.mvt = True
                else:
                    self.player.move_up()
                    if self.anime:
                        self.player.change_animation("right", 10, 5)
                    else:
                        self.player.change_animation("left", 10, 5)
            elif pressed[pygame.K_s] and self.bool_mvt_auto:
                if pressed[pygame.K_d]:
                    self.player.move_diag_right_down()
                    self.player.change_animation("right", 10, 5)
                    self.anime = True
                    self.mvt = True
                elif pressed[pygame.K_q]:
                    self.player.move_diag_left_down()
                    self.player.change_animation("left", 10, 5)
                    self.anime = False
                    self.mvt = True
                else:
                    self.player.move_down()
                    if self.anime:
                        self.player.change_animation("right", 10, 5)
                    else:
                        self.player.change_animation("left", 10, 5)
            elif pressed[pygame.K_d] and self.bool_mvt_auto:
                self.player.change_animation("right", 10, 5)
                self.anime = True
                self.mvt = True
                if pressed[pygame.K_z]:
                    self.player.move_diag_right_up()
                elif pressed[pygame.K_s]:
                    self.player.move_diag_right_down()
                else:
                    self.player.move_right()
            elif pressed[pygame.K_q] and self.bool_mvt_auto:
                self.player.change_animation("left", 10, 5)
                self.anime = False
                self.mvt = True
                if pressed[pygame.K_z]:
                    self.player.move_diag_left_up()
                elif pressed[pygame.K_s]:
                    self.player.move_diag_left_down()
                else:
                    self.player.move_left()
            elif not pressed[pygame.K_z] and not pressed[pygame.K_s] and not pressed[pygame.K_q] and not pressed[
                pygame.K_d] and self.bool_mvt_auto:
                if self.anime:
                    self.player.change_animation("no_mvt_right", 5, 5)
                else:
                    self.player.change_animation("no_mvt_left", 5, 5)
                self.mvt = False
            # test pour le moment
            if pressed[pygame.K_UP]:
                self.player.get_health(20)
            elif pressed[pygame.K_DOWN]:
                self.player.get_damage(20)
            if pressed[pygame.K_SPACE]:
                now = pygame.time.get_ticks()
                if now - self.last4 >= self.auto_attack_cooldown:
                    self.last4 = now
                    if self.anime:
                        auto_attack = AutoPlayer((self.player.position[0] + 24), (self.player.position[1] - 10))
                        self.group.add(auto_attack)
                        auto_attack.change_animation("auto_attack", 8, 5)
                        self.sound_manager.play_sound("auto_attack")
                        self.bool_auto = True
                        self.auto_time = pygame.time.get_ticks()
                    elif not self.anime:
                        auto_attack = AutoPlayer((self.player.position[0]), (self.player.position[1] - 10))
                        self.group.add(auto_attack)
                        auto_attack.change_animation("auto_attack", 8, 5)
                        self.sound_manager.play_sound("auto_attack")
                        self.bool_auto = True
                        self.auto_time = pygame.time.get_ticks()
            now9 = pygame.time.get_ticks()
            if (now9 - self.auto_time) >= 300 and self.bool_auto:
                self.bool_auto = False

    def handle_input_attack(self):
        if self.death_bool:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_z] and self.bool_mvt_auto:
                if pressed[pygame.K_d]:
                    self.player.move_diag_right_up()
                    self.player.change_animation("deplacement_auto_right", 5, 4)
                    self.anime = True
                    self.mvt = True
                elif pressed[pygame.K_q]:
                    self.player.move_diag_left_up()
                    self.player.change_animation("deplacement_auto_left", 5, 4)
                    self.anime = False
                    self.mvt = True
                else:
                    self.player.move_up()
                    if self.anime:
                        self.player.change_animation("deplacement_auto_right", 5, 4)
                    else:
                        self.player.change_animation("deplacement_auto_left", 5, 4)
            elif pressed[pygame.K_s] and self.bool_mvt_auto:
                if pressed[pygame.K_d]:
                    self.player.move_diag_right_down()
                    self.player.change_animation("deplacement_auto_right", 5, 4)
                    self.anime = True
                    self.mvt = True
                elif pressed[pygame.K_q]:
                    self.player.move_diag_left_down()
                    self.player.change_animation("deplacement_auto_left", 5, 4)
                    self.anime = False
                    self.mvt = True
                else:
                    self.player.move_down()
                    if self.anime:
                        self.player.change_animation("deplacement_auto_right", 5, 4)
                    else:
                        self.player.change_animation("left", 10, 5)
            elif pressed[pygame.K_d] and self.bool_mvt_auto:
                self.player.change_animation("deplacement_auto_right", 5, 4)
                self.anime = True
                self.mvt = True
                if pressed[pygame.K_z]:
                    self.player.move_diag_right_up()
                elif pressed[pygame.K_s]:
                    self.player.move_diag_right_down()
                else:
                    self.player.move_right()
            elif pressed[pygame.K_q] and self.bool_mvt_auto:
                self.player.change_animation("deplacement_auto_left", 5, 4)
                self.anime = False
                self.mvt = True
                if pressed[pygame.K_z]:
                    self.player.move_diag_left_up()
                elif pressed[pygame.K_s]:
                    self.player.move_diag_left_down()
                else:
                    self.player.move_left()
            elif not pressed[pygame.K_z] and not pressed[pygame.K_s] and not pressed[pygame.K_q] and not \
            pressed[
                pygame.K_d] and self.bool_mvt_auto:
                if self.anime:
                    self.player.change_animation("surplace_auto_right", 5, 5)
                else:
                    self.player.change_animation("surplace_auto_left", 5, 5)
                self.mvt = False
            if pressed[pygame.K_UP]:
                self.player.get_health(20)
            elif pressed[pygame.K_DOWN]:
                self.player.get_damage(20)
            if pressed[pygame.K_SPACE]:
                now = pygame.time.get_ticks()
                if now - self.last4 >= self.auto_attack_cooldown:
                    self.last4 = now
                    if self.anime:
                        auto_attack = AutoPlayer((self.player.position[0] + 24), (self.player.position[1] - 10))
                        self.group.add(auto_attack)
                        auto_attack.change_animation("auto_attack", 8, 5)
                        self.sound_manager.play_sound("auto_attack")
                        self.bool_auto = True
                        self.auto_time = pygame.time.get_ticks()
                    elif not self.anime:
                        auto_attack = AutoPlayer((self.player.position[0]), (self.player.position[1] - 10))
                        self.group.add(auto_attack)
                        auto_attack.change_animation("auto_attack", 8, 5)
                        self.sound_manager.play_sound("auto_attack")
                        self.bool_auto = True
                        self.auto_time = pygame.time.get_ticks()
            now9 = pygame.time.get_ticks()
            if (now9 - self.auto_time) >= 300 and self.bool_auto:
                self.bool_auto = False

            if pressed[pygame.K_e]:
                now3 = pygame.time.get_ticks()
                if now3 - self.last49 >= self.heal_cooldown:
                    self.last49 = now3
                    self.heal = Heal(self.player.position[0], self.player.position[1])
                    self.group.add(self.heal)
                    self.heal_bool = True
                    self.player.get_health(400)
                    self.heal_time = pygame.time.get_ticks()
                    self.heal.change_animation("heal", 8, 8)
                    self.heal_time = pygame.time.get_ticks()
            now7 = pygame.time.get_ticks()
            if (now7 - self.heal_time) >= 1700 and self.heal_bool:
                self.group.remove(self.heal)
                self.heal_bool = False

    def auto_boss(self):
        if self.auto_boss_bool:
            if self.death_bool:
                if (self.player.position[1] - self.boss.position[1]) < 200:
                    player_x, player_y = self.player.position[0], self.player.position[1]
                    now = pygame.time.get_ticks()
                    if now - self.last2 >= self.auto_boss_cooldown:
                        self.last2 = now
                        auto_boss = AutoBoss((self.boss.position[0]+58), (self.boss.position[1]+80), player_x, player_y)
                        self.group.add(auto_boss)
                        auto_boss.change_animation("auto_attack", 8, 5)
                        self.sound_manager.play_sound("auto_attack")

    def update(self):
        self.group.update()
        # verif collision/death
        self.tmx_data = pytmx.util_pygame.load_pygame("map/map_2.tmx")
        if self.death_bool:
            for sprite in self.group.sprites():
                if sprite.feet.collidelist(self.walls) > -1:
                    sprite.move_back()
                elif sprite.feet.collidelist(self.lava) > -1:
                    now = pygame.time.get_ticks()
                    if now - self.last3 >= self.lava_cooldown:
                        self.last3 = now
                        self.player.get_damage(50)
                elif sprite.feet.collidelist(self.arena) > -1:
                    self.arena_bool = True
            if self.arena_bool and self.b:
                self.sound_manager.change_music("sound/Elden Ring OST - Radagon.mp3", 1)
                self.b = False
                self.bool_vie = True
                self.boss_attack = True
                for obj in self.tmx_data.objects:
                    if obj.type == "collision_2":
                        self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if self.mvt:
                now = pygame.time.get_ticks()
                if now - self.last >= self.running_cooldown:
                    self.last = now
                    # self.sound_manager.play_sound("running")
            if type(sprite) is AutoPlayer:
                if sprite.rect.colliderect(self.boss.rect):
                    self.boss.get_damage(4000)
                    self.group.remove(sprite)
            if type(sprite) is AutoBoss:
                if sprite.rect.colliderect(self.player.rect):
                    self.player.get_damage(100)
                    self.group.remove(sprite)
            if self.heal_bool:
                self.heal.position[0] = (self.player.position[0]-5)
                self.heal.position[1] = (self.player.position[1]-5)
            if self.boss.target_health == 0:
                self.player.position[0] = self.reward.x
                self.player.position[1] = self.reward.y

    def run(self):

        clock = pygame.time.Clock()
        running = True
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1, 0.0)

        while running:

            self.player.save_location()
            if self.bool_auto:
                self.handle_input_attack()
            else:
                self.handle_input()
            self.auto_boss()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            self.interface()
            now = pygame.time.get_ticks()
            if (self.player.position[1] - self.boss.position[1]) <= 200:
                self.auto_boss_bool = True
            else:
                self.auto_boss_bool = False
            if self.player.target_health == 0 and self.death_bool:
                self.death_time = pygame.time.get_ticks()
                self.death_bool = False
                self.death_bool_2 = True
            if (now - self.death_time) >= self.death_cooldown and self.death_bool_2:
                self.reinit()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                clock.tick(60)
            pygame.display.flip()

        pygame.quit()
