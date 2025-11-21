import pytest
from datetime import datetime

from main import Phone, Birthday, InvalidPhoneException, InvalidBirthdayException


def test_phone_valid():
    p = Phone("0123456789")
    assert p.value == "0123456789"
    assert str(p) == "0123456789"


def test_phone_invalid_raises():
    with pytest.raises(InvalidPhoneException):
        Phone("not-a-number")
    with pytest.raises(InvalidPhoneException):
        Phone("123")  # too short
    with pytest.raises(InvalidPhoneException):
        Phone("01234567890")  # too long


def test_birthday_valid():
    b = Birthday("01.02.2000")
    # Birthday stores a datetime object (per your implementation)
    assert isinstance(b.value, datetime)
    assert b.value.day == 1
    assert b.value.month == 2
    assert b.value.year == 2000
    assert "2000" in str(b) or "01" in b.value.strftime("%d.%m.%Y")


def test_birthday_invalid_raises():
    with pytest.raises(InvalidBirthdayException):
        Birthday("2000-01-01")  # wrong format
    with pytest.raises(InvalidBirthdayException):
        Birthday("30.02.2000")  # invalid date

