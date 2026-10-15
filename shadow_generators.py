# Допоміжна функція для безпечного витягування числа з рядка
def extract_amount(tx_string):
    try:
        parts = str(tx_string).split()
        if len(parts) == 2:
            return float(parts[1])
    except (ValueError, AttributeError):
        pass
    return 0.0

# 1. Перший декоратор: Тіньовий ліміт
def shadow(limit=200):
    def decorator(func):
        def wrapper(*args, **kwargs):
            gen = func(*args, **kwargs)
            total_sum = 0
            limit_reached = False
            
            for item in gen:
                amount = extract_amount(item)
                total_sum += amount
                
                # Перевірка ліміту
                if total_sum > limit and not limit_reached:
                    print("Тіньовий ліміт перевищено. Активую схему.")
                    limit_reached = True
                
                yield item # Передаємо елемент далі по ланцюжку
            
            # Повертаємо фінальну суму (перехоплюється через StopIteration)[cite: 7]
            return total_sum
        return wrapper
    return decorator

# 2. Другий декоратор: Підозрілі транзакції[cite: 7]
def suspicious_counter(threshold=100):
    def decorator(func):
        def wrapper(*args, **kwargs):
            gen = func(*args, **kwargs)
            suspicious_sum = 0
            
            for item in gen:
                amount = extract_amount(item)
                # Незалежно рахуємо суми, що перевищують поріг[cite: 7]
                if amount > threshold:
                    suspicious_sum += amount
                    print(f"Попередження: Підозріла транзакція на суму {amount}!")
                
                yield item
                
        return wrapper
    return decorator

# 3. Базовий генератор транзакцій з навішаними декораторами[cite: 7]
@suspicious_counter(threshold=150)
@shadow(limit=200)
def transaction_generator():
    transactions = [
        "payment 120",
        "refund 50",
        "transfer 300", # Ця транзакція проб'є ліміт і викличе підозру
        "invalid_string", # Ігнорується[cite: 7]
        "payment abc",    # Ігнорується[cite: 7]
        "payment 40"
    ]
    for tx in transactions:
        yield tx

# 4. Клієнтський код для запуску та перевірки
if __name__ == "__main__":
    print("--- Запуск генератора ---")
    gen = transaction_generator()
    
    # Ітерація по генератору та виведення в консоль[cite: 7]
    try:
        for tx in gen:
            print(f"Оброблено: {tx}")
    except StopIteration as e:
        # Отримання фінальної суми, яку повертає генератор[cite: 7]
        print(f"\nФінальна сума транзакцій: {e.value}")