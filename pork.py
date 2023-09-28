
import pvporcupine
import pyaudio
import struct
import os
#import resampy
from logging import getLogger
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)

MODEL_FILE_PATH = "/Volumes/Untitled/Assistent/clap_gpt/models/porcupine_params_ru.pv"
KEYWORD_FILE_PATH = "/Volumes/Untitled/Assistent/clap_gpt/models/jarvis.ppn"
KEYWORD_FILE_PATH_4 = "/Volumes/Untitled/Assistent/clap_gpt/models/mango_en_raspberry-pi_v2_2_0.ppn"
KEYWORD_FILE_PATH_5 = "/Volumes/Untitled/Assistent/clap_gpt/models/mango_en_mac_v2_2_0.ppn"
KEYWORD_FILE_PATH_3 = "/Volumes/Untitled/Assistent/clap_gpt/models/alisa.ppn"
KEYWORD_FILE_PATH_2 = "/Volumes/Untitled/Assistent/clap_gpt/models/adamant.ppn"
ACCESS_KEY = os.getenv("porcupine_api")

"""class Config:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100 #16000  # Porcupine requires a sample rate of 16000
    FRAME_LENGTH = 512  # Porcupine processes 512 samples at a time"""
class Config:
    logger.info("Configuring...")
    # 16-bit int format
    FORMAT = pyaudio.paInt16
    # Mono
    CHANNELS = 1
    # Sample rate (44100 for high-quality, 16000 for voice recognition)
    RATE = 44100
    # Number of samples per frame
    FRAME_LENGTH = 512

class WakeWordDetector:
    def __init__(self, p):
        logger.info("Initializing...")
        self.audio = p
        self.porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            #keywords=['picovoice', 'bumblebee']
            keyword_paths=[KEYWORD_FILE_PATH_5]#KEYWORD_FILE_PATH_3],#,KEYWORD_FILE_PATH,KEYWORD_FILE_PATH_2],
            #model_path= MODEL_FILE_PATH
        )
        logger.info("Initialized!")
        self.stream = self.audio.open(
            rate=Config.RATE,
            channels=Config.CHANNELS,
            format=Config.FORMAT,
            input=True,
            frames_per_buffer=Config.FRAME_LENGTH
        )
        logger.info("Stream opened!")
    
    """def preprocess_audio(self, audio):
        # Resample audio to the required sample rate
        resampled_audio = resampy.resample(audio, Config.INPUT_RATE, Config.OUTPUT_RATE)
        return resampled_audio"""
    
    def detect_wake_word(self):
        logger.info("Detecting...")
        try:
            while True:
                pcm = self.stream.read(Config.FRAME_LENGTH)
                pcm = struct.unpack_from("h" * Config.FRAME_LENGTH, pcm)
                #pcm = self.preprocess_audio(pcm) #---
                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    logger.info("Wake word detected!")
                    print("Wake word detected!")
                    return True
        except KeyboardInterrupt:
            logger.info("Stopping...")
        finally:
            self.stop_stream()
            logger.info("Stopped!")

    def stop_stream(self):
        logger.info("Stopping stream...")
        self.stream.stop_stream()
        self.stream.close()
        #self.audio.terminate()
        self.porcupine.delete()

if __name__ == '__main__':
    p = pyaudio.PyAudio()
    detector = WakeWordDetector(p)
    detector.detect_wake_word()
