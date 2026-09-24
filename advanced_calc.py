def calculate(expression):
    # Спочатку прибираємо всі пробіли, щоб вони не заважали
    expression = expression.replace(" ", "")

    def parse(expr):
        # Якщо рядок порожній, повертаємо 0
        if not expr:
            return 0
        
        # КРОК 1: Шукаємо додавання або віднімання ПОЗА дужками.
        # Йдемо з кінця рядка на початок.
        depth = 0
        for i in range(len(expr) - 1, -1, -1):
            char = expr[i]
            if char == ')':
                depth += 1
            elif char == '(':
                depth -= 1
            elif depth == 0 and char in ('+', '-'):
                # Знайшли операцію! Розбиваємо вираз на ліву і праву частини
                left = parse(expr[:i])
                right = parse(expr[i+1:])
                if char == '+': return left + right
                if char == '-': return left - right

        # КРОК 2: Якщо плюсів і мінусів немає, шукаємо множення або ділення ПОЗА дужками
        depth = 0
        for i in range(len(expr) - 1, -1, -1):
            char = expr[i]
            if char == ')':
                depth += 1
            elif char == '(':
                depth -= 1
            elif depth == 0 and char in ('*', '/'):
                left = parse(expr[:i])
                right = parse(expr[i+1:])
                if char == '*': return left * right
                if char == '/': 
                    if right == 0:
                        return "Помилка: ділення на нуль"
                    return left / right

        # КРОК 3: Якщо жодних дій поза дужками немає, можливо, весь вираз обгорнутий дужками?
        if expr[0] == '(' and expr[-1] == ')':
            # Відкидаємо зовнішні дужки і рахуємо те, що всередині
            return parse(expr[1:-1]) 
        
        # КРОК 4: Якщо це не дія і не дужки — значить, залишилося просто число!
        return float(expr)

    # Запускаємо нашу функцію парсингу
    return parse(expression)

# --- Головна частина програми ---
user_input = input("Введіть математичний вираз (наприклад, 2 + 3 * (4 - 1)): ")
try:
    result = calculate(user_input)
    print("Результат:", result)
except Exception:
    print("Сталася помилка. Перевірте правильність виразу!")