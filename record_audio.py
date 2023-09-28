from os.path import exists, join
from os import makedirs
from pyaudio import paInt16
from wave import open
from audioop import rms
from time import time, strftime, sleep
from wisper import speak
from logging import getLogger
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)
class Config:
    logger.info("Configuring")
    FRAME_SIZE = 704  # adjust frame size
    RATE = 16000 #44100
    CHANNELS = 1
    FORMAT = paInt16  # 16 bit int
    THRESHOLD_REC = 250  #600 The threshold for volume
    SILENCE_LIMIT = 5  # Silence limit in seconds
    RECORD_LIMIT = 60  # Record limit in seconds
    START_SILENCE_LIMIT = 10  # Start silence limit in seconds

def record_audio(filename, p):
    logger.info("Recording audio...")
    #p = pyaudio.PyAudio()
    speak("Задайте вопрос")
    stream = p.open(input_device_index=0,format=Config.FORMAT,
                                channels=Config.CHANNELS,
                                rate=Config.RATE,
                                input=True,
                                frames_per_buffer=Config.FRAME_SIZE)
    logger.info("Waiting for signal...")
    print("Waiting for signal...")
    recording = []
    started = False
    silence_start = None
    noise_detected = False
    start_time = time()

    while True:
        try:
            # Read the frame from the stream
            frame = stream.read(Config.FRAME_SIZE)
            if not frame:
                logger.info("No frame")
                break

            # Calculate the volume of the frame
            volume = rms(frame, 2)
            recording.append(frame)
            print(f"\rCurrent volume: {volume}")
            if not started:
                if volume >= Config.THRESHOLD_REC:
                    noise_detected = True
                    logger.info("Recording started...")
                    print("Recording started...")
                    started = True
                elif time() - start_time >= Config.START_SILENCE_LIMIT and not noise_detected:
                    logger.info("No signal detected.")
                    print("No signal detected.")
                    # Stop and close the stream
                    stream.stop_stream()
                    stream.close()
                    sleep(5)
                    return False
                elif noise_detected:
                    logger.info("Recording started 2...")
                    print("Recording started 2...")
                    started = True

            if started:
                if volume < Config.THRESHOLD_REC:
                    if silence_start is None:
                        logger.info("Silence detected...")
                        silence_start = time()
                        
                    elif time() - silence_start > Config.SILENCE_LIMIT:
                        logger.info("Silence limit reached, stopping recording...")
                        break
                else:
                    silence_start = None
                

                if len(recording)*Config.FRAME_SIZE/Config.RATE > Config.RECORD_LIMIT:
                    logger.info("Record limit reached, stopping recording...")
                    break
        except IOError as e:
            # This is the error code for an input overflowed error
            if e.errno == -9981:
                logger.info("Input overflowed, skipping this frame.")
                print("Input overflowed, skipping this frame.")
                continue
            # This is the error code for a stream closed error
            elif e.errno == -9988:
                logger.info("Stream closed, trying to reopen.")
                print("Stream closed, trying to reopen.")
                stream = p.open(format=Config.FORMAT,
                                channels=Config.CHANNELS,
                                rate=Config.RATE,
                                input=True,
                                frames_per_buffer=Config.FRAME_SIZE)
                
                continue
            else:
                logger.info(f"missed {e}")
                print(f"missed {e}")
                # Stop and close the stream
                stream.stop_stream()
                stream.close()
                return False
        except Exception as e:
            logger.info(f"missed {e}")
            print(f"missed {e}")
            # Stop and close the stream
            stream.stop_stream()
            stream.close()
            return False
    logger.info("Recording stopped.")
    print("Recording stopped.")
    speak("Хорошо")
    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Save recording to WAV file
    logger.info("Saving recording to file...")
    wf = open(filename, 'wb')
    wf.setnchannels(Config.CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(Config.RATE)
    wf.writeframes(b''.join(recording))
    wf.close()
    logger.info("Recording saved.")
    return True

def get_question(p):
    timestamp = strftime("%Y%m%d_%H%M%S")
    rec_dir = "records"
    if not exists(rec_dir):
        makedirs(rec_dir)
    output_path = join(rec_dir,f"question_{timestamp}.wav")
    result = record_audio(output_path, p)

    logger.info(f"Recorded question: {result}")
    return output_path if result else False

if __name__ == "__main__":
    from pyaudio import PyAudio
    p = PyAudio()

    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device ID:", i)
            print(p.get_device_info_by_host_api_device_index(0, i).get('name'))

    question_path = get_question(p)
    if question_path:
        print("Question saved in the file:", question_path)
    else:
        print("No question recorded.")

