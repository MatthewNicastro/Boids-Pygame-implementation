from config import window_size
from config import params
from settings_ui.setting_config import adjs

from pygameui.clickable.button import Button
from pygameui.clickable.toggle_button import ToggleButton
from pygameui.text_object import TextObject
from pygameui.row_border import RowBorder

import pygame


max_speed_tag = TextObject([0,0],
                           [255,0,0],
                           pygame.font.SysFont('arial', 20),
                           'Max Speed(px):    {}'.format(params['max_speed']))

def adj_max_speed_func():
    params.update({'max_speed' : max(1, min(30, params['max_speed'] + adjs['delta_max_speed']))})
    max_speed_tag.set_text('Max Speed(px):    {}'.format(params['max_speed']))
    max_speed_tag.__build__()
    pygame.time.wait(150)

adjust_max_speed = Button([0, 0],
                          [255, 0, 0],
                          pygame.font.SysFont('arial', 20),
                          'Adjust Speed',
                          [0, 255, 0],
                          [30, 10],
                          on_hold = adj_max_speed_func)

toggle_max_speed_adj_direction = ToggleButton([0, 0],
                                              [[255, 0, 0], [0, 255, 0]],
                                              pygame.font.SysFont('arial', 20),
                                              ['INCREASE', 'DECREASE'],
                                              [30, 10],
                                              on_click = lambda: adjs.update({'delta_max_speed' : adjs['delta_max_speed'] * -1}))
max_speed_row = RowBorder([window_size[0]//4, 100],
                          [0,255, 255],
                          950,
                          10,
                          [max_speed_tag, adjust_max_speed, toggle_max_speed_adj_direction])
