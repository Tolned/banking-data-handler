"""
Модуль тестирования функции поиска банковских операций по описанию.

Проверяет работу filter_operations_by_description на пустых входных данных,
регистронезависимом поиске и устойчивости к некорректным типам значений в словарях.
"""

# Инструмент для указания произвольного типа значений в словарях при проверке через mypy
from typing import Any

# Импорт тестируемой функции поиска операций из модуля регулярных выражений
from src.regular_expressions import filter_operations_by_description


def test_filter_empty_search_string(sample_operations_two: list[dict[str, Any]]) -> None:
    """Тест возврата пустого списка при передаче пустой строки поиска."""
    result = filter_operations_by_description(sample_operations_two, "")
    assert result == []


def test_filter_empty_operations_list() -> None:
    """Тест возврата пустого списка при передаче пустого списка операций."""
    result = filter_operations_by_description([], "интернет")
    assert result == []


def test_filter_by_description_case_insensitive_and_invalid_types(
    sample_operations_two: list[dict[str, Any]],
) -> None:
    """Тест регистронезависимого поиска и пропуска записей без строкового description."""
    result = filter_operations_by_description(sample_operations_two, "оплата")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 4
