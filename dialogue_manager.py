#  dialogue_manager.py 
from record_audio import get_question
from wisper import OpenAITranscriber, speak
from chatGPT import call_chatgpt
from database import get_cached_answer, cache_answer
from os import remove
from logging import getLogger
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)
def run_your_function(p):
    logger.info("run_your_function")
    word = "Манго!"
    question = get_question(p)
    if question:
        logger.info("question")
        speak("Услышал ваш вопрос, перевожу в текст..")
        transcriber = OpenAITranscriber()
        transcription = transcriber.transcribe_audio(question)
        
        remove(question)
        if transcription:
            logger.info("transcription")
            speak(f"Вы сказали, {transcription}. Сейчас спрошу у Манго..")
            print("Вопрос: {transcription}")
            fast_model = True
            # Проверка наличия ответа в кэше
            if transcription.lower().startswith("ты умная"):#быстро"):
                logger.info("fast_model")
                fast_model = False
                transcription = transcription[7:]
            """s1 = transcription.lower().startswith("покажи картинку")
            s2 = transcription.lower().startswith("покажи большую картинку")
            s3 = transcription.lower().startswith("покажи маленькую картинку")"""
            """           if s1 or s2 or s3:
                fast_model = True
                size = 1024
                if s1:
                    #transcription = transcription[16:]
                    size = 512
                elif s2:
                    size = 1024
                    #transcription = transcription[25:]
                elif s3:
                    size = 256
                    #transcription = transcription[26:]
                speak("Перевожу на английский..")
                transcription_en = call_chatgpt(f"Напиши на английском короткое описание картинки, которую имел ввиду пользователь таким запросом: '{transcription}' Только описание картинки без просьбы. Можно одну фразу от себя добавить к описанию, усиливающую данное пользователем описание.", model="gpt-3.5-turbo")
                if s1:
                    transcription = transcription[16:]
                elif s2:
                    transcription = transcription[25:]
                elif s3:
                    transcription = transcription[26:]
                #transcription_en = call_chatgpt(f"Переведи на английский: {transcription}", model="gpt-3.5-turbo")
                if not transcription_en:
                    speak(f"Возникла непредвиденная ошибка. Попробуйте переформулировать вопрос. Не забудьте сначала сказать {word}")   
                    
                    return None
                discription =  call_chatgpt(f"Переведи на русский следующий текст: '{transcription_en}'", model="gpt-3.5-turbo")
                speak("Показываю картинку")
                api_key = os.getenv("LEONARDO_API_KEY")
                generator = LeonardoService(api_key)
                image_path = generator.generate(prompt=f"{transcription_en}, photorealistic, ultraphotorealistic", size=size)#"1024x1024"256x256, 512x512
                if not image_path:
                    speak(f"Возникла непредвиденная ошибка. Попробуйте переформулировать вопрос. Не забудьте сначала сказать {word}")
                    return None
                # Открываем изображение
                img = Image.open(image_path)
                # Отображаем изображение
                img.show()
                if discription:
                    speak(f"Вот {discription}.")
                else:
                    speak(f"Вот {transcription}.")
                """          """if response:
                    # Process the response
                    if 'data' in response and isinstance(response['data'], list):
                        for idx, image_data in enumerate(response['data']):
                            if 'url' in image_data:
                                image_url = image_data['url']
                                save_path = f"image_{idx}.jpg"  # Specify the desired save path and file name
                                generator.save_image_from_url(image_url, save_path)
                                print("Generated image saved:", save_path)
                                # Открываем изображение
                                img = Image.open(save_path)
                                # Отображаем изображение
                                img.show()
                                speak(f"Вот {transcription}.")
                                transcription = f"Коротко расскажи про: {transcription}"
                            elif 'b64' in image_data:
                                # Process the base64-encoded image data as needed
                                print("Generated image (base64):", image_data['b64'])
                                speak(f"Возникла непредвиденная ошибка. Попробуйте переформулировать вопрос. Не забудьте сначала  сказать {word}")
                    else:
                        print("Unexpected response format:", response)
                        speak(f"Возникла непредвиденная ошибка. Попробуйте переформулировать вопрос. Не забудьте сначала сказать {word}")
                else:
                    speak(f"Возникла непредвиденная ошибка. Попробуйте переформулировать вопрос. Не забудьте сначала сказать {word}")"""

            
            #cached_answer = get_cached_answer(transcription, fast_model)
            #if cached_answer:
            #    response = cached_answer
            #    speak(response)
            #    speak(f"Если захотите спросить еще - скажите {word}")
            #else:
            if fast_model:
                response = call_chatgpt(f"{transcription}.", model="gpt-3.5-turbo")
                logger.info("fast_model")
                # В начала ответа пиши 'Алиса,', а потому уже ответ"
            else:
                response = call_chatgpt(transcription)
                logger.info("not fast_model")
            if response:
                logger.info("response")
                #cache_answer(transcription, response, fast_model)
                speak(f"Алиса ответила следующее: {response}")
                print(f"Ответ: {response}")
                #speak(f"Если захотите спросить еще - скажите {word}")#хлопните 2 раза.")
            else:
                logger.info("not response")
                speak(f"Возникла непредвиденная ошибка. Попробуйте переформулировать вопрос.")# Не забудьте сначала сказать {word}")

