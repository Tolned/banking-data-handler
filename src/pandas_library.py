"""
Модуль для чтения финансовых транзакций из табличных файлов (CSV и Excel).

Содержит функции для загрузки и первичной обработки данных о банковских
операциях из форматов .csv (через стандартный модуль csv) и .xlsx (через библиотеку pandas).
"""

# Встроенные модули для работы с CSV-файлами и путями файловой системы
import csv
import os

# Инструменты для аннотации типов и проверки через mypy
from typing import Any

# Библиотека для анализа данных и чтения таблиц Excel
import pandas as pd

# Константа для обозначения кода российской валюты
RUB = "RUB"


def _resolve_file_path(file_path: str) -> str:
    """Вспомогательная функция: строит абсолютный путь к файлу относительно текущего модуля."""
    if os.path.isabs(file_path):
        return file_path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, file_path)


def read_transactions(file_path: str = "../data/transactions.csv") -> list[dict[str, Any]]:
    """
    Считывает финансовые транзакции из CSV-файла с разделителем ';'.

    :param file_path: Относительный или абсолютный путь к CSV-файлу.
    :return: Список словарей с транзакциями (пустой список, если файл не найден).
    """
    full_path = _resolve_file_path(file_path)
    transactions: list[dict[str, Any]] = []

    try:
        with open(full_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                # Создаем копию строки с типом Any для значений, чтобы избежать конфликта типов с float
                typed_row: dict[str, Any] = dict(row)
                if "amount" in typed_row:
                    try:
                        typed_row["amount"] = float(typed_row["amount"])
                    except (ValueError, TypeError):
                        typed_row["amount"] = 0.0
                transactions.append(typed_row)

    except FileNotFoundError:
        print(f"Ошибка: Файл {full_path} не найден.")

    return transactions


def read_transactions_from_excel(file_path: str = "../data/transactions_excel.xlsx") -> list[dict[str, Any]]:
    """
    Считывает финансовые операции из файла Excel (.xlsx) и возвращает список словарей.

    :param file_path: Относительный или абсолютный путь к XLSX-файлу.
    :return: Список словарей с данными транзакций (пустой список при ошибке чтения).
    """
    full_path = _resolve_file_path(file_path)

    try:
        # Считываем таблицу Excel в объект DataFrame
        df = pd.read_excel(full_path)

        # Приводим названия колонок к строкам и удаляем полностью пустые строки
        df.columns = df.columns.astype(str)
        df = df.dropna(how="all")

        # Превращаем таблицу DataFrame в список словарей формата [{колонка: значение}, ...]
        raw_records = df.to_dict(orient="records")
        return [{str(k): v for k, v in record.items()} for record in raw_records]

    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


# Пример локального запуска для ручной проверки (исключен из подсчета покрытия тестами)
if __name__ == "__main__":  # pragma: no cover
    all_transactions = read_transactions()

    if not all_transactions:
        print("Список транзакций пуст или файл не найден.")
    else:
        print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет")
        rub_choice = input("\nПользователь: ").strip().lower()

        if rub_choice == "да":
            rub_transactions = [t for t in all_transactions if t.get("currency_code") == RUB]
            if rub_transactions:
                print(f"\nПрограмма: Найдено транзакций в рублях: {len(rub_transactions)}")
                print("-" * 50)
                for idx, tx in enumerate(rub_transactions, 1):
                    amount = tx.get("amount", 0.0)
                    description = tx.get("description", "Без описания")
                    date = str(tx.get("date", "Нет даты"))
                    print(f"{idx}. {date[:10]} | {description} | {amount:.2f} {RUB}")
            else:
                print("\nПрограмма: Рублевые транзакции не найдены.")
        elif rub_choice == "нет":
            print(f"\nПрограмма: Вывожу все транзакции (всего: {len(all_transactions)}):")
            print("-" * 50)
            for idx, tx in enumerate(all_transactions, 1):
                print(f"{idx}. {tx}")
        else:
            print("\nПрограмма: Некорректный ввод. Пожалуйста, введите Да или Нет.")

    # Проверка чтения из Excel
    excel_data = read_transactions_from_excel()
    print(f"\nЗагружено записей из Excel: {len(excel_data)}")
