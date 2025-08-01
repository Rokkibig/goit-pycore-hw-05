import re
from typing import Callable

def generator_numbers(text: str):
    """
    Генерує всі дійсні числа, чітко відокремлені пробілами у тексті.
    """
    # Пошук чисел, які мають пробіли з обох боків
    for match in re.finditer(r'\s(\d+\.\d+)\s', text):
        yield float(match.group(1))

def sum_profit(text: str, func: Callable):
    """
    Підсумовує всі числа, знайдені генератором func у тексті.
    """
    return sum(func(text))

# Приклад використання
if __name__ == "__main__":
    text = ("Загальний дохід працівника складається з декількох частин: "
            "1000.01 як основний дохід, доповнений додатковими надходженнями "
            "27.45 і 324.00 доларів.")
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")