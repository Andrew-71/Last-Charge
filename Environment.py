import math

import pygame


class AmmoCrate(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = list(pos)

        self.image = pygame.Surface([8, 8])
        self.image.fill(pygame.Color('green'))

        self.rect = self.image.get_rect(x=self.pos[0], y=self.pos[1])
        self.radius = self.rect.width / 2

    def behaviour(self, player):
        if pygame.sprite.collide_circle(self, player.sprite):
            player.sprite.weapon.ammunition += 20
            self.kill()

    def render(self, surface):
        surface.blit(self.image, self.pos)


class Column(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = list(pos)

        self.image = pygame.Surface([20, 20])
        self.image.fill(pygame.Color('gray'))

        self.rect = self.image.get_rect(x=self.pos[0], y=self.pos[1])
        self.radius = self.rect.width / 2

    def render(self, surface):
        surface.blit(self.image, self.pos)