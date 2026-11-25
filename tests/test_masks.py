import pytest

from src.masks import get_mask_account_number, get_mask_card_number


def test_get_mask_card_number_with_name() -> None:
    """Тест маскирования карты с названием платежной системы."""
    card = "Visa Platinum 7000792289606361"
    assert get_mask_card_number(card) == "Visa Platinum 7000 79** **** 6361"


def test_get_mask_card_number_only_digits() -> None:
    """Тест маскирования карты, если переданы только цифры."""
    card = "7000792289606361"
    assert get_mask_card_number(card) == "7000 79** **** 6361"


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
    ]
)
def test_get_mask_account_number_parametrized(account_input: str, expected_output: str) -> None:
    """Параметризованный тест для различных типов счетов и некорректных данных."""
    assert get_mask_account_number(account_input) == expected_output
