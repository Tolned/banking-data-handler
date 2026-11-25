"""
Модуль тестирования функции загрузки транзакций из JSON-файлов (load_transactions).

Проверяет обработку всех возможных сценариев: успешное чтение списка,
отсутствие файла, пустой файл, неверную структуру JSON (словарь вместо списка),
ошибки парсинга (JSONDecodeError) и ошибки ввода-вывода (OSError).
"""

# Инструменты для подмены встроенных функций (open, os.path.exists) и создания мок-файлов
from unittest.mock import mock_open, patch

# Импорт тестируемой функции загрузки транзакций из модуля utils
from src.utils import load_transactions


def test_load_transactions_file_not_found() -> None:
    """Тест возврата пустого списка, если файл не найден на диске."""
    with patch("os.path.exists", return_value=False):
        result = load_transactions("non_existent_file.json")
        assert result == []


def test_load_transactions_file_is_empty() -> None:
    """Тест возврата пустого списка, если файл существует, но абсолютно пустой."""
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data="")),
    ):
        result = load_transactions("empty.json")
        assert result == []


def test_load_transactions_json_is_empty_list() -> None:
    """Тест возврата пустого списка, если в JSON записан пустой массив []."""
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data="[]")),
    ):
        result = load_transactions("empty_list.json")
        assert result == []


def test_load_transactions_valid_json_list() -> None:
    """Тест успешной загрузки валидного списка банковских транзакций."""
    sample_json = '[{"id": 1, "amount": 100}]'
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data=sample_json)),
    ):
        result = load_transactions("valid.json")
        assert result == [{"id": 1, "amount": 100}]


def test_load_transactions_json_is_not_list() -> None:
    """Тест возврата пустого списка, если корневой элемент JSON — словарь, а не список."""
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data='{"not_a_list": "value"}')),
    ):
        result = load_transactions("not_a_list.json")
        assert result == []


def test_load_transactions_json_decode_error() -> None:
    """Тест возврата пустого списка при синтаксической ошибке внутри JSON-файла."""
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data="некорректный json контент")),
    ):
        result = load_transactions("invalid_format.json")
        assert result == []


def test_load_transactions_io_error() -> None:
    """Тест возврата пустого списка при ошибке ввода-вывода (OSError) во время чтения."""
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", side_effect=OSError("Ошибка доступа к диску")),
    ):
        result = load_transactions("io_error_file.json")
        assert result == []
