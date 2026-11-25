from collections import Counter
from typing import Any, Dict, List


def count_operations_by_category(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество банковских операций для заданного списка категорий.

    :param transactions: Список словарей, содержащих данные о транзакциях (должен быть ключ 'description').
    :param categories: Список строк с названиями категорий для подсчета.
    :return: Словарь с количеством операций для каждой категории.
    """
    # Извлекаем названия категорий (поле 'description') из всех транзакций
    descriptions = [transaction.get("description") for transaction in transactions if "description" in transaction]

    # Используем Counter для подсчета вхождений
    description_counts = Counter(descriptions)

    # Формируем результат только для тех категорий, которые есть в переданном списке
    result = {category: description_counts.get(category, 0) for category in categories}

    return result
