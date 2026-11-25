import unittest
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.external_api import convert_currency_from_transaction


class TestLoadTransactions(unittest.TestCase):

    def test_convert_currency_rub(self):
        """Тест без отправки запроса, если валюта изначально RUB."""
    rub_transaction = {
        "operationAmount": {
            "amount": "500.00",
            "currency": {"code": "RUB"}
        }
    }
    # Запрос в requests.get вообще не должен уходить
    with patch('src.external_api.requests.get') as mock_get:
        result = convert_currency_from_transaction(rub_transaction)
        assert result == 500.00
        mock_get.assert_not_called()

    def test_convert_currency_unsupported_currency(self):
        """Тест ошибки: Передана неподдерживаемая валюта (например, GBP)."""
    gbp_transaction = {
        "operationAmount": {
            "amount": "10.00",
            "currency": {"code": "GBP"}
        }
    }
    with pytest.raises(ValueError, match="Конвертация для валюты GBP не поддерживается"):
        convert_currency_from_transaction(gbp_transaction)


@patch('src.external_api.requests.get')
def test_convert_currency_api_http_error(mock_get, usd_transaction):
    """Тест ошибки: API вернул ошибку HTTP (например, 401 Unauthorized)."""
    mock_response = MagicMock()
    # Имитируем выброс исключения HTTPError при вызове raise_for_status()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Unauthorized")
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Ошибка при обращении к API"):
        convert_currency_from_transaction(usd_transaction)


if __name__ == '__main__':
    unittest.main()
