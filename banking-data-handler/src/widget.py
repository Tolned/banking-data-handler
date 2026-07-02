from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info_string: str) -> str:
    """Функция принимает строку с названием и номером карты/счета, маскирует номер и возвращает строку в прежнем
    формате."""
    # Разделяем строку на части (например, ["Visa", "Platinum", "7000..."] или ["Счет",
    # "7365..."])
    parts = info_string.split()

    # Последняя часть - это номер
    number = parts[-1]

    # Название (все части кроме последней)
    name = " ".join(parts[:-1])

    if "Счет" in name:
        # Применяем маскировку для счета (скрываем до последних 4 цифр)
        # Пример использования функции из модуля masks
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_str: str) -> str:
    """Принимает строку '2024-03-11T02:26:18.671407' и возвращает '11.03.2024'."""
    # 1. Парсим входящую строку в объект datetime
    # %f используется для микросекунд
    dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')

    # 2. Форматируем объект datetime в нужную строку
    return dt.strftime('%d.%m.%Y')


# Тесты
if __name__ == "__main__":  # pragma: no cover
    print(mask_account_card("Visa Platinum 7000792289606361"))
    # Visa Platinum 7000 79** **** 6361
    print(mask_account_card("Maestro 7000792289606361"))  # Maestro 7000 79** **** 6361
    print(mask_account_card("Счет 73654108430135874305"))  # Счет **4305

# Пример использования:
    input_date = '2024-03-11T02:26:18.671407'
    formatted_date = get_date(input_date)
    print(formatted_date)  # Вывод: 11.03.2024
