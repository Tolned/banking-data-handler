from src.masks import get_mask_card_number
from src.pandas_library import read_transactions, read_transactions_from_excel
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions


def main() -> None:
    """Основная логика проекта для взаимодействия с пользователем."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # 1. Выбор файла
    choice = input("\nПользователь: ").strip()

    if choice == "1":
        print("\nПрограмма: Для обработки выбран JSON-файл.")
        file_path = "../data/operations.json"
        transactions = load_transactions(file_path)
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

    # 2. Фильтрация по статусу (с валидацией)
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status_input = input("\nПользователь: ").strip().upper()

        if status_input in valid_statuses:
            transactions = filter_by_state(transactions, status_input)
            print(f'\nПрограмма: Операции отфильтрованы по статусу "{status_input}"')
            break
        else:
            print(f'\nПрограмма: Статус операции "{status_input}" недоступен.')

    # 3. Сортировка по дате
    print("\nПрограмма: Отсортировать операции по дате? Да/Нет")
    sort_choice = input("\nПользователь: ").strip().lower()

    if sort_choice == "да":
        print("\nПрограмма: Отсортировать по возрастанию или по убыванию?")
        order_choice = input("\nПользователь: ").strip().lower()
        descending = True if "убыванию" in order_choice else False
        transactions = sort_by_date(transactions, descending=descending)

    # 4. Фильтрация по валюте (Рубли) — УНИВЕРСАЛЬНАЯ
    print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет")
    rub_choice = input("\nПользователь: ").strip().lower()

    if rub_choice == "да":
        # Проверяем структуру JSON и плоскую структуру CSV/Excel одновременно
        transactions = [
            t for t in transactions
            if t.get("currency_code") == "RUB"
            or t.get("currency") == "RUB"
            or t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]
        # Отладочный принт, теперь он не будет пустым для CSV/Excel!
        print(f"\n[ОТЛАДКА] Найдено рублевых транзакций: {len(transactions)}")

    # 5. Фильтрация по слову в описании
    print("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    word_choice = input("\nПользователь: ").strip().lower()

    if word_choice == "да":
        search_word = input("\nВведите слово для поиска: ").strip().lower()
        # Убрана ошибочная функция filter_by_currency
        transactions = [
            t for t in transactions
            if search_word in t.get("description", "").lower()
        ]

    # 6. Вывод результатов
    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")

    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}\n")

    for t in transactions:
        # Извлечение и форматирование даты
        date_str = t.get("date", "")[:10]
        if date_str and "-" in date_str:
            date_str = ".".join(reversed(date_str.split("-")))
        else:
            date_str = "Нет даты"

        descr = t.get("description", "Без описания")

        # Извлечение суммы и валюты под оба формата файлов
        if "operationAmount" in t and isinstance(t["operationAmount"], dict):
            amount = t["operationAmount"].get("amount", "0")
            currency = t["operationAmount"].get("currency", {}).get("code", "")
        else:
            amount = t.get("amount", "0")
            currency = t.get("currency_code") or t.get("currency") or ""

        # Форматирование суммы до копеек
        try:
            amount = f"{float(amount):.2f}"
        except (ValueError, TypeError):
            amount = str(amount)

        # Маскирование счетов/карт перед выводом
        from_info = get_mask_card_number(t.get("from", ""))
        to_info = get_mask_card_number(t.get("to", ""))

        # Вывод в требуемом красивом формате
        print(f"{date_str} {descr}")
        if from_info and to_info:
            print(f"{from_info} -> {to_info}")
        elif to_info:
            print(f"{to_info}")
        print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":  # pragma: no cover
    main()
