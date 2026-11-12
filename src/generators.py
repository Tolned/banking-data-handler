"""
Модуль генераторов для потоковой обработки банковских транзакций.

Содержит генераторы для фильтрации операций по валюте, извлечения
их описаний и последовательной генерации номеров банковских карт.
"""

# Инструменты для аннотации типов генераторов и словарей
from typing import Any, Generator


def filter_by_currency(
    transactions_list: list[dict[str, Any]],
    currency_code: str,
) -> Generator[dict[str, Any], None, None]:
    """
    Фильтрует транзакции по заданной валюте и возвращает их по одной.

    :param transactions_list: Список словарей с транзакциями.
    :param currency_code: Код валюты для фильтрации (например, 'USD').
    :return: Генератор транзакций с нужной валютой.
    """
    for transaction in transactions_list:
        # Безопасно извлекаем код валюты из вложенных словарей
        currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")

        if currency == currency_code:
            yield transaction


def transaction_descriptions(tx_list: list[dict[str, Any]]) -> Generator[str, None, None]:
    """
    Поочередно возвращает описание каждой транзакции из списка.

    :param tx_list: Список словарей с транзакциями.
    :return: Генератор строк с описанием операций.
    """
    for transaction in tx_list:
        yield str(transaction.get("description", "Описание отсутствует"))


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генерирует номера банковских карт в формате 'XXXX XXXX XXXX XXXX'.

    :param start: Начальное число для генерации (от 1 до 9999999999999999).
    :param end: Конечное число для генерации (от start до 9999999999999999).
    :return: Генератор отформатированных номеров карт.
    :raises ValueError: Если границы диапазона выходят за пределы 16-значного номера.
    """
    # Проверяем корректность начального и конечного значений диапазона
    if not (1 <= start <= 9999999999999999):
        raise ValueError("Начальное значение должно быть в диапазоне от 1 до 9999999999999999")
    if not (start <= end <= 9999999999999999):
        raise ValueError("Конечное значение должно быть в диапазоне от start до 9999999999999999")

    for num in range(start, end + 1):
        # Преобразуем число в строку и дополняем нулями слева до 16 символов
        num_str = str(num).zfill(16)
        # Разбиваем строку на блоки по 4 цифры и соединяем их пробелами
        formatted_card_number = " ".join(num_str[i : i + 4] for i in range(0, 16, 4))
        yield formatted_card_number


# Пример локального запуска для ручной проверки (исключен из подсчета покрытия тестами)
if __name__ == "__main__":  # pragma: no cover
    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
    ]

    # Проверка фильтрации по валюте
    usd_transactions = filter_by_currency(transactions, "USD")
    for _ in range(2):
        print(next(usd_transactions))

    # Проверка генератора описаний
    descriptions = transaction_descriptions(transactions)
    for _ in range(3):
        print(next(descriptions))

    # Проверка генератора номеров карт
    for card_number in card_number_generator(1, 5):
        print(card_number)
