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
    """
    Конвертирует сумму из транзакции (словаря) в рубли (RUB).

    Args:
        transaction: Словарь с данными транзакции, должен содержать 'amount' и 'currency'.

    Returns:
        Сумма в рублях (float).

    Raises:
        ValueError: Если валюта не поддерживается, нет нужных ключей, или произошла ошибка API.
    """
    # Извлекаем данные из словаря
    amount = transaction.get("operationAmount").get('amount')
    from_currency = transaction.get("operationAmount").get('currency').get("code")

    if amount is None or from_currency is None:
        raise ValueError("Словарь транзакции должен содержать ключи 'amount' и 'currency'.")

    # Приводим amount к числу
    amount = float(amount)

    if from_currency == 'RUB':
        return amount  # Уже в рублях

    if from_currency not in ['USD', 'EUR']:
        raise ValueError(f"Конвертация для валюты {from_currency} не поддерживается.")

    # Настройки для API
    params = {
        'from': from_currency,
        'to': 'RUB',
        'amount': amount
    }
    headers = {
        'apikey': API_KEY,  # Передаем API-ключ в заголовках
        'User-Agent': 'Python/requests'
    }

    try:
        response = requests.get(URL, headers=headers, params=params)
        response.raise_for_status()  # Выбросит ошибку, если HTTP-статус >= 400

        data = response.json()

        if 'result' not in data:
            return None

        rate = data['result']
        return rate

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Ошибка при обращении к API: {e}")
    except KeyError as e:
        raise ValueError(f"Некорректный ответ от API: отсутствует ключ {e}")
