from unittest.mock import patch

from src.main import main


@patch('src.main.print')
@patch('src.main.input')
def test_main_invalid_menu_choice(mock_input, mock_print):
    """Тест ввода неверного пункта меню (программа должна завершиться)."""
    mock_input.return_value = '5'

    main()

    # Проверяем, что вывелось сообщение об ошибке
    mock_print.assert_any_call('\nПрограмма: Неверный пункт меню. Программа завершена.')
