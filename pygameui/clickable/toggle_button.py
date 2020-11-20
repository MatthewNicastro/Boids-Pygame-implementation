from pygameui.clickable.button import Button
from typing import List, Callable, Optional
import pygame

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
