"""
Модуль тестирования функций маскирования банковских карт и счетов.

Проверяет корректность работы get_mask_card_number и get_mask_account_number
на стандартных данных (с названием платежной системы и без), а также
обработку граничных и некорректных значений (пустые строки, короткие номера, None).
"""

# Инструмент для указания произвольного типа входных данных при проверке некорректных значений
from typing import Any

# Фреймворк pytest для параметризации тестовых сценариев
import pytest

# Импорт тестируемых функций маскирования карт и счетов из модуля masks
from src.masks import get_mask_account_number, get_mask_card_number


def test_get_mask_card_number_with_name() -> None:
    """Тест маскирования карты с названием платежной системы."""
    card = "Visa Platinum 7000792289606361"
    assert get_mask_card_number(card) == "Visa Platinum 7000 79** **** 6361"


def test_get_mask_card_number_only_digits() -> None:
    """Тест маскирования карты, если переданы только цифры без названия."""
    card = "7000792289606361"
    assert get_mask_card_number(card) == "7000 79** **** 6361"


@pytest.mark.parametrize(
    "card_input, expected_output",
    [
        # Корректные карты с разными названиями
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        # Граничные случаи: слишком короткий номер, пустая строка и None
        ("Visa 12345", "Visa 12345"),
        ("", ""),
        (None, ""),
    ],
)
def test_get_mask_card_number_parametrized(card_input: Any, expected_output: str) -> None:
    """Параметризованный тест для различных карт и некорректных входных данных."""
    assert get_mask_card_number(card_input) == expected_output


def test_get_mask_account_number_with_name() -> None:
    """Тест маскирования счета со словом 'Счет'."""
    account = "Счет 73654108430135874305"
    assert get_mask_account_number(account) == "Счет **4305"


@pytest.mark.parametrize(
    "account_input, expected_output",
    [
        # Счета с названиями
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Текущий счет 9876543210", "Текущий счет **3210"),
        # Счет без текстового названия
        ("73654108430135874305", "**4305"),
        # Граничные случаи: некорректная длина или невалидный тип данных
        ("123", "123"),
        ("", ""),
        (None, ""),
    ],
)
def test_get_mask_account_number_parametrized(account_input: Any, expected_output: str) -> None:
    """Параметризованный тест для различных типов счетов и некорректных данных."""
    assert get_mask_account_number(account_input) == expected_output
