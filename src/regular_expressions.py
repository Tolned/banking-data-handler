"""
Модуль для поиска банковских операций с использованием регулярных выражений.

Содержит функции для регистронезависимого поиска транзакций по ключевым
словам и фразам в описании платежа.
"""

# Встроенный модуль Python для работы с регулярными выражениями
import re

# Инструмент для указания типов содержимого словарей при проверке через mypy
from typing import Any


def filter_operations_by_description(operations: list[dict[str, Any]], search_string: str) -> list[dict[str, Any]]:
    """
    Фильтрует список транзакций по заданной строке поиска в описании ('description').

    :param operations: Список словарей с банковскими операциями.
    :param search_string: Строка или слово для поиска в описании операции.
    :return: Новый список транзакций, в описании которых найдено совпадение.
    """
    # Если строка поиска пустая, возвращаем пустой список
    if not search_string:
        return []

    # Экранируем спецсимволы (например, точки или скобки) и компилируем шаблон без учета регистра
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    filtered_operations: list[dict[str, Any]] = []

    for operation in operations:
        # Безопасно извлекаем описание и проверяем, что это именно строка
        description = operation.get("description")
        if isinstance(description, str) and pattern.search(description):
            filtered_operations.append(operation)

    return filtered_operations
