import re


def filter_operations_by_description(
    operations: list[dict], search_string: str
) -> list[dict]:
    """Фильтрует список транзакций по заданной строке в описании."""
    if not search_string:
        return []

    # Экранируем спецсимволы в строке поиска для корректного регулярного выражения
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    filtered_operations = []

    for operation in operations:
        # Проверяем наличие ключа 'description' и строковый тип его значения
        description = operation.get("description")
        if isinstance(description, str) and pattern.search(description):
            filtered_operations.append(operation)

    return filtered_operations
