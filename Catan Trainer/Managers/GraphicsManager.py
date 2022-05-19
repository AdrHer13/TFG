import pathlib as pl

import pygame

class GraphicsManager:
    image = ''
    background = ''
    size = 877, 717
    screen = pygame.display.set_mode(size)

    def __init__(self):
        # pygame.init()
        self.screen_size(self.size)
        self.import_background()

    def import_background(self):
        path = pl.Path("startingmap.png")
        self.image = pygame.image.load(path.absolute())

        self.screen.fill([255, 255, 255])
        self.background = pygame.Surface(self.image.get_rect().size)
        self.background.blit(self.image, self.size)
        self.background.convert()
        self.flip()

    def screen_size(self, size):
        pygame.display.set_mode(size)
        self.screen.fill([255, 255, 255])

    def flip(self):
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        pygame.display.update()