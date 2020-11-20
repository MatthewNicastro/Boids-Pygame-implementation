from config import window_size
from config import params

from pygameui.text_object import TextObject
from pygameui.__screen_object__ import ScreenObject

import pygame
import numpy as np
from typing import List
from boid import Boid

demo_boid = Boid([1425, 950], 
                 params['max_speed'],
                 params['influence'], 
                 params['min_dist'], 
                 params['obj_margin'],
                 window_size,
                 params['cohesion_factor'],
                 params['separation_factor'], 
                 params['align_factor'],
                 random_theta = False)

jitter_demo_text = TextObject([demo_boid.center[0], demo_boid.center[1] - 20], 
                              [0,0,0], 
                              pygame.font.SysFont('arial', 20), 
                              'Jitter Demo')

demo_boid.__jitter__(np.pi/(2 * params['jitter']))

#Speed line
speed_offset_x = 175
speed_offset_y = 50
speed_p1 = [demo_boid.center[0] - speed_offset_x, demo_boid.center[1] - speed_offset_y]
speed_text = TextObject([demo_boid.center[0] - speed_offset_x, demo_boid.center[1] - speed_offset_y + 10 - params['max_speed']], 
                   [0,0,0], 
                   pygame.font.SysFont('arial', 20), 
                   'Speed')
#Perception line
perception_offset_x = 50
perception_offset_y = 50
perception_p1 = [demo_boid.center[0] - perception_offset_x, demo_boid.center[1] - perception_offset_y]
perception_text = TextObject([demo_boid.center[0] - perception_offset_x, demo_boid.center[1] - perception_offset_y - 10 - params['influence']], 
                        [0,0,0], 
                        pygame.font.SysFont('arial', 20), 
                        'Visual Perception')

#Min distance line
min_dist_offset_x = -125
min_dist_offset_y = 50
min_dist_p1 = [demo_boid.center[0] - min_dist_offset_x, demo_boid.center[1] - min_dist_offset_y]
min_dist_text = TextObject([demo_boid.center[0] - min_dist_offset_x, demo_boid.center[1] - min_dist_offset_y - 10 - params['min_dist']], 
                        [0,0,0], 
                        pygame.font.SysFont('arial', 20), 
                        'Minimum Distance')

#Object margin line
obj_margin_offset_x = -275
obj_margin_offset_y = 50
obj_margin_p1 = [demo_boid.center[0] - obj_margin_offset_x, demo_boid.center[1] - obj_margin_offset_y]
obj_margin_text = TextObject([demo_boid.center[0] - obj_margin_offset_x, demo_boid.center[1] - obj_margin_offset_y - 10 - params['obj_margin']], 
                        [0,0,0], 
                        pygame.font.SysFont('arial', 20), 
                        'Object Margin')
k = 0
def settings_loop(screen: pygame.display, screen_objects: List[ScreenObject]):
    global k, params, demo_boid
    demo_boid.set_speed(params['max_speed'])
    demo_boid.set_inf_2(params['influence'])
    demo_boid.set_min_dist_2(params['min_dist'])
    demo_boid.set_obj_margin_2(params['obj_margin'])
    demo_boid.set_cohesion_factor(params['cohesion_factor'])
    demo_boid.set_separation_factor(params['separation_factor'])
    demo_boid.set_align_factor(params['align_factor'])
    if params['jitter'] > 0:
        if k >= 10: 
            demo_boid.__jitter__(np.pi/params['jitter'])
            k = 0
        else: k += 1
    demo_boid.draw(screen)
    jitter_demo_text.draw(screen)
    
    #Speed line
    speed_p2 = [demo_boid.center[0] - speed_offset_x, demo_boid.center[1] - speed_offset_y - params['max_speed']]
    speed_text.center = [demo_boid.center[0] - speed_offset_x, demo_boid.center[1] - speed_offset_y - 10 - params['max_speed']]
    speed_text.__build__()
    speed_text.draw(screen)
    pygame.draw.line(screen, [255,0,0], speed_p1, speed_p2, 5)
    
    #Perception line
    perception_p2 = [demo_boid.center[0] - perception_offset_x, demo_boid.center[1] - perception_offset_y - params['influence']]
    perception_text.center = [demo_boid.center[0] - perception_offset_x, demo_boid.center[1] - perception_offset_y - 10 - params['influence']]
    perception_text.__build__()
    perception_text.draw(screen)
    pygame.draw.line(screen, [0,255,0], perception_p1, perception_p2, 5)
    
    #Min distance line
    min_dist_p2 = [demo_boid.center[0] - min_dist_offset_x, demo_boid.center[1] - min_dist_offset_y - params['min_dist']]
    min_dist_text.center = [demo_boid.center[0] - min_dist_offset_x, demo_boid.center[1] - min_dist_offset_y - 10 - params['min_dist']]
    min_dist_text.__build__()
    min_dist_text.draw(screen)
    pygame.draw.line(screen, [0,0,255], min_dist_p1, min_dist_p2, 5)
    
    #Object margin line
    obj_margin_p2 = [demo_boid.center[0] - obj_margin_offset_x, demo_boid.center[1] - obj_margin_offset_y - params['obj_margin']]
    obj_margin_text.center = [demo_boid.center[0] - obj_margin_offset_x, demo_boid.center[1] - obj_margin_offset_y - 10 - params['obj_margin']]
    obj_margin_text.__build__()
    obj_margin_text.draw(screen)
    pygame.draw.line(screen, [255,0,255], obj_margin_p1, obj_margin_p2, 5)
    
    for obj in screen_objects:
        obj.__build__()
        obj.draw(screen)


