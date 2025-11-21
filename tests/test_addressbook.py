import pytest
from main import AddressBook, Record, Phone


@pytest.fixture
def abook():
    return AddressBook()


def test_add_find_delete_record(abook):
    r = Record("Bob")
    r.add_phone("0123456789")
    abook.add_record(r)

    found = abook.find("Bob")
    assert isinstance(found, Record)
    assert found.name.value == "Bob"
    assert found.find_phone("0123456789") is not None

    deleted = abook.delete("Bob")
    assert isinstance(deleted, Record)
    assert abook.find("Bob") is None


def test_str_contains_records(abook):
    r = Record("Carl")
    r.add_phone("0123456789")
    r.add_birthday("02.02.1992")
    abook.add_record(r)

    s = str(abook)
    # Basic checks: name and phone are present in string representation
    assert "Carl" in s
    assert "0123456789" in s


def test_get_upcoming_birthdays_empty(abook):
    # The implementation of get_upcoming_birthdays in your code expects specific structure;
    # call it on empty and expect empty list
    res = abook.get_upcoming_birthdays()
    assert isinstance(res, list)
    assert res == []
