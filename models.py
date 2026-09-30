from abc import ABC, abstractmethod

# Абстрактний базовий клас
class Medicine(ABC):
    def __init__(self, name: str, quantity: int, price: float):
        # Перевірка типів у конструкторі
        if not isinstance(name, str):
            raise TypeError("Name має бути рядком (str)")
        if not isinstance(quantity, int):
            raise TypeError("Quantity має бути цілим числом (int)")
        if not isinstance(price, (float, int)):
            raise TypeError("Price має бути числом (float або int)")
        
        self.name = name
        self.quantity = quantity
        self.price = float(price)

    @abstractmethod
    def requires_prescription(self) -> bool:
        pass

    @abstractmethod
    def storage_requirements(self) -> str:
        pass

    # Метод із реалізацією за замовчуванням
    def total_price(self) -> float:
        return self.quantity * self.price

    @abstractmethod
    def info(self) -> str:
        pass


# Підклас Антибіотик
class Antibiotic(Medicine):
    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "8-15°C, темне місце"

    def info(self) -> str:
        req = "За рецептом" if self.requires_prescription() else "Без рецепта"
        return f"Антибіотик '{self.name}': {self.quantity} шт., {self.total_price():.2f} грн. ({req}, Зберігання: {self.storage_requirements()})"


# Підклас Вітамін
class Vitamin(Medicine):
    def requires_prescription(self) -> bool:
        return False

    def storage_requirements(self) -> str:
        return "15-25°C, сухо"

    def info(self) -> str:
        req = "За рецептом" if self.requires_prescription() else "Без рецепта"
        return f"Вітамін '{self.name}': {self.quantity} шт., {self.total_price():.2f} грн. ({req}, Зберігання: {self.storage_requirements()})"


# Підклас Вакцина
class Vaccine(Medicine):
    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "2-8°C, холодильник"

    # Перевизначаємо метод, щоб додати 10% до вартості
    def total_price(self) -> float:
        base_price = super().total_price()
        return base_price * 1.10

    def info(self) -> str:
        req = "За рецептом" if self.requires_prescription() else "Без рецепта"
        return f"Вакцина '{self.name}': {self.quantity} шт., {self.total_price():.2f} грн. ({req}, Зберігання: {self.storage_requirements()})"