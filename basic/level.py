
import os

import pygame

from general_funcs import read_json

CHUNK_SIZE = 16


class Tile:

    def __init__(self, x, y, w, h, name, img_path, is_invisible, is_solid, game):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name
        self.img_path = img_path
        self.img = pygame.image.load(f'data{os.sep}{img_path}').convert()
        self.game = game
        self.is_invisible = is_invisible
        self.is_solid = is_solid

    def __eq__(self, other):
        return (self.x, self.y, self.w, self.h, self.name, self.is_invisible, self.is_solid) == (other.x, other.y, other.w, other.h, other.name, other.is_invisible, other.is_solid)

    def update(self, surf=None):
        if surf is None:
            self.game.assets.camera.render(self.img, self.pos)
        else:
            surf.blit(self.img, self.pos)

    def collides(self, rect):
        try:
            return self.rect.colliderect(rect)
        except AttributeError:
            return self.rect.colliderect(rect.rect)

    @property
    def pos(self):
        return [self.x, self.y]

    @pos.setter
    def pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    @rect.setter
    def rect(self, rect):
        self.x = rect.x
        self.y = rect.y
        self.w = rect.w
        self.h = rect.h


class Chunk:

    def __init__(self, tile_list, game):    # pass in list from json file as tile in tile_list
        self.tiles = []
        for tile in tile_list:
            self.tiles.append(Tile(*tile, game))
        self.pos = self.x, self.y = min(tile.x for tile in self.tiles), min(tile.y for tile in self.tiles)
        self.size = CHUNK_SIZE
        self.chunk_pos = self.chunk_x, self.chunk_y = self.x // self.size, self.y // self.size
        self.game = game
        self.collision_mesh = self.get_collision_mesh()

    def __contains__(self, rect):
        if isinstance(rect, Tile):
            return rect in self.tiles
        else:
            return bool(self.rect.contains(rect))

    def __eq__(self, other):
        try:
            return self.tiles == other.tiles
        except AttributeError:
            return False

    def update(self, surf=None):
        for tile in self.tiles:
            tile.update(surf)

    def get_collision_mesh(self):
        tiles = [tile.rect for tile in self.tiles if tile.is_solid]
        for i in range(len(tiles) // 20):
            for tile1 in tiles:
                for tile2 in tiles:
                    if tile1 == tile2:
                        continue
                    if (tile2.topleft == tile1.topright and tile2.h == tile1.h) or (tile2.bottomleft == tile1.topleft and tile2.w == tile1.w) or (tile2.bottomright == tile1.bottomleft and tile2.h == tile1.h) or (tile2.topright == tile1.bottomright and tile2.w == tile1.w) or (tile1.topleft == tile2.topright and tile1.h == tile2.h) or (tile1.bottomleft == tile2.topleft and tile1.w == tile2.w) or (tile1.bottomright == tile2.bottomleft and tile1.h == tile2.h) or (tile1.topright == tile2.bottomright and tile1.w == tile2.w):
                        tiles.append(tile1.union(tile2))
                        if tile1 in tiles:
                            tiles.remove(tile1)
                        if tile2 in tiles:
                            tiles.remove(tile2)
        return tiles

    @property
    def rect(self):
        return pygame.Rect((self.x, self.y), (self.size, self.size))


class Level:

    def __init__(self, chunk_list, game):
        self.chunks = chunk_list
        for i, chunk in enumerate(self.chunks):
            self.chunks[i] = Chunk(chunk, game)
        self.chunks_dict = {chunk.chunk_pos: chunk for chunk in self.chunks}
        self.game = game
        self.chunk_size = CHUNK_SIZE
        self.collision_mesh = self.get_collision_mesh()

    def get_all_tiles(self):
        return_list = []
        for chunk in self.chunks:
            for tile in chunk.tiles:
                return_list.append(tile)
        return return_list

    def get_collision_mesh(self, chunks=()):
        return_list = []
        if not chunks:
            for chunk in self.chunks:
                for tile in chunk.collision_mesh:
                    return_list.append(tile)
        else:
            for pos in chunks:
                chunk = self.chunks_dict[pos]
                for tile in chunk.collision_mesh:
                    return_list.append(tile)
        return return_list

    def update(self, surf=None):
        for chunk in self.chunks:
            chunk.update(surf)


class World:

    def __init__(self, name, chunk_list, game, entities=()):
        self.name = name
        self.level = Level(chunk_list, game)
        self.entities = entities
        self.game = game

    def update(self, dt, surf=None):
        self.level.update(surf)
        for entity in self.entities:
            if entity.is_active:
                entity.update(surf, dt)


class WorldManager:

    def __init__(self, game, path):
        self.path = path
        self.worlds = {}
        for world in os.listdir(path):
            if not world.startswith('.'):
                data = read_json(f'{path}{os.sep}{world}')
                self.worlds[world.split('.')[0]] = World(world.split('.')[0], data['level']['chunks'], game, data['entities'])
        self.active_world = '0'
        self.game = game

    def update(self, dt, surf=None):
        self.worlds[self.active_world].update(dt, surf=surf)

    def get_active_world(self):
        return self.worlds[self.active_world]
