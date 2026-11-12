"""
Модуль для первичной фильтрации и сортировки банковских операций.

Содержит функции для отбора транзакций по статусу выполнения
и упорядочивания списка операций по дате совершения.
"""

# Инструмент для указания произвольного типа значений в словарях транзакций
from typing import Any


def filter_by_state(data: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param data: Список словарей с банковскими операциями для фильтрации.
    :param state: Значение состояния для отбора (по умолчанию 'EXECUTED').
    :return: Новый список словарей с соответствующим состоянием.
    """
    # Создаем новый список, чтобы не изменять исходные данные
    filtered_list: list[dict[str, Any]] = []

    for item in data:
        # Используем .get(), чтобы избежать ошибки KeyError, если ключа 'state' нет в словаре
        if item.get("state") == state:
            filtered_list.append(item)

    return filtered_list


def sort_by_date(operations: list[dict[str, Any]], descending: bool = True) -> list[dict[str, Any]]:
    """
    Сортирует список операций по дате ('date').

    :param operations: Список словарей с банковскими операциями.
    :param descending: Порядок сортировки (True — по убыванию, False — по возрастанию).
    :return: Новый отсортированный список операций.
    """
    # Функция sorted() возвращает новый список, оставляя исходный без изменений.
    # Конструкция str(x.get('date') or '') защищает от падения, если дата отсутствует или равна None.
    sorted_operations = sorted(
        operations,
        key=lambda x: str(x.get("date") or ""),
        reverse=descending,
    )

    return sorted_operations


# Пример локального запуска для ручной проверки (исключен из подсчета покрытия тестами)
if __name__ == "__main__":  # pragma: no cover
    sample_data: list[dict[str, Any]] = [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    # Сортировка по убыванию (по умолчанию — сначала самые новые)
    print("--- По убыванию (сначала новые) ---")
    for op in sort_by_date(sample_data):
        print(op)

    # Фильтрация со статусом по умолчанию ('EXECUTED')
    print("\n--- Только выполненные (EXECUTED) ---")
    print(filter_by_state(sample_data))

    # Фильтрация со статусом 'CANCELED'
    print("\n--- Только отмененные (CANCELED) ---")
    print(filter_by_state(sample_data, state="CANCELED"))
