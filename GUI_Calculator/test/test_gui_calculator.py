import tkinter as tk
import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # noqa: E402
from gui_calculator import gui_calculator


@pytest.fixture
def calculator():
    root = tk.Tk()
    calc = gui_calculator(root)
    return calc


'''Test for GUI Calculator'''


def test_init(calculator):
    # Test the initialization of the calculator.
    assert calculator.master.title() == "GUI Calculator"
    # Test that geometry() is callable and does not raise
    try:
        geometry_str = calculator.master.geometry()
    except Exception:
        geometry_str = None
    assert geometry_str is not None
    # Test that resizable() returns a tuple
    resizable_val = calculator.master.resizable()
    assert isinstance(resizable_val, tuple)


def test_create_widgets(calculator):
    # Test the creation of widgets in the calculator.
    assert isinstance(calculator.entry, tk.Entry)
    # width is the number of characters, not pixels
    assert int(calculator.entry['width']) == 16
    # font is a string, check substring
    assert 'Arial' in calculator.entry['font']
    assert '24' in calculator.entry['font']
    assert int(calculator.entry['borderwidth']) == 2
    assert calculator.entry['relief'] == 'ridge'


def test_on_button_click(calculator, mocker):
    # Test the button click functionality.
    mocker.patch('builtins.eval', return_value=10)
    calculator.entry.insert(tk.END, '5+5')
    calculator.on_button_click('=')
    assert calculator.entry.get() == '10'

    calculator.on_button_click('C')
    assert calculator.entry.get() == ''
    assert calculator.result_var.get() == 'result: '


def test_zero_division_error(calculator, mocker):
    # Test handling of division by zero.
    mocker.patch('builtins.eval', side_effect=ZeroDivisionError)
    calculator.entry.insert(tk.END, '10/0')
    calculator.on_button_click('=')
    # After error, entry should be empty
    assert calculator.entry.get() == ''
    assert calculator.result_var.get() == 'error'


def test_on_key_press(calculator, mocker):
    # Test the key press functionality.
    mocker.patch('builtins.eval', return_value=20)
    calculator.entry.insert(tk.END, '10*2')
    mock_event = mocker.Mock()
    mock_event.char = '\r'  # Simulate pressing Return
    calculator.on_key_press(mock_event)
    assert calculator.entry.get() == '20'

    calculator.entry.delete(0, tk.END)
    mock_event.char = '\x1b'  # Simulate pressing Escape
    calculator.on_key_press(mock_event)
    assert calculator.entry.get() == ''


def test_bind_keys(calculator):
    # Test the key binding functionality.
    assert calculator.master.bind('<Return>') is not None
    assert calculator.master.bind('<Escape>') is not None
    assert calculator.master.bind('<KeyPress>') is not None


def test_log_result(calculator, mocker):
    # Test logging of results
    mock_log = mocker.patch.object(calculator, 'log_result')
    calculator.entry.insert(tk.END, '3+7')
    calculator.on_button_click('=')
    mock_log.assert_called_once_with(10, '3+7')

    calculator.entry.delete(0, tk.END)
    calculator.on_button_click('C')
    assert calculator.result_var.get() == 'result: '


def test_main(calculator, mocker):
    """Run the tests."""
    mocker.patch('tkinter.Tk.mainloop')
    # If you have a main method, call it on the calculator instance
    assert calculator.master.title() == "GUI Calculator"
    assert callable(calculator.master.geometry)
    assert isinstance(calculator.master.resizable(), tuple)
