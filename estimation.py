import threading
import time
import random


class Warehouse:
    def __init__(self, name: str, meds: int, price_per_unit: float):
        self.name = name
        self.initial_meds = meds 
        self.meds = meds
        self.price_per_unit = price_per_unit
        self.total_stolen = 0     
        self.lock = threading.Lock() 

    def steal(self, amount: int, use_lock: bool = True):
        if use_lock:
            self.lock.acquire()
        try:
            if not use_lock:
                current_meds = self.meds
                time.sleep(0.002)
                actual_steal = min(amount, current_meds)
                if actual_steal > 0:
                    self.meds = current_meds - actual_steal
                    self.total_stolen += actual_steal
                    return actual_steal
                return 0
            else:
               
                actual_steal = min(amount, self.meds)
                if actual_steal > 0:
                    self.meds -= actual_steal
                    self.total_stolen += actual_steal
                    return actual_steal
                return 0
        finally:
            if use_lock:
                self.lock.release()

class Runner(threading.Thread):
    def __init__(self, name: str, warehouses: list, use_lock: bool = True):
        super().__init__()
        self.runner_name = name
        self.warehouses = warehouses
        self.use_lock = use_lock
        self.earned = 0  

    def run(self):
        for _ in range(10):  
            warehouse = random.choice(self.warehouses)
            amount_to_steal = random.randint(10, 30)  

            stolen = warehouse.steal(amount_to_steal, use_lock=self.use_lock)
            self.earned += stolen * warehouse.price_per_unit



def run_simulation(use_lock: bool = True, num_runners: int = 5):
    warehouses = [
        Warehouse(name="Склад А", meds=random.randint(100, 300), price_per_unit=15.0),
        Warehouse(name="Склад Б", meds=random.randint(100, 300), price_per_unit=20.0),
        Warehouse(name="Склад В", meds=random.randint(100, 300), price_per_unit=10.0),
    ]

    runners = [Runner(name=f"Бігун-{i+1}", warehouses=warehouses, use_lock=use_lock) for i in range(num_runners)]

    for r in runners:
        r.start()

    for r in runners:
        r.join()

    total_earned_money = sum(r.earned for r in runners)

    for w in warehouses:
        assert w.meds >= 0, f"Інваріант 1 зламався! На складі {w.name} від'ємна кількість: {w.meds}"
        
        assert w.initial_meds == w.meds + w.total_stolen, (
            f"Інваріант 2 зламався для {w.name}! "
            f"Було: {w.initial_meds}, Залишилось: {w.meds}, Вкрали: {w.total_stolen}"
        )

    calculated_total_earned = sum(w.total_stolen * w.price_per_unit for w in warehouses)
    assert abs(total_earned_money - calculated_total_earned) < 1e-5, (
        f"Інваріант 3 зламався! Заробіток ({total_earned_money}) "
        f"не збігається з вартістю вкраденого ({calculated_total_earned})"
    )

    return warehouses, total_earned_money



if __name__ == "__main__":
    print("=== ЕТАП 1: Прогін 100 симуляцій ІЗ БЛОКУВАННЯМ (Lock) ===")
    success_with_lock = True
    for run_idx in range(1, 101):
        try:
            run_simulation(use_lock=True, num_runners=5)
            print(f"[Lock] Прогін {run_idx}/100 успішний", end="\r")
        except AssertionError as e:
            print(f"\nПомилка на прогоні {run_idx}: {e}")
            success_with_lock = False
            break

    if success_with_lock:
        print("\n[Успіх] Усі 100 прогонів із Lock пройшли перевірку інваріантів без жодної помилки!\n")

    print("=== ЕТАП 2: Прогін симуляцій БЕЗ БЛОКУВАННЯ (Race Condition) ===")
    print("Шукаємо злам інваріантів (50 бігунів)...")
    
    broken_at_run = None
    for run_idx in range(1, 101):
        try:
            run_simulation(use_lock=False, num_runners=50)
            print(f"[Без Lock] Прогін {run_idx}/100 безпечний", end="\r")
        except AssertionError as e:
            broken_at_run = run_idx
            print(f"\n\n[!] ІНВАРІАНТ ЗЛАМАВСЯ на прогоні №{run_idx}!")
            print(f"Причина помилки: {e}")
            break

    if not broken_at_run:
        print("\nЗа 100 прогонів стан гонки не спровокував падіння.")
    else:
        print(f"\n[Висновок]: Через відсутність `threading.Lock()` та неатомарність операції (читання -> пауза -> запис) сталася гонка потоків, що гарантовано зламало інваріант на прогоні #{broken_at_run}!")