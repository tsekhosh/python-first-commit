def process_medications(medications):
    for med in medications:
        name = med['назва']
        qty = med['кількість']
        cat = med['категорія']
        temp = med['температура']

        # 1. Перевірка типів даних
        if type(qty) is not int or type(temp) is not float:
            print(f"{name}: Помилка даних")
            continue  

        # 2. Перевірка температури
        if temp < 5.0:
            temp_status = "Надто холодно"
        elif temp > 25.0:
            temp_status = "Надто жарко"
        else:
            temp_status = "Норма"

        # 3. Перевірка категорії через класичний if/elif (бо старий Python)
        if cat == "antibiotic":
            cat_status = "Рецептурний препарат"
        elif cat == "vitamin":
            cat_status = "Вільний продаж"
        elif cat == "vaccine":
            cat_status = "Потребує спецзберігання"
        else:
            cat_status = "Невідома категорія"

        # 4. Виведення результату
        print(f"{name}: {cat_status}, {temp_status}")

# Тестові дані
test_data = [
    {"назва": "Амоксицилін", "кількість": 50, "категорія": "antibiotic", "температура": 20.5},
    {"назва": "Вітамін С", "кількість": 100, "категорія": "vitamin", "температура": 26.0},
    {"назва": "Вакцина", "кількість": 10, "категорія": "vaccine", "температура": 3.0},
    {"назва": "Пластир", "кількість": 5, "категорія": "other", "температура": 15.0},
    {"назва": "Бракований 1", "кількість": "багато", "категорія": "vitamin", "температура": 20.0},
    {"назва": "Бракований 2", "кількість": 20, "категорія": "vitamin", "температура": 20}
]

print("--- Звіт по препаратах ---")
process_medications(test_data)