
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

    def update(self, time, starting_time, vel_update=(0, 0)):
        self.vel[0] += vel_update[0]
        self.vel[1] += vel_update[1]
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        size = self.size * time / starting_time
        surf = pygame.Surface((2 * size, 2 * size), pygame.SRCALPHA)
        if self.shape == 'rect':
            pygame.draw.rect(surf, (self.colour[0], self.colour[1], self.colour[2], 255 * time / starting_time) if self.fade else self.colour, surf.get_rect(), self.width)
        elif self.shape == 'circle':
            pygame.draw.circle(surf, (self.colour[0], self.colour[1], self.colour[2], 255 * time / starting_time) if self.fade else self.colour, (size, size), size, self.width)
        self.game.assets.camera.render(surf, self.pos)


class ParticleBurst:    # TODO: finish this, use sin and cos since speed is float, maybe add gravity option

    def __init__(self, amount, colour, time_to_live, speed, type='burst'):
        self.particles = []
        self.time = time_to_live
        self.type = type
        for i in range(amount):
            pass
