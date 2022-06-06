
import pygame  # TODO, add Button, Menu, general UI || Buttons can have funcs attached to them

import font
from general_funcs import centre_blit, centre_of_rect


class TextBox:

    def __init__(self, x, y, w, h, text_list, used_font, bg_colour, border_colour, border_width, game, menus=[]):  # TODO, menus in the textbox
        self.rect = pygame.Rect(x, y, w, h)
        self.texts = text_list
        self.used_font = used_font
        self.bg_colour = bg_colour
        self.border_colour = border_colour
        self.border_width = border_width
        self.game = game
        self.index = 0
        self.current_text = text_list[self.index]

    def render(self, surf, pos=None, use_scroll=False):
        if pos is None:
            pos = (self.rect.x, self.rect.y)
        box_surf = pygame.Surface((self.rect.w, self.rect.h))
        box_surf.fill(self.bg_colour)
        pygame.draw.rect(box_surf, self.border_colour, self.rect, self.border_width)

        if not isinstance(self.used_font, font.SysFont):
            text_surf = self.used_font[self.current_text]
        else:
            text_surf = self.used_font.render(self.current_text, True, (255, 255, 255))
        if text_surf.get_width() <= box_surf.get_width() and text_surf.get_height() <= box_surf.get_height():
            centre_blit(text_surf, box_surf, centre_of_rect(pygame.Rect(0, 0, box_surf.get_width(), box_surf.get_height())))
        else:
            if text_surf.get_width() > box_surf.get_width():
                if text_surf.get_height() <= box_surf.get_height():
                    text_surf = pygame.transform.scale(text_surf, box_surf.get_size())
                else:
                    text_surf = pygame.transform.scale(text_surf, (box_surf.get_width(), text_surf.get_height()))
            else:
                text_surf = pygame.transform.scale(text_surf, (text_surf.get_width(), box_surf.get_height()))
            centre_blit(text_surf, box_surf, centre_of_rect(pygame.Rect(0, 0, box_surf.get_width(), box_surf.get_height())))

        if use_scroll:
            surf.blit(box_surf, (pos[0] - self.game.assets.camera.scroll[0], pos[1] - self.game.assets.camera.scroll[1]))
        else:
            surf.blit(box_surf, pos)

    def next_text(self):
        if self.index >= len(self.texts) - 1:
            self.index += 1
            self.current_text = text_list[self.index]
        else:
            self.current_text = ''
            self.index = len(self.texts)


class Button:

    def __init__(self, x, y, w, h, colour, highlight_colour, border_width, text, font, action, *action_parametres):
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = colour
        self.highlight_colour = highlight_colour
        self.text = text
        self.action = action
        self.parametres = action_parametres
        self.font = font
        self.is_highlighted = False

    def render(self, surf, pos=None):
        if pos is None:
            pos = self.rect.x, self.rect.y
        button_surf = pygame.Surface((self.rect.w, self.rect.h))
        button_surf.fill(self.colour if not self.is_highlighted else self.highlight_colour)

        if not isinstance(self.font, font.SysFont):
            text_surf = font[self.text]
        else:
            text_surf = font.render(self.text, True, (255, 255, 255))
        if text_surf.get_width() <= button_surf.get_width() and text_surf.get_height() <= button_surf.get_height():
            centre_blit(text_surf, button_surf, centre_of_rect(pygame.Rect(0, 0, button_surf.get_width(), button_surf.get_height())))
        else:
            if text_surf.get_width() > button_surf.get_width():
                if text_surf.get_height() <= button_surf.get_height():
                    text_surf = pygame.transform.scale(text_surf, uttonx_surf.get_size())
                else:
                    text_surf = pygame.transform.scale(text_surf, (button_surf.get_width(), text_surf.get_height()))
            else:
                text_surf = pygame.transform.scale(text_surf, (text_surf.get_width(), box_surf.get_height()))
            centre_blit(text_surf, button_surf, centre_of_rect(pygame.Rect(0, 0, button_surf.get_width(), button_surf.get_height())))

        pygame.draw.rect(button_surf, self.colour if self.is_highlighted else self.highlight_colour, pygame.Rect((0, 0), button_surf.get_size()))
        surf.blit(button_surf, pos)

    def do_action(self):
        self.action(*self.parametres)
