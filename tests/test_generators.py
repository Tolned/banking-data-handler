"""
Модуль тестирования генераторов для обработки банковских транзакций.

Проверяет работу filter_by_currency, transaction_descriptions и card_number_generator
на корректность фильтрации, извлечения описаний, форматирования номеров карт
и обработку некорректных диапазонов значений.
"""

# Инструменты для аннотации типов словарей, списков и объектов-генераторов
from typing import Any, Generator

# Фреймворк pytest для параметризации тестов, перехвата исключений и работы с фикстурами
import pytest

# Импорт тестируемых функций-генераторов из модуля generators
from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency_empty_list(empty_transactions: list[dict[str, Any]]) -> None:
    """Тест для проверки работы с пустым списком транзакций."""
    result = list(filter_by_currency(empty_transactions, "USD"))
    assert result == []


@pytest.mark.parametrize(
    "currency_code, expected_ids",
    [
        ("USD", [1, 3]),  # Ожидаем две транзакции в долларах
        ("EUR", [2]),  # Ожидаем одну транзакцию в евро
        ("RUB", []),  # Валюта, которой нет в списке (ожидаем пустой результат)
    ],
)
def test_filter_by_currency_success(
    sample_transactions: list[dict[str, Any]],
    currency_code: str,
    expected_ids: list[int],
) -> None:
    """Параметризованный тест для проверки фильтрации по разным валютам."""
    result = list(filter_by_currency(sample_transactions, currency_code))

    # Извлекаем ID для удобства проверки
    result_ids = [t.get("id") for t in result if "id" in t]

    assert result_ids == expected_ids


def test_transaction_descriptions_empty(empty_transactions: list[dict[str, Any]]) -> None:
    """Проверяем поведение генератора описаний на пустом списке."""
    gen = transaction_descriptions(empty_transactions)
    with pytest.raises(StopIteration):
        next(gen)


@pytest.mark.parametrize(
    "input_transactions, expected_descriptions",
    [
        # Случай 1: Все транзакции с описанием
        (
            [
                {"description": "Покупка продуктов"},
                {"description": "Кешбэк"},
            ],
            ["Покупка продуктов", "Кешбэк"],
        ),
        # Случай 2: Часть транзакций без описания
        (
            [
                {"description": "Перевод"},
                {"amount": 500},
                {},
            ],
            ["Перевод", "Описание отсутствует", "Описание отсутствует"],
        ),
        # Случай 3: Специфические значения (пустая строка)
        (
            [
                {"description": ""},
            ],
            [""],
        ),
    ],
    ids=["all_have_desc", "missing_desc", "empty_string_desc"],
)
def test_transaction_descriptions_parameterized(
    input_transactions: list[dict[str, Any]],
    expected_descriptions: list[str],
) -> None:
    """Параметризованная проверка различных сценариев наполнения данных."""
    gen = transaction_descriptions(input_transactions)
    result = list(gen)
    assert result == expected_descriptions


def test_generator_returns_iterator() -> None:
    """Проверяем, что функция возвращает объект-генератор."""
    gen = card_number_generator(1, 3)
    assert isinstance(gen, Generator)


def test_generator_correct_formatting() -> None:
    """Проверяем правильность формата (16 цифр, разделенных пробелами)."""
    gen = card_number_generator(12345, 12345)
    result = next(gen)
    assert result == "0000 0000 0001 2345"
    assert len(result) == 19  # 16 цифр + 3 пробела


def test_generator_range_boundaries(valid_small_range: dict[str, Any]) -> None:
    """Проверяем, что генерируется точное количество элементов, включая границы."""
    gen = card_number_generator(valid_small_range["start"], valid_small_range["end"])
    results = list(gen)
    assert results == valid_small_range["expected"]


@pytest.mark.parametrize(
    "start, end, expected_first, expected_last, expected_count",
    [
        (1, 1, "0000 0000 0000 0001", "0000 0000 0000 0001", 1),
        (9999, 10001, "0000 0000 0000 9999", "0000 0000 0001 0001", 3),
        (
            9999999999999998,
            9999999999999999,
            "9999 9999 9999 9998",
            "9999 9999 9999 9999",
            2,
        ),
    ],
)
def test_generator_valid_ranges(
    start: int,
    end: int,
    expected_first: str,
    expected_last: str,
    expected_count: int,
) -> None:
    """Параметризованный тест для проверки корректных диапазонов."""
    gen = list(card_number_generator(start, end))
    assert len(gen) == expected_count
    assert gen[0] == expected_first
    assert gen[-1] == expected_last


@pytest.mark.parametrize(
    "start, end",
    [
        (0, 5),  # Начало меньше 1
        (-10, 5),  # Отрицательное начало
        (10, 5),  # Конец меньше начала
        (1, 10000000000000000),  # Конец больше 16 цифр
    ],
)
def test_generator_invalid_ranges(start: int, end: int) -> None:
    """Проверка выброса ValueError при передаче некорректных границ диапазона."""
    with pytest.raises(ValueError):
        list(card_number_generator(start, end))
