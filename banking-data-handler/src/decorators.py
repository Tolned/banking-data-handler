import logging
import sys
from functools import wraps
from typing import Any, Callable, Optional

from click.core import F


def log(filename: Optional[str] = None) -> Callable[[F], F]:
    """Логирует начало и конец выполнения функции, а также ее результаты или возникшие ошибки."""
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Настройка логгера
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)
            logger.handlers.clear()  # Очищаем старые обработчики, чтобы избежать дублирования

            # Определение вывода (файл или консоль)
            if filename:
                handler = logging.FileHandler(filename, encoding='utf-8')
            else:
                handler = logging.StreamHandler(sys.stdout)

            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            try:
                # Выполнение функции
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok")
                return result
            except Exception as e:
                # Обработка ошибки
                error_type = type(e).__name__
                logger.error(f"{func.__name__} error: {error_type}. Inputs: {args}, {kwargs}")
                raise

        return wrapper
    return decorator


# Пример использования
if __name__ == "__main__":  # pragma: no cover
    @log(filename="mylog.txt")
    def my_function(x, y):
        return x + y
    my_function(1, 2)
