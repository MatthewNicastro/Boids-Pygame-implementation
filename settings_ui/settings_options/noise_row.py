from config import window_size
from config import params
from settings_ui.setting_config import adjs

from pygameui.clickable.button import Button
from pygameui.clickable.toggle_button import ToggleButton
from pygameui.text_object import TextObject
from pygameui.row_border import RowBorder

import pygame

noise_tag = TextObject([0,0],
                       [255, 0, 0],
                       pygame.font.SysFont('arial', 20),
                       'Noise Bounds:    +-{}'.format(params['noise']))

def adj_noise_func():
    params.update({'noise' : max(0, min(30, adjs['delta_noise'] + params['noise']))})
    noise_tag.set_text('Noise Bounds:    +-{}'.format(params['noise']))
    noise_tag.__build__()
    pygame.time.wait(150)

adjust_noise = Button([0, 0],
                       [255, 0, 0],
                       pygame.font.SysFont('arial', 20),
                       'Adjust Noise',
                       [0, 255, 0],
                       [30, 10],
                       on_hold = adj_noise_func)

toggle_noise_adj_direction = ToggleButton([0, 0],
                                          [[255, 0, 0], [0, 255, 0]],
                                          pygame.font.SysFont('arial', 20),
                                          ['INCREASE', 'DECREASE'],
                                          [30, 10],
                                          on_click = lambda: adjs.update({'delta_noise' : adjs['delta_noise'] * -1}))

noise_row = RowBorder([window_size[0]//4, 730],
                       [0, 255, 255],
                       950,
                       10,
                       [noise_tag, adjust_noise, toggle_noise_adj_direction])
