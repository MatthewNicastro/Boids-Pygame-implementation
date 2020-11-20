from config import window_size
from config import params
from settings_ui.setting_config import adjs

from pygameui.clickable.button import Button
from pygameui.clickable.toggle_button import ToggleButton
from pygameui.text_object import TextObject
from pygameui.row_border import RowBorder

import numpy as np
import pygame

jitter_tag = TextObject([0,0],
                           [255, 0, 0],
                           pygame.font.SysFont('arial', 20),
                           'Jitter (Radians):    PI/{}'.format(params['jitter']))

def adj_jitter_func():
    params.update({'jitter' : max(0, min(100, adjs['delta_jitter'] + params['jitter']))})
    if params['jitter'] > 0: jitter_tag.set_text('Jitter (Radians):    PI/{}'.format(params['jitter']))
    else: jitter_tag.set_text('Jitter (Radians):    OFF')
    jitter_tag.__build__()
    pygame.time.wait(150)

adjust_jitter = Button([0, 0],
                       [255, 0, 0],
                       pygame.font.SysFont('arial', 20),
                       'Adjust jitter',
                       [0, 255, 0],
                       [30, 10],
                       on_hold = adj_jitter_func)

toggle_jitter_adj_direction = ToggleButton([0, 0],
                                           [[255, 0, 0], [0, 255, 0]],
                                           pygame.font.SysFont('arial', 20),
                                           ['INCREASE', 'DECREASE'],
                                           [30, 10],
                                           on_click = lambda: adjs.update({'delta_jitter' : adjs['delta_jitter'] * -1}))

toggle_delta_jitter = ToggleButton([0, 0],
                                   [[255, 0, 0], [255, 0, 0]],
                                   pygame.font.SysFont('arial', 20),
                                   ['1', '10'],
                                   [30, 10],
                                   on_click = lambda: adjs.update({'delta_jitter' : adjs['delta_jitter'] * 10})
                                                         if -10 < adjs['delta_jitter'] < 10 else
                                                         adjs.update({'delta_jitter' : np.sign(adjs['delta_jitter'])}))

jitter_row = RowBorder([window_size[0]//4, 660],
                       [0, 255, 255],
                       950,
                       10,
                       [jitter_tag, adjust_jitter, toggle_jitter_adj_direction, toggle_delta_jitter])
