import os

import pytest


@pytest.fixture
def sample_card_number():
    """Возвращает корректный номер карты для теста."""
    return "1234567812345678"


@pytest.fixture
def sample_account_number():
    """Возвращает тестовый 20-значный номер расчетного счета."""
    return "73654108430135874305"


@pytest.fixture
def card_info():
    """ Возвращает строку с замаскированной информацией о карте."""
    return "Visa Platinum 7000792289606617"


@pytest.fixture
def valid_date_str():
    """Возвращает валидную строку даты и времени."""
    return "2024-03-11T02:26:18.671407"


@pytest.fixture
def sample_date():
    """Фикстура для передачи тестовых наборов (вход, ожидаемый результат)."""
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2000-01-01T00:00:00.000000", "01.01.2000"),
        ("2024-02-29T10:00:00.000000", "29.02.2024")
    ]


@pytest.fixture
def sample_operations():
    """Создает список тестовых транзакций для проверки логики фильтрации и сортировки."""
    return [
        {"id": 1, "date": "2019-08-26T10:50:58.294041"},
        {"id": 2, "date": "2018-06-15T08:12:35.123456"},
        {"id": 3, "date": "2021-12-30T15:00:00.000000"},
    ]


@pytest.fixture
def sample_transactions():
    """Фикстура с базовым списком транзакций."""
    return [
        {
            "id": 1,
            "operationAmount": {"amount": "100.00", "currency": {"code": "USD"}},
        },
        {
            "id": 2,
            "operationAmount": {"amount": "200.00", "currency": {"code": "EUR"}},
        },
        {
            "id": 3,
            "operationAmount": {"amount": "50.00", "currency": {"code": "USD"}},
        },
        {
            "id": 4,  # Транзакция без нужных ключей для проверки безопасности
            "description": "Перевод без указания валюты",
        },
    ]


@pytest.fixture
def empty_transactions():
    """Фикстура для пустого списка транзакций."""
    return []


@pytest.fixture
def valid_small_range():
    """Фикстура для проверки обычного небольшого диапазона."""
    return {"start": 1, "end": 3, "expected": ["0000 0000 0000 0001",
                                               "0000 0000 0000 0002",
                                               "0000 0000 0000 0003"]}


@pytest.fixture()
def log_file():
    """Фикстура для автоматической очистки созданных файлов логов."""
    path = "test_log.txt"
    yield path
    if not os.path.exists(path):
        return
    os.remove(path)


@pytest.fixture
def usd_transaction():
    """Фикстура базовой успешной транзакции в USD."""
    return {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }


@pytest.fixture
def sample_operations_two():
    """Фикстура с тестовым набором операций"""
    return [
        {"id": 1, "description": "Оплата за интернет"},
        {"id": 2, "description": "Перевод другу"},
        {"id": 3, "description": "Покупка в супермаркете"},
        {"id": 4, "description": "ОПЛАТА ПО СЧЕТУ"},
        {"id": 5},  # Операция без ключа description
        {"id": 6, "description": 12345}  # Description не строка
    ]


@pytest.fixture
def sample_operations_three():
    """Возвращает тестовый список транзакций."""
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Оплата услуг"},
        {"id": 3, "description": "Перевод со счета на счет"},
        {"id": 4, "description": "Открытие вклада"},
        {"id": 5, "description": "Перевод на карту (Visa/Mastercard)"},
        {"id": 6, "amount": 100},  # Отсутствует ключ description
        {"id": 7, "description": None},  # Значение description не строка
    ]
