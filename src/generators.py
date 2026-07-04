from typing import Any, Dict, Generator, List


def filter_by_currency(
    transactions_list: List[Dict[str, Any]],
    currency_code: str
) -> Generator[Dict[str, Any], None, None]:
    """
    Фильтрует транзакции по заданной валюте.

    :param transactions_list: Список словарей с транзакциями.
    :param currency_code: Код валюты (например, 'USD').
    :return: Генератор транзакций с нужной валютой.
    """
    for transaction in transactions_list:
        currency = (
            transaction.get("operationAmount", {})
            .get("currency", {})
            .get("code")
        )

        if currency == currency_code:
            yield transaction


def transaction_descriptions(tx_list: list[dict]) -> Generator[str, None, None]:
    for transaction in tx_list:
        yield transaction.get("description", "Описание отсутствует")


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.
    Args:
        start (int): Начальное число для генерации (от 1 до 9999999999999999).
        end (int): Конечное число для генерации (до 9999999999999999).
    Yields:
        str: Номер карты в формате 'XXXX XXXX XXXX XXXX'.
    """
    # Проверяем корректность входных параметров
    if not (1 <= start <= 9999999999999999):
        raise ValueError("Начальное значение должно быть в диапазоне "
                         "от 1 до 9999999999999999")
    if not (start <= end <= 9999999999999999):
        raise ValueError("Конечное значение должно быть в диапазоне "
                         "от start до 9999999999999999")

    for num in range(start, end + 1):
        # Преобразуем число в строку и дополняем нулями слева до 16 цифр
        num_str = str(num).zfill(16)
        # Разбиваем строку на блоки по 4 цифры и соединяем пробелами
        formatted_card_number = ' '.join(num_str[i:i + 4] for i in range(0, 16, 4))
        yield formatted_card_number


# Пример использования
if __name__ == "__main__":  # pragma: no cover
    transactions = (
        [
            {
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
                "operationAmount": {
                    "amount": "9824.07",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод организации",
                "from": "Счет 75106830613657916952",
                "to": "Счет 11776614605963066702"
            },
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {
                    "amount": "79114.93",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 19708645243227258542",
                "to": "Счет 75651667383060284188"
            },
            {
                "id": 873106923,
                "state": "EXECUTED",
                "date": "2019-03-23T01:09:46.296404",
                "operationAmount": {
                    "amount": "43318.34",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 44812258784861134719",
                "to": "Счет 74489636417521191160"
            },
            {
                "id": 895315941,
                "state": "EXECUTED",
                "date": "2018-08-19T04:27:37.904916",
                "operationAmount": {
                    "amount": "56883.54",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод с карты на карту",
                "from": "Visa Classic 6831982476737658",
                "to": "Visa Platinum 8990922113665229"
            },
            {
                "id": 594226727,
                "state": "CANCELED",
                "date": "2018-09-12T21:27:25.241689",
                "operationAmount": {
                    "amount": "67314.70",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод организации",
                "from": "Visa Platinum 1246377376343588",
                "to": "Счет 14211924144426031657"
            }
        ]
    )
    usd_transactions = filter_by_currency(transactions, "USD")
    for _ in range(2):
        print(next(usd_transactions))

    var_one = {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }
    var_two = {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    }


# Тестовый список транзакций
transactions = [
    {"id": 1, "description": "Перевод организации"},
    {"id": 2, "description": "Перевод со счета на счет"},
    {"id": 3, "description": "Перевод со счета на счет"},
    {"id": 4, "description": "Перевод с карты на карту"},
    {"id": 5, "description": "Перевод организации"},
    {"id": 6, "description": "Оплата услуг"}
]

# Инициализируем генератор
descriptions = transaction_descriptions(transactions)

# Выводим первые 5 описаний
for _ in range(5):
    print(next(descriptions))

# Пример использования
for card_number in card_number_generator(1, 5):
    print(card_number)
