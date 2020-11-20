from typing import List, Callable, Optional
import pygame
import numpy as np
from pygameui.clickable.__clickable__ import Clickable
from pygameui.text_object import TextObject

class Button(Clickable): 
    def __init__(self,
                 center: List[int],
                 color: List[int],
                 font: pygame.font.Font, 
                 text: str, 
                 pressed_color: List[int],
                 padding: List[int],
                 text_color: Optional[List[int]] = [0,0,0],
                 on_click: Optional[Callable] = (lambda: None),
                 on_press: Optional[Callable] = (lambda: None),
                 on_hold: Optional[Callable] = (lambda: None), 
                 on_release: Optional[Callable] = (lambda: None)):
        
        def onpress():
            self.change_press_color()
            on_press()
        
        def onrelease():
            self.change_release_color()
            on_release()
        
        super().__init__(center, 
                         color,
                         [],
                         on_click, 
                         onpress, 
                         on_hold, 
                         onrelease)
        
        self.base_color = color
        self.pressed_color = pressed_color
        self.text = TextObject(center, color, font, text)
        self.padding = padding
        self.__build__()
    
    def __build__(self):
        self.text.center = self.center
        self.text.__build__()
        p_x, p_y = self.padding
        left, top, width, height = list(self.text.text_rect)
        self.points = np.array([[left - p_x, top - p_y],
                                [left + width + p_x, top - p_y],
                                [left + width + p_x, top + height + p_y],
                                [left - p_x, top + height + p_y]])
    
    def change_press_color(self):
        self.color = self.pressed_color
    
    def change_release_color(self): 
        self.color = self.base_color
          
    def draw(self, screen: pygame.display):
        if self.is_visible:
            pygame.draw.polygon(screen, self.color, self.points)
            self.text.draw(screen)