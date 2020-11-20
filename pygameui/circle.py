from pygameui.__screen_object__ import ScreenObject

from typing import List
import pygame


class Circle(ScreenObject): 
    
    def __init__(self, 
                 radius: int, 
                 center: List[int], 
                 color: List[int]): 
        
        super().__init__(center, color, [])
        self.radius = radius
    
    def draw(self, screen: pygame.display):
        '''
        Draws the boid on the pygame screen

        Parameters
        ----------
        screen : pygame.display
            Current pygame screen display

        Returns
        -------
        None.

        '''
        pygame.draw.circle(screen, self.color, self.center, self.radius)
    
    def __build__(self): pass