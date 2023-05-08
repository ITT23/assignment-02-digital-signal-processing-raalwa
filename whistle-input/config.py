'''
This module stores defaults values for application
'''
import pyaudio
import numpy as np

# Set up audio stream
# reduce chunk size and sampling rate for lower latency
CHUNK_SIZE = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Audio sampling rate (Hz)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
KERNEL_SIZE = 5
KERNEL_SIGMA = 3
THRESHOLD = 50
LAST_VALUES_COUNTER = np.arange(0,10,1).reshape((-1,1))
DEFAULT_COLOR = (147,191,207)
HIGHLIGHT_COLOR = (96,150,180)
BOX_WIDTH = 150
SPACING = 10
BOX_HEIGHT = 75