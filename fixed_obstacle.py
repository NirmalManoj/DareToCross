import pygame
import configme

# This is the class for the fixed obstacles


class Fixed(pygame.sprite.Sprite):

    def __init__(self, posx, posy):

        pygame.sprite.Sprite.__init__(self)
        # Loading image for the fixed obstacle
        self.image = pygame.image.load("images/nails.png").convert()
        # self.image.set_colorkey(configme.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
