import os

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем API-ключ из .env.template
API_KEY = os.getenv('EXCHANGE_API_KEY')
# Правильный URL для API Layer (Exchangerates Data API)
URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_currency_from_transaction(transaction: dict) -> float | None:

    operation = transaction.get("operationAmount")

    if not isinstance(operation, dict):
        raise ValueError("operationAmount должен быть dict")

    amount = operation["amount"]
    currency_data = operation["currency"]

    if not currency_data:
        raise ValueError("Нет данных о валюте")

    from_currency = currency_data.get("code")

    if amount is None or from_currency is None:
        raise ValueError("Некорректная структура транзакции")

    amount = float(amount)

    if from_currency == 'RUB':
        return amount

    if from_currency not in ['USD', 'EUR']:
        raise ValueError(f"Конвертация для валюты {from_currency} не поддерживается.")

    if not API_KEY:
        raise ValueError("API_KEY не задан")

    params = {
        'from': from_currency,
        'to': 'RUB',
        'amount': amount
    }

    headers = {
        'apikey': API_KEY,
        'User-Agent': 'Python/requests'
    }

    try:
        response = requests.get(URL, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        result = data.get('result')
        return result

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Ошибка API: {e}")
