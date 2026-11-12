"""
Модуль тестирования функций виджетов (mask_account_card и get_date).

Проверяет маскирование номеров различных платежных систем и банковских счетов,
а также преобразование строк даты и времени в формат 'ДД.ММ.ГГГГ' и обработку ошибок.
"""

# Фреймворк pytest для параметризации тестовых сценариев и перехвата исключений
import pytest

# Импорт тестируемых функций форматирования реквизитов и дат из модуля widget
from src.widget import get_date, mask_account_card


def test_mask_account_card_visa(card_info: str) -> None:
    """Тест для карты Visa с использованием фикстуры card_info."""
    assert mask_account_card(card_info) == "Visa Platinum 7000 79** **** 6617"


def test_mask_account_card_mastercard() -> None:
    """Тест для карты MasterCard."""
    arg = "MasterCard 7158300714729458"
    expected = "MasterCard 7158 30** **** 9458"
    assert mask_account_card(arg) == expected


def test_mask_account_card_account() -> None:
    """Тест для банковского счета."""
    arg = "Счет 73654108430135874305"
    expected = "Счет **4305"
    assert mask_account_card(arg) == expected


def test_mask_account_card_maestro() -> None:
    """Тест для карты с коротким названием платежной системы."""
    arg = "Maestro 1596837812345511"
    expected = "Maestro 1596 83** **** 5511"
    assert mask_account_card(arg) == expected


@pytest.mark.parametrize(
    "info, expected",
    [
        ("Visa Classic 6831982476731327", "Visa Classic 6831 98** **** 1327"),
        ("Счет 64686453647365145212", "Счет **5212"),
        ("", ""),
    ],
)
def test_mask_account_card_parametrized(info: str, expected: str) -> None:
    """Параметризованный тест для разных карт, счетов и пустой строки."""
    assert mask_account_card(info) == expected


def test_get_date_valid(valid_date_str: str) -> None:
    """Проверка корректного преобразования даты с использованием фикстуры valid_date_str."""
    assert get_date(valid_date_str) == "11.03.2024"
    assert get_date("2023-12-31T23:59:59.999999") == "31.12.2023"


def test_get_date_invalid_format() -> None:
    """Проверка поведения при неверном формате даты (ожидается ValueError)."""
    with pytest.raises(ValueError):
        get_date("11-03-2024")


@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2025-01-01T00:00:00.000000", "01.01.2025"),
    ],
)
def test_get_date(input_str: str, expected_output: str) -> None:
    """Параметризованный тест форматирования разных дат."""
    assert get_date(input_str) == expected_output
