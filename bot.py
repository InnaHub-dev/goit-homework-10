import functools
import re
from collections import OrderedDict
from collections import UserDict
from typing import Callable


class MyException(Exception):
    pass

class AddressBook(UserDict):
        
    def __getitem__(self, name):
        if not name in self.data.keys():
            raise MyException("This user isn't in the Book")
        user = self.data[name]
        return user
 
    def add_record(self, record):
        self.data.update({record.name.value:record})
        return 'Done!'
    
    def delete_record(self, name):
        try:
            self.data.pop(name)
            return f"{name} was removed"
        except KeyError:
            return "This user isn't in the Book"

    def show_records(self):
        sorted_dict = OrderedDict(sorted(self.data.items()))
        return "\n".join([record.show_record() for record in sorted_dict.values()])
            

class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:

    def __init__(self, name: Name, phone: Phone=None) -> None:
        self.name = name
        self.phones = [phone] if phone else []

    def add_phone(self, phone: Phone) -> None:
        self.phones.append(phone)

    def add_numbers(self, phones: list[Phone]):
        self.phones.extend(phones)

    def delete_number(self, pos: int = 0) -> None:
        if len(self.phones) > 1:
            pos = self.ask_index()
        self.phones.remove(self.phones[pos])

    def edit_number(self, phone: Phone, pos: int = 0) -> str:    
            if len(self.phones) > 1:
                pos = self.ask_index()
            elif len(self.phones) == 0:
                self.phones.append(phone)
            self.phones[pos] = phone
            return 'Done!'

    def show_record(self):
        return f"{self.name.value}: {', '.join([phone.value for phone in self.phones])}"

    def ask_index(self):
        print(self.name.value) 
        for i, number in enumerate([phone.value for phone in self.phones], 0): 
            print(f'{i}: {number}')
        while True: 
            try:        
                pos = int(input('Enter the index of a phone you want to edit >>> '))
                if pos > len(self.phones) - 1:
                    raise IndexError
                return pos
            except IndexError:
                print('Wrong index. Try again.')
            except ValueError:
                print('Index should be a number. Try again.')


def decorator_input(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*words):
        try:
            return func(*words)
        except KeyError as err:
            return err
        except IndexError:
            return "You didn't enter the phone or a user"
        except TypeError:
            return "Sorry, this command doesn't exist"
        except Exception as err:
            return err
    return wrapper

@decorator_input
def add_user(*args: str) -> str:
    name = Name(args[0])
    if name.value in contacts.keys():
        return "This user already exists."
    else:
        try:
            phone = Phone(args[1])
        except IndexError:
            phone = None
        record = Record(name, phone)
        contacts.add_record(record)
        return 'Done!'

@decorator_input
def add_number(*args: str) -> str:
    record = contacts.get(args[0])
    record.add_phone(Phone(args[1]))
    return 'Done!'

@decorator_input
def change(*args: str) -> str:
    record = contacts.get(args[0])
    record.edit_number(Phone(args[1]))
    return 'Done!'

@decorator_input
def delete_number(*args: str) -> str:
    record = contacts.get(args[0])
    record.delete_number()
    return 'Done!'

@decorator_input
def delete_user(*args: str) -> str:
    return contacts.delete_record(args[0])

def get_command(words: str) -> Callable:
    for key in commands_dict.keys():
        if re.search(fr'\b{words[0].lower()}\b', str(key)):
            func = commands_dict[key]
            return func
    raise KeyError("This command doesn't exist")

def get_contacts() -> AddressBook:
    with open('contacts.txt', 'a+') as fh:
        fh.seek(0)
        text = fh.readlines()
        contacts = AddressBook()
        for line in text:
            if line != '\n':
                name, phones = line.split(': ')
                record = Record(Name(name))
                phones = phones.split(', ')
                record.add_numbers([Phone(phone.strip()) for phone in phones])
                contacts.add_record(record) 
        return contacts      

@decorator_input
def goodbye() -> str:
    return 'Goodbye!'

@decorator_input
def hello() -> str:
    return 'How can I help you?'

@decorator_input
def phone(*args: str) -> str:
    record = contacts[args[0]]
    return record.show_record()

def write_contacts() -> None:
    with open('contacts.txt', 'w') as fh:
        fh.write(contacts.show_records())
        fh.write('\n')

contacts = get_contacts()

commands_dict = {('hello','hi', 'hey'):hello,
                 ('add',):add_user,
                 ('add_number',):add_number,
                 ('change',):change,
                 ('delete_number',):delete_number,
                 ('delete_user',):delete_user,
                 ('phone',):phone,
                 ('showall',):contacts.show_records,
                 ('goodbye','close','exit','quit'):goodbye
}

def main():

    while True:
        words = input(">>> ").split(' ')
        try:
            func = get_command(words)
        except KeyError as error:
            print(error)
            continue
        print(func(*words[1:])) 
        if func.__name__ == 'goodbye':
            write_contacts()
            break

if __name__ == '__main__':
    main()