from collections import UserDict
from re import compile,fullmatch
from datetime import datetime, timedelta

phone_validator = compile(r"^[0-9]{10}$")


class InvalidPhoneException(ValueError):
    pass


class InvalidBirthdayException(ValueError):
    pass


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidPhoneException as e:
            print(e)
        except InvalidBirthdayException as e:
            print(e)
        except ValueError as e:
            print(e)
        except (IndexError, KeyError):
            print("Invalid arguments provided")
    return inner


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
    pass


class Phone(Field):
    def __init__(self, value):
        if fullmatch(phone_validator, value):
            super().__init__(value)
        else:
            raise InvalidPhoneException(f'{value} is not a valid phone number')


class Birthday(Field):
    def __init__(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(date)
        except ValueError:
            raise InvalidBirthdayException("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, person_name):
        self.name = Name(person_name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def find_phone(self, phone):
        try:
            return next(filter(lambda p: p.value == phone, self.phones), None)
        except InvalidPhoneException:
            return None

    def remove_phone(self, phone):
        self.phones = list(filter(lambda p: p.value != phone, self.phones))

    def edit_phone(self, old_phone, new_phone):
        try:
            old_phone_validated = Phone(old_phone)
            idx = next(i for i,item in enumerate(self.phones) if item.value == old_phone_validated.value)
            self.phones[idx] = Phone(new_phone)
            return True
        except ValueError:
            raise InvalidPhoneException("Invalid phone number provided")
        except StopIteration:
            raise InvalidPhoneException("The target phone is not found")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday:
            return self.birthday.value.date()
        else:
            raise InvalidBirthdayException(f"No Birthday provided for this contact")

    def __str__(self):
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {birthday_str}"


class AddressBook(UserDict):
    def add_record(self, person_record: Record):
        self.data[person_record.name.value] = person_record

    def find(self, person_name: str):
        return self.data.get(person_name)

    def delete(self, person_name):
        return self.data.pop(person_name)

    def get_upcoming_birthdays(self) -> str:
        congrats = []
        today = datetime.now().date()
        congrats_treshold = today + timedelta(days=7)
        for user, record in self.data.items():
            if record.birthday:
                birthday = record.birthday.value

                # if current month is December and Birthday is in January add 1 year to check in the next year
                if today.month == 12 and birthday.month == 1:
                    next_birthday = datetime(year=today.year + 1, month=birthday.month, day=birthday.day).date()
                else:
                    next_birthday = datetime(year=today.year, month=birthday.month, day=birthday.day).date()
                # check if treshold is in the future and not more than 7 days ahead
                if congrats_treshold - next_birthday <= timedelta(days=7) and congrats_treshold > next_birthday:
                    # if Bithday date is on Saturday or Sunday, we need to add respected days (1 or 2) to get next Monday
                    if next_birthday.weekday() > 4:
                        congrats.append(f"name: {user}, congratulation_date: {(next_birthday + timedelta(days=7 - next_birthday.weekday())).strftime('%Y.%m.%d')}")
                    else:
                        congrats.append(f"name: {user}, congratulation_date: {next_birthday.strftime('%Y.%m.%d')}")
        return '\n'.join(congrats) if len(congrats) > 0 else "Birthdays not found"

    def __str__(self):
        lines = []
        for name, record in self.data.items():
            lines.append(f"Contact name: {name}, phones: {'; '.join(p.value for p in record.phones)}, birthday: {record.birthday}")
        return "\n".join(lines)


def parse_input(user_input):
    try:
        cmd, *args = user_input.split()
        return cmd.strip().casefold(), *args
    except ValueError:
        return None, []

'''add [ім'я] [телефон]: Додати або новий контакт з іменем і телефонним номером, або телефонний номер до контакту, який уже існує.'''
@input_error
def add_contact(args, book: AddressBook):
    name = args[0]
    phone = args[1] if len(args) > 1 else None
    record = book.find(name)
    if record is None:
        record = Record(name)
        if phone:
            record.add_phone(phone)
        book.add_record(record)
        return f"Contact {name} is created. Phone number {phone} is added to contact"
    else:
        if phone:
            if record.find_phone(phone):
                raise InvalidPhoneException("This phone number already exists in this contact")
            else:
                record.add_phone(phone)
                return f"Phone number {phone} is added to contact {name}"
        else:
            raise InvalidPhoneException("This contact is already exists. Please add the phone number")


'''change [ім'я] [старий телефон] [новий телефон]: Змінити телефонний номер для вказаного контакту.'''
@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated"
    else:
        return "404. Contact not found."


'''phone [ім'я]: Показати телефонні номери для вказаного контакту.'''
@input_error
def show_phone(args, book):
    name, *rest = args
    record = book.find(name)
    if record:
        print(record)
    else:
        return "404. Contact not found."


'''all: Показати всі контакти в адресній книзі.'''
@input_error
def show_all(book):
    if book:
        print(book)
    else:
        return "No contacts found."


@input_error
def add_birthday(args, book:AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added"
    return ("Contact not found.")


@input_error
def show_birthday(args, book:AddressBook):
    [name] = args
    record = book.find(name)
    if record:
        return record.show_birthday()
    return ("Contact not found.")


@input_error
def birthdays(book:AddressBook):
    return book.get_upcoming_birthdays()


def main():
    contact_book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            '''close або exit: Закрити програму.'''
            print("Good bye!")
            break
        elif command == "hello":
            '''hello: Отримати вітання від бота.'''
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contact_book))
        elif command == "change":
            print(change_contact(args, contact_book))
        elif command == "phone":
            print(show_phone(args, contact_book))
        elif command == "add-birthday":
            print(add_birthday(args, contact_book))
        elif command == "show-birthday":
            print(show_birthday(args, contact_book))
        elif command == "all":
            print(show_all(contact_book))
        elif command == "birthdays":
            print(birthdays(contact_book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()