import unittest
from unittest.mock import mock_open, patch

from src.utils import load_transactions


class TestLoadTransactions(unittest.TestCase):

    @patch('os.path.exists', return_value=False)
    def test_file_not_found(self, mock_exists):
        """Тест: Файл не найден."""
        result = load_transactions('non_existent_file.json')
        self.assertEqual(result, [])

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_file_is_empty(self, mock_file, mock_exists):
        """Тест: Файл существует, но пустой."""
        result = load_transactions('empty.json')
        self.assertEqual(result, [])

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_json_is_empty_list(self, mock_file, mock_exists):
        """Тест: В файле содержится пустой список []."""
        result = load_transactions('empty_list.json')
        self.assertEqual(result, [])

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='[{"id": 1, "amount": 100}]')
    def test_valid_json_list(self, mock_file, mock_exists):
        """Тест: Успешная загрузка списка транзакций."""
        result = load_transactions('valid.json')
        self.assertEqual(result, [{"id": 1, "amount": 100}])

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"not_a_list": "value"}')
    def test_json_is_not_list(self, mock_file, mock_exists):
        """Тест: JSON не является списком (например, передан словарь)."""
        result = load_transactions('not_a_list.json')
        self.assertEqual(result, [])

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='некорректный json контент')
    def test_json_decode_error(self, mock_file, mock_exists):
        """Тест: Ошибка декодирования JSON."""
        result = load_transactions('invalid_format.json')
        self.assertEqual(result, [])

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', side_effect=IOError)
    def test_io_error(self, mock_file, mock_exists):
        """Тест: Ошибка ввода-вывода (IOError) при чтении файла."""
        result = load_transactions('io_error_file.json')
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
