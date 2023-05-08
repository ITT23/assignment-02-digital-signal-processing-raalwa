'''
This module triggers Keyboard events based on audio input

Whisteled upward chirps lead to arrow up events, downward chirps to arrow down events.
This module also provides a demo to select list items via audio input.
'''
import pyglet
import pyaudio
import numpy as np
from scipy import signal
from enum import Enum
import config
from sklearn.linear_model import LinearRegression
from pynput.keyboard import Key, Controller
import box

window = pyglet.window.Window(
        width=config.WINDOW_WIDTH,
        height=config.WINDOW_HEIGHT)

background_image = pyglet.resource.image('assets/background.png')

class NavState(Enum):
    '''
    Helper class to indicate whether Keyboard Event should be dispatched
    '''
    DOWN = 0,
    NOTHING = 1,
    UP = 1

def init() -> None:
    '''
    Handles global vars, input selection and audio stream setup
    '''
    global p, input_device, stream, state, last_frequencies, keyboard, boxes, background, batch
    p = pyaudio.PyAudio()

    last_frequencies = np.zeros(10)

    state = NavState.NOTHING

    keyboard = Controller()

    boxes = []

    for i in range(3):
        boxes.append(box.Box(y_position = config.WINDOW_HEIGHT*0.6-i*(config.BOX_HEIGHT+config.SPACING)))

    boxes[0].switch()

    background = pyglet.sprite.Sprite(img=background_image)


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

def calculate_frequency(data: bytes) -> int:
    '''
    Uses raw audio data to compute major frequency

    Args:
        data (bytes): Raw data from PyAudio.Stream.read()
    
    Returns:
        int: major frequency in audio segment
    '''
    # transform into np array:
    data = np.frombuffer(data, dtype=np.int16)

    # filter out frequencies above 500Hz
    filter = signal.butter(1, 500 ,btype='low',analog=False,output='sos',fs=config.RATE)
    filtered = signal.sosfilt(filter, data)

    # filter out noise with gaussion transformation:
    kernel = signal.gaussian(config.KERNEL_SIZE, config.KERNEL_SIGMA)
    kernel /= np.sum(kernel)

    gauss_data = np.convolve(filtered, kernel, 'same')

    spectrum = np.abs(np.fft.fft(gauss_data))
    frequencies = np.fft.fftfreq(len(gauss_data), 1/config.RATE)

    mask = frequencies >= 0
    freq = np.argmax(spectrum[mask])

    return freq

def calculate_trend() -> None:
    '''
    Uses last 10 non silent audio inputs to find trend via linear regression
    '''
    global last_frequencies, state
    if (last_frequencies > 10).sum() > 9:
        # https://realpython.com/linear-regression-in-python/#simple-linear-regression
        model = LinearRegression().fit(config.LAST_VALUES_COUNTER, last_frequencies)
        trend = model.coef_
        if trend > 0:
            state = NavState.UP
        else:
            state = NavState.DOWN
        last_frequencies.fill(0)
    else:
        state = NavState.NOTHING

def handle_navigation() -> None:
    '''
    Dispatches Keyboard Events according to upward or downward chirp
    '''
    global state
    if state == NavState.UP:
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    if state == NavState.DOWN:
        keyboard.press(Key.down)
        keyboard.release(Key.down)
    state = NavState.NOTHING

def append_frequency(freq: int) -> None:
    '''
    Saves latest audio frequency and drops oldest record
    '''
    global last_frequencies
    last_frequencies[0] = freq
    last_frequencies = np.roll(last_frequencies, -1)

@window.event
def on_key_press(symbol, modifiers) -> None:
    '''
    Catches arrow up and down Keyboard Events and selects list items accordingly
    '''
    global boxes
    if symbol == pyglet.window.key.UP:
        for i, box in enumerate(boxes):
            if box.is_selected:
                index = i
        boxes[index-1].switch()
        boxes[index].switch()
    if symbol == pyglet.window.key.DOWN:
        for i, box in enumerate(boxes):
            if box.is_selected:
                index = i
        boxes[(index+1)%3].switch()
        boxes[index].switch()

@window.event
def on_draw() -> None:
    '''
    Handler for pyglet.windows.on_draw() event
    '''
    window.clear()
    background.draw()
    data = stream.read(config.CHUNK_SIZE)
    freq = calculate_frequency(data=data)
    append_frequency(freq=freq)
    calculate_trend()
    handle_navigation()
    for box in boxes:
        box.update()

if __name__ == '__main__':
    init()
