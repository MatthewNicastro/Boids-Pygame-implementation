from config import window_size
from config import params
from settings_ui.setting_config import adjs

from pygameui.clickable.button import Button
from pygameui.clickable.toggle_button import ToggleButton
from pygameui.text_object import TextObject
from pygameui.row_border import RowBorder

import pygame

min_dist_tag = TextObject([0,0],
                          [255, 0, 0],
                          pygame.font.SysFont('arial', 20),
                          'Minimum distance(px):    {}'.format(params['min_dist']))

def adj_min_dist_func():
    params.update({'min_dist' : max(20, min(50, adjs['delta_min_dist'] + params['min_dist']))})
    min_dist_tag.set_text('Minimum distance(px):    {}'.format(params['min_dist']))
    min_dist_tag.__build__()
    pygame.time.wait(150)

adjust_min_dist = Button([0, 0],
                          [255, 0, 0],
                          pygame.font.SysFont('arial', 20),
                          'Adjust Min Distance',
                          [0, 255, 0],
                          [30, 10],
                          on_hold = adj_min_dist_func)

toggle_min_dist_adj_direction = ToggleButton([0, 0],
                                             [[255, 0, 0], [0, 255, 0]],
                                             pygame.font.SysFont('arial', 20),
                                             ['INCREASE', 'DECREASE'],
                                             [30, 10],
                                             on_click = lambda: adjs.update({'delta_min_dist' : adjs['delta_min_dist'] * -1}))

min_dist_row = RowBorder([window_size[0]//4, 240],
                          [0,255, 255],
                          950,
                          10,
                          [min_dist_tag, adjust_min_dist, toggle_min_dist_adj_direction])
