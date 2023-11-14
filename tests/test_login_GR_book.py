import unittest
from unittest.mock import patch, Mock
import login_GR_book  

class TestYourModule(unittest.TestCase):

    @patch('builtins.open')
    @patch('subprocess.Popen')
    @patch('login_GR_book.auth_flow.finish')
    @patch('login_GR_book.auth_code_entry.get')
    def test_get_key(self, mock_get, mock_finish, mock_popen, mock_open):
        
        mock_get.return_value = 'mocked_auth_code'

        mock_x = Mock()
        mock_x.access_token = 'mocked_access_token'
        mock_finish.return_value = mock_x

        login_GR_book.get_key()

        # Assertions
        mock_get.assert_called_once()  # Ensure auth_code_entry.get() was called
        mock_finish.assert_called_once_with('mocked_auth_code')  # Ensure auth_flow.finish() was called
        mock_open.assert_called_once_with('key.txt', 'w')  # Ensure open was called with the correct arguments
        mock_open().write.assert_called_once_with('mocked_access_token')  # Ensure write was called with the correct arguments
        mock_popen.assert_called_once_with(["python", "GR_book.py"])  # Ensure subprocess.Popen was called with the correct arguments

if __name__ == '__main__':
    unittest.main()