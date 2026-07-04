from src.regular_expressions import filter_operations_by_description


def test_filter_by_description_success(sample_operations_three):
    """Проверка успешной фильтрации по обычному слову."""
    result = filter_operations_by_description(sample_operations_three, "Перевод")
    assert len(result) == 3
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3
    assert result[2]["id"] == 5


def test_filter_by_description_ignore_case(sample_operations_three):
    """Проверка работы фильтра без учета регистра."""
    result = filter_operations_by_description(sample_operations_three, "пЕрЕвОд")
    assert len(result) == 3


def test_filter_by_description_with_special_characters(sample_operations_three):
    """Проверка корректного экранирования спецсимволов."""
    result = filter_operations_by_description(sample_operations_three, "(Visa/Mastercard)")
    assert len(result) == 1
    assert result[0]["id"] == 5
