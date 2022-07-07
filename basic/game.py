
import time

import pygame

import assets
import input
import entity


class Game:

    def __init__(self, fps, name):
        pygame.display.set_caption(name)
        self.assets = assets.Assets(self)
        self.clock = pygame.time.Clock()
        self.dt = 1.
        self.fps = fps
        self.lt = time.time()
        self._stop = False
        self.last_input = []
        player_surf = pygame.Surface((24, 32))
        player_surf.fill((255, 255, 255))
        self.player = entity.Player(0, 0, 24, 32, player_surf, self)

    def update(self):
        self.dt = time.time() - self.lt
        self.dt *= self.fps
        self.lt = time.time()
        self.last_input *= 0
        for event in self.assets.input.get():
            if event.type == input.QUIT:
                self.stop()
            if event.type == input.KEYDOWN2:
                if event.key == input.ESCAPE:
                    self.stop()
            self.last_input.append(event)
        self.assets.update(self.dt)
        self.clock.tick(self.fps)

    def stop(self):
        self._stop = True

    def run(self):
        while not self._stop:
            self.update()


Game(120, 'Test').run()
