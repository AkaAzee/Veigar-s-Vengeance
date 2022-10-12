import pygame
import pytmx
import pyscroll


from game import Game

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    tmx_data = pytmx.util_pygame.load_pygame("map/map_2.tmx")
    pygame.display.set_caption("Veigar's Vengeance")
    game = Game(screen, tmx_data)
    running = True
    game.run()
