import json
import logging
import os
from typing import Any, Dict, List

# 1. Создаем отдельный объект логера для модуля utils
logger = logging.getLogger('utils')

# Устанавливаем минимальный уровень логирования не меньше DEBUG
logger.setLevel(logging.DEBUG)

# 2. Настраиваем file_handler для записи логов в файл
os.makedirs('logs', exist_ok=True)
file_handler = logging.FileHandler('logs/utils.log', encoding='utf-8')

# 3. Настраиваем file_formatter
# Формат: метка времени, название модуля, уровень серьезности, сообщение
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 4. Устанавливаем форматер для handler'а и добавляем handler к логеру
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает список финансовых транзакций из JSON-файла. Если файл пустой, не найден или содержит не список,
     возвращает пустой список."""
    # Логируем начало выполнения функции
    logger.info(f"Начало загрузки транзакций из файла: {file_path}")
    # Если файл не найден, возвращаем пустой список
    if not os.path.exists(file_path):
        logger.warning(f"Файл не найден по пути: {file_path}")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Читаем содержимое файла
            content = file.read().strip()

            # Если файл пустой, возвращаем пустой список
            if not content:
                logger.warning(f"Файл пуст: {file_path}")
                return []

            data = json.loads(content)

            # Проверяем, является ли загруженный JSON списком
            if isinstance(data, list):
                logger.info(f"Успешно загружено {len(data)} транзакций из файла: {file_path}")
                return data

            logger.error(f"Данные в файле {file_path} не являются списком. Тип данных: {type(data).__name__}")
            return []

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON в файле {file_path}: {e}")
        return []

    except IOError as e:
        logger.error(f"Ошибка ввода-вывода при работе с файлом {file_path}: {e}")
        return []
