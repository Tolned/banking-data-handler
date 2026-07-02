import csv
import os
from typing import Any, Dict, Hashable, List

import pandas as pd

# Константа для валюты
RUB = "RUB"


def read_transactions(file_path: str = "../data/transactions.csv") -> List[Dict[str, Any]]:
    """
    Считывает финансовые транзакции из CSV-файла.

    Функция определяет абсолютный путь к файлу относительно текущего
    расположения модуля, читает CSV-файл с разделителем `;` и преобразует
    значение поля `amount` в число типа `float`.

    Если преобразование `amount` невозможно (например, пустая строка
    или некорректное значение), ему присваивается 0.0.

    Args:
        file_path (str, optional):
            Относительный или абсолютный путь к CSV-файлу.
            По умолчанию: "../data/transactions.csv".

    Returns:
        List[Dict[str, Any]]:
            Список транзакций, где каждая транзакция представлена словарём:
            - ключи — названия колонок CSV
            - значения — данные строки

            Возвращает пустой список, если файл не найден.

    Raises:
        Никакие исключения не пробрасываются наружу.
        FileNotFoundError обрабатывается внутри функции.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, file_path)

    transactions = []
    try:
        with open(full_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                if "amount" in row:
                    try:
                        row["amount"] = float(row["amount"])
                    except ValueError:
                        row["amount"] = 0
                transactions.append(row)

    except FileNotFoundError:
        print(f"Ошибка: Файл {full_path} не найден.")

    return transactions


def read_transactions_from_excel(file_path="../data/transactions_excel.xlsx") -> list[dict[Hashable, Any]] | list[Any]:
    """
    Считывает финансовые операции из файла Excel и возвращает их в виде списка словарей.

    :return: Список словарей с данными транзакций
    """
    try:
        df = pd.read_excel(file_path)

        # Приводим названия колонок к строкам и удаляем пустые строки
        df.columns = df.columns.astype(str)
        df = df.dropna(how='all')

        # Превращаем DataFrame в список словарей
        transactions = df.to_dict(orient='records')
        return transactions

    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


# Пример использования:
if __name__ == "__main__":  # pragma: no cover
    # 1. Загружаем ВСЕ транзакции
    all_transactions = read_transactions()

    if not all_transactions:
        print("Список транзакций пуст или файл не найден.")
    else:
        # 2. Запрашиваем выбор пользователя
        print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет")
        rub_choice = input("\nПользователь: ").strip().lower()

        if rub_choice == "да":
            rub_transactions = [t for t in all_transactions if t.get("currency_code") == "RUB"]
            if rub_transactions:
                print(f"\nПрограмма: Найдено транзакций в рублях: {len(rub_transactions)}")
                print("-" * 50)
                for idx, tx in enumerate(rub_transactions, 1):
                    amount = tx.get('amount', 0)
                    description = tx.get("description", "Без описания")
                    date = tx.get("date", "Нет даты")
                    print(f"{idx}. {date[:10]} | {description} | {amount:.2f} RUB")
            else:
                print("\nПрограмма: Рублевые транзакции не найдены.")
        elif rub_choice == "нет":
            print(f"\nПрограмма: Вывожу все транзакции (всего: {len(all_transactions)}):")
            print("-" * 50)
            for idx, tx in enumerate(all_transactions, 1):
                print(f"{idx}. {tx}")
        else:
            print("\nПрограмма: Некорректный ввод. Пожалуйста, введите Да или Нет.")

    # Пример для excel
    data = read_transactions_from_excel()
    print(data)
