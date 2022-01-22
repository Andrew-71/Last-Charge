import pygame
import math
from Weapon import Weapon  # ..I need a weapon...


def normalize_vector(vector):
    if vector == [0, 0]:
        return [0, 0]

    pythagoras = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    return vector[0] / pythagoras, vector[1] / pythagoras


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.faces = (pygame.image.load('textures/faces/happy.png'), pygame.image.load('textures/faces/neutral.png'),
                      pygame.image.load('textures/faces/sad.png'), pygame.image.load('textures/faces/super_happy.png'))
        self.image = pygame.image.load('textures/faces/happy.png')

        self.weapon = Weapon(300, 'Gun', 50, 350)
        self.energy = 2500
        self.hp = 100
        self.pos = list(pos)

        self.velocity = [0, 0]

        self.projectiles = pygame.sprite.Group()
        self.damage_indicators = pygame.sprite.Group()

        self.rect = self.image.get_rect(x=self.pos[0], y=self.pos[1])
        self.radius = self.rect.width / 2

    def move(self, mobs, columns, time_delta):
        if self.energy > 2000:
            if self.energy > 2450 and self.weapon.ammunition > 90:
                self.image = self.faces[3]  # Hehehe
            else:
                self.image = self.faces[0]  # Happy
        elif self.energy > 600:
            self.image = self.faces[1]  # Neutral
        else:
            self.image = self.faces[2]  # Sad

        # We cal velocity at abs(e).
        if self.velocity[0] > 3:
            self.velocity[0] = 3
        if self.velocity[1] > 3:
            self.velocity[1] = 3
        if self.velocity[0] < -3:
            self.velocity[0] = -3
        if self.velocity[1] < -3:
            self.velocity[1] = -3

        self.pos[0] += self.velocity[0] * time_delta * 0.01
        self.rect.topleft = self.pos
        block_hit_list = pygame.sprite.spritecollide(self, columns, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.velocity[0] > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
        self.pos = list(self.rect.topleft)

        self.pos[1] += self.velocity[1] * time_delta * 0.01
        self.rect.topleft = self.pos
        block_hit_list = pygame.sprite.spritecollide(self, columns, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.velocity[1] > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
        self.pos = list(self.rect.topleft)

        # Collision handling with mobs
        move_vector = [0, 0]
        for sprite in mobs:
            if pygame.sprite.collide_circle(self, sprite):
                pass
                #move_vector[0] += self.pos[0] - sprite.pos[0]
                #move_vector[1] += self.pos[1] - sprite.pos[1]

        move_vector = normalize_vector(move_vector)
        self.pos[0] += move_vector[0] * self.velocity[0]
        self.pos[1] += move_vector[1] * self.velocity[1]
        self.rect.topleft = self.pos

    def shoot(self, mouse_pos, surface):
        self.weapon.shoot(self, mouse_pos, surface)

    def render(self, surface):

        surface.blit(self.image, self.pos)