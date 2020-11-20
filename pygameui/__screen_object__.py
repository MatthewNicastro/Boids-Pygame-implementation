from typing import List, Optional
import numpy as np
import pygame
from abc import ABC, abstractmethod

class ScreenObject(ABC): 
    def __init__(self, center: List[int], color: List[int], points: List[int], is_visible: Optional[bool] = True):
        self.center = np.array(center)
        self.color = color
        self.points = points
        self.is_visible = is_visible
    
    def change_visibility(self, state: bool): self.is_visible = state 
    
    @abstractmethod
    def draw(self, screen: pygame.display): pass
    
    @abstractmethod
    def __build__(self): pass