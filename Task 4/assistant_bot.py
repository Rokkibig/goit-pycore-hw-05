# assistant_bot.py

from typing import Callable, Dict, List, Tuple

Contacts = Dict[str, str]


def input_error(messages: Dict[type, str] | None = None) -> Callable:
    """
    Декоратор для обробки типових помилок користувацького вводу.
    Дозволяє налаштувати повідомлення для кожної функції окремо.
    """
    messages = messages or {}

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyError:
                return messages.get(KeyError, "Contact not found.")
            except ValueError:
                return messages.get(ValueError, "Give me name and phone please.")
            except IndexError:
                return messages.get(IndexError, "Enter the argument for the command.")
        return wrapper
    return decorator


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd, *args = parts
    return cmd.lower(), args


@input_error(messages={
    ValueError: "Give me name and phone please.",
    IndexError: "Enter the argument for the command."
})
def add_contact(args: List[str], contacts: Contacts) -> str:
    if len(args) < 2:
        # імітуємо поведінку з прикладу: коли немає аргументів — IndexError
        if len(args) == 0:
            raise IndexError
        # коли аргумент один — ValueError (неповний формат)
        raise ValueError
    name, phone = args[0], args[1]
    contacts[name] = phone
    return "Contact added."


@input_error(messages={
    KeyError: "Contact not found.",
    ValueError: "Enter user name and new phone please.",
    IndexError: "Enter the argument for the command."
})
def change_contact(args: List[str], contacts: Contacts) -> str:
    if len(args) < 2:
        if len(args) == 0:
            raise IndexError
        raise ValueError
    name, new_phone = args[0], args[1]
    if name not in contacts:
        raise KeyError
    contacts[name] = new_phone
    return "Phone updated."


@input_error(messages={
    KeyError: "Contact not found.",
    ValueError: "Enter user name, please.",
    IndexError: "Enter the argument for the command."
})
def get_phone(args: List[str], contacts: Contacts) -> str:
    if len(args) == 0:
        raise IndexError
    if len(args) != 1:
        raise ValueError
    name = args[0]
    if name not in contacts:
        raise KeyError
    return f"{name}: {contacts[name]}"


@input_error(messages={
    ValueError: "This command takes no arguments.",
})
def show_all(args: List[str], contacts: Contacts) -> str:
    if len(args) != 0:
        raise ValueError
    if not contacts:
        return "No contacts."
    return "\n".join(f"{n}: {p}" for n, p in contacts.items())


def help_text() -> str:
    return (
        "Available commands:\n"
        "  add <name> <phone>       — add a new contact\n"
        "  change <name> <phone>    — change phone for contact\n"
        "  phone <name>             — show phone by name\n"
        "  all                      — show all contacts\n"
        "  hello                    — greeting\n"
        "  help                     — show this help\n"
        "  exit | close | good bye  — quit\n"
    )


def main():
    contacts: Contacts = {}
    print("Welcome to the assistant bot! Type 'help' to list commands.")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ("exit", "close") or user_input.lower() == "good bye":
            print("Good bye!")
            break

        if command == "hello":
            print("How can I help you?")
            continue

        if command == "help":
            print(help_text())
            continue

        handlers = {
            "add": add_contact,
            "change": change_contact,
            "phone": get_phone,
            "all": show_all,
        }

        handler = handlers.get(command)
        if not handler:
            # Поведінка з прикладу: якщо команда без аргументів або невідома
            # — виведемо підказку
            if command:
                print("Unknown command. Type 'help' to see available commands.")
            else:
                print("Enter the argument for the command")
            continue

        result = handler(args, contacts)
        if result:
            print(result)


if __name__ == "__main__":
    main()
