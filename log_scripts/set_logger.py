#  src/logging/set_logger.py
import logging
from datetime import datetime
from os import mkdir, makedirs, remove, walk
from os.path import exists, join, getsize
#import os
from shutil import make_archive
from time import time

logs_dir = 'logs'

def archive_large_logs(logs_dir, max_size_mb=10):
    """
    Архивирует большие лог-файлы в указанной директории.
    
    Параметры:
    - logs_dir (str): Путь до директории с лог-файлами.
    - max_size_mb (int, optional): Максимальный размер файла в мегабайтах. По умолчанию 10 MB.
    
    Примеры использования:
    >>> archive_large_logs('/path/to/logs', 5)
    """
    
    # Преобразование мегабайт в байты
    max_size_bytes = max_size_mb * 1024 * 1024  
    
    # Проход по всем файлам и папкам в директории
    for root, dirs, files in walk(logs_dir):
        for file in files:
            # Проверяем, что файл является логом
            if not file.endswith('.log'):  
                continue
            
            file_path = join(root, file)
            
            # Проверка размера файла
            if getsize(file_path) > max_size_bytes:
                archive_dir = join(root, 'archive')
                
                # Создание папки 'archive', если она не существует
                if not exists(archive_dir):
                    makedirs(archive_dir)
                
                # Извлечение даты из имени файла
                file_date_str = file.split('_')[0]  
                
                # Формирование имени архивного файла
                archive_file = join(archive_dir, f'{file_date_str}_{int(time())}_large.zip')
                
                # Архивирование, если такого архива еще нет
                if not exists(archive_file):
                    make_archive(join(archive_dir, f'{file_date_str}_{int(time())}_large'), 'zip', root, file)
                
                # Удаление исходного файла после архивации
                remove(file_path)  


def archive_old_logs(logs_dir):
    """
    Архивирует устаревшие лог-файлы в указанной директории.
    
    Параметры:
    - logs_dir (str): Путь до директории с лог-файлами.

    Примеры использования:
    >>> archive_old_logs('/path/to/logs')
    """
    
    # Получение текущей даты
    today = datetime.now().date()
    
    # Проход по всем файлам и папкам в директории
    for root, dirs, files in walk(logs_dir):
        for file in files:
            # Проверяем, что файл является логом
            if not file.endswith('.log'):
                continue
            
            # Извлечение даты из имени файла
            file_date_str = file.split('_')[0]
            file_date = datetime.strptime(file_date_str, "%Y-%m-%d").date()
            
            # Проверка, является ли файл устаревшим
            if file_date < today:
                archive_dir = join(root, 'archive')
                
                # Создание папки 'archive', если она не существует
                if not exists(archive_dir):
                    makedirs(archive_dir)
                
                # Формирование имени архивного файла
                archive_file = join(archive_dir, f'{file_date_str}.zip')
                
                # Архивирование, если такого архива еще нет
                if not exists(archive_file):
                    make_archive(join(archive_dir, file_date_str), 'zip', root, file)
                
                # Удаление исходного файла после архивации
                remove(join(root, file))




def create_handler(log_dir, level, formatter):
    """
    Создает и настраивает обработчик для логгера.

    Параметры:
    - log_dir (str): Путь до директории с лог-файлами.
    - level (str): Уровень логгирования.
    - formatter (logging.Formatter): Форматирование для сообщений лога.

    Возвращает:
    - logging.Handler: Настроенный обработчик.
    """
    if not exists(log_dir):
        mkdir(log_dir)
    handler = logging.FileHandler(join(log_dir, f'{datetime.now().strftime("%Y-%m-%d")}_{level}.log'))
    handler.setLevel(logging.getLevelName(level.upper()))
    handler.setFormatter(formatter)
    return handler

def set_logger_(logger, logs_dir):
    """
    Настройка логгера с обработчиками для различных уровней сообщений и компонентов.

    Параметры:
    - logger (logging.Logger): Логгер для настройки.
    - logs_dir (str): Путь до директории с лог-файлами.

    Возвращает:
    - logging.Logger: Настроенный логгер.
    """
    if not exists(logs_dir):
        mkdir(logs_dir)
    component_name = logger.name
    logger.setLevel(logging.DEBUG)
    
    # Архивация старых и больших лог-файлов
    archive_old_logs(logs_dir)
    archive_large_logs(logs_dir)
    
    # Формат сообщений для логгера
    formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')
    
    # Создание и настройка обработчиков для различных уровней логгирования
    levels = ['all', 'debug', 'info', 'warning', 'error', 'critical']
    for level in levels:
        handler = create_handler(join(logs_dir, level), level, formatter)
        logger.addHandler(handler)
    
    # Создание директории для компонента, если не существует
    log_components_dir = join(logs_dir, 'components', component_name)
    if not exists(log_components_dir):
        mkdir(log_components_dir)
        
    # Создание и настройка обработчика для компонента
    file_handler_component = create_handler(log_components_dir, 'all', formatter)
    logger.addHandler(file_handler_component)
    
    return logger

def set_logger(logger):
    component_name = logger.name
    logger.setLevel(logging.DEBUG)
    # Вызовите эту функцию перед созданием новых файлов логов:
    archive_old_logs(logs_dir)
    archive_large_logs(logs_dir)
    # Форматирование сообщений лога
    formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')

    """# Создание обработчика для вывода сообщений в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    console_handler.setFormatter(formatter)"""

    # Добавление обработчика к логгеру
    #logger.addHandler(console_handler)

    
    # Общий файл лога
    file_handler_all = logging.FileHandler(join(logs_dir,'all', f'{datetime.now().strftime("%Y-%m-%d")}_app_all.log'))
    file_handler_all.setFormatter(formatter)
    logger.addHandler(file_handler_all)

    # Файлы лога по уровням сообщений
    debug_handler = logging.FileHandler(join(logs_dir, 'debug', f'{datetime.now().strftime("%Y-%m-%d")}_debug.log'))
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)
    logger.addHandler(debug_handler)

    info_handler = logging.FileHandler(join(logs_dir, 'info', f'{datetime.now().strftime("%Y-%m-%d")}_info.log'))
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    logger.addHandler(info_handler)

    warning_handler = logging.FileHandler(join(logs_dir, 'warning', f'{datetime.now().strftime("%Y-%m-%d")}_warning.log'))
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(formatter)
    logger.addHandler(warning_handler)

    error_handler = logging.FileHandler(join(logs_dir, 'error', f'{datetime.now().strftime("%Y-%m-%d")}_error.log'))
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    critical_handler = logging.FileHandler(join(logs_dir, 'critical', f'{datetime.now().strftime("%Y-%m-%d")}_critical.log'))
    critical_handler.setLevel(logging.CRITICAL)
    critical_handler.setFormatter(formatter)
    logger.addHandler(critical_handler)

    log_components_dir = join(logs_dir, 'components', component_name)
    if not exists(log_components_dir):
        mkdir(log_components_dir)
    # Файлы лога для каждого компонента
    file_handler_component = logging.FileHandler(join(log_components_dir, f'{datetime.now().strftime("%Y-%m-%d")}_{component_name}_all.log'))
    file_handler_component.setFormatter(formatter)
    logger.addHandler(file_handler_component)

    return logger