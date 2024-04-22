from info import *
from abc import ABC, abstractmethod

class UserInterface(ABC):
    @abstractmethod
    def display_contacts(self, book):
        pass
    
    @abstractmethod
    def display_commands(self):
        pass

class ConsoleUserInterface(UserInterface):
    def display_contacts(self, book):
        if (len(book)) == 0:
            print ("Contacts is empty")
        else:    
            print("Contacts:")
            print (book)

    def display_commands(self):
        print("Available commands:")
        print("- add: Add a new contact")
        print("- change: Change contact's phone number")
        print("- phone: Show contact's phone number")
        print("- all: Show all contacts")
        print("- add-birthday: Add birthday to a contact")
        print("- show-birthday: Show contact's birthday")
        print("- birthdays: Show upcoming birthdays")
        print("- exit: Close the application")    

def main():
    print("Welcome to the assistant bot!")
    book = load_data()
    ui = ConsoleUserInterface()
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            ui.display_contacts(book)
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            ui.display_commands()

if __name__ == "__main__":
    main()
