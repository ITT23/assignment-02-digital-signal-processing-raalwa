'''
This module handles UI, gamelogic and audio input
'''
import pyglet
import pyaudio
import numpy as np
from matplotlib import pyplot as plt
import config
from scipy import signal
import note
import song

window = pyglet.window.Window(
        width=config.WINDOW_WIDTH,
        height=config.WINDOW_HEIGHT)

# all assets from pixabay.com
background_image = pyglet.resource.image('assets/background.png')
endscreen_image = pyglet.resource.image('assets/endscreen.png')

def init():
    '''
    Initializes globals, handles input selection and audio stream setup
    '''
    global p, input_device, stream, this_note, gamestate, this_song, score, score_display, background, endscreen, end_label
    p = pyaudio.PyAudio()

    this_song = song.Song()

    score = 0

    background = pyglet.sprite.Sprite(img=background_image)
    endscreen = pyglet.sprite.Sprite(img=endscreen_image)

    score_display = pyglet.text.Label(text=f"Score: {score}",
                                      font_size=25,
                                      x=10,
                                      y=config.WINDOW_HEIGHT-50)
    
    end_label = pyglet.text.Label(text=f"Score: {score}",
                                      font_size=50,
                                      x=config.WINDOW_WIDTH/2,
                                      y=config.WINDOW_HEIGHT/2,
                                      color=config.DEFAULT_COLOR,
                                      anchor_x='center')

    this_note = note.Note(x_position=config.WINDOW_WIDTH/2, radius=10, max_freq=500)
    gamestate = config.GameState.START
    # print info about audio devices
    # let user select audio device
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    print('select audio device:')
    input_device = int(input())

    stream = p.open(format=config.FORMAT,
                channels=config.CHANNELS,
                rate=config.RATE,
                input=True,
                frames_per_buffer=config.CHUNK_SIZE,
                input_device_index=input_device)
    
    pyglet.app.run()

def calculate_frequency(data):
    '''
    Uses raw audio data to compute major frequency

    Args:
        data (bytes): Raw data from PyAudio.Stream.read()
    
    Returns:
        int: major frequency in audio segment
    '''
    # transform into np array:
    data = np.frombuffer(data, dtype=np.int16)

    spectrum = np.abs(np.fft.fft(data))
    frequencies = np.fft.fftfreq(len(data), 1/config.RATE)

    mask = frequencies >= 0
    freq = np.argmax(spectrum[mask])

    return freq

def check_collision(required_note):
    '''
    Checks whether whisteled note matches required note and updates score accordingly

    Args:
        required_note: pyglet.Rectangle which is used for position calculation
    '''
    global score
    if (this_note.shape.y + this_note.shape.radius) > required_note.y and (this_note.shape.y - this_note.shape.radius) < (required_note.y + required_note.height):
        score += 10

def update_score():
    '''
    Updates score display to show current score
    '''
    score_display.text=f"Score: {score}"
    score_display.draw()

def handle_game_end(is_over: bool):
    '''
    Switches gamestate if song is over

    Args:
        is_over (bool): Indicates whether last note is off screen
    '''
    global gamestate
    if is_over:
        gamestate = config.GameState.END

@window.event
def on_key_press(symbol, modifiers) -> None:
    '''
    Pyglet listener for "R" button to restart game
    '''
    if symbol == pyglet.window.key.R:
        init()

@window.event
def on_draw():
    '''
    Handler for pyglet.windows.on_draw() event
    '''
    window.clear()
    background.draw()
    if gamestate == config.GameState.START:
        data = stream.read(config.CHUNK_SIZE)
        freq = calculate_frequency(data=data)
        this_song.update()
        this_note.update(freq=freq)
        required_note = this_song.check_note_playing()
        if required_note is not None:
            check_collision(required_note)
        update_score()
        handle_game_end(this_song.check_song_over())
    elif gamestate == config.GameState.END:
        endscreen.draw()
        end_label.text = f"{score}"
        end_label.draw()

if __name__ == '__main__':
    init()
