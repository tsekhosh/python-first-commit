from models import Antibiotic, Vitamin, Vaccine, Medicine

# Одна функція, яка обробляє будь-які медикаменти без перевірки типу (поліморфізм)
def print_medicines_info(medicines_list: list[Medicine]):
    for med in medicines_list:
        # Викликаємо метод info(), і Python сам знає, чий саме info() викликати
        print(med.info())

if __name__ == "__main__":
    # Створюємо список різних видів Medicine
    meds = [
        Antibiotic(name="Амоксицилін", quantity=10, price=50.0),
        Vitamin(name="Аскорбінка", quantity=20, price=15.0),
        Vaccine(name="Пфайзер", quantity=5, price=500.0)
    ]
    
    print("--- Інформація про медикаменти на складі ---\n")
    print_medicines_info(meds)