import builtins
import pytest

def run_interaction(inputs):
    """
    Helper to run main() with given list of input lines.
    Returns captured stdout lines as a joined string.
    """
    inputs_iter = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(inputs_iter)
        except StopIteration:
            raise EOFError

    # Patch builtins.input and run main
    import importlib, sys
    # Reload module to reset state between tests
    import main as contacts_mod
    importlib.reload(contacts_mod)

    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(builtins, "input", fake_input)
    try:
        # Capture print output using pytest's capsys is handled by test function; here we just call main and let tests capture
        contacts_mod.main()
    except EOFError:
        # in case inputs exhausted and code tries to read more, just ignore
        pass
    finally:
        monkeypatch.undo()


def test_cli_add_phone_and_exit(monkeypatch, capsys):
    # Provide a sequence of user inputs and then "exit"
    inputs = [
        "add John 0123456789",
        "phone John",
        "add-birthday John 01.01.1990",
        "all",
        "change John 0123456789 1111111111",
        "phone John",
        "exit"
    ]
    inputs_iter = iter(inputs)

    def fake_input(prompt=""):
        return next(inputs_iter)

    monkeypatch.setattr("builtins.input", fake_input)
    # reload module to reset book state
    import importlib
    import main as contacts_mod
    importlib.reload(contacts_mod)

    # Run main — prints will be captured by capsys
    contacts_mod.main()
    captured = capsys.readouterr()
    output = captured.out

    # Basic assertions: output should contain welcome, and some responses
    assert "Welcome to the assistant bot!" in output
    assert "Contact John is created" in output or "is created" in output
    # show phone should have printed contact or phone details
    assert "phones" in output or "0123456789" in output or "1111111111" in output
