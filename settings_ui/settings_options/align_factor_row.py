from config import window_size
from config import params
from settings_ui.setting_config import adjs

from pygameui.clickable.button import Button
from pygameui.clickable.toggle_button import ToggleButton
from pygameui.text_object import TextObject
from pygameui.row_border import RowBorder

import numpy as np
import pygame

align_factor_tag = TextObject([0,0],
                                   [255, 0, 0],
                                   pygame.font.SysFont('arial', 20),
                                   'Alignment Factor:    {:.2f}'.format(round(params['align_factor'], 2)))

def adj_align_factor_func():
    params.update({'align_factor' : max(0, min(0.5, adjs['delta_align_factor'] + params['align_factor']))})
    align_factor_tag.set_text('Alignment Factor:    {:.2f}'.format(round(params['align_factor'], 2)))
    align_factor_tag.__build__()
    pygame.time.wait(150)

adjust_align_factor = Button([0, 0],
                             [255, 0, 0],
                             pygame.font.SysFont('arial', 20),
                             'Adjust Alignment Factor',
                             [0, 255, 0],
                             [30, 10],
                             on_hold = adj_align_factor_func)

toggle_align_factor_adj_direction = ToggleButton([0, 0],
                                                 [[255, 0, 0], [0, 255, 0]],
                                                 pygame.font.SysFont('arial', 20),
                                                 ['INCREASE', 'DECREASE'],
                                                 [30, 10],
                                                 on_click = lambda: adjs.update({'delta_align_factor' : adjs['delta_align_factor'] * -1.0}))

toggle_delta_align_factor = ToggleButton([0, 0],
                                         [[255, 0, 0], [255, 0, 0], [255, 0 ,0]],
                                         pygame.font.SysFont('arial', 20),
                                         ['0.01', '0.1'],
                                         [30, 10],
                                         on_click = lambda: adjs.update({'delta_align_factor' : 0.1 * np.sign(adjs['delta_align_factor'])})
                                                               if -0.05 < adjs['delta_align_factor'] < 0.05 else
                                                               adjs.update({'delta_align_factor' : 0.01 * np.sign(adjs['delta_align_factor'])}))

align_factor_row = RowBorder([window_size[0]//4, 520],
                             [0,255, 255],
                             950,
                             10,
                             [align_factor_tag, adjust_align_factor, toggle_align_factor_adj_direction, toggle_delta_align_factor])
