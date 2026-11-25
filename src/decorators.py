"""
Модуль для логирования работы функций.

Содержит декоратор @log, который записывает в файл или выводит в консоль статус
успешного выполнения функции либо информацию о возникшей ошибке.
"""

# Встроенный модуль Python для ведения журналов событий (логов)
import logging

# Встроенный модуль для доступа к стандартному потоку вывода (консоли)
import sys

# Инструмент, который сохраняет исходное имя и документацию декорируемой функции
from functools import wraps

# Инструменты для аннотации типов и проверки кода через mypy
from typing import Any, Callable, Optional, TypeVar

# Создаем универсальный тип F для обозначения любой переданной в декораторе функции
F = TypeVar("F", bound=Callable[..., Any])


def log(filename: Optional[str] = None) -> Callable[[F], F]:
    """Логирует результат выполнения функции или возникшие ошибки в файл или консоль."""

    # Внутренняя функция, которая принимает саму декорируемую функцию (например, my_function)
    def decorator(func: F) -> F:

        # @wraps(func) копирует метаданные (имя, докстринг) из func в wrapper
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Создаем или получаем логгер с именем декорируемой функции
            logger = logging.getLogger(func.__name__)
            # Устанавливаем минимальный уровень важности сообщений (INFO и выше, включая ERROR)
            logger.setLevel(logging.INFO)
            # Очищаем старые обработчики, чтобы при повторном вызове функции логи не дублировались
            logger.handlers.clear()

            # Выбираем, куда отправлять записи: в файл на диске или в консоль
            handler: logging.Handler
            if filename:
                handler = logging.FileHandler(filename, encoding="utf-8")
            else:
                handler = logging.StreamHandler(sys.stdout)

            # Задаем формат записи: выводим только само сообщение без лишних дат и тегов
            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            # Привязываем настроенный обработчик к логгеру
            logger.addHandler(handler)

            try:
                # Пытаемся выполнить исходную функцию с переданными аргументами
                result = func(*args, **kwargs)
                # Если ошибок не было, записываем сообщение об успехе
                logger.info(f"{func.__name__} ok")
                # Возвращаем результат работы функции
                return result
            except Exception as e:
                # Если внутри функции произошла ошибка, узнаем название ее класса (например, ValueError)
                error_type = type(e).__name__
                # Записываем в лог имя функции, тип ошибки и аргументы, с которыми она упала
                logger.error(f"{func.__name__} error: {error_type}. Inputs: {args}, {kwargs}")
                # Пробрасываем ошибку дальше, чтобы программа знала о сбое (не «проглатываем» ее)
                raise
            finally:
                # Обязательно закрываем файл и отвязываем обработчик, чтобы Windows не блокировал файл в тестах
                handler.close()
                logger.removeHandler(handler)

        # Возвращаем функцию-обертку
        return wrapper  # type: ignore[return-value]

    return decorator


# Блок с примером запуска. Комментарий # pragma: no cover говорит pytest-cov не учитывать этот блок при подсчете
# покрытия тестами
if __name__ == "__main__":  # pragma: no cover

    @log(filename="mylog.txt")
    def my_function(x: int, y: int) -> int:
        return x + y

    my_function(1, 2)
