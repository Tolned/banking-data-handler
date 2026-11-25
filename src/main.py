"""
Главный модуль приложения для обработки и фильтрации банковских транзакций.

Объединяет загрузку данных из JSON, CSV и XLSX, фильтрацию по статусу,
валюте и ключевым словам, а также форматированный вывод операций в консоль.
"""

# Встроенный модуль для безопасного построения путей к файлам проекта
from pathlib import Path

# Импорт функций из внутренних модулей проекта
from src.masks import get_mask_card_number  # Замените на mask_account_card из src.widget, если он реализован
from src.pandas_library import read_transactions, read_transactions_from_excel
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions

# Определяем путь к папке data в корне проекта (на уровень выше папки src)
BASE_DIR = Path(__file__).resolve().parent.parent
JSON_FILE_PATH = BASE_DIR / "data" / "operations.json"


def main() -> None:
    """Основная логика проекта для консольного взаимодействия с пользователем."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # 1. Выбор источника данных
    choice = input("\nПользователь: ").strip()

    if choice == "1":
        print("\nПрограмма: Для обработки выбран JSON-файл.")
        transactions = load_transactions(str(JSON_FILE_PATH))
    elif choice == "2":
        print("\nПрограмма: Для обработки выбран CSV-файл.")
        transactions = read_transactions()
    elif choice == "3":
        print("\nПрограмма: Для обработки выбран XLSX-файл.")
        transactions = read_transactions_from_excel()
    else:
        print("\nПрограмма: Неверный пункт меню. Программа завершена.")
        return

    if not transactions:
        print("\nПрограмма: Данные не загружены или файл пуст.")
        return

    # 2. Фильтрация по статусу операции (с проверкой корректности ввода)
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status_input = input("\nПользователь: ").strip().upper()

        if status_input in valid_statuses:
            transactions = filter_by_state(transactions, status_input)
            print(f'\nПрограмма: Операции отфильтрованы по статусу "{status_input}"')
            break

        print(f'\nПрограмма: Статус операции "{status_input}" недоступен.')

    # 3. Сортировка по дате
    print("\nПрограмма: Отсортировать операции по дате? Да/Нет")
    sort_choice = input("\nПользователь: ").strip().lower()

    if sort_choice == "да":
        print("\nПрограмма: Отсортировать по возрастанию или по убыванию?")
        order_choice = input("\nПользователь: ").strip().lower()
        descending = "убыванию" in order_choice
        transactions = sort_by_date(transactions, descending=descending)

    # 4. Фильтрация по рублевым транзакциям (поддерживает форматы JSON и CSV/XLSX)
    print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет")
    rub_choice = input("\nПользователь: ").strip().lower()

    if rub_choice == "да":
        transactions = [
            t
            for t in transactions
            if t.get("currency_code") == "RUB"
            or t.get("currency") == "RUB"
            or (
                isinstance(t.get("operationAmount"), dict)
                and t["operationAmount"].get("currency", {}).get("code") == "RUB"
            )
        ]

    # 5. Фильтрация по ключевому слову в описании операции
    print("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    word_choice = input("\nПользователь: ").strip().lower()

    if word_choice == "да":
        search_word = input("\nВведите слово для поиска: ").strip().lower()
        transactions = [t for t in transactions if search_word in str(t.get("description") or "").lower()]

    # 6. Форматирование и вывод итогового списка транзакций
    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")

    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}\n")

    for t in transactions:
        # Приводим дату из формата YYYY-MM-DD... к виду ДД.ММ.ГГГГ
        raw_date = str(t.get("date") or "")[:10]
        if raw_date and "-" in raw_date:
            date_str = ".".join(reversed(raw_date.split("-")))
        else:
            date_str = "Нет даты"

        descr = str(t.get("description") or "Без описания")

        # Извлекаем сумму и код валюты с учетом различий между JSON и CSV/XLSX
        operation_amount = t.get("operationAmount")
        if isinstance(operation_amount, dict):
            amount = operation_amount.get("amount", "0")
            currency = operation_amount.get("currency", {}).get("code", "")
        else:
            amount = t.get("amount", "0")
            currency = t.get("currency_code") or t.get("currency") or ""

        # Форматируем сумму до двух знаков после запятой
        try:
            formatted_amount = f"{float(amount):.2f}"
        except (ValueError, TypeError):
            formatted_amount = str(amount)

        # Маскируем номера счетов или карт отправителя и получателя
        raw_from = str(t.get("from") or "")
        raw_to = str(t.get("to") or "")
        from_info = get_mask_card_number(raw_from) if raw_from else ""
        to_info = get_mask_card_number(raw_to) if raw_to else ""

        # Выводим карточку операции в консоль
        print(f"{date_str} {descr}")
        if from_info and to_info:
            print(f"{from_info} -> {to_info}")
        elif to_info:
            print(f"{to_info}")
        print(f"Сумма: {formatted_amount} {currency}\n")


if __name__ == "__main__":  # pragma: no cover
    main()
