from collections import UserDict
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class Field(ABC):    
    def __init__(self, value):
        if self.is_valid(value):
            self.value = value            
        else:
            return None
        
    @abstractmethod    
    def is_valid(self, value):
        pass
        
    def __str__(self):
        return str(self.value)
    

class Name(Field):
    def is_valid(self, value):
        return True


class Phone(Field):
    def is_valid(self, value):
        return len(value) == 10 and value.isdigit()
    
    
class Birthday(Field):
    def is_valid(self, value):
        datetime.strptime(value, "%d.%m.%Y")
        return True
  
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        if self.find_phone(new_phone.value):
            pass
        else:
            self.phones.append(new_phone)
            return new_phone        
           
    def find_phone(self, f_phone):
        for num in self.phones:
            if num.value == f_phone:
                return num
        else:
            return None            
    
    def remove_phone(self, phone_del_number):
        if self.find_phone(phone_del_number):
            phone = self.find_phone(phone_del_number)
            self.phones.remove(phone)
        else:
            return None

    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(old_phone):
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
        else:
            return None          
    
    def __str__(self):
        return f"_____________________ \n\
Contact name: {str(self.name.value)} \nphones: {'; '.join(str(p) for p in self.phones)}\
        \nbirthday: {str(self.birthday)}\n_____________________\n"
        


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        if name in self.data:
            return self.data.get(name)
        else:
            return None

    def delete(self, name):
        if name in self.data:
            return self.data.pop(name)
        else:
            return None    
    
# -----------------------------------------------------  
    @staticmethod
    def get_upcoming_birthdays(book): 
        today = datetime.today().date()
        upcoming_birthdays = []
        result = []   
        for record in book.values():
            if record.birthday:  
                birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                birthday = birthday.replace(year=today.year)
                if birthday.weekday() >= 5:
                    birthday += timedelta(days=7 - birthday.weekday())
                if birthday < today and birthday.weekday() < 5: 
                    birthday = birthday.replace(year=today.year + 1)
                delta = birthday.toordinal() - today.toordinal()
                if 0 <= delta <= 7:
                    birthday_str = birthday.strftime('%d.%m.%Y') 
                    upcoming_birthdays.append({"name": record.name.value, "congratulation_date": birthday_str})
        for item in upcoming_birthdays:
            result.append(f"{item['name']}: {item['congratulation_date']}")
        return '_' * 20 + '\n' + '\n'.join(result) + '\n' + '_' * 20
# -----------------------------------------------------
        
    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())
        
