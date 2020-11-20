from typing import List, Callable, Optional
import pygame
import numpy as np
from pygameui.ScreenObjectsAPI import ScreenObject

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
    
    def __build__(self): pass
    
    def draw(self, screen: pygame.display): pass
    
    def is_targeted(self, mouse_x: int, mouse_y: int) -> bool:
        if self.is_visible:
            if self.points[0][0] <= mouse_x <= self.points[1][0]:
                if self.points[0][1] <= mouse_y <= self.points[2][1]:
                    return True
        return False

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

class ToggleButton(Button):
    def __init__(self,
                 center: List[int],
                 colors: List[List[int]], 
                 font: pygame.font.Font,
                 texts: List[str], 
                 padding: List[int], 
                 pressed_color: Optional[List[int]] = [0, 255, 0],
                 text_color: Optional[List[int]] = [0,0,0],
                 on_click: Optional[Callable] = (lambda: None)):
        
        def onclick():
            self.state = (self.state + 1) % min(len(self.colors), len(self.texts))
            self.color = self.colors[self.state]
            self.text.t = self.texts[self.state]
            self.__build__()
            on_click()

        super().__init__(center, 
                         colors[0],
                         font,
                         texts[0], 
                         pressed_color,
                         padding, 
                         text_color = text_color,
                         on_click = onclick)
        self.state = 0
        self.colors = colors
        self.texts = texts
        
    def __build__(self): super().__build__()
    def draw(self, screen: pygame.display): 
        if self.is_visible: super().draw(screen)

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

        