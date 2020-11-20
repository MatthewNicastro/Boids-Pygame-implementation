from pygameui.__screen_object__ import ScreenObject

from typing import List, Optional
import numpy as np
import pygame


class TextObject(ScreenObject):
    def __init__(self,
                 center: List[int],
                 color: List[int],
                 font: pygame.font.Font,
                 text: str,
                 text_color: Optional[List[int]] = [0,0,0]):

        super().__init__(center, color, [])
        self.font = font
        self.t = str(text)
        self.text_color = text_color
        self.__build__()

    def __build__(self):
        self.text = self.font.render(self.t, True, self.text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.center
        left, top, width, height = list(self.text_rect)
        self.points = np.array([[left, top],
                                [left + width, top],
                                [left + width, top + height],
                                [left, top + height]])
    def set_text(self, t): self.t = t
    def draw(self, screen: pygame.display):
        if self.is_visible: screen.blit(self.text, self.text_rect)
