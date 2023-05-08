'''
This module represents a song composed of multiple pyglet rectangles
'''
import pyglet
import config

class Song():
    def frequency_to_y_position(self, freq: int):
        '''
        Maps frequency to y-value

        Args:
            freq (int): Frequency of note

        Result:
            position (int): Corresponding y-value
        '''
        position = self.y_lower_bound + self.y_distance*(freq/self.max_freq)
        return position
    
    def __init__(self) -> None:
        '''
        Sets up list of pyglet rectangles to act as notes

        x position represents, when a note should be "played"
        y position represents, which note should be "played"
        '''
        self.notes = []
        self.y_lower_bound = config.GAME_AREA_LOWER_Y
        self.y_distance = config.GAME_AREA_UPPER_Y - self.y_lower_bound
        self.max_freq = config.FREQUENCY_CUTOFF
        self.note_1 = pyglet.shapes.Rectangle(x=config.WINDOW_WIDTH,
                                              y=self.frequency_to_y_position(216),
                                              width=200,
                                              height=20)
        self.note_2 = pyglet.shapes.Rectangle(x=config.WINDOW_WIDTH + 300,
                                              y=self.frequency_to_y_position(242),
                                              width=200,
                                              height=20)
        self.note_3 = pyglet.shapes.Rectangle(x=config.WINDOW_WIDTH + 600,
                                              y=self.frequency_to_y_position(257),
                                              width=200,
                                              height=20)
        self.notes.append(self.note_1)
        self.notes.append(self.note_2)
        self.notes.append(self.note_3)

        self.note_playing = False
        
    def update(self):
        '''
        Renders notes and moves them to the left
        '''
        for note in self.notes:
            note.x -= 10
            note.draw()

    def check_note_playing(self):
        '''
        Checks if a note is on the players x position

        Returns:
            note:   pyglet.shapes.rectangle object which should be "played"
            |None: Nothing if no note should be "played"
        '''
        for note in self.notes:
            if note.x <= config.WINDOW_WIDTH/2 and (note.x + note.width) >= config.WINDOW_WIDTH/2:
                return note
        return None
    
    def check_song_over(self):
        '''
        Checks if last moved off screen to the left

        Returns:
            True:   Every note off screen and song over
            False:  Notes are still displayed on screen
        '''
        last_note = self.notes[2]
        if (last_note.x + last_note.width) <= 0:
            return True
        else:
            return False