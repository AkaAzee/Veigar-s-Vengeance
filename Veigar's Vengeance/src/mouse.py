import pygame


class Mouse:

    def __init__(self):
        self.ratio = 0.25

    def mouse_position(self, map_player_x, map_player_y):
        screen_player_x = 960
        screen_player_y = 540
        screen_mouse_x, screen_mouse_y = pygame.mouse.get_pos()
        diff_x = screen_mouse_x - screen_player_x
        diff_y = screen_mouse_y - screen_player_y
        map_diff_x = diff_x * self.ratio
        map_diff_y = diff_y * self.ratio
        map_mouse_x = map_player_x + map_diff_x
        map_mouse_y = map_player_y + map_diff_y
        mouse = (map_mouse_x, map_mouse_y)
        return mouse
