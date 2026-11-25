"""
Модуль тестирования функции поиска банковских операций по описанию.

Проверяет работу filter_operations_by_description на корректный поиск,
игнорирование регистра, экранирование спецсимволов и обработку краевых случаев.
"""

# Инструмент для указания произвольного типа значений в словарях для проверки через mypy
from typing import Any

# Импорт тестируемой функции поиска операций из модуля регулярных выражений
from src.regular_expressions import filter_operations_by_description


def test_filter_by_description_success(sample_operations_three: list[dict[str, Any]]) -> None:
    """Проверка успешной фильтрации по обычному слову."""
    result = filter_operations_by_description(sample_operations_three, "Перевод")
    assert len(result) == 3
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3
    assert result[2]["id"] == 5


def test_filter_by_description_ignore_case(sample_operations_three: list[dict[str, Any]]) -> None:
    """Проверка работы фильтра без учета регистра."""
    result = filter_operations_by_description(sample_operations_three, "пЕрЕвОд")
    assert len(result) == 3


def test_filter_by_description_with_special_characters(sample_operations_three: list[dict[str, Any]]) -> None:
    """Проверка корректного экранирования спецсимволов (скобок и слэша)."""
    result = filter_operations_by_description(sample_operations_three, "(Visa/Mastercard)")
    assert len(result) == 1
    assert result[0]["id"] == 5


def test_filter_by_description_empty_search(sample_operations_three: list[dict[str, Any]]) -> None:
    """Проверка возврата пустого списка при передаче пустой строки поиска."""
    result = filter_operations_by_description(sample_operations_three, "")
    assert result == []


def test_filter_by_description_no_matches(sample_operations_three: list[dict[str, Any]]) -> None:
    """Проверка возврата пустого списка, если совпадений не найдено."""
    result = filter_operations_by_description(sample_operations_three, "Несуществующая операция")
    assert result == []
