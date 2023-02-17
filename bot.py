import functools
import json 
import re
from collections import OrderedDict
from collections import UserDict
from typing import Callable


class MyException(Exception):
    pass

class AddressBook(UserDict):

    def __init__(self):
        self.data = {}
        self.names = self.data.keys()
        self.users = self.data.values()
     
    def add_record(self, name, *phone):
        if name in self.names:
            raise MyException('This user exists.')
        user = Record(name, *phone)
        self.data.update({user.name.value:user})
        return 'Done!'
    
    def delete_record(self, name):
        try:
            self.data.pop(name)
            return f"{name} was removed"
        except KeyError:
            return "This user isn't in the Book"
    
    def get(self, name):
        if not name in self.names:
            raise MyException("This user isn't in the Book")
        user = self.data[name]
        return user

    def show_records(self):
        normal_data = {}
        for name, record in self.data.items():
            name: Name.value
            record: Record
            normal_data.update({name: [phone.value for phone in record.phone]})
        json_look = json.dumps(normal_data, indent=4, sort_keys = True)
        return json_look
    

class Field:
    pass


class Name(Field):

    def __init__(self, name: str) -> None:
        self.value: str
        self.value = name


class Phone(Field):

    def __init__(self, *phones: list) -> None:
       self.value = [*phones][0]


class Record:

    def __init__(self, name: str, *phones: list) -> None:
        self.name = Name(name)
        if len(phones) == 0:
            self.phone = []

        else:
            self.phone = [Phone(phone) for phone in phones]

    def add_number(self, phone: str) -> None:
        self.phone.append(Phone(phone))

    def delete_number(self, pos: int = 0) -> None:
       
        if len(self.phone) > 1:
            pos = self.ask_index()
        self.phone.remove(self.phone[pos])

    def edit_number(self, phone: str, pos: int = 0) -> str: 
            
            if len(self.phone) > 1:
                pos = self.ask_index()

            elif len(self.phone) == 0:
                self.phone.append(Phone(phone))
            self.phone[pos] = Phone(phone)
            return 'Done!'

    def show_record(self):
        print(self.name.value)  
        for i, number in enumerate([phone.value for phone in self.phone], 0): 
            print(f'{i}: {number}')

    def ask_index(self):

        self.show_record()
        while True: 
            try:        
                pos = int(input('Enter the index of a phone you want to edit >>> '))
                if pos > len(self.phone) - 1:
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
    contacts.add_record(*args)
    return 'Done!'

@decorator_input
def add_number(*args: str) -> str:
    user = contacts.get(args[0])
    user.add_number(args[1])
    return 'Done!'

@decorator_input
def change(*args: str) -> str:
    user = contacts.get(args[0])
    user.edit_number(args[1])
    return 'Done!'

@decorator_input
def delete_number(*args: str) -> str:
    user = contacts.get(args[0])
    user.delete_number()
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
            words = line.split(': ')
            phones = re.findall(r'[+()\-0-9]+(?=[\'])', words[1])
            contacts.add_record(words[0], *phones) 
        return contacts      

@decorator_input
def goodbye() -> str:
    return 'Goodbye!'

@decorator_input
def hello() -> str:
    return 'How can I help you?'

@decorator_input
def phone(*args: str) -> str:
    user = contacts.get(args[0])
    phones = [phone.value for phone in user.phone]
    return phones

def write_contacts() -> None:
    text = []
    contacts_ord = OrderedDict(sorted(contacts.items()))
    for name, record in contacts_ord.items():
        text.append(f'{name}: {[num.value for num in record.phone]}\n')
    with open('contacts.txt', 'w') as fh:
        fh.write(''.join(text))

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