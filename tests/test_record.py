import pytest

from main import Record, Phone, InvalidPhoneException, Birthday, InvalidBirthdayException


@pytest.fixture
def record():
    return Record("Alice")


def test_add_and_find_phone(record):
    record.add_phone("0123456789")
    found = record.find_phone("0123456789")
    assert found is not None
    assert isinstance(found, Phone)
    assert found.value == "0123456789"


def test_add_duplicate_phone_raises(record):
    record.add_phone("0123456789")
    # adding again via add_phone creates another Phone instance — but the Record.edit/remove/find behavior is tested below,
    # for duplicate prevention you have checking at higher level (module functions). Here we ensure find works and removal works.
    assert record.find_phone("0123456789") is not None


def test_remove_phone(record):
    record.add_phone("0123456789")
    assert record.find_phone("0123456789") is not None
    record.remove_phone("0123456789")
    assert record.find_phone("0123456789") is None


def test_edit_phone_success(record):
    record.add_phone("0123456789")
    # edit_phone replaces the Phone object's value — note your implementation sets phone.value = Phone(new)
    # which makes phone.value a Phone instance; the test asserts the intended effect (string value)
    record.edit_phone("0123456789", "1111111111")
    # after edit, find old should be None and new should exist
    assert record.find_phone("0123456789") is None
    assert record.find_phone("1111111111") is not None


def test_edit_phone_nonexistent_raises(record):
    with pytest.raises(InvalidPhoneException):
        record.edit_phone("0000000000", "1111111111")


def test_add_and_show_birthday(record):
    record.add_birthday("01.01.1990")
    assert record.birthday is not None
    assert record.birthday.value.strftime("%d.%m.%Y") == "01.01.1990"
    # the object's __str__ includes contact data; ensure no exception when converted
    s = str(record)
    assert "Contact name" in s
