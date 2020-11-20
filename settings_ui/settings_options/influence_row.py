from config import window_size
from config import params
from settings_ui.setting_config import adjs

from pygameui.clickable.button import Button
from pygameui.clickable.toggle_button import ToggleButton
from pygameui.text_object import TextObject
from pygameui.row_border import RowBorder

import numpy as np
import pygame

influence_tag = TextObject([0,0],
                           [255, 0, 0],
                           pygame.font.SysFont('arial', 20),
                           'Visual perception(px):    {}'.format(params['influence']))

def adj_influence_func():
    params.update({'influence' : max(20, min(800, adjs['delta_influence'] + params['influence']))})
    influence_tag.set_text('Visual perception(px):    {}'.format(params['influence']))
    influence_tag.__build__()
    pygame.time.wait(150)

adjust_influence = Button([0, 0],
                          [255, 0, 0],
                          pygame.font.SysFont('arial', 20),
                          'Adjust Influence',
                          [0, 255, 0],
                          [30, 10],
                          on_hold = adj_influence_func)

toggle_influence_adj_direction = ToggleButton([0, 0],
                                              [[255, 0, 0], [0, 255, 0]],
                                              pygame.font.SysFont('arial', 20),
                                              ['INCREASE', 'DECREASE'],
                                              [30, 10],
                                              on_click = lambda: adjs.update({'delta_influence' : adjs['delta_influence'] * -1}))

toggle_delta_influence = ToggleButton([0, 0],
                                      [[255, 0, 0], [255, 0, 0], [255, 0 ,0]],
                                      pygame.font.SysFont('arial', 20),
                                      ['1', '10', '100'],
                                      [30, 10],
                                      on_click = lambda: adjs.update({'delta_influence' : adjs['delta_influence'] * 10})
                                                         if -100 < adjs['delta_influence'] < 100 else
                                                         adjs.update({'delta_influence' : np.sign(adjs['delta_influence'])}))

influence_row = RowBorder([window_size[0]//4, 170],
                          [0,255, 255],
                          950,
                          10,
                          [influence_tag, adjust_influence, toggle_influence_adj_direction, toggle_delta_influence])
