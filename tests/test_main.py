"""
Модуль тестирования главной функции приложения main().

Проверяет сценарии консольного взаимодействия с пользователем с помощью
встроенных фикстур pytest: capsys (перехват вывода) и monkeypatch (имитация ввода).
"""

# Стандартный модуль для работы с потоками ввода-вывода (имитация клавиатуры)
import io

# Инструмент для указания произвольного типа значений в словарях
from typing import Any

# Фреймворк pytest для перехвата вывода в консоль (capsys) и подмены объектов (monkeypatch)
import pytest

# Импорт главной функции приложения из модуля main
from src.main import main


def test_main_invalid_menu_choice(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Тест ввода неверного пункта меню (программа должна завершиться)."""
    # Имитируем ввод пользователем числа '5' с клавиатуры
    monkeypatch.setattr("sys.stdin", io.StringIO("5\n"))

    main()

    # Перехватываем весь текст, который программа вывела в консоль через print()
    captured = capsys.readouterr()
    assert "Неверный пункт меню. Программа завершена." in captured.out


def test_main_empty_transactions(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Тест поведения программы при выборе JSON-файла, если список транзакций пуст."""
    monkeypatch.setattr("sys.stdin", io.StringIO("1\n"))
    monkeypatch.setattr("src.main.load_transactions", lambda _: [])

    main()

    captured = capsys.readouterr()
    assert "Данные не загружены или файл пуст." in captured.out


def test_main_full_flow_success(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Тест полного цикла работы программы: загрузка JSON, фильтрация и вывод транзакции."""
    # Передаем последовательность ответов пользователя через перенос строки \n
    user_inputs = "1\nEXECUTED\nнет\nда\nнет\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(user_inputs))

    # Подготавливаем тестовую рублевую транзакцию
    mock_data: list[dict[str, Any]] = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-03-11T02:26:18.671407",
            "operationAmount": {"amount": "1500.00", "currency": {"code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Classic 6831982476737658",
            "to": "Счет 73654108430135874305",
        }
    ]
    monkeypatch.setattr("src.main.load_transactions", lambda _: mock_data)

    main()

    captured = capsys.readouterr()
    assert "Всего банковских операций в выборке: 1" in captured.out
