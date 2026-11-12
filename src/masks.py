"""
Модуль для маскирования номеров банковских карт и счетов.

Содержит функции для скрытия части цифр платежных реквизитов в целях безопасности,
а также настраивает отдельное логирование операций маскирования в файл masks.log.
"""

# Встроенные модули для логирования и работы с путями файловой системы
import logging
import os

# Создаем отдельный объект логгера для модуля masks
logger = logging.getLogger("masks")
# Устанавливаем минимальный уровень логирования (DEBUG записывает все события)
logger.setLevel(logging.DEBUG)
# Отключаем передачу логов в корневой логгер, чтобы избежать дублирования в консоли
logger.propagate = False

# Динамически определяем путь к файлу логов рядом с текущим модулем masks.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(BASE_DIR, "masks.log")

# Добавляем обработчик файла только если он еще не был привязан к логгеру
if not logger.handlers:
    file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
    file_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def get_mask_card_number(card_info: str) -> str:
    """
    Маскирует номер банковской карты в формате 'Название XXXX XX** **** XXXX'.

    :param card_info: Строка с номером карты (или названием и номером карты).
    :return: Замаскированная строка или пустая строка при некорректных данных.
    """
    logger.info(f"Начало маскирования карты. Длина входных данных: {len(str(card_info))}")

    if not card_info or not isinstance(card_info, str):
        logger.warning("Переданы некорректные данные для маскирования карты.")
        return ""

    # Разделяем название карты и сам номер (например, "Visa Gold 7000792289606361")
    parts = card_info.split()
    card_number = parts[-1]
    card_name = " ".join(parts[:-1])

    clean_number = card_number.replace(" ", "")

    if len(clean_number) < 16 or not clean_number.isdigit():
        logger.warning(f"Некорректный номер карты: {clean_number}")
        return card_info

    # Формируем маску: первые 6 цифр, 6 звездочек и последние 4 цифры
    start = clean_number[:6]
    end = clean_number[-4:]
    masked_number = f"{start[:4]} {start[4:]}** **** {end}"

    # Собираем итоговую строку с названием карты, если оно присутствовало
    result = f"{card_name} {masked_number}".strip()

    logger.debug(f"Успешно замаскирована карта: {result}")
    return result


def get_mask_account_number(account_info: str) -> str:
    """
    Маскирует номер банковского счета в формате 'Название **XXXX'.

    :param account_info: Строка с номером счета (например, 'Счет 73654108430135874305').
    :return: Замаскированная строка или пустая строка при некорректных данных.
    """
    logger.info("Начало маскирования счета.")

    if not account_info or not isinstance(account_info, str):
        logger.warning("Переданы некорректные данные для маскирования счета.")
        return ""

    # Разделяем название и номер счета
    parts = account_info.split()
    account_number = parts[-1]
    account_name = " ".join(parts[:-1])

    account_str = account_number.replace(" ", "")

    if len(account_str) < 4 or not account_str.isdigit():
        logger.warning(f"Некорректный номер счета: {account_str}")
        return account_info

    # Берем последние 4 символа номера счета
    last_four = account_str[-4:]
    masked_account = f"**{last_four}"

    # Собираем итоговую строку со словом "Счет" (если оно было передано)
    result = f"{account_name} {masked_account}".strip()

    logger.debug(f"Успешно замаскирован счет: {result}")
    return result


# Пример локального запуска (исключен из подсчета покрытия тестами)
if __name__ == "__main__":  # pragma: no cover
    card = "Visa Platinum 7000792289606361"
    print(f"{card} -> {get_mask_card_number(card)}")

    account = "Счет 73654108430135874305"
    print(f"{account} -> {get_mask_account_number(account)}")
