"""
Модуль виджетов для форматирования банковских реквизитов и дат.

Содержит функции для автоматического определения типа реквизита (карта или счет),
его маскирования и приведения даты операции к читаемому формату ДД.ММ.ГГГГ.
"""

# Встроенный класс для работы с датой и временем
from datetime import datetime

# Импорт функций маскирования номеров карт и счетов из модуля masks
from src.masks import get_mask_account_number, get_mask_card_number


def mask_account_card(info_string: str) -> str:
    """
    Принимает строку с типом и номером карты или счета и возвращает её с замаскированным номером.

    :param info_string: Строка вида 'Visa Platinum 7000792289606361' или 'Счет 73654108430135874305'.
    :return: Строка с замаскированным номером в исходном формате.
    """
    if not info_string or not info_string.strip():
        return ""

    # Разделяем строку на слова (например, ["Visa", "Platinum", "7000..."] или ["Счет", "7365..."])
    parts = info_string.split()

    # Последний элемент списка — это сам номер карты или счета
    number = parts[-1]
    # Все элементы до последнего — название платежной системы или слово "Счет"
    name = " ".join(parts[:-1])

    # Выбираем способ маскирования в зависимости от типа реквизита
    if "Счет" in name:
        masked_number = get_mask_account_number(number)
    else:
        masked_number = get_mask_card_number(number)

    # Возвращаем склеенную строку, убирая лишний пробел, если название отсутствовало
    return f"{name} {masked_number}".strip()


def get_date(date_str: str) -> str:
    """
    Преобразует строку с датой в формате ISO в формат 'ДД.ММ.ГГГГ'.

    :param date_str: Строка с датой (например, '2024-03-11T02:26:18.671407').
    :return: Отформатированная дата в виде '11.03.2024'.
    """
    # Парсим строку в объект datetime (поддерживает формат с микросекундами и без них)
    dt = datetime.fromisoformat(date_str)

    # Форматируем объект datetime в строку нужного вида
    return dt.strftime("%d.%m.%Y")


# Пример локального запуска для ручной проверки (исключен из подсчета покрытия тестами)
if __name__ == "__main__":  # pragma: no cover
    print(mask_account_card("Visa Platinum 7000792289606361"))  # Visa Platinum 7000 79** **** 6361
    print(mask_account_card("Maestro 7000792289606361"))  # Maestro 7000 79** **** 6361
    print(mask_account_card("Счет 73654108430135874305"))  # Счет **4305

    # Проверка форматирования даты
    input_date = "2024-03-11T02:26:18.671407"
    formatted_date = get_date(input_date)
    print(formatted_date)  # Вывод: 11.03.2024
