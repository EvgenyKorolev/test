import subprocess
import sys
from io import StringIO
from unittest.mock import patch, mock_open

from subscriber import (
    PrintOutput,
    SentToAllOutput,
    WriteToFile,
    PrintNull,
    PrintInErr,
)

# Тесты для класса PrintOutput
def test_print_output_key():
    subscriber = PrintOutput()
    assert subscriber.key() == 'stdout'

@patch('builtins.print')
def test_print_output_update(mock_print):
    subscriber = PrintOutput()
    message = "Test message"
    subscriber.update(message)
    mock_print.assert_called_once_with(message)

# Тесты для класса SentToAllOutput
def test_sent_to_all_output_key():
    subscriber = SentToAllOutput()
    assert subscriber.key() == 'wall'

@patch('subprocess.Popen')
def test_sent_to_all_output_update(mock_popen):
    mock_process = mock_popen.return_value
    mock_process.communicate.return_value = (None, None)
    
    subscriber = SentToAllOutput()
    message = "Wall message"
    subscriber.update(message)
    
    mock_popen.assert_called_once_with(['wall'], stdin=subprocess.PIPE, text=True)
    mock_process.communicate.assert_called_once_with(input=message)

@patch('subprocess.Popen', side_effect=Exception("Test error"))
def test_sent_to_all_output_update_exception(mock_popen):
    subscriber = SentToAllOutput()
    subscriber.update("Message")
    # Проверяем, что исключение перехватывается и метод завершается без ошибки

# Тесты для класса WriteToFile
def test_write_to_file_key():
    subscriber = WriteToFile()
    assert subscriber.key() == 'file'

@patch('builtins.open', new_callable=mock_open)
def test_write_to_file_update(mock_file):
    subscriber = WriteToFile()
    message = "Log message"
    subscriber.update(message)
    mock_file.assert_called_once_with('log.txt', 'a', encoding='utf-8')
    mock_file().write.assert_called_once_with(message + '\n')

@patch('builtins.open', new_callable=mock_open)
def test_write_to_file_set_filename(mock_file):
    subscriber = WriteToFile()
    new_filename = 'custom.log'
    subscriber.setFileName(new_filename)
    message = "Custom log"
    subscriber.update(message)
    mock_file.assert_called_with(new_filename, 'a', encoding='utf-8')

# Тесты для класса PrintNull
def test_print_null_key():
    subscriber = PrintNull()
    assert subscriber.key() == 'null'

def test_print_null_update():
    subscriber = PrintNull()
    # update не должен вызывать исключений
    try:
        subscriber.update("Any message")
    except Exception:
        assert False, "update() raised an exception"
    # Поведение не влияет на вывод, проверка отсутствия побочных эффектов

# Тесты для класса PrintInErr
def test_print_in_err_key():
    subscriber = PrintInErr()
    assert subscriber.key() == 'stderr'

@patch('sys.stderr', new_callable=StringIO)
def test_print_in_err_update(mock_stderr):
    subscriber = PrintInErr()
    message = "Error message"
    subscriber.update(message)
    assert mock_stderr.getvalue() == message + '\n'