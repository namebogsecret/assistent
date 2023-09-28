
import os
import requests
from dotenv import load_dotenv
#import pyttsx3
from time import sleep
from logging import getLogger
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)


load_dotenv()

class OpenAITranscriber:
    def __init__(self, model="whisper-1", language="ru"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        self.model = model
        self.language = language
        self.api_url = "https://api.openai.com/v1/audio/transcriptions"
        self.api_url_en = "https://api.openai.com/v1/audio/translations"
        logger.info(f"Setting OpenAITrancriver")
        


    def transcribe_audio(self, file_path, in_english=False):
        logger.debug(f"Transcribing audio in {file_path}")
        with open(file_path, 'rb') as audio_file:
            if in_english:
                logger.info(f"Transcribing audio in english")
                url = self.api_url_en
                data = {
                    "model": self.model
                }
            else:
                logger.info(f"Transcribing audio in russian")
                url = self.api_url
                data = {
                    "model": self.model,
                    "language": self.language
                }
            
            files = {
                "file": audio_file,
            }
            
            response = requests.post(url, headers=self.headers, data=data, files=files)

            if response.status_code == 200:
                logger.info(f"Transcription successfull")
                return response.json().get("text")
            else:
                logger.error(f"Transcription failed with status code {response.status_code}")
                return False

def speak(text, voice='Milena'):
    logger.info(f"Speaking text: {text}")
    os.system(f"say -v Milena '{text}'")
    #os.system(f"say -v '{voice}' '{text}'")
"""
def speak7(text):
    os.system(f"espeak -vru -k5 -s150 '{text}'")
    
def speak2(text):
    os.system(f"echo '{text}' | festival --tts --language russian")

def speak4(text):
    os.system(f'echo {text} | RHVoice-test')

def speak5(text, voice='Anna', language='Russian'):
    os.system(f'echo {text} | RHVoice-test -p {voice} -v {language}')


def speak3(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'russian')
    engine.say(text)
    engine.runAndWait()
    #engine.stop()

def speak6(text, voice="umka", language="Russian"):
    profile = f"{language}/{voice}"
    os.system(f'echo "{text}" | RHVoice-test -p {voice}')"""
    
def speak_(text, voice="aleksandr"):#anatol"):#arina"):
    logger.info(f"Speaking text: {text}")
    #profile = f"{language}/{voice}"
    #os.system(f'echo "{text}" | RHVoice-test -p {voice}')

    os.system(f'echo "{text}" | RHVoice-test -p {voice}')# -o /home/vladimir/Assistent/output.wav')

    #os.system("aplay /home/vladimir/Assistent/output.wav")
    #os.system("aplay /home/vladimir/Assistent/output.wav")
"""
def speak8(text):
    # инициализация pyttsx3
    engine = pyttsx3.init()

    # установка голоса
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'rhvoice' in voice.id:
            engine.setProperty('voice', voice.id)
            break
        print(f"{voice.id} voice.id, {voice.name} voice.name, {voice.languages} voice.languages")"""
"""
def say_test(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"Voice: {voice.name}, ID: {voice.id}, Languages: {voice.languages}, ")
        if 'russian' in voice.languages:  # find a Russian voice
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()"""

"""
Albanian              Czech    Esperanto  Macedonian  Russian  Ukrainian
Brazilian-Portuguese  English  Kyrgyz     Polish      Tatar    Uzbek
vladimir@raspberrypi:~ $ ls /usr/local/share/RHVoice/voices/
alan          artemiy      evgeniy-rus   marianna  sevinch   umka        zdenek
aleksandr     azamat       hana          michal    slt       victoria
aleksandr-hq  bdl          irina         mikhail   spomenka  vitaliy
alicja        cezary       kiko          natalia   suze      vitaliy-ng
anatol        clb          Leticia-F123  natan     talgat    volodymyr
anna          elena        lyubov        nazgul    tatiana   vsevolod
arina         evgeniy-eng  magda         pavel     timofey   yuriy"""

if __name__ == "__main__":
    transcriber = OpenAITranscriber()
    #test = transcriber.transcribe_audio("/Volumes/Cache/VsCode/test/question_20230609_175538.wav", in_english=True)
    #print(test)
    #sleep(10)
    #text = "Я вас люблю!"
    #speak(text)
    """speak2(text)
    speak3(text)
    speak4(text)
    speak5(text)
    speak6(text)
    speak7(text)"""
    """voices = ["alan", "artemiy", "evgeniy-rus", "marianna", "sevinch", "umka", "zdenek", "aleksandr", "azamat",
          "hana", "michal", "slt", "victoria", "aleksandr-hq", "bdl", "irina", "mikhail", "spomenka", "vitaliy",
          "alicja", "cezary", "kiko", "natalia", "suze", "vitaliy-ng", "anatol", "clb", "Leticia-F123", "natan",
          "talgat", "volodymyr", "anna", "elena", "lyubov", "nazgul", "tatiana", "vsevolod", "arina", "evgeniy-eng",
          "magda", "pavel", "timofey", "yuriy"]"""
    voices = ["aleksandr", "timofey"]#, "victoria"] # "victoria", "arina",
    test = "Я вас люблю!"
    for voice in voices:
        print (voice)
        speak(f"А сейчас хочу рассказать о себе, я проводник чата джипити. Вы можете задавать любые вопросы и я постараюсь на них ответить. Меня зовут {voice}.", voice=voice)
        #speak(f"{test} Меня зовут {voice}. I love you. I'm {voice}.", voice=voice)
        
    #speak8(text="Я вас люблю!")