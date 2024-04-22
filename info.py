from functools import wraps
from hw_class import Birthday, Record, AddressBook
import pickle

Debug = True

def input_error(func):
    if Debug:
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as err:
                return f'1Give me name and phone please! {err}'
            except IndexError as err:
                return f'2Give me name please! {err}'
            except KeyError as err:
                return f'3Enter the argument for the command. {err}'
            except NameError as err:
                return f'4Enter the argument for the command.{err}'
            except TypeError as err:
                return f'5Enter the argument for the command.{err}'
            except AttributeError as err:
                return f'6Enter the argument for the command.{err}'
        return inner
    
@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args    

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    name = name.title()
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message
    
@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    name = name.title()
    record = book.find(name)
    if record and old_phone in [phone.value for phone in record.phones] and new_phone.isdigit():
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        return "Contact not find or phone isn't digital"
    
@input_error
def show_all(contacts):
    return contacts

@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    name = name.title()        
    record  = book.find(name)
    if record:
        return ", ".join(str(phone) for phone in record.phones)
    else:
        return (f"Contact: {name} no found")

@input_error    
def add_birthday (args, book: AddressBook):
    name, birthday = args
    name = name.title()
    record = book.find(name)
    message = "Birthday added."
    if record:
        record.birthday = Birthday(birthday)
        return message
    else:
        None

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    name = name.title()
    record = book.find(name)
    if record and record.birthday:
        return str(record.birthday)
    else:
        return f"No birthday found for {name}"
    
@input_error    
def birthdays(book: AddressBook):
    return str(book.get_upcoming_birthdays(book))

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
 