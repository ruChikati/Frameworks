
import os

import pygame

pygame.joystick.init()

import animation
import camera
import font
import general_funcs
import input
import level
import particle
import sfx


class Assets:   # TODO, add UI when it's done

    def __init__(self, game, camera_specs=(pygame.display.Info().current_w, pygame.display.Info().current_h, f'data{os.sep}cutscenes', (0, 0, 0)), sfx_path=f'data{os.sep}sfx', world_path=f'data{os.sep}worlds', anim_path=f'data{os.sep}anims', font_path=f'data{os.sep}fonts'):
        self.camera = camera.Camera(camera_specs[0], camera_specs[1], game, camera_specs[2], camera_specs[3])
        self.sfx = sfx.SFXManager(game, sfx_path)
        self.worlds = level.WorldManager(game, world_path)
        self.funcs = general_funcs
        self.anims = animation.AnimationManager(anim_path, game)
        self.fonts = font.FontManager(font_path)
        self.input = input.Input(game, 128)
        self.particle = particle
        self.game = game

    def update(self, dt):
        self.sfx.update()
        self.worlds.update(dt)
        self.game.player.update()
        self.game.test_particle_burst.update(dt)
        self.camera.center((self.game.player.x, self.game.player.y))
        self.camera.update()
