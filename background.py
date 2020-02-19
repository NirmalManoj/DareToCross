import pygame
import configme


# Background class contains details of the
# background image once the round starts
class Background(pygame.sprite.Sprite):
    # (location of the images file, location on screen)
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
