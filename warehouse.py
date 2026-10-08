# 1. Клас для опису предмета на складі[cite: 7]
class JunkItem:
    def __init__(self, name: str, quantity: int, value: float):
        self.name = name
        self.quantity = quantity
        self.value = value

    def __str__(self):
        return f"JunkItem(назва='{self.name}', кількість={self.quantity}, ціна={self.value})"


# 2. Окремий інтерфейс (абстракція) для роботи зі сховищем[cite: 7]
# Клієнтський код працюватиме тільки з цими методами, не знаючи про файли чи бази даних[cite: 7].
class JunkRepository:
    def save(self, items: list[JunkItem]):
        raise NotImplementedError

    def load(self) -> list[JunkItem]:
        raise NotImplementedError


# 3. Конкретна реалізація сховища у файлі (формат CSV з роздільником |)[cite: 7]
class FileJunkStorage(JunkRepository):
    def __init__(self, filename: str):
        self.filename = filename

    # Метод для запису у файл з кастомним форматуванням (дроби через кому)[cite: 7]
    def serialize(self, items: list[JunkItem], filename: str):
        with open(filename, 'w', encoding='utf-8') as file:
            for item in items:
                # Заміна крапки на кому для десяткових дробів[cite: 7]
                value_str = str(item.value).replace('.', ',')
                file.write(f"{item.name}|{item.quantity}|{value_str}\n")

    # Метод для читання та перевірки на зіпсовані рядки[cite: 7]
    def parse(self, filename: str) -> list[JunkItem]:
        items = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split('|')
                    
                    # Перевірка: чи рівно 3 поля[cite: 7]
                    if len(parts) != 3:
                        print(f"[Помилка] Рядок {line_num} не має трьох полів. Пропущено: '{line}'")
                        continue
                    
                    name_str, qty_str, val_str = parts
                    
                    try:
                        # Перевірка: чи кількість є цілим числом, а ціна - дробовим (після заміни коми на крапку)[cite: 7]
                        quantity = int(qty_str)
                        value = float(val_str.replace(',', '.'))
                        items.append(JunkItem(name_str, quantity, value))
                    except ValueError:
                        print(f"[Помилка] Рядок {line_num} містить невірні типи даних (не число). Пропущено: '{line}'")
        except FileNotFoundError:
            print("Файл сховища поки не існує. Повертається порожній список.")
            
        return items

    # Реалізація методів абстрактного інтерфейсу
    def save(self, items: list[JunkItem]):
        self.serialize(items, self.filename)

    def load(self) -> list[JunkItem]:
        return self.parse(self.filename)


# 4. Демонстрація роботи системи[cite: 7]
if __name__ == "__main__":
    # Створюємо предмети за умовою[cite: 7]
    initial_items = [
        JunkItem("Бляшанка", 5, 2.5),
        JunkItem("Стара плата", 3, 7.8),
        JunkItem("Купка дротів", 10, 1.2)
    ]

    # Використовуємо інтерфейс JunkRepository. Клієнт не прив'язаний намертво до формату[cite: 7]
    repository: JunkRepository = FileJunkStorage("storage.txt")

    print("=== 1. Збереження предметів у файл ===")
    repository.save(initial_items)
    print("Предмети успішно записані.\n")

    # Штучно додаємо зіпсовані рядки у файл для демонстрації валідації[cite: 7]
    with open("storage.txt", 'a', encoding='utf-8') as f:
        f.write("Зламаний предмет|десять|5,5\n")  # Кількість не int
        f.write("Неповний запис|5\n")             # Немає 3 полів

    print("=== 2. Відновлення предметів з файлу (з перевіркою) ===")
    restored_items = repository.load()

    print("\n=== 3. Результат читання (перевірка значень) ===")
    for item in restored_items:
        print(item)