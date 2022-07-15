
import random

import pygame


class Particle:

    def __init__(self, colour, pos, vel, size, game, shape='circle', width=0, shrink=True, fade=False):
        self.colour = colour
        self.pos = pos
        self.vel = vel
        self.size = size
        self.shape = shape
        self.game = game
        self.shrink = shrink
        self.fade = fade
        self.width = width

    def update(self, time, starting_time, dt, vel_update=(0, 0)):
        self.vel[0] += vel_update[0]
        self.vel[1] += vel_update[1]
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        if self.shrink:
            size = self.size * time // starting_time
        else:
            size = self.size
        surf = pygame.Surface((2 * size, 2 * size), pygame.SRCALPHA)
        if self.shape == 'rect':
            pygame.draw.rect(surf, (self.colour[0], self.colour[1], self.colour[2], 255 * time / starting_time) if self.fade else self.colour, surf.get_rect(), self.width)
        elif self.shape == 'circle':
            pygame.draw.circle(surf, (self.colour[0], self.colour[1], self.colour[2], 255 * time / starting_time) if self.fade else self.colour, (size, size), size, self.width)
        self.game.assets.camera.render(surf, self.pos)


class ParticleBurst:    # TODO: finish this, use sin and cos since speed is float, maybe add gravity option

    def __init__(self, pos, size, amount, colours, time_to_live, speed, game, type='burst', shape='circle', width=0, shrink=True, fade=False):
        self.particles = []
        self.starting_time = time_to_live
        self.time = time_to_live
        self.type = type
        self.colours = colours
        self.middle = pos
        self.particle_size = size
        self.game = game
        self.shrinks = shrink
        self.fades = fade
        if type == 'burst':
            for i in range(amount):
                self.particles.append(Particle(random.choice(self.colours), self.middle, [random.randint(-speed * 10, speed * 10) / 10, random.randint(-speed * 10, speed * 10) / 10], size, self.game, shape, width, shrink, fade))

    def update(self, dt, vel_update=(0, 0)):
        if self.time > 0:
            self.time -= 1
        elif self.time < 0:
            pass
        else:
            self.particles *= 0
        for particle in self.particles:
            particle.update(self.time if self.time > 0 else 1, self.starting_time if self.starting_time > 0 else 1, dt, vel_update)

