import pygame
pygame.init()

from config import params
from config import window_size

from boid import Boid
from pygameui.__screen_object__ import ScreenObject
from pygameui.clickable.button import Button
from pygameui.row_border import RowBorder
from pygameui.circle import Circle
from pygameui.clickable.__clickable__ import Clickable

from settings_ui.settings_options.max_speed_row import max_speed_row, adjust_max_speed, toggle_max_speed_adj_direction
from settings_ui.settings_options.influence_row import influence_row, adjust_influence, toggle_influence_adj_direction, toggle_delta_influence
from settings_ui.settings_options.min_dist_row import min_dist_row, adjust_min_dist, toggle_min_dist_adj_direction
from settings_ui.settings_options.obj_margin_row import obj_margin_row,adjust_obj_margin, toggle_obj_margin_adj_direction, toggle_delta_obj_margin
from settings_ui.settings_options.cohesion_factor_row import cohesion_factor_row, adjust_cohesion_factor, toggle_cohesion_factor_adj_direction, toggle_delta_cohesion_factor
from settings_ui.settings_options.separation_factor_row import separation_factor_row, adjust_separation_factor, toggle_separation_factor_adj_direction, toggle_delta_separation_factor
from settings_ui.settings_options.align_factor_row import align_factor_row, adjust_align_factor, toggle_align_factor_adj_direction, toggle_delta_align_factor
from settings_ui.settings_options.always_limit_speed_row import always_limit_speed_row, toggle_always_limit_speed
from settings_ui.settings_options.jitter_row import jitter_row, adjust_jitter, toggle_jitter_adj_direction, toggle_delta_jitter
from settings_ui.settings_options.noise_row import noise_row, adjust_noise, toggle_noise_adj_direction
from settings_ui.settings_loop import settings_loop

import numpy as np
from typing import List
from enum import Enum
import sys

screen = pygame.display.set_mode(window_size)

settings_menu = [max_speed_row, 
                 influence_row, 
                 min_dist_row,
                 obj_margin_row,
                 cohesion_factor_row,
                 separation_factor_row,
                 align_factor_row,
                 always_limit_speed_row,
                 jitter_row,
                 noise_row]

settings_clickables = [adjust_max_speed, 
                       toggle_max_speed_adj_direction, 
                       adjust_influence, 
                       toggle_influence_adj_direction, 
                       toggle_delta_influence,
                       adjust_min_dist, 
                       toggle_min_dist_adj_direction,
                       adjust_obj_margin, 
                       toggle_obj_margin_adj_direction, 
                       toggle_delta_obj_margin, 
                       adjust_cohesion_factor, 
                       toggle_cohesion_factor_adj_direction, 
                       toggle_delta_cohesion_factor,
                       adjust_separation_factor, 
                       toggle_separation_factor_adj_direction, 
                       toggle_delta_separation_factor,
                       adjust_align_factor, 
                       toggle_align_factor_adj_direction, 
                       toggle_delta_align_factor,
                       toggle_always_limit_speed,
                       adjust_jitter, 
                       toggle_jitter_adj_direction, 
                       toggle_delta_jitter,
                       adjust_noise, 
                       toggle_noise_adj_direction]

class ActiveScreen(Enum):
    Main = 1
    Menu = 2

num_boids = 50
background_color = [255, 255, 255]
state = {
    'selected clickable' : None,
    'active screen' : ActiveScreen.Main
}

def on_click_settings():
    if state['active screen'] == ActiveScreen.Main:
        state.update({'active screen' : ActiveScreen.Menu})
    else:
        for boid in boids:
            boid.set_speed(params['max_speed'])
            boid.set_inf_2(params['influence'])
            boid.set_min_dist_2(params['min_dist'])
            boid.set_obj_margin_2(params['obj_margin'])
            boid.set_cohesion_factor(params['cohesion_factor'])
            boid.set_separation_factor(params['separation_factor'])
            boid.set_align_factor(params['align_factor'])
            
        state.update({'active screen' : ActiveScreen.Main})

settings = Button([0, 0], 
                  [255, 0, 0], 
                  pygame.font.SysFont('arial', 20), 
                  'Settings', 
                  [0, 255, 0], 
                  [30, 10],
                  on_click = on_click_settings)
                                        
main_clickables = [settings]
topbar = RowBorder([950, 30], [0,0,0], 1900, 10, main_clickables)      
 
def main_loop(screen: pygame.display, 
              boids : List[Boid], 
              screen_objects : List[ScreenObject],
              noise: int,
              always_limit_speed: bool, 
              jitter: float):
    
    for obj in screen_objects: obj.draw(screen)
    for boid in boids: 
        boid.move(boids, 
                  screen_objects, 
                  noise_factor = noise, 
                  always_limit_speed = always_limit_speed, 
                  jitter_factor = jitter)
        boid.draw(screen)

boids = []
for _ in range(num_boids):
    loc = [int(window_size[0] * np.random.random()),
           int(window_size[1] * np.random.random())]
    loc[1] = min(max(300, loc[1]), 860)
    boids += [Boid(loc, 
                   params['max_speed'],
                   params['influence'], 
                   params['min_dist'], 
                   params['obj_margin'],
                   window_size,
                   params['cohesion_factor'],
                   params['separation_factor'], 
                   params['align_factor'])]
    if params['jitter'] > 0:
        boids[-1].__jitter__(np.pi/(4 * params['jitter']))
    
circles = []
for i in range(0, 48):
    circles += [Circle(20, np.array([40*i, 100]), [255, 0, 0]), 
                Circle(20, np.array([40*i, 900]), [255, 0, 0])]

clickables = main_clickables

while True: 
    if isinstance(state['selected clickable'], Clickable):
        if state['selected clickable'].is_targeted(*pygame.mouse.get_pos()):
            state['selected clickable'].on_hold()
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN: 
            pos = pygame.mouse.get_pos()
            for clickable in clickables: 
                if clickable.is_targeted(*pos):
                    clickable.on_press()
                    state['selected clickable'] = clickable
                    break
                                    
        if event.type == pygame.MOUSEBUTTONUP:
            if isinstance(state['selected clickable'], Clickable):
                state['selected clickable'].on_release()
                state['selected clickable'].on_click()
                state['selected clickable'] = None
    
    screen.fill(background_color)
    topbar.draw(screen)
    
    if state['active screen'] == ActiveScreen.Main:
        clickables = main_clickables
        main_loop(screen, boids, circles, params['noise'], params['always_limit_speed'], float(params['jitter']))
    
    elif state['active screen'] == ActiveScreen.Menu: 
        clickables = main_clickables + settings_clickables
        settings_loop(screen, settings_menu)
    
    pygame.display.update()