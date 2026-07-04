from src.regular_expressions import filter_operations_by_description


def test_filter_empty_search_string(sample_operations_two):
    """Тест пустого поиска."""
    result = filter_operations_by_description(sample_operations_two, "")
    assert result == []


def test_filter_empty_operations_list(sample_operations_two):
    """Тест пустого списка операций."""
    result = filter_operations_by_description([], "интернет")
    assert result == []


def test_filter_empty_search(sample_operations_two):
    """Тест пустого поиска."""
    result = filter_operations_by_description(sample_operations_two, "")
    assert result == []


def test_filter_empty_operations(sample_operations_two):
    """Тест пустого списка операций."""
    result = filter_operations_by_description([], "интернет")
    assert result == []
