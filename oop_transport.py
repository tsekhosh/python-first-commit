from abc import ABC, abstractmethod

# Базовий абстрактний клас
class Transport(ABC):
    def __init__(self, name: str, speed: int, capacity: int):
        self.name = name
        self.speed = speed
        self.capacity = capacity

    @abstractmethod
    def move(self, distance: float) -> float:
        pass

    @abstractmethod
    def fuel_consumption(self, distance: float) -> float:
        pass

    @abstractmethod
    def info(self) -> str:
        pass

    # Метод у базовому класі для розрахунку загальних витрат у грошах
    def calculate_cost(self, distance: float, price_per_unit: float) -> float:
        return self.fuel_consumption(distance) * price_per_unit


# Підклас Car (Автомобіль)
class Car(Transport):
    def move(self, distance: float) -> float:
        return distance / self.speed

    def fuel_consumption(self, distance: float) -> float:
        return distance * 0.07

    def info(self) -> str:
        return f"Легковий автомобіль {self.name} (Швидкість: {self.speed} км/год)"


# Підклас Bus (Автобус)
class Bus(Transport):
    def __init__(self, name: str, speed: int, capacity: int, passengers: int):
        super().__init__(name, speed, capacity)
        self.passengers = passengers

    def move(self, distance: float) -> float:
        return distance / self.speed

    def fuel_consumption(self, distance: float) -> float:
        return distance * 0.15

    def info(self) -> str:
        overload_msg = " — Перевантажено!" if self.passengers > self.capacity else ""
        return f"Автобус {self.name} (Пасажирів: {self.passengers}/{self.capacity}){overload_msg}"


# Підклас Bicycle (Велосипед)
class Bicycle(Transport):
    def __init__(self, name: str, speed: int, capacity: int = 1):
        # Швидкість обмежена 20 км/год
        actual_speed = min(speed, 20)
        super().__init__(name, actual_speed, capacity)

    def move(self, distance: float) -> float:
        return distance / self.speed

    def fuel_consumption(self, distance: float) -> float:
        return 0.0

    def info(self) -> str:
        return f"Велосипед {self.name} (Швидкість: {self.speed} км/год)"


# Підклас ElectricCar (Електромобіль), успадкований від Car
class ElectricCar(Car):
    def battery_usage(self, distance: float) -> float:
        return distance * 0.2

    def fuel_consumption(self, distance: float) -> float:
        return 0.0  # Пальне завжди 0

    def info(self) -> str:
        return f"Електромобіль {self.name} (Швидкість: {self.speed} км/год)"


# --- Виконання завдання: Список різних видів транспорту ---
if __name__ == "__main__":
    transports = [
        Car("Toyota Camry", speed=120, capacity=5),
        Bus("Богдан", speed=80, capacity=40, passengers=45),  # Спеціально перевантажили
        Bus("Еталон", speed=70, capacity=30, passengers=15),
        Bicycle("Pride", speed=35),  # Спробуємо задати 35, але обріжеться до 20
        ElectricCar("Tesla Model 3", speed=150, capacity=5)
    ]

    distance_to_travel = 100.0  # Відстань 100 км

    print(f"\n--- Дані для поїздки на {distance_to_travel} км ---\n")
    
    for t in transports:
        print(t.info())
        print(f"Назва: {t.name}")
        print(f"Час у дорозі: {t.move(distance_to_travel):.2f} год")
        print(f"Витрати пального: {t.fuel_consumption(distance_to_travel):.2f} л")
        
        # Якщо це електромобіль, виводимо ще й витрату батареї
        if isinstance(t, ElectricCar):
            print(f"Витрата батареї: {t.battery_usage(distance_to_travel):.2f} кВт⋅год")
            
        print("-" * 40)