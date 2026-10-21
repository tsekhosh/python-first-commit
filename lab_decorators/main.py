from collections import Counter
from datetime import datetime
from functools import wraps

VALID_TYPES = {"GATE", "CARGO", "ACCESS", "ALARM", "SENSOR", "CALL", "SYSTEM"}


def is_valid_line(line: str) -> bool:
    """Перевіряє коректність рядка журналу."""
    parts = line.split("|")
    if len(parts) < 3:
        return False

    timestamp, event_type, *params = parts

    # 1. Перевірка дати і часу YYYY-MM-DDTHH:MM:SS
    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return False

    # 2. Перевірка типу події
    if event_type not in VALID_TYPES:
        return False

    # 3. Перевірка параметрів ключ=значення
    for param in params:
        if "=" not in param:
            return False
        key, _ = param.split("=", 1)
        if not key:
            return False

    return True


def filter_corrupted(func):
    """Декоратор 1: відсіює биті рядки та веде їх підрахунок."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        corrupted_count = 0
        for line in func(*args, **kwargs):
            cleaned = line.strip()
            if not cleaned:
                continue  # Порожні рядки не є битими

            if is_valid_line(cleaned):
                yield cleaned
            else:
                corrupted_count += 1

        print(f"Кількість битих рядків: {corrupted_count}")

    return wrapper


def count_and_report(func):
    """Декоратор 2: підраховує типи подій і друкує підсумковий звіт."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        type_counts = Counter()

        for line in func(*args, **kwargs):
            event_type = line.split("|")[1]
            type_counts[event_type] += 1
            yield line

        print("\n=== ЗВІТ ЗА ТИПАМИ ПОДІЙ ===")
        for event_type, count in sorted(type_counts.items()):
            print(f"{event_type:8}: {count}")
        print("============================\n")

    return wrapper


@count_and_report
@filter_corrupted
def read_hub_log(filepath: str = "hub_log.txt"):
    """Генератор читання файлу рядок за рядком."""
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            yield line


if __name__ == "__main__":
    for _ in read_hub_log("hub_log.txt"):
        pass