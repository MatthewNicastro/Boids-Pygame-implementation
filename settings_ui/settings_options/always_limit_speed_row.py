from config import window_size
from config import params

from pygameui.clickable.toggle_button import ToggleButton
from pygameui.text_object import TextObject
from pygameui.row_border import RowBorder

import pygame

always_limit_speed_tag = TextObject([0,0], 
                                    [255, 0, 0],
                                    pygame.font.SysFont('arial', 20),
                                    'Always Limit Speed:   ')

toggle_always_limit_speed = ToggleButton([0, 0],
                                         [[255, 0, 0], [255, 0, 0]], 
                                         pygame.font.SysFont('arial', 20), 
                                         ['ACTIVE', 'INACTIVE'],
                                         [30, 10],
                                         on_click = lambda: params.update({'always_limit_speed' : False})
                                                             if params['always_limit_speed'] else
                                                             params.update({'always_limit_speed' : True}))

always_limit_speed_row = RowBorder([window_size[0]//4, 590],
                                   [0, 255, 255],
                                   950,
                                   10,
                                   [always_limit_speed_tag, toggle_always_limit_speed])