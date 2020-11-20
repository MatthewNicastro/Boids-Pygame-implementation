from pygameui.__screen_object__ import ScreenObject
from typing import List, Optional
import pygame
import numpy as np

class RowBorder(ScreenObject):
    def __init__(self,
                 center: List[int],
                 color: List[int],
                 width: List[int],
                 padding: Optional[int] = 10,
                 objs: Optional[List[ScreenObject]] = []):

        super().__init__(center, color, [])
        self.objs = objs
        self.padding = padding
        self.width = width
        self.__build__()

    def __build__(self):
        tallest = 0
        if self.objs != []:
            next_x_placement = self.padding
            tallest = 0
            for obj in self.objs:
                if obj.is_visible:
                    d =  obj.points[-1][1] - obj.points[0][1]
                    if d > tallest: tallest = d

            for i in range(len(self.objs)):
                obj = self.objs[i]
                if obj.is_visible:
                    l = obj.points[1][0] - obj.points[0][0]
                    obj.center = [next_x_placement + l//2, self.center[1]]
                    obj.__build__()
                    next_x_placement += self.padding + l
                    self.objs[i] = obj

        top_left = [self.center[0] - self.width//2, self.center[1] - tallest//2 - self.padding]

        self.points = np.array([top_left,
                                [top_left[0] + self.width, top_left[1]],
                                [top_left[0] + self.width, top_left[1] + tallest + 2 * self.padding],
                                [top_left[0], top_left[1] + tallest + 2 * self.padding]])

    def draw(self, screen: pygame.display):
        self.__build__()
        pygame.draw.polygon(screen, self.color, self.points)
        for obj in self.objs:
            if obj.is_visible: obj.draw(screen)
