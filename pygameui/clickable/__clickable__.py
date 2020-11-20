from typing import List, Callable
import pygame
from abc import abstractmethod
from pygameui.__screen_object__ import ScreenObject

class Clickable(ScreenObject):
    def __init__(self,
                 center: List[int],
                 color: List[int],
                 points: List[int],
                 on_click: Callable,
                 on_press: Callable,
                 on_hold: Callable,
                 on_release: Callable):

        super().__init__(center, color, [])
        self.on_click = on_click
        self.on_press = on_press
        self.on_hold = on_hold
        self.on_release = on_release

    def is_targeted(self, mouse_x: int, mouse_y: int) -> bool:
        if self.is_visible:
            if self.points[0][0] <= mouse_x <= self.points[1][0]:
                if self.points[0][1] <= mouse_y <= self.points[2][1]:
                    return True
        return False

    @abstractmethod
    def __build__(self): pass

    @abstractmethod
    def draw(self, screen: pygame.display): pass
