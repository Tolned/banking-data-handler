import pytest

from src.decorators import log


def test_log_success_stdout(log_file, capsys):
    """Тест успешного выполнения (консоль и capsys)."""
    @log()
    def my_func(x):
        return x * 2

    result = my_func(5)
    captured = capsys.readouterr()

    assert result == 10
    assert "my_func ok" in captured.out


def test_log_error_stdout(log_file, capsys):
    """Тест перехвата ошибки (консоль и capsys)."""
    @log()
    def fail_func(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        fail_func(10, 0)

    captured = capsys.readouterr()
    assert "fail_func error: ZeroDivisionError" in captured.out
