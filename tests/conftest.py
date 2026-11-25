"""
Модуль общих фикстур для тестирования проекта с помощью pytest.

Содержит подготовленные наборы тестовых данных (номера карт и счетов,
даты, списки банковских транзакций) и временные файлы для всех тестовых модулей.
"""

# Встроенные модули для работы с путями и аннотациями типов
from pathlib import Path
from typing import Any, Generator

# Фреймворк для написания и запуска модульных тестов
import pytest


@pytest.fixture
def sample_card_number() -> str:
    """Возвращает корректный 16-значный номер карты для теста."""
    return "1234567812345678"


@pytest.fixture
def sample_account_number() -> str:
    """Возвращает тестовый 20-значный номер расчетного счета."""
    return "73654108430135874305"


@pytest.fixture
def card_info() -> str:
    """Возвращает исходную строку с названием и номером карты."""
    return "Visa Platinum 7000792289606617"


@pytest.fixture
def valid_date_str() -> str:
    """Возвращает валидную строку даты и времени в формате ISO."""
    return "2024-03-11T02:26:18.671407"


@pytest.fixture
def sample_date() -> list[tuple[str, str]]:
    """Возвращает список кортежей (входная дата ISO, ожидаемый результат ДД.ММ.ГГГГ)."""
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2000-01-01T00:00:00.000000", "01.01.2000"),
        ("2024-02-29T10:00:00.000000", "29.02.2024"),
    ]


@pytest.fixture
def sample_operations() -> list[dict[str, Any]]:
    """Возвращает список тестовых транзакций для проверки фильтрации и сортировки."""
    return [
        {"id": 1, "date": "2019-08-26T10:50:58.294041"},
        {"id": 2, "date": "2018-06-15T08:12:35.123456"},
        {"id": 3, "date": "2021-12-30T15:00:00.000000"},
    ]


@pytest.fixture
def sample_transactions() -> list[dict[str, Any]]:
    """Возвращает базовый список транзакций с вложенной структурой валют."""
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
def empty_transactions() -> list[dict[str, Any]]:
    """Возвращает пустой список транзакций."""
    return []


@pytest.fixture
def valid_small_range() -> dict[str, Any]:
    """Возвращает словарь с границами диапазона и ожидаемым списком номеров карт."""
    return {
        "start": 1,
        "end": 3,
        "expected": [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
        ],
    }


@pytest.fixture
def log_file(tmp_path: Path) -> Generator[str, None, None]:
    """Создает путь к временному файлу логов в изолированной папке pytest и удаляет его после теста."""
    path = tmp_path / "test_log.txt"
    yield str(path)
    if path.exists():
        path.unlink()


@pytest.fixture
def usd_transaction() -> dict[str, Any]:
    """Возвращает базовую транзакцию в долларах США (USD)."""
    return {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"},
        }
    }


@pytest.fixture
def sample_operations_two() -> list[dict[str, Any]]:
    """Возвращает тестовый набор операций для проверки поиска по описанию."""
    return [
        {"id": 1, "description": "Оплата за интернет"},
        {"id": 2, "description": "Перевод другу"},
        {"id": 3, "description": "Покупка в супермаркете"},
        {"id": 4, "description": "ОПЛАТА ПО СЧЕТУ"},
        {"id": 5},  # Операция без ключа description
        {"id": 6, "description": 12345},  # Значение description не строка
    ]


@pytest.fixture
def sample_operations_three() -> list[dict[str, Any]]:
    """Возвращает тестовый список транзакций для подсчета статистики по категориям."""
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Оплата услуг"},
        {"id": 3, "description": "Перевод со счета на счет"},
        {"id": 4, "description": "Открытие вклада"},
        {"id": 5, "description": "Перевод на карту (Visa/Mastercard)"},
        {"id": 6, "amount": 100},  # Отсутствует ключ description
        {"id": 7, "description": None},  # Значение description не строка
    ]
