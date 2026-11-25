"""
Модуль тестирования функций чтения транзакций из CSV и Excel файлов.

Проверяет работу read_transactions и read_transactions_from_excel из модуля pandas_library
с использованием временных файлов (tmp_path), мок-объектов (mocker) и перехвата вывода (capsys).
"""

# Встроенный модуль для работы с путями во временной директории тестов
from pathlib import Path

# Библиотека pandas для создания тестовых объектов DataFrame
import pandas as pd

# Фреймворк pytest для использования встроенных фикстур (capsys, tmp_path)
import pytest

# Тип фикстуры mocker из плагина pytest-mock для проверки кода через mypy
from pytest_mock import MockerFixture

# Импорт тестируемых функций чтения CSV и Excel из модуля pandas_library
from src.pandas_library import read_transactions, read_transactions_from_excel


def test_read_transactions_csv_success(tmp_path: Path) -> None:
    """Тестирует успешное чтение и парсинг транзакций из CSV-файла."""
    # Создаем временный CSV-файл с разделителем ';'
    csv_file = tmp_path / "test_transactions.csv"
    csv_content = (
        "id;state;date;amount;currency_code;description\n"
        "1;EXECUTED;2026-06-01;1500.50;RUB;Оплата услуг\n"
        "2;CANCELED;2026-06-02;invalid_amount;USD;Перевод\n"
    )
    csv_file.write_text(csv_content, encoding="utf-8")

    transactions = read_transactions(file_path=str(csv_file))

    assert len(transactions) == 2
    assert transactions[0]["amount"] == 1500.50
    assert transactions[0]["description"] == "Оплата услуг"
    # Проверяем, что некорректная сумма корректно превратилась в 0.0
    assert transactions[1]["amount"] == 0.0


def test_read_transactions_csv_file_not_found(capsys: pytest.CaptureFixture[str]) -> None:
    """Тестирует возврат пустого списка и вывод сообщения, если CSV-файл не найден."""
    transactions = read_transactions(file_path="non_existent_file.csv")

    assert transactions == []
    captured = capsys.readouterr()
    assert "не найден" in captured.out


def test_read_transactions_from_excel_success(mocker: MockerFixture) -> None:
    """Тестирует успешное чтение транзакций из Excel-файла с помощью мока pandas.read_excel."""
    # Создаем тестовый DataFrame, который должен вернуться при чтении Excel
    mock_df = pd.DataFrame(
        {
            "date": ["2026-06-01"],
            "amount": [5000.0],
            "description": ["Зарплата"],
        }
    )

    # Мокаем функцию pandas.read_excel
    mock_read_excel = mocker.patch("pandas.read_excel", return_value=mock_df)

    transactions = read_transactions_from_excel(file_path="dummy.xlsx")

    # Проверяем, что метод был вызван один раз, а данные сконвертированы в список словарей
    mock_read_excel.assert_called_once()
    assert len(transactions) == 1
    assert transactions[0]["amount"] == 5000.0
    assert transactions[0]["description"] == "Зарплата"


def test_read_transactions_from_excel_exception(
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Тестирует перехват исключения и возврат пустого списка при ошибке чтения Excel."""
    # Мокаем pandas.read_excel так, чтобы она вызывала исключение
    mocker.patch("pandas.read_excel", side_effect=Exception("Файл поврежден"))

    transactions = read_transactions_from_excel(file_path="bad_file.xlsx")

    # Проверяем возврат пустого списка и вывод сообщения об ошибке в консоль
    assert transactions == []
    captured = capsys.readouterr()
    assert "Ошибка при чтении файла: Файл поврежден" in captured.out
