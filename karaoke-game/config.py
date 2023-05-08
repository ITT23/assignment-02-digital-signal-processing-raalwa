import pyaudio
from enum import Enum

# Set up audio stream
# reduce chunk size and sampling rate for lower latency
CHUNK_SIZE = 8192  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Audio sampling rate (Hz)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
KERNEL_SIZE = 5
KERNEL_SIGMA = 3
MIDI_PATH = "karaoke-game/assets/song.mid"
GAME_AREA_LOWER_Y = 100
GAME_AREA_UPPER_Y = 500
FREQUENCY_CUTOFF = 500
PLAYER_COLOR = (255,215,0)
DEFAULT_COLOR = (0,0,0,200)

class GameState(Enum):
    START = 1
    END = 2