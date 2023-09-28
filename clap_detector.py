#  clap_detector.py
from pyaudio import paInt16
from audioop import rms
from time import time
from collections import deque
from logging import getLogger
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)
class Config:
    FORMAT = paInt16
    CHANNELS = 1
    RATE = 44100
    FRAME_SIZE = 704  # Adjusted frame size
    THRESHOLD = 1000
    FON = 300
    CLAP_INTERVAL = 0.6
    IGNORE_TIME = 0.15
    VOLUME_DROP_TIME = 0.3 
    VOLUME_AVERAGE_LENGTH = 0.1
    VOLUME_AVERAGE_LENGTH_FRAMES = int(RATE * VOLUME_AVERAGE_LENGTH / FRAME_SIZE)
    MAX_BAR_LENGTH = 100
    CLAP_DURATION = (0.1, 0.2)
    CLAP_VOLUME = (1500, 10000)
    BACKGROUND_NOISE = (300, 400)

class ClapDetector:
    def __init__(self, p):
        self.audio = p #pyaudio.PyAudio()
        while not self.is_device_available():
            print("not available")
            
        self.stream = self.audio.open(format=Config.FORMAT,
                                      channels=Config.CHANNELS,
                                      rate=Config.RATE,
                                      input=True,
                                      frames_per_buffer=Config.FRAME_SIZE,
                                      input_device_index=3)  # Added input_device_index parameter

        self.last_clap = None
        self.ignore_until = None
        self.high_volume_start = None
        self.volumes = deque(maxlen=Config.VOLUME_AVERAGE_LENGTH_FRAMES)

        self.double_clap_count = 0
        self.long_sounds_count = 0
        self.peak_volume = 0
        self.new_clap = False
        self.sound_duration = 0
        self.double_clap_duration = 0
        self.claps_count = 0

    def is_device_available(self):
        try:
            info = self.audio.get_device_info_by_index(3)
            if info and info.get('maxInputChannels')>0:

                return True
            else:
                return False
        except:
            return False

    def detect_claps(self):
        try:
            while True:
                try:
                    frame = self.stream.read(Config.FRAME_SIZE, exception_on_overflow=False)
                    if not frame:
                        break  # Exit the loop if there are no more frames to read
                    volume = rms(frame, 2)
                    self.volumes.append(volume)
                    average_volume = sum(self.volumes) / len(self.volumes)
                    if volume > Config.THRESHOLD and self.new_clap:
                        self.peak_volume = volume
                        self.new_clap = False
                        self.claps_count += 1
                    elif volume > self.peak_volume:
                        self.peak_volume = max(volume, self.peak_volume)

                    self.display_status(average_volume)

                    current_time = time()
                    if self.check_for_claps(current_time, volume, average_volume):
                        return True
                    #self.stop_stream()
                except IOError as e:
                    # This is the error code for an input overflowed error
                    if e.errno == -9981:
                        print("Input overflowed, skipping this frame.")
                        continue
                    # This is the error code for a stream closed error
                    elif e.errno == -9988:
                        print("Stream closed, trying to reopen.")
                        self.stream = self.audio.open(format=Config.FORMAT,
                                        channels=Config.CHANNELS,
                                        rate=Config.RATE,
                                        input=True,
                                        frames_per_buffer=Config.FRAME_SIZE,
                                        input_device_index=3)
                        
                        continue
                    else:
                        print(f"missed {e}")
                        return False
                except Exception as e:
                     print("Error: ", e)
                     #self.stop_stream()
        finally:
	    

            self.stop_stream()


    def check_for_claps(self, current_time, volume, average_volume):

        if volume > Config.THRESHOLD and self.high_volume_start is None and average_volume > Config.FON:
            self.high_volume_start = current_time
            self.new_clap = True

        if volume < Config.FON and self.high_volume_start is not None:
            sound_duration = current_time - self.high_volume_start
            if sound_duration < Config.VOLUME_DROP_TIME:
                if self.new_clap:
                    self.new_clap = False
                    self.claps_count += 1
                    self.peak_volume = max(self.volumes)
                    self.sound_duration = sound_duration
                if self.last_clap and current_time - self.last_clap < Config.CLAP_INTERVAL:
                    self.double_clap_count += 1
                    print("Double clap detected!")
                    self.last_clap = None
                    self.ignore_until = current_time + Config.IGNORE_TIME
                    self.double_clap_duration = sound_duration
                    #self.stop_stream()
                    # Add this to run your function
                    print("detected")
                    self.stop_stream()
                    return True
                    
                    # Reset accumulated frames
                    self.volumes.clear()
                    self.stream.read(self.stream.get_read_available(), exception_on_overflow=False)
            
                else:
                    self.last_clap = current_time
                    self.ignore_until = current_time + Config.IGNORE_TIME
            elif sound_duration > Config.CLAP_DURATION[1]:
                print("Long sound detected!")
                self.long_sounds_count += 1

            self.high_volume_start = None


    def display_status(self, average_volume):
        bar_length = min(int(average_volume / 50), Config.MAX_BAR_LENGTH)
        bar = '|' * bar_length
        max_volume = max(self.volumes)
        min_volume = min(self.volumes)
        
        print("\033c", end="")
        print(f"Max volume: {max_volume} \n Min volume: {min_volume} \n Current average volume: {average_volume} \n{bar}")
        print(f"Peak volume: {self.peak_volume}")
        print(f"Total claps detected: {self.claps_count}")
        print(f"Double claps detected: {self.double_clap_count}")
        print(f"Last sound duration: {self.sound_duration} seconds")
        print(f"Double clap duration: {self.double_clap_duration} seconds")

    def stop_stream(self):
        try:
            self.stream.stop_stream()
            self.stream.close()
            #self.audio.terminate()
        except:
            print ("alredy done")

