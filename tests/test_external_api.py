"""
Модуль тестирования функции конвертации валют convert_currency_from_transaction.

Проверяет корректную конвертацию USD/EUR через мок-запросы к внешнему API,
возврат суммы в рублях без сетевого запроса, а также обработку ошибок API и входных данных.
"""

# Инструменты для указания типов словарей и создания мок-объектов в тестах
from typing import Any
from unittest.mock import MagicMock, patch

# Фреймворк pytest для перехвата исключений, фикстур и подмены атрибутов (monkeypatch)
import pytest

# Библиотека requests для имитации сетевых исключений (HTTPError)
import requests

# Импорт тестируемой функции конвертации валют из модуля external_api
from src.external_api import convert_currency_from_transaction


def test_convert_currency_usd_success(
    usd_transaction: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Тест успешной конвертации суммы из USD в RUB с мокированием ответа API."""
    # Безопасно подменяем API_KEY только на время выполнения этого теста
    monkeypatch.setattr("src.external_api.API_KEY", "test_fake_api_key")

    with patch("src.external_api.requests.get") as mock_get:
        # Настраиваем фейковый ответ от сервера
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": 9500.50}
        mock_get.return_value = mock_response

        result = convert_currency_from_transaction(usd_transaction)

        assert result == 9500.50
        mock_get.assert_called_once()


def test_convert_currency_rub() -> None:
    """Тест возврата суммы без отправки сетевого запроса, если валюта изначально RUB."""
    rub_transaction = {
        "operationAmount": {
            "amount": "500.00",
            "currency": {"code": "RUB"},
        }
    }

    # Запрос в requests.get вообще не должен уходить
    with patch("src.external_api.requests.get") as mock_get:
        result = convert_currency_from_transaction(rub_transaction)
        assert result == 500.00
        mock_get.assert_not_called()


def test_convert_currency_unsupported_currency() -> None:
    """Тест ошибки при передаче неподдерживаемой валюты (например, GBP)."""
    gbp_transaction = {
        "operationAmount": {
            "amount": "10.00",
            "currency": {"code": "GBP"},
        }
    }

    with pytest.raises(ValueError, match="Конвертация для валюты GBP не поддерживается"):
        convert_currency_from_transaction(gbp_transaction)


def test_convert_currency_api_http_error(
    usd_transaction: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Тест ошибки при возврате сервером HTTP-ошибки (например, 401 Unauthorized)."""
    # Безопасно подменяем API_KEY, чтобы тест не зависел от наличия файла .env
    monkeypatch.setattr("src.external_api.API_KEY", "test_fake_api_key")

    with patch("src.external_api.requests.get") as mock_get:
        mock_response = MagicMock()
        # Имитируем выброс исключения HTTPError при вызове raise_for_status()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Unauthorized")
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Ошибка при обращении к API"):
            convert_currency_from_transaction(usd_transaction)
