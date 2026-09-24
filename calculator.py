# Запитуємо у користувача числа та операцію
num1 = float(input("Введіть перше число: "))
operation = input("Введіть операцію (+, -, *, /): ")
num2 = float(input("Введіть друге число: "))

# Логіка калькулятора за допомогою умов
if operation == '+':
    result = num1 + num2
    print("Результат:", result)
elif operation == '-':
    result = num1 - num2
    print("Результат:", result)
elif operation == '*':
    result = num1 * num2
    print("Результат:", result)
elif operation == '/':
    # Перевірка на ділення на нуль
    if num2 == 0:
        print("Помилка: ділити на нуль не можна!")
    else:
        result = num1 / num2
        print("Результат:", result)
else:
    print("Помилка: невідома операція!")