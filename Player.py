import pygame
import math
from Weapon import Weapon  # ..I need a weapon...


def normalize_vector(vector):
    if vector == [0, 0]:
        return [0, 0]

    pythagoras = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    return vector[0] / pythagoras, vector[1] / pythagoras


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([8, 8])
        self.image.fill('black')

        self.weapon = Weapon(300, 'Energy Rifle', 50, 200, 15)
        self.energy = 5000
        self.hp = 100
        self.pos = [5, 5]

        self.velocity = [0, 0]

        self.projectiles = pygame.sprite.Group()
        self.damage_indicators = pygame.sprite.Group()

        self.rect = self.image.get_rect(x=self.pos[0], y=self.pos[1])
        self.radius = self.rect.width / 2

    def move(self, mobs, time_delta):
        if self.velocity[0] > 3:
            self.velocity[0] = 3
        if self.velocity[1] > 3:
            self.velocity[1] = 3
        if self.velocity[0] < -3:
            self.velocity[0] = -3
        if self.velocity[1] < -3:
            self.velocity[1] = -3

        self.pos[0] += self.velocity[0] * time_delta * 0.01
        self.pos[1] += self.velocity[1] * time_delta * 0.01

        if self.pos[0] > 780:
            self.pos[0] -= (self.pos[0] - 780)
        if self.pos[0] < 20:
            self.pos[0] += (20 - self.pos[0])

        if self.pos[1] > 580:
            self.pos[1] -= (self.pos[1] - 580)
        if self.pos[1] < 20:
            self.pos[1] += (20 - self.pos[1])

        # Collision handling with mobs
        move_vector = [0, 0]
        for sprite in mobs:
            if pygame.sprite.collide_circle(self, sprite):
                move_vector[0] += self.pos[0] - sprite.pos[0]
                move_vector[1] += self.pos[1] - sprite.pos[1]

        move_vector = normalize_vector(move_vector)
        self.pos[0] += move_vector[0] * self.velocity[0]
        self.pos[1] += move_vector[1] * self.velocity[1]

        self.rect.topleft = self.pos

    def shoot(self, mouse_pos):
        self.weapon.shoot(self, mouse_pos)

    def render(self, surface):
        surface.blit(self.image, self.pos)