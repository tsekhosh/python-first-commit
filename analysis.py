import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 8. Додаємо підтримку передачі CSV через argparse
parser = argparse.ArgumentParser(description="Аналіз даних постачань препаратів")
parser.add_argument('--file', type=str, default='supplies.csv', help="Шлях до CSV файлу з даними")
args = parser.parse_args()

# 1. Завантажуємо дані з CSV за допомогою pandas
df = pd.read_csv(args.file)

# 2. Обчислення за допомогою NumPy:
# - середня ціна всіх препаратів (price_per_unit)
mean_price = np.mean(df['price_per_unit'])
# - медіана кількості (quantity)
median_quantity = np.median(df['quantity'])
# - стандартне відхилення ціни (price_per_unit)
std_price = np.std(df['price_per_unit'], ddof=1)  # вибіркове стандартне відхилення

# 4. Додаємо обчислене поле total_price у DataFrame (quantity * price_per_unit)
df['total_price'] = df['quantity'] * df['price_per_unit']

# 3. Робота з pandas:
# - знайти постачальника з найбільшим загальним прибутком
supplier_profit = df.groupby('supplier')['total_price'].sum()
top_supplier = supplier_profit.idxmax()
max_profit = supplier_profit.max()

# - обчислити сумарну кількість препаратів за категоріями (groupby)
category_quantity = df.groupby('category')['quantity'].sum()

# - відфільтрувати усі записи, де quantity < 100, і зберегти у новий CSV (low_supply.csv)
low_supply_df = df[df['quantity'] < 100]
low_supply_filename = 'low_supply.csv'
low_supply_df.to_csv(low_supply_filename, index=False)

# 5. Відсортувати дані за total_price у порядку спадання й вивести перші три рядки в консоль
sorted_df = df.sort_values(by='total_price', ascending=False)
print("=== Перші три рядки за загальною вартістю (total_price) ===")
print(sorted_df.head(3))
print("-" * 50)

# 6. Створити простий звіт у форматі .txt (report.txt)
report_content = f"""ЗВІТ З АНАЛІЗУ ПОСТАЧАНЬ
=============================
1. Середні показники (NumPy):
   - Середня ціна препарату: {mean_price:.2f}
   - Медіана кількості (quantity): {median_quantity}
   - Стандартне відхилення ціни: {std_price:.2f}

2. Постачальник з найбільшим загальним прибутком:
   - {top_supplier} (загальний прибуток: {max_profit:.2f})

3. Дефіцитні постачальники:
   - Збережено у файл: {low_supply_filename} (записи з кількістю менше 100)

4. Сумарна кількість препаратів за категоріями:
{category_quantity.to_string()}
"""

with open('report.txt', 'w', encoding='utf-8') as f:
    f.write(report_content)
print("Звіт успішно збережено у файл report.txt")

# 7. Побудувати графік (через matplotlib) розподілу кількості препаратів за категоріями
plt.figure(figsize=(8, 5))
category_quantity.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Розподіл кількості препаратів за категоріями')
plt.xlabel('Категорія')
plt.ylabel('Сумарна кількість (quantity)')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Зберігаємо графік (можна також показати через plt.show())
plt.savefig('category_distribution.png')
print("Графік збережено у файл category_distribution.png")
plt.show()