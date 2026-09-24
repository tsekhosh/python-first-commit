def process_medication_batch(medications):
    results = []

    for item in medications:
        name, quantity, category, temp = item


        if type(quantity) is not int or type(temp) is not float:
            results.append(f"{name}: Помилка даних")
            continue

        match category:
            case "antibiotic":
                cat_status = "Рецептурний препарат"
            case "vitamin":
                cat_status = "Вільний продаж"
            case "vaccine":
                cat_status = "Потребує спецзберігання"
            case _:
                cat_status = "Невідома категорія"

     
        if temp < 5.0:
            temp_status = "Надто холодно"
        elif temp > 25.0:
            temp_status = "Надто жарко"
        else:
            temp_status = "Норма"

        results.append(f"{name}: Категорія — «{cat_status}», Температура — «{temp_status}»")

    return results



batch = [
    ("Амоксицилін", 50, "antibiotic", 18.5),
    ("Вітамін C", 100, "vitamin", 3.0),
    ("Вакцина КПК", 15, "vaccine", 28.0),
    ("Ібупрофен", 30, "painkiller", 20.0),
    ("Сироп від кашлю", "двадцять", "vitamin", 15.0), 
    ("Краплі", 10, "antibiotic", 12),                 
]


for entry in process_medication_batch(batch):
    print(entry)