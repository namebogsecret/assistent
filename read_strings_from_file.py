from logging import getLogger
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)
def read_strings_from_file(file_path = "clap_gpt/strings.txt"):
    strings_dict = {}
    current_key = None

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('[') and line.endswith(']\n'):
                current_key = line[1:-2]
                strings_dict[current_key] = ''
            elif current_key is not None:
                if strings_dict[current_key]:  # Если строка не пустая, добавляем символ новой строки
                    strings_dict[current_key] += '\n'
                strings_dict[current_key] += line.strip()  # Удаляем символы новой строки в начале и конце строки


    return strings_dict

if __name__ == '__main__':
    strings =read_strings_frim_file()
    print(strings)