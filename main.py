import time

import pygame
import math
import random

import Mobs  # Mobs
import Player  # Player class
import Environment  # Environment objects

pygame.init()
pygame.font.init()

size = (800, 600)
BGCOLOR = (0, 255, 255)
BGCOLOR = (100, 255, 255)
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


# Renders sprite around the center of the screen
def render_sprite(player, sprite, surface):
    screen_size = surface.get_size()
    middle = [screen_size[0] // 2, screen_size[1] // 2]
    difference = [middle[0] - player.pos[0], middle[1] - player.pos[1]]
    local_position = [sprite.pos[0] + difference[0], sprite.pos[1] + difference[1]]
    surface.blit(sprite.image, local_position)


def render_entities(main_character, enemies):
    render_sprite(main_character.sprite, main_character.sprite, screen)
    for enemy in enemies:
        render_sprite(main_character.sprite, enemy, screen)


def render_hud(player, notifications, score):
    # Draw damage indicators
    for i in player.sprite.damage_indicators:
        i.behaviour(tickrate)
        i.render(player.sprite, screen)

    # Font used to render most of hud
    hud_font = pygame.font.SysFont('Arial', 30)

    # Create darkened areas for hud
    HUD_window = pygame.Surface((150, 80))
    HUD_window.set_alpha(128)
    HUD_window.fill('black')
    screen.blit(HUD_window, (0, 0))
    HUD_window = pygame.Surface((300, 190))
    HUD_window.set_alpha(128)
    HUD_window.fill('black')
    screen.blit(HUD_window, (600, 0))

    # Show remaining health and ammo
    screen.blit(pygame.image.load('textures/heart.png'), (10, 20))
    screen.blit(hud_font.render(str(player.sprite.energy), True, (255, 255, 255)), (30, 10))
    screen.blit(pygame.image.load('textures/bullet.png'), (10, 52))
    screen.blit(hud_font.render(str(player.sprite.weapon.ammunition), True, (255, 255, 255)), (30, 45))

    # Show score and recent XP gains
    screen.blit(hud_font.render(f'Score: {score}', True, (255, 255, 255)), (610, 10))
    notifications_text = ''
    limit = 0
    for i in notifications:
        limit += 1
        screen.blit(pygame.font.SysFont('Arial', 20).render(f'+{i.xp} {i.message}', True, i.colour),
                    (610, 30 + limit * 20))
        if limit == 5:
            break


# Render walls, pickups, powerup stations, the player and mobs.
def render_environment(columns, ammo_crates, stations, player, mobs):
    for i in ammo_crates.sprites():
        render_sprite(player.sprite, i, screen)
        i.behaviour(player)

    for i in columns.sprites():
        render_sprite(player.sprite, i, screen)

    for i in player.sprite.projectiles:
        i.behaviour(mobs, columns, tickrate)
        render_sprite(player.sprite, i, screen)

    for i in stations.sprites():
        render_sprite(player.sprite, i, screen)
        i.behaviour(screen, player)


# Adjust player velocity based on keys pressed
def process_keys(keys, player):
    if keys[pygame.K_w]:
        player.velocity[1] -= 0.7
    elif keys[pygame.K_s]:
        player.velocity[1] += 0.7

    elif player.velocity[1] > 0:
        player.velocity[1] -= 1
    elif player.velocity[1] < 0:
        player.velocity[1] += 1

    if keys[pygame.K_a]:
        player.velocity[0] -= 0.7
    elif keys[pygame.K_d]:
        player.velocity[0] += 0.7

    elif player.velocity[0] < 0:
        player.velocity[0] += 1
    elif player.velocity[0] > 0:
        player.velocity[0] -= 1


# W = wall, S = spawnpoint, P = Powerup station, E = enemy spawns
def level_to_list(level_name):
    f = open(level_name, 'r')
    level_list = []
    for i in f.read().split('\n'):
        level_list.append(i)
    return level_list


# Shoot the gun and slow down time
def process_mouse(mouse, player):
    global tickrate
    if mouse[0]:
        player.sprite.shoot(pygame.mouse.get_pos(), screen)
    if mouse[2]:
        player.sprite.energy -= 0.05
        tickrate -= 50


def game_loop():
    global tickrate
    done = False

    # Create mobs group
    mobs = pygame.sprite.Group()
    last_spawned = time.time()

    # Create environment sprite groups
    columns = pygame.sprite.Group()
    stations = pygame.sprite.Group()
    ammo_crates = pygame.sprite.Group()
    spawn_points = list()

    # Load the level.
    level = level_to_list('arena_level.txt')
    x = y = 120
    spawn_point = (x, y)
    for row in level:
        for col in row:
            if col == "W":
                columns.add(Environment.Column((x, y)))
            if col == "S":
                spawn_point = (x + 2, y + 2)
            if col == "P":
                stations.add(Environment.PowerupSpawn((x + 4, y + 4)))
            if col == "E":
                spawn_points.append([x, y])
            x += 20
        y += 20
        x = 120

    player = pygame.sprite.GroupSingle(Player.Player(spawn_point))  # Create the player

    notifications = []  # XP notifications
    total_score = 0  # Total score of the player

    while player.sprite.alive and not done:
        tickrate = 100  # Reset the tickrate in case player was in bullet time

        # Process the keys
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        process_keys(keys, player.sprite)
        process_mouse(mouse, player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        screen.fill(BGCOLOR)  # Reset the frame

        # Move mobs
        for i in mobs.sprites():
            killed = i.behaviour(mobs, columns, tickrate, player)
            if killed is not None:
                notifications.append(killed[0])
                total_score += killed[0].xp
                if killed[1] is not None:
                    ammo_crates.add(killed[1])

        # Create new mobs if there are too little of them
        if len(mobs) < 20 and time.time() - last_spawned > 0.8:
            mobs.add(Mobs.create_enemy(player, spawn_points))
            last_spawned = time.time()

        player.sprite.move(mobs, columns, tickrate)  # Move the player

        # Render everything
        render_environment(columns, ammo_crates, stations, player, mobs)
        render_entities(player, mobs)
        render_hud(player, notifications, total_score)

        # Remove old notifications
        for i in notifications:
            if int(time.time()) - i.start > 3:
                notifications.remove(i)

        # Check if the game is over
        player.sprite.energy = round(player.sprite.energy, 2)
        if player.sprite.energy <= 0:
            done = True
            return total_score

        # Update the screen
        pygame.display.flip()
        pygame.time.Clock().tick(tickrate)


while __name__ == '__main__':
    screen.fill(BGCOLOR)
    pygame.display.flip()
    print(game_loop())

pygame.quit()
