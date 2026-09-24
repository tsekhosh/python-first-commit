def sort_clients(deals):
    results = []

    for name, amount, status in deals:
        if type(amount) not in (int, float):
            results.append(f"{name}: Фальш")
            continue

        if amount < 100:
            category = "Дрібнота"
        elif amount <= 999:
            category = "Середнячок"
        else:
            category = "Великий клієнт"

       
        match status:
            case "clean":
                decision = "Працювати без питань"
            case "suspicious":
                decision = "Перевірити документи"
            case "fraud":
                decision = "У чорний список"
            case _:
                decision = "Невідомий статус"

        results.append(f"{name}: Категорія — «{category}», Рішення — «{decision}»")

    return results



deals_list = [
    ("Матвій", 50, "clean"),
    ("Дмитро", 450.50, "suspicious"),
    ("Соломія", 2500, "fraud"),
    ("Ніколь", "тисяча", "clean"), 
    ("Назар", 800, "unknown"),    
]
for client in sort_clients(deals_list):
    print(client)