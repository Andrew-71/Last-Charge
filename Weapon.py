import pygame
from pygame import mixer
import math

mixer.init()


def normalize_vector(vector):
    if vector == [0, 0]:
        return [0, 0]
    pythagoras = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    return vector[0] / pythagoras, vector[1] / pythagoras


class DamageIndicator(pygame.sprite.Sprite):
    def __init__(self, start_pos, damage_done):
        super().__init__()

        self.font = pygame.font.SysFont('Arial', 10)
        self.text = self.font.render(f'-{damage_done}', True, (0, 150, 255))

        self.pos_start = list(start_pos)
        self.pos = list(start_pos)
        self.move_vector = -1
        self.damage = damage_done
        self.distance = 10

    def behaviour(self, time_delta):
        self.pos[1] += self.move_vector * time_delta * 0.005

        # If bullet reached its range it stops existing
        dist_x = self.pos[0] - self.pos_start[0]
        dist_y = self.pos[1] - self.pos_start[1]
        if math.sqrt(dist_x ** 2 + dist_y ** 2) >= self.distance:
            self.kill()

    def render(self, surface):
        surface.blit(self.text, self.pos)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, direction, damage, distance, player):
        super().__init__()

        self.image = pygame.Surface([4, 4])
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect(x=start_pos[0], y=start_pos[1])

        self.pos_start = list(start_pos)
        self.pos = list(start_pos)
        self.move_vector = direction
        self.damage = damage
        self.distance = distance

        self.player = player

        pygame.draw.circle(self.image, 'blue',
                           (self.rect.width // 2, self.rect.height // 2),
                           self.rect.width // 2)

    def behaviour(self, mobs, columns, time_delta):
        # Move
        self.pos[0] += self.move_vector[0] * time_delta * 0.12
        self.pos[1] += self.move_vector[1] * time_delta * 0.12

        # Try killing enemies
        for sprite in mobs:
            if pygame.sprite.collide_circle(self, sprite):
                sprite.hp -= self.damage
                self.player.damage_indicators.add(DamageIndicator(self.pos, self.damage))
                self.kill()

        for sprite in columns:
            if pygame.sprite.collide_circle(self, sprite):
                self.kill()

        # If bullet reached its range it stops existing
        dist_x = self.pos[0] - self.pos_start[0]
        dist_y = self.pos[1] - self.pos_start[1]
        if math.sqrt(dist_x ** 2 + dist_y ** 2) >= self.distance:
            self.kill()

        # Adjust.. hitbox? Idk what this does but too scared to remove
        self.rect.topleft = self.pos

    def render(self, surface):
        pygame.draw.circle(self.image, 'blue',
                           (self.rect.width // 2, self.rect.height // 2),
                           self.rect.width // 2)
        surface.blit(self.image, self.pos)


class Weapon:
    def __init__(self, cooldown, name, damage, weapon_range):
        self.last_shot = 0
        self.name = name
        self.cooldown = cooldown
        self.damage = damage
        self.weapon_range = weapon_range
        self.ammunition = 30

        self.sound_effect = mixer.Sound('sounds/shoot.wav')
        self.no_round_sound = mixer.Sound('sounds/no_round.wav')

    def shoot(self, user, mouse_pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.cooldown:
            self.last_shot = pygame.time.get_ticks()

            if self.ammunition > 0:
                self.ammunition -= 1

                direction = (mouse_pos[0] - user.pos[0], mouse_pos[1] - user.pos[1]) \
                    if mouse_pos != user.pos else (1, 1)

                user.projectiles.add(Projectile(user.pos,
                                                normalize_vector(direction),
                                                self.damage, self.weapon_range, user))

                self.sound_effect.play()
            else:
                self.no_round_sound.play()