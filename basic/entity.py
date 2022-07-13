
import pygame

import input


class Entity:

    def __init__(self, x, y, w, h, name, img, game):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.name = name
        self.img = img
        self.game = game
        self.action = 'idle'
        self.vel = [0, 0]

    def update(self):
        self.game.assets.camera.render(self.img, (self.x, self.y))

    def move(self, movement, tiles, dt):
        self.rect.x += movement[0] * dt
        collision_tiles = [tile for tile in tiles if self.rect.colliderect(tile)]
        for tile in collision_tiles:
            if movement[0] > 0:
                self.rect.x = tile.x - self.w
            elif movement[0] < 0:
                self.rect.x = tile.right
        self.rect.y += movement[1] * dt
        collision_tiles = [tile for tile in tiles if self.rect.colliderect(tile)]
        for tile in collision_tiles:
            if movement[1] > 0:
                self.rect.y = tile.y - self.h
            elif movement[1] < 0:
                self.rect.y = tile.bottom
        self.y, self.x = self.rect.y, self.rect.x


class Player(Entity):

    def __init__(self, x, y, w, h, img, game):
        super().__init__(x, y, w, h, f'player', img, game)
        self.anims = {anim.split(self.name)[-1]: self.game.assets.anims.anims[anim] for anim in self.game.assets.anims.anims if self.name in anim}

    def update(self):   # TODO: only get chunks in vicinity of player
        for event in self.game.last_input:
            if event.type == input.KEYHOLD:
                if event.key == input.S:
                    self.move((0, 2), self.game.assets.worlds.get_active_world().level.collision_mesh, self.game.dt)
                if event.key == input.W:
                    self.move((0, -2), self.game.assets.worlds.get_active_world().level.collision_mesh, self.game.dt)
                if event.key == input.A:
                    self.move((-2, 0), self.game.assets.worlds.get_active_world().level.collision_mesh, self.game.dt)
                if event.key == input.D:
                    self.move((2, 0), self.game.assets.worlds.get_active_world().level.collision_mesh, self.game.dt)
                if event.key == input.RETURN:
                    self.x, self.y = 0, 0
                    self.rect.x, self.rect.y = 0, 0
        self.anims[self.action].play(self.game.dt)
        self.anims[self.action].render_main((self.x, self.y))
