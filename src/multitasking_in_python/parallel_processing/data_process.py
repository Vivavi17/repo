import random


def generate_data(n: int) -> list[int]:
    return [random.randint(1, 1000) for _ in range(n)]


def process_number(number: int) -> int:
    result = 1
    for i in range(1, number + 1):
        result *= i
    return result
