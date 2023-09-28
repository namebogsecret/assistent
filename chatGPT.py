
from requests import post, exceptions
import os
from dotenv import load_dotenv
from logging import getLogger
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)
load_dotenv()
def call_chatgpt(prompt, tokens_limit=4096, model="gpt-4", temperature: float=0.9, timeout = 240, addition = ""): #"gpt-3.5-turbo""gpt-4"
    logger.debug(f"Calling chatGPT with prompt: {prompt}")
    key = os.getenv("OPENAI_API_KEY")
    """prompt_tokens = count_tokens(prompt)
    max_model_tokens = tokens_limit
    max_tokens = max_model_tokens - prompt_tokens"""
    #timeout = int(await read_strings_from_file("timeout"))
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature#,#float(temperature),
        #"max_tokens": max_tokens
    }
    try:
        response = post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=timeout)
            # Check if the request was successful
        if response.status_code == 200:
            logger.debug(f"ChatGPT response: {response.json()}")
            response = response.json()
            
        else:
            logger.error(f"ChatGPT error: {response.json()}")
            response = response.json()
            error_message = response.get("error", {}).get("message", "Unknown error")
            
            
    except exceptions.ReadTimeout:
        logger.error("Ошибка чтения: запрос занял слишком много времени")
        #print("Ошибка чтения: запрос занял слишком много времени")
        return "Ошбика 101"  # too long
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        #print(f"Произошла ошибка: {e}")
        return "Ошибка 102"  # other response error

    test = None
    try:
        logger.debug(f"response: {response}")
        test = response['choices']
        #await  append_to_file("log.txt", f"{now}:: test: {test}\n")
    except Exception as e:
        logger.error(f"error: {e}")
        #print (f"error: {e}")
        return "Ошибка 103" # parse error
    if test[0]['finish_reason'] == 'stop' or test[0]['finish_reason'] == 'length':
        logger.debug(f"finish_reason: {test[0]['finish_reason']}")
        return test[0]['message']['content']
    #print (f"finish_reason: {response['choices'][0]['finish_reason']}")
    logger.error(f"Ошибка 104: {test[0]['finish_reason']}")
    return "Ошибка 104" # other error