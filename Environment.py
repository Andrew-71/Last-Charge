import math
import random
from time import time
import pygame
from pygame import mixer
from main import render_sprite

mixer.init()


class Crate(pygame.sprite.Sprite):
    def __init__(self, pos, colour):
        super().__init__()
        self.pos = list(pos)

        self.image = pygame.Surface([8, 8])
        self.image.fill(pygame.Color(colour))

        self.rect = self.image.get_rect(x=self.pos[0], y=self.pos[1])
        self.radius = self.rect.width / 2

        self.sound_effect = mixer.Sound('sounds/pickup.wav')

    def render(self, surface):
        surface.blit(self.image, self.pos)


class AmmoCrate(Crate):
    def __init__(self, pos):
        super().__init__(pos, 'green')

    def behaviour(self, player):
        if pygame.sprite.collide_circle(self, player.sprite):
            if player.sprite.weapon.ammunition < 100:
                player.sprite.weapon.ammunition += 20
                if player.sprite.weapon.ammunition > 100:
                    player.sprite.weapon.ammunition = 100
                self.sound_effect.play()
                self.kill()
                return 'used'


class HealthCrate(Crate):
    def __init__(self, pos):
        super().__init__(pos, 'red')

    def behaviour(self, player):
        if pygame.sprite.collide_circle(self, player.sprite):
            if player.sprite.energy < 2500:
                player.sprite.energy += 150
                if player.sprite.energy > 2500:
                    player.sprite.energy = 2500
                self.sound_effect.play()
                self.kill()
                return 'used'


class Column(pygame.sprite.Sprite):
    def __init__(self, pos, size=[20, 20]):
        super().__init__()
        self.pos = list(pos)

        self.image = pygame.Surface(size)
        self.image.fill(pygame.Color('gray'))

        self.rect = self.image.get_rect(x=self.pos[0], y=self.pos[1])
        self.radius = self.rect.width / 2

    def render(self, surface):
        surface.blit(self.image, self.pos)


class PowerupSpawn(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = list(pos)

        self.image = pygame.Surface([12, 12])
        self.image.fill(pygame.Color('yellow'))

        self.last_activated = int(time())

        self.spawn_pos = [self.pos[0] + 2, self.pos[1] + 2]

        self.crate = random.choice([AmmoCrate(self.spawn_pos), HealthCrate(self.spawn_pos)])

    def behaviour(self, surface, player):
        if int(time()) - self.last_activated > 15 and self.crate is None:
            self.crate = random.choice([AmmoCrate(self.spawn_pos), HealthCrate(self.spawn_pos)])
        elif self.crate is not None:
            render_sprite(player.sprite, self.crate, surface)
            if pygame.sprite.collide_circle(self.crate, player.sprite):
                if self.crate.behaviour(player) == 'used':
                    self.crate = None
                self.last_activated = int(time())
