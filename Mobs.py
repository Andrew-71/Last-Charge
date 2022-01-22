import pygame
import math
import random
from HUD import Indicator
from Environment import AmmoCrate


def normalize_vector(vector):
    if vector == [0, 0]:
        return [0, 0]

    pythagoras = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    return vector[0] / pythagoras, vector[1] / pythagoras


class BaseMob(pygame.sprite.Sprite):
    def __init__(self, hp, speed, position):
        super().__init__()
        # TODO: Placeholder
        self.image = pygame.Surface([16, 16])
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
        if new_waypoint[0] > 550:
            new_waypoint[0] -= (new_waypoint[0] - 550)
        if new_waypoint[0] < 145:
            new_waypoint[0] += (145 - new_waypoint[0])

        if new_waypoint[1] > 550:
            new_waypoint[1] -= (new_waypoint[1] - 550)
        if new_waypoint[1] < 145:
            new_waypoint[1] += (145 - new_waypoint[1])

        # If player is close enough the mob targets them
        distance_x = player.sprite.pos[0] - self.pos[0]
        distance_y = player.sprite.pos[1] - self.pos[1]
        if math.sqrt(distance_x ** 2 + distance_y ** 2) < 210:
            new_waypoint = [player.sprite.pos[0],
                            player.sprite.pos[1]]

        self.waypoint = new_waypoint

    def move(self, mobs, columns, time_delta, main_player):
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

        for sprite in columns:
            if pygame.sprite.collide_rect(self, sprite):
                move_vector[0] += self.pos[0] - sprite.pos[0]
                move_vector[1] += self.pos[1] - sprite.pos[1]

        # Collision handling with mobs
        move_vector = [0, 0]
        for sprite in mobs:
            if pygame.sprite.collide_rect(self, sprite):
                move_vector[0] += self.pos[0] - sprite.pos[0]
                move_vector[1] += self.pos[1] - sprite.pos[1]

        move_vector = normalize_vector(move_vector)
        self.pos[0] += move_vector[0]
        self.pos[1] += move_vector[1]

        # Collision test with main player
        move_vector = [0, 0]
        if pygame.sprite.collide_rect(self, main_player.sprite):
            move_vector[0] += self.pos[0] - main_player.sprite.pos[0]
            move_vector[1] += self.pos[1] - main_player.sprite.pos[1]
        move_vector = normalize_vector(move_vector)
        self.pos[0] += move_vector[0] * 2
        self.pos[1] += move_vector[1] * 2
        self.rect.topleft = self.pos

    def attempt_drain_battery(self, player):
        distance_x = player.sprite.pos[0] - self.pos[0]
        distance_y = player.sprite.pos[1] - self.pos[1]
        if math.sqrt(distance_x ** 2 + distance_y ** 2) < 20:
            player.sprite.energy -= 3

    def behaviour(self, mobs, columns, time_delta, main_player):
        self.image.fill(pygame.Color('black'))  # Reset colour in case the mob was attacked

        # If waypoint is reached get a new one
        distance_x = self.waypoint[0] - self.pos[0]
        distance_y = self.waypoint[1] - self.pos[1]
        distance_p_x = main_player.sprite.pos[0] - self.pos[0]
        distance_p_y = main_player.sprite.pos[1] - self.pos[1]
        if math.sqrt(distance_x ** 2 + distance_y ** 2) < 10 or math.sqrt(distance_p_x ** 2 + distance_p_y ** 2) < 100:
            self.pick_waypoint(main_player)

        # Move and attempt to attack the player
        self.move(mobs, columns, time_delta, main_player)
        self.attempt_drain_battery(main_player)

        # If mob is dead tell that to main system
        if self.hp <= 0:
            self.kill()
            return Indicator(15, 'Enemy killed'),  AmmoCrate(self.pos) if random.randint(1, 6) == 1 else None

    def render(self, surface):
        surface.blit(self.image, self.pos)


def create_enemy(player, spawnpoints):
    available = []
    for i in spawnpoints:
        if abs(i[0] - player.sprite.pos[0] + i[1] - player.sprite.pos[1]) > 150:
            available.append(i)
    return BaseMob(100, 0.01, random.choice(available))
