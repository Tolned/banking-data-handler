"""
Модуль для конвертации валют по данным банковских транзакций.

Использует внешний API Exchangerates Data для перевода
сумм из долларов (USD) и евро (EUR) в российские рубли (RUB).
"""

# Встроенный модуль для работы с переменными окружения операционной системы
import os

# Инструмент для указания типов в словарях и проверки через mypy
from typing import Any

# Сторонняя библиотека для выполнения HTTP-запросов к внешним API
import requests

# Функция для загрузки секретных ключей из скрытого файла .env
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env в память программы
load_dotenv()

# Получаем секретный API-ключ из переменных окружения
API_KEY = os.getenv("EXCHANGE_API_KEY")
# Базовый адрес сервиса конвертации валют (API Layer)
URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_currency_from_transaction(transaction: dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли (RUB) по актуальному курсу API.

    :param transaction: Словарь с данными о транзакции (ожидается ключ 'operationAmount').
    :return: Сумма операции в рублях в виде числа с плавающей точкой.
    :raises ValueError: При некорректной структуре данных, неподдерживаемой валюте или сбое API.
    """
    # Извлекаем вложенный словарь с информацией о сумме и валюте операции
    operation = transaction.get("operationAmount")

    if not isinstance(operation, dict):
        raise ValueError("operationAmount должен быть dict")

    # Безопасно получаем сумму и словарь с данными о валюте
    amount = operation.get("amount")
    currency_data = operation.get("currency")

    if not isinstance(currency_data, dict):
        raise ValueError("Нет данных о валюте")

    # Извлекаем трехбуквенный код валюты (например, 'RUB', 'USD', 'EUR')
    from_currency = currency_data.get("code")

    if not isinstance(amount, (str, int, float)) or not isinstance(from_currency, str):
        raise ValueError("Некорректная структура транзакции")

    # Преобразуем строковую сумму (например, "31957.58") в число с плавающей точкой
    numeric_amount = float(amount)

    # Если операция уже в рублях, возвращаем сумму сразу без обращения к внешнему API
    if from_currency == "RUB":
        return numeric_amount

    # Проверяем, поддерживается ли конвертация для данной валюты
    if from_currency not in ["USD", "EUR"]:
        raise ValueError(f"Конвертация для валюты {from_currency} не поддерживается.")

    # Проверяем, что API-ключ успешно загрузился из файла .env
    if not API_KEY:
        raise ValueError("API_KEY не задан")

    # Формируем параметры запроса (из какой валюты, в какую и какая сумма)
    params: dict[str, str | float] = {
        "from": from_currency,
        "to": "RUB",
        "amount": numeric_amount,
    }

    # Передаем API-ключ в заголовках запроса для авторизации на сервере
    headers = {
        "apikey": API_KEY,
        "User-Agent": "Python/requests",
    }

    try:
        # Отправляем GET-запрос к API с ограничением ожидания ответа в 10 секунд
        response = requests.get(URL, headers=headers, params=params, timeout=10)
        # Вызываем исключение, если сервер вернул код ошибки (4xx или 5xx)
        response.raise_for_status()

        # Преобразуем JSON-ответ сервера в словарь Python
        data = response.json()
        result = data.get("result")

        if result is None:
            raise ValueError("API не вернул результат конвертации")

        return float(result)

    except requests.exceptions.RequestException as e:
        # Перехватываем любые сетевые ошибки и превращаем их в единый ValueError
        raise ValueError(f"Ошибка при обращении к API: {e}")
