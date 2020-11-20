from config import window_size
from config import params
from settings_ui.setting_config import adjs

from pygameui.clickable.button import Button
from pygameui.clickable.toggle_button import ToggleButton
from pygameui.text_object import TextObject
from pygameui.row_border import RowBorder

import numpy as np
import pygame

cohesion_factor_tag = TextObject([0,0],
                                 [255, 0, 0],
                                 pygame.font.SysFont('arial', 20),
                                 'Cohesion Factor:    {:.2f}'.format(round(params['cohesion_factor'], 2)))

def adj_cohesion_factor_func():
    params.update({'cohesion_factor' : max(0, min(0.99, adjs['delta_cohesion_factor'] + params['cohesion_factor']))})
    cohesion_factor_tag.set_text('Cohesion Factor:    {:.2f}'.format(round(params['cohesion_factor'], 2)))
    cohesion_factor_tag.__build__()
    pygame.time.wait(150)

adjust_cohesion_factor = Button([0, 0],
                          [255, 0, 0],
                          pygame.font.SysFont('arial', 20),
                          'Adjust Cohesion Factor',
                          [0, 255, 0],
                          [30, 10],
                          on_hold = adj_cohesion_factor_func)

toggle_cohesion_factor_adj_direction = ToggleButton([0, 0],
                                               [[255, 0, 0], [0, 255, 0]],
                                               pygame.font.SysFont('arial', 20),
                                               ['INCREASE', 'DECREASE'],
                                               [30, 10],
                                               on_click = lambda: adjs.update({'delta_cohesion_factor' : adjs['delta_cohesion_factor'] * -1}))

toggle_delta_cohesion_factor = ToggleButton([0, 0],
                                            [[255, 0, 0], [255, 0, 0], [255, 0 ,0]],
                                            pygame.font.SysFont('arial', 20),
                                            ['0.01', '0.1'],
                                            [30, 10],
                                            on_click = lambda: adjs.update({'delta_cohesion_factor' : 0.1 * np.sign(adjs['delta_cohesion_factor'])})
                                                               if -0.05 < adjs['delta_cohesion_factor'] < 0.05 else
                                                               adjs.update({'delta_cohesion_factor' : 0.01 * np.sign(adjs['delta_cohesion_factor'])}))

cohesion_factor_row = RowBorder([window_size[0]//4, 380],
                                [0,255, 255],
                                950,
                                10,
                                [cohesion_factor_tag, adjust_cohesion_factor, toggle_cohesion_factor_adj_direction, toggle_delta_cohesion_factor])
