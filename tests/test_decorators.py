"""
Модуль тестирования декоратора логирования @log.

Проверяет корректность записи сообщений об успешном выполнении функций
и возникших исключениях как в стандартный вывод (консоль), так и в файл.
"""

# Фреймворк pytest для перехвата исключений (pytest.raises) и использования фикстур
import pytest

# Импорт тестируемого декоратора логирования из модуля decorators
from src.decorators import log


def test_log_success_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест успешного выполнения функции с выводом лога в консоль."""

    @log()
    def my_func(x: int) -> int:
        return x * 2

    result = my_func(5)
    # Считываем перехваченный вывод из консоли
    captured = capsys.readouterr()

    assert result == 10
    assert "my_func ok" in captured.out


def test_log_error_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест перехвата ошибки с выводом информации об исключении в консоль."""

    @log()
    def fail_func(a: int, b: int) -> float:
        return a / b

    # Проверяем, что исключение ZeroDivisionError пробрасывается наружу
    with pytest.raises(ZeroDivisionError):
        fail_func(10, 0)

    captured = capsys.readouterr()
    assert "fail_func error: ZeroDivisionError" in captured.out
    assert "Inputs: (10, 0), {}" in captured.out


def test_log_success_file(log_file: str) -> None:
    """Тест успешного выполнения функции с записью лога в файл."""

    @log(filename=log_file)
    def add_func(x: int, y: int) -> int:
        return x + y

    result = add_func(3, 4)

    assert result == 7
    with open(log_file, mode="r", encoding="utf-8") as file:
        content = file.read()
    assert "add_func ok" in content


def test_log_error_file(log_file: str) -> None:
    """Тест записи информации об ошибке в файл при падении функции."""

    @log(filename=log_file)
    def fail_value_func(text: str) -> int:
        return int(text)

    with pytest.raises(ValueError):
        fail_value_func("не_число")

    with open(log_file, mode="r", encoding="utf-8") as file:
        content = file.read()
    assert "fail_value_func error: ValueError" in content
