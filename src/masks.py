import logging
import os

# 1. Создан отдельный объект логера для модуля masks
logger = logging.getLogger("masks")

# Установлен уровень логирования не меньше, чем DEBUG
logger.setLevel(logging.DEBUG)

# Предотвращаем дублирование логов в корневой логер, если необходимо
logger.propagate = False

# ИСПРАВЛЕНИЕ: Динамическое определение пути к файлу логов
# Получаем абсолютный путь к папке, где физически лежит этот файл masks.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(BASE_DIR, "masks.log")

# 2. Настроен file_handler для логера модуля masks с использованием абсолютного пути
file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")

# 3. Настроен file_formatter (метка времени, название модуля, уровень, сообщение)
file_formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 4. Связываем форматер с хендлером и добавляем хендлер к логеру
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_info: str) -> str:
    """Принимает информацию о карте, возвращает маску в формате Название XXXX XX** **** XXXX."""
    logger.info(f"Начало маскирования карты. Длина входных данных: {len(str(card_info))}")

    if not card_info or not isinstance(card_info, str):
        logger.warning("Переданы некорректные данные для маскирования карты.")
        return ""

    # Разделяем название карты и номер (например, "Visa Gold 7000792289606361")
    parts = card_info.split()
    card_number = parts[-1]
    card_name = " ".join(parts[:-1])

    clean_number = card_number.replace(" ", "")

    if len(clean_number) < 16:
        logger.warning(f"Длина номера карты меньше 16 символов: {clean_number}")
        return card_info

    # Формируем маску: первые 6, затем 6 звездочек, затем последние 4
    start = clean_number[:6]
    end = clean_number[-4:]
    masked_number = f"{start[:4]} {start[4:]}** **** {end}"

    # Собираем обратно с названием карты, если оно было
    result = f"{card_name} {masked_number}".strip()

    logger.debug(f"Успешно замаскирована карта: {result}")
    return result


def get_mask_account_number(account_info: str) -> str:
    """Принимает информацию о счете, возвращает маску в формате Название **XXXX."""
    logger.info("Начало маскирования счета.")

    if not account_info or not isinstance(account_info, str):
        logger.warning("Переданы некорректные данные для маскирования счета.")
        return ""

    # Разделяем название и номер (например, "Счет 73654108430135874305")
    parts = account_info.split()
    account_number = parts[-1]
    account_name = " ".join(parts[:-1])

    account_str = str(account_number).replace(" ", "")

    if len(account_str) < 4:
        logger.warning(f"Длина номера счета меньше 4 символов: {account_str}")
        return account_info

    # Берем последние 4 символа
    last_four = account_str[-4:]
    masked_account = f"**{last_four}"

    # Собираем обратно с названием типа "Счет"
    result = f"{account_name} {masked_account}".strip()

    logger.debug(f"Успешно замаскирован счет: {result}")
    return result


# Пример использования
if __name__ == "__main__":  # pragma: no cover
    card = "Visa Platinum 7000792289606361"
    masked = get_mask_card_number(card)
    print(f"{card} -> {masked}")

    account = "Счет 73654108430135874305"
    print(f"{account} -> {get_mask_account_number(account)}")
