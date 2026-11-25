import pandas as pd

from src.pandas_library import read_transactions_from_excel


def test_read_transactions_from_excel_success(mocker):
    """Тестирует успешное чтение транзакций из Excel-файла.

    Проверяет, что при корректных данных pandas.read_excel вызывается
    с правильным путем, а результат преобразуется в список словарей.
    """
    # Создаем тестовый DataFrame, который должен вернуться при чтении Excel
    mock_df = pd.DataFrame({
        "date": ["2026-06-01"],
        "amount": [5000.0],
        "description": ["Зарплата"]
    })

    # Мокаем функцию pandas.read_excel
    mock_read_excel = mocker.patch("pandas.read_excel", return_value=mock_df)

    transactions = read_transactions_from_excel(file_path="dummy.xlsx")

    # Проверяем, что метод был вызван, и данные сконвертированы
    mock_read_excel.assert_called_once_with("dummy.xlsx")
    assert len(transactions) == 1
    assert transactions[0]["amount"] == 5000.0


def test_read_transactions_from_excel_exception(mocker, capsys):
    """Тестирует поведение функции при возникновении ошибки чтения Excel.

    Проверяет, что при исключении в pandas.read_excel функция перехватывает
    ошибку, выводит сообщение в консоль и возвращает пустой список.
    """
    # Мокаем pandas.read_excel так, чтобы она вызывала исключение
    mocker.patch("pandas.read_excel", side_effect=Exception("Файл поврежден"))

    transactions = read_transactions_from_excel(file_path="bad_file.xlsx")

    # Проверяем возврат пустого списка и перехват ошибки
    assert transactions == []
    captured = capsys.readouterr()
    assert "Ошибка при чтении файла: Файл поврежден" in captured.out
