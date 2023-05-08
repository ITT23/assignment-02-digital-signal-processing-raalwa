'''
This module represents the whisteled note of a player as a pyglet.shapes.Circle
'''
import pyglet
import config

class Note:
    def __init__(self, x_position: int, radius: int, max_freq: int):
        '''
        Sets up pyglet Circle

        Args:
            x_position (int): Fixed x starting postition of circle
            radius (int): Radius of circle
            max_freq (int): Only frequencies below this cutoff are considered
        '''
        self.y_lower_bound = config.GAME_AREA_LOWER_Y
        self.shape = pyglet.shapes.Circle(x=x_position,y=self.y_lower_bound,radius=radius, color = config.PLAYER_COLOR)
        self.y_distance = config.GAME_AREA_UPPER_Y - self.y_lower_bound
        self.max_freq = max_freq

    def update(self, freq: int):
        '''
        Renders Circle and updates height according to frequency

        Args:
            freq (int): Whisteled frequency 
        '''
        if freq > self.max_freq:
            freq = self.max_freq
        updated_position = self.y_lower_bound + self.y_distance*(freq/self.max_freq)
        if freq > 50:
            self.shape.y = updated_position
        else:
            self.shape.y = self.y_lower_bound
        self.shape.draw()