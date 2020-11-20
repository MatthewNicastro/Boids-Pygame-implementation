from config import window_size
from config import params
from settings_ui.setting_config import adjs

from pygameui.clickable.button import Button
from pygameui.clickable.toggle_button import ToggleButton
from pygameui.text_object import TextObject
from pygameui.row_border import RowBorder

import numpy as np
import pygame

obj_margin_tag = TextObject([0,0],
                           [255, 0, 0],
                           pygame.font.SysFont('arial', 20),
                           'Object Margin(px):    {}'.format(params['obj_margin']))

def adj_obj_margin_func():
    params.update({'obj_margin' : max(75, min(250, adjs['delta_obj_margin'] + params['obj_margin']))})
    obj_margin_tag.set_text('Object Margin(px):    {}'.format(params['obj_margin']))
    obj_margin_tag.__build__()
    pygame.time.wait(150)

adjust_obj_margin = Button([0, 0],
                          [255, 0, 0],
                          pygame.font.SysFont('arial', 20),
                          'Adjust Object Margin',
                          [0, 255, 0],
                          [30, 10],
                          on_hold = adj_obj_margin_func)

toggle_obj_margin_adj_direction = ToggleButton([0, 0],
                                               [[255, 0, 0], [0, 255, 0]],
                                               pygame.font.SysFont('arial', 20),
                                               ['INCREASE', 'DECREASE'],
                                               [30, 10],
                                               on_click = lambda: adjs.update({'delta_obj_margin' : adjs['delta_obj_margin'] * -1}))

toggle_delta_obj_margin = ToggleButton([0, 0],
                                      [[255, 0, 0], [255, 0, 0], [255, 0 ,0]],
                                      pygame.font.SysFont('arial', 20),
                                      ['1', '10', '100'],
                                      [30, 10],
                                      on_click = lambda: adjs.update({'delta_obj_margin' : adjs['delta_obj_margin'] * 10})
                                                         if -100 < adjs['delta_obj_margin'] < 100 else
                                                         adjs.update({'delta_obj_margin' : np.sign(adjs['delta_obj_margin'])}))

obj_margin_row = RowBorder([window_size[0]//4, 310],
                           [0,255, 255],
                           950,
                           10,
                           [obj_margin_tag, adjust_obj_margin, toggle_obj_margin_adj_direction, toggle_delta_obj_margin])
