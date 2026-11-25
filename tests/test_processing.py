import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_empty_list(sample_date):
    """Тест пустых входных данных"""
    assert filter_by_state([]) == []


@pytest.mark.parametrize(
    "data, state, expected",
    [
        # 1. Обычная фильтрация (EXECUTED)
        (
            [
                {"id": 1, "state": "EXECUTED"},
                {"id": 2, "state": "CANCELED"},
                {"id": 3, "state": "EXECUTED"},
            ],
            "EXECUTED",
            [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}],
        ),
        # 2. Фильтрация другого состояния (CANCELED)
        (
            [
                {"id": 1, "state": "EXECUTED"},
                {"id": 2, "state": "CANCELED"},
            ],
            "CANCELED",
            [{"id": 2, "state": "CANCELED"}],
        ),
        # 3. Случай, когда ключа 'state' нет в словаре
        (
            [
                {"id": 1, "state": "EXECUTED"},
                {"id": 2},  # Ключа нет
                {"id": 3, "state": "EXECUTED"},
            ],
            "EXECUTED",
            [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}],
        ),
        # 4. Пустой список данных
        ([], "EXECUTED", []),
        # 5. Состояние, которого нет в списке
        (
            [{"id": 1, "state": "EXECUTED"}],
            "PENDING",
            [],
        ),
    ],
)
def test_filter_by_state(data, state, expected):
    """Тестирует фильтрацию списка словарей по заданному состоянию."""
    assert filter_by_state(data, state) == expected


def test_sort_by_date_descending(sample_operations):
    """Тест сортировки по убыванию (по умолчанию)"""
    result = sort_by_date(sample_operations)
    assert result[0]["id"] == 3
    assert result[1]["id"] == 1
    assert result[2]["id"] == 2


def test_sort_by_date_ascending(sample_operations):
    """Тест сортировки по возрастанию"""
    result = sort_by_date(sample_operations, descending=False)
    assert result[0]["id"] == 2
    assert result[1]["id"] == 1
    assert result[2]["id"] == 3


def test_sort_by_date_empty(sample_operations):
    """Тест работы с пустым списком"""
    assert sort_by_date([]) == []


def test_sort_by_date_immutability(sample_operations):
    """Проверка, что исходный список не изменился (функция возвращает новый)."""
    original_copy = sample_operations.copy()
    sort_by_date(sample_operations)
    assert sample_operations == original_copy


@pytest.mark.parametrize(
    "operations, descending, expected_order",
    [
        # 1. Одинаковые даты (сохранение порядка исходного списка - стабильная сортировка)
        (
            [{'date': '2023-01-01', 'id': 1}, {'date': '2023-01-01', 'id': 2}],
            True,
            [{'date': '2023-01-01', 'id': 1}, {'date': '2023-01-01', 'id': 2}]
        )
    ]
)
def test_sort_by_date_parametrized(operations, descending, expected_order):
    """Параметризованный тест для функции sort_by_date."""
    result = sort_by_date(operations, descending)
    assert result == expected_order
