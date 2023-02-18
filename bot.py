import functools
import json 
import re
from collections import OrderedDict
from collections import UserDict
from typing import Callable


class MyException(Exception):
    pass

class AddressBook(UserDict):

    # Це лишне, так Ви прибираєте всю функціональність класу, від якого успадковуєте(
    # def __init__(self):
    #     self.data = {}
    #     # self.names = self.data.keys()
    #     # self.users = self.data.values()
    
    # Сюди просто приймаємо екземпляр класу рекорд 
    def add_record(self, record): #name, *phone
        # if name in self.names:
        #     raise MyException('This user exists.')
        # user = # Record(name, *phone) Всі записи створюємо явно зовні коду
        self.data[record.name.value] = record #.update({user.name.value:user})
        return 'Done!'
    
    def delete_record(self, name):
        try:
            self.data.pop(name)
            return f"{name} was removed"
        except KeyError:
            return "This user isn't in the Book"
    
    def get(self, name):
        if not name in self.data:
            raise MyException("This user isn't in the Book")
        user = self.data[name]
        return user

    def show_records(self):
        # name: Name.value
        # record: Record
        # normal_data = {}
        # for name, record in self.data.items():
        #     normal_data.update({name: [phone.value for phone in record.phone]})
        # json_look = json.dumps(normal_data, indent=4, sort_keys = True)
        # return json_look
        return "\n".join([f"{r.name.value}: {', '.join([p.value for p in r.phones])}"
                          for r in self.data.values()])
    

class Field: # От тут дуже даремно)))
    def __init__(self, value) -> None:
        self.value = value


class Name(Field):
    pass
    # def __init__(self, name: str) -> None:
    #     self.value: str
    #     self.value = name


class Phone(Field): # клас описує тільки одну сутність!
    pass
    # def __init__(self, *phones: list) -> None:
    #    self.value = [*phones][0]


class Record:

    def __init__(self, name: Name, phone: Phone=None) -> None: # Може бути телефон, а може і не бути)
        self.name = name
        self.phones = [phone] if phone else []
        # if len(phones) == 0:
        #     self.phone = []

        # else:
        #     self.phone = [Phone(phone) for phone in phones]

    def add_number(self, phone: Phone) -> None:
        # self.phone.append(Phone(phone))
        self.phones.append(phone)
        
    def add_numbers(self, phones: list[Phone]) -> None:
        self.phones += phones

    def delete_number(self, phone: Phone) -> None:  
        for p in self.phones:
            if phone.value == p.value:
                self.phones.remove(p)   
        # if len(self.phone) > 1:
        #     pos = self.ask_index()
        # self.phone.remove(self.phone[pos])

    def edit_number(self, phone: Phone, new_phone: Phone) -> str: 
            # можна додати перевірки
            self.delete_number(phone)
            self.add_number(new_phone)
            # if len(self.phone) > 1:
            #     pos = self.ask_index()

            # elif len(self.phone) == 0:
            #     self.phone.append(Phone(phone))
            # self.phone[pos] = Phone(phone)
            return 'Done!'

    def show_record(self):
        # print(self.name.value)  
        # for i, number in enumerate([phone.value for phone in self.phone], 0): 
        #     print(f'{i}: {number}')
        return f'{self.name.value}: {",".join([p.value for p in self.phones])}'

    # def ask_index(self):

    #     self.show_record()
    #     while True: 
    #         try:        
    #             pos = int(input('Enter the index of a phone you want to edit >>> '))
    #             if pos > len(self.phone) - 1:
    #                 raise IndexError
    #             return pos
    #         except IndexError:
    #             print('Wrong index. Try again.')
    #         except ValueError:
    #             print('Index should be a number. Try again.')


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
    try:
        phone = Phone(args[1])
    except IndexError:
        phone = None
    rec = Record(name, phone)
    contacts.add_record(rec)

@decorator_input
def add_number(*args: str) -> str:
    name = Name(args[0])
    phone = Phone(args[1])
    rec = contacts[name.value]
    rec.add_number(phone)    
    # user = contacts.get(name.value)
    # user.add_number(args[1])
    return 'Done!'

@decorator_input
def change(*args: str) -> str:
    name = Name(args[0])
    phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec = contacts.get(name.value)
    rec.edit_number(phone, new_phone)
    # user = contacts.get(args[0])
    # user.edit_number(args[1])
    return 'Done!'

@decorator_input
def delete_number(*args: str) -> str:
    rec = contacts.get(args[0])
    rec.delete_number(Phone(args[0]))
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
    with open('contacts.txt', 'r') as fh:
        # fh.seek(0)
        text = fh.readlines()
        contacts = AddressBook()
        for line in text:
            name, phones = line.split(': ')
            phones = phones.split(",")
            rec = Record(Name(name))
            rec.add_numbers([Phone(p.strip()) for p in phones])
            contacts.add_record(rec) 
        return contacts      

@decorator_input
def goodbye() -> str:
    return 'Goodbye!'

@decorator_input
def hello() -> str:
    return 'How can I help you?'

@decorator_input
def phone(*args: str) -> str:
    rec = contacts.get(args[0])
    # phones = [phone.value for phone in user.phone]
    return rec.show_record()

def write_contacts() -> None:
    text = []
    # contacts_ord = OrderedDict(sorted(contacts.items()))
    # for rec in contacts:
    #     text.append(r)
    with open('contacts.txt', 'w') as fh:
        fh.write(contacts.show_records())
        fh.write("\n")

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