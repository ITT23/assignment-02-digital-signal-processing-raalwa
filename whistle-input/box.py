'''
This module defines pyglet Rectangles which act as list elements
'''

import pyglet
import config

class Box():
    def __init__(self, y_position: int):
        '''
        Sets up pyglet Rectangle and default state if list elements is selected

        Args:
            y_position (int): defines position at which rectangle should be drawn
        '''
        self.shape = pyglet.shapes.Rectangle(x = config.WINDOW_WIDTH/2 - config.BOX_WIDTH/2,
                                                y = y_position,
                                                width=config.BOX_WIDTH,
                                                height=config.BOX_HEIGHT,
                                                color=config.DEFAULT_COLOR)
        self.is_selected = False

    def update(self):
        '''
        Renders Rectangle and changes color if rectangle is selected
        Called every on_draw() cycle in whistle_input.py
        '''
        if self.is_selected:
            self.shape.color = config.HIGHLIGHT_COLOR
        else:
            self.shape.color = config.DEFAULT_COLOR
        self.shape.draw()

    def switch(self):
        '''
        Switches between selection states
        '''
        self.is_selected =  not self.is_selected