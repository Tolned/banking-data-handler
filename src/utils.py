"""
Утилитарный модуль для загрузки финансовых данных из JSON-файлов.

Содержит функцию для безопасного чтения и валидации списка транзакций
с подробным логированием всех этапов работы в файл logs/utils.log.
"""

# Встроенные модули для работы с форматом JSON, логированием и файловой системой
import json
import logging
import os
from pathlib import Path
from typing import Any

# Создаем отдельный объект логгера для модуля utils
logger = logging.getLogger("utils")
# Устанавливаем минимальный уровень логирования (DEBUG записывает все события)
logger.setLevel(logging.DEBUG)
# Отключаем передачу логов в корневой логгер, чтобы избежать дублирования в консоли
logger.propagate = False

# Определяем путь к папке logs в корне проекта (на уровень выше папки src)
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOG_FILE_PATH = LOGS_DIR / "utils.log"


# Настраиваем обработчик файла только один раз, чтобы избежать дублирования записей
if not logger.handlers:
    os.makedirs(LOGS_DIR, exist_ok=True)
    file_handler = logging.FileHandler(LOG_FILE_PATH, mode="a", encoding="utf-8")
    file_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def load_transactions(file_path: str) -> list[dict[str, Any]]:
    """
    Загружает список финансовых транзакций из JSON-файла.

    Если файл пустой, не найден или содержит структуру, отличную от списка,
    записывает предупреждение в лог и возвращает пустой список.

    :param file_path: Путь к JSON-файлу с транзакциями.
    :return: Список словарей с данными транзакций или пустой список при ошибке.
    """
    logger.info(f"Начало загрузки транзакций из файла: {file_path}")

    # Проверяем, существует ли файл по указанному пути
    if not os.path.exists(file_path):
        logger.warning(f"Файл не найден по пути: {file_path}")
        return []

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            # Считываем содержимое файла и удаляем пробельные символы по краям
            content = file.read().strip()

            # Если файл оказался пустым, возвращаем пустой список
            if not content:
                logger.warning(f"Файл пуст: {file_path}")
                return []

            data: Any = json.loads(content)

            # Проверяем, что корневым элементом JSON является именно список
            if isinstance(data, list):
                logger.info(f"Успешно загружено {len(data)} транзакций из файла: {file_path}")
                return data

            logger.error(f"Данные в файле {file_path} не являются списком. Тип данных: {type(data).__name__}")
            return []

    except json.JSONDecodeError as e:
        # Перехватываем ошибки некорректного синтаксиса JSON
        logger.error(f"Ошибка парсинга JSON в файле {file_path}: {e}")
        return []

    except OSError as e:
        # Перехватываем ошибки чтения файла (например, нет прав доступа)
        logger.error(f"Ошибка ввода-вывода при работе с файлом {file_path}: {e}")
        return []
