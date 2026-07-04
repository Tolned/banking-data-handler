from typing import Any, Dict, Generator, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency_empty_list(sample_transactions):
    """Тест для проверки работы с пустым списком транзакций."""
    transactions: List[Dict[str, Any]] = []
    result = list(filter_by_currency(transactions, "USD"))
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
    sample_transactions: List[Dict[str, Any]],
    currency_code: str,
    expected_ids: List[int],
) -> None:
    """Параметризованный тест для проверки фильтрации по разным валютам."""
    result = list(filter_by_currency(sample_transactions, currency_code))

    # Извлекаем ID для удобства проверки
    result_ids = [t.get("id") for t in result if "id" in t]

    assert result_ids == expected_ids


def test_transaction_descriptions_empty(empty_transactions):
    """Проверяем поведение на пустом списке."""
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
                {"description": "Кешбэк"}
            ],
            ["Покупка продуктов", "Кешбэк"]
        ),
        # Случай 2: Часть транзакций без описания
        (
            [
                {"description": "Перевод"},
                {"amount": 500},
                {}
            ],
            ["Перевод", "Описание отсутствует", "Описание отсутствует"]
        ),
        # Случай 3: Специфические значения (пустая строка)
        (
            [
                {"description": ""}
            ],
            [""]
        )
    ],
    ids=["all_have_desc", "missing_desc", "empty_string_desc"]
)
def test_transaction_descriptions_parameterized(input_transactions, expected_descriptions):
    """Параметризованная проверка различных сценариев наполнения данных."""
    gen = transaction_descriptions(input_transactions)
    result = list(gen)
    assert result == expected_descriptions


def test_generator_returns_iterator(valid_small_range):
    """Проверяем, что функция возвращает генератор."""
    gen = card_number_generator(1, 3)
    assert isinstance(gen, Generator)


def test_generator_correct_formatting(valid_small_range):
    """Проверяем правильность формата (16 цифр, разделенных пробелами)."""
    gen = card_number_generator(12345, 12345)
    result = next(gen)
    assert result == "0000 0000 0001 2345"
    assert len(result) == 19  # 16 цифр + 3 пробела


def test_generator_range_boundaries(valid_small_range):
    """Проверяем, что генерируется точное количество элементов, включая границы."""
    gen = card_number_generator(1, 3)
    results = list(gen)
    assert len(results) == 3
    assert results[0] == "0000 0000 0000 0001"
    assert results[2] == "0000 0000 0000 0003"


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
            2
        ),
    ]
)
def test_generator_valid_ranges(start, end, expected_first, expected_last, expected_count):
    """Параметризованный тест для проверки корректных диапазонов."""
    gen = list(card_number_generator(start, end))
    assert len(gen) == expected_count
    assert gen[0] == expected_first
    assert gen[-1] == expected_last
