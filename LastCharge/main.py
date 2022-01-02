import pygame
import math
import random

import Mobs  # Mobs
import Player  # Player class

pygame.init()
pygame.font.init()

size = (800, 600)
BGCOLOR = (0, 255, 255)
PLAYERCOLOR = (255, 0, 0)
screen = pygame.display.set_mode(size)

global tickrate
tickrate = 100


# What does this do? No idea. But is kinda works.
def normalize_vector(vector):
    if vector == [0, 0]:
        return [0, 0]
    pythagoras = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    return vector[0] / pythagoras, vector[1] / pythagoras


def render_entities(main_character, enemies):
    main_character.sprite.render(screen)
    for enemy in enemies:
        enemy.render(screen)


def process_keys(keys, player):
    if keys[pygame.K_w]:
        player.velocity[1] -= 1
    elif keys[pygame.K_s]:
        player.velocity[1] += 1

    elif player.velocity[1] > 0:
        player.velocity[1] -= 1
    elif player.velocity[1] < 0:
        player.velocity[1] += 1

    if keys[pygame.K_a]:
        player.velocity[0] -= 1
    elif keys[pygame.K_d]:
        player.velocity[0] += 1

    elif player.velocity[0] < 0:
        player.velocity[0] += 1
    elif player.velocity[0] > 0:
        player.velocity[0] -= 1


def process_mouse(mouse, player):
    global tickrate
    if mouse[0]:
        player.sprite.shoot(pygame.mouse.get_pos())
    if mouse[2]:
        player.sprite.energy -= 0.05
        tickrate -= 50


def game_loop():
    global tickrate
    done = False

    mobs = pygame.sprite.Group()
    for i in range(100):
        position = [random.randint(10, size[0] - 10), random.randint(10, size[0] - 10)]
        distance_x = position[0]
        distance_y = position[1]
        if math.sqrt(distance_x ** 2 + distance_y ** 2) <= 100:
            position[0] += (100 - distance_x)
            position[1] += (100 - distance_y)

        mob = Mobs.BaseMob(100, 0.01, position)
        mobs.add(mob)

    player = pygame.sprite.GroupSingle(Player.Player())

    while player.sprite.alive and not done:

        tickrate = 100

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        process_keys(keys, player.sprite)
        process_mouse(mouse, player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        screen.fill(BGCOLOR)

        for i in mobs.sprites():
            i.behaviour(mobs, tickrate, player)
            i.render(screen)

        for i in player.sprite.projectiles:
            i.behaviour(mobs, tickrate)
            i.render(screen)

        for i in player.sprite.damage_indicators:
            i.behaviour(tickrate)
            i.render(screen)

        player.sprite.move(mobs, tickrate)
        player.sprite.render(screen)

        player.sprite.energy = round(player.sprite.energy, 2)
        if player.sprite.energy <= 0:
            done = True
        # TODO: Placeholder energy display
        screen.blit(pygame.font.SysFont('Arial', 30).render(f'E: {player.sprite.energy}', True, (0, 150, 255)), (10, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(tickrate)


while __name__ == '__main__':
    screen.fill(BGCOLOR)
    pygame.display.flip()
    game_loop()

pygame.quit()
