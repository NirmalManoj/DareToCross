import pygame
import configme

# This is the class for the moving obstacle sharks
# which comes once the player reaches the third level.


class Shark(pygame.sprite.Sprite):
    speed = 0

    def __init__(self, posx, posy, speed):

        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = pygame.image.load("images/shark.png")
        self.image.set_colorkey(configme.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy

    # Once the sharks cross the screen,
    # put them on the left side of the display again.

    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 1000:
            self.rect.x = -100
