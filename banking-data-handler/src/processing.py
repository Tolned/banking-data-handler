from typing import Dict, List


def filter_by_state(data: List[Dict], state: str = 'EXECUTED') -> List[Dict]:
    """
    Фильтрует data: список словарей по значению ключа 'state'.
    :param Список словарей для фильтрации.
    :param state: Значение состояния для фильтрации (по умолчанию 'EXECUTED').
    :return: Новый список словарей с соответствующим состоянием.
    """
    filtered_list = []
    for item in data:
        # Используем .get(), чтобы избежать ошибки, если ключа 'state' нет
        if item.get('state') == state:
            filtered_list.append(item)

    return filtered_list


def sort_by_date(operations: List[Dict], descending: bool = True) -> List[Dict]:
    """
    Сортирует список операций по дате (date).
    :param operations: Список словарей с операциями.
    :param descending: Порядок сортировки (True - убывание, False - возрастание).
    :return: Новый отсортированный список.
    """
    # sorted() создает новый список, не меняя старый.
    # Ключом сортировки служит значение по ключу 'date'.
    sorted_operations = sorted(
        operations,
        key=lambda x: x['date'],
        reverse=descending
    )

    return sorted_operations


# --- Пример использования ---
if __name__ == "__main__":  # pragma: no cover
    data = [
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    # Сортировка по убыванию (по умолчанию)
    print("--- По убыванию (сначала новые) ---")
    sorted_desc = sort_by_date(data)
    for op in sorted_desc:
        print(op)

# Пример использования
    data = [
        {'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    # Выход функции со статусом по умолчанию 'EXECUTED'
    print(filter_by_state(data))

    # Выход функции, если вторым аргументом передано 'CANCELED'
    print(filter_by_state(data, state='CANCELED'))
