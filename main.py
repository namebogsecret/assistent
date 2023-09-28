# main.py
from clap_detector import ClapDetector
from dialogue_manager import run_your_function
from pyaudio import PyAudio
from pork import WakeWordDetector
from wisper import speak
from logging import getLogger
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)

def is_device_available(p):
    try:
        info = p.get_device_info_by_index(3)
        if info and info.get('maxInputChannels')>0:
            logger.info("Device is available")
            return True
        else:
            logger.info("Device is not available")
            return False
    except:
        return False

if __name__ == '__main__':
    try:
        p = PyAudio()
        speak("Привет, я Манго, готов ответить на любой ваш вопрос. Если захотите спросить - скажите Манго.")# пиковойс или бамбелби!")
        #speak("Jarvis",voice = "alan") #picovoice, bumblebee", voice="alan")
        logger.info("Starting main loop")
        while True:
            if is_device_available(p):
                detector = WakeWordDetector(p)
                if detector.detect_wake_word():
                    logger.info("Wake word detected")
                    run_your_function(p)
                    speak("Если захотите спросить - скажите Манго") #Алиса или Джарвис!")# пиковойс или бамбелби!")
                    #speak("Jarvis", voice="alan")
                #clap_detector = ClapDetector(p)
                #if clap_detector.detect_claps():
                #    run_your_function(p)
            else:
                logger.info("Device is not available")
    finally:
        logger.info("Terminating")
        p.terminate()
