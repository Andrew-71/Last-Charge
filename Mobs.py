import pygame
import math
import random


def normalize_vector(vector):
    if vector == [0, 0]:
        return [0, 0]

    pythagoras = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    return vector[0] / pythagoras, vector[1] / pythagoras


class BaseMob(pygame.sprite.Sprite):
    def __init__(self, hp, speed, position):
        super().__init__()
        # TODO: Placeholder
        self.image = pygame.Surface([8, 8])
        self.image.fill(pygame.Color('black'))

        self.hp = hp
        self.speed = speed
        self.pos = list(position)
        self.waypoint = list(position)

        self.rect = self.image.get_rect(x=self.pos[0], y=self.pos[1])
        self.radius = self.rect.width / 2

    def pick_waypoint(self, player):
        new_waypoint = [random.randint(int(self.pos[0]) - 50, int(self.pos[0]) + 50),
                        random.randint(int(self.pos[1]) - 50, int(self.pos[1]) + 50)]

        # TODO: ADJUST FOR VARIABLE WINDOW
        if new_waypoint[0] > 780:
            new_waypoint[0] -= (new_waypoint[0] - 780)
        if new_waypoint[0] < 20:
            new_waypoint[0] += (20 - new_waypoint[0])

        if new_waypoint[1] > 580:
            new_waypoint[1] -= (new_waypoint[1] - 580)
        if new_waypoint[1] < 20:
            new_waypoint[1] += (20 - new_waypoint[1])

        # If player is close enough the mob targets them
        distance_x = player.sprite.pos[0] - self.pos[0]
        distance_y = player.sprite.pos[1] - self.pos[1]
        if math.sqrt(distance_x ** 2 + distance_y ** 2) < 100:
            new_waypoint = [player.sprite.pos[0],
                            player.sprite.pos[1]]

        self.waypoint = new_waypoint

    def move(self, mobs, time_delta, main_player):
        # Create direction vector to waypoint
        # Fancy words, doesn't make me understand it any more
        move_vector = (self.waypoint[0] - self.pos[0],
                       self.waypoint[1] - self.pos[1])
        move_vector = normalize_vector(move_vector)

        # Move
        self.pos[0] += move_vector[0] * self.speed * time_delta
        self.pos[1] += move_vector[1] * self.speed * time_delta

        # Collision handling with other mobs
        move_vector = [0, 0]
        for sprite in mobs:
            if sprite is self:
                continue
            if pygame.sprite.collide_circle(self, sprite):
                move_vector[0] += self.pos[0] - sprite.pos[0]
                move_vector[1] += self.pos[1] - sprite.pos[1]
        move_vector = normalize_vector(move_vector)
        self.pos[0] += move_vector[0]
        self.pos[1] += move_vector[1]

        # Collision test with main player
        move_vector = [0, 0]
        if pygame.sprite.collide_circle(self, main_player.sprite):
            move_vector[0] += self.pos[0] - main_player.sprite.pos[0]
            move_vector[1] += self.pos[1] - main_player.sprite.pos[1]
        move_vector = normalize_vector(move_vector)
        self.pos[0] += move_vector[0] * 2
        self.pos[1] += move_vector[1] * 2

        self.rect.topleft = self.pos

    def attempt_drain_battery(self, player):
        distance_x = player.sprite.pos[0] - self.pos[0]
        distance_y = player.sprite.pos[1] - self.pos[1]

        if math.sqrt(distance_x ** 2 + distance_y ** 2) < 10:
            player.sprite.energy -= 1

    def behaviour(self, mobs, time_delta, main_player):
        # If waypoint is reached get a new one
        distance_x = self.waypoint[0] - self.pos[0]
        distance_y = self.waypoint[1] - self.pos[1]
        distance_p_x = main_player.sprite.pos[0] - self.pos[0]
        distance_p_y = main_player.sprite.pos[1] - self.pos[1]
        if math.sqrt(distance_x ** 2 + distance_y ** 2) < 10 or math.sqrt(distance_p_x ** 2 + distance_p_y ** 2) < 100:
            self.pick_waypoint(main_player)

        # Move and attempt to attack the player
        self.move(mobs, time_delta, main_player)
        self.attempt_drain_battery(main_player)

        # If mob is dead tell that to main system
        if self.hp <= 0:
            self.kill()

    def render(self, surface):
        surface.blit(self.image, self.pos)

