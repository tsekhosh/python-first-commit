import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox

FILENAME = "warehouse.csv"

def load_data():
    tree.delete(*tree.get_children())
    if os.path.exists(FILENAME):
        with open(FILENAME, mode="r", encoding="utf-8") as f:
            for row in csv.reader(f):
                if row: tree.insert("", tk.END, values=row)

def save_data():
    with open(FILENAME, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for row in tree.get_children():
            writer.writerow(tree.item(row)["values"])

def add_item():
    try:
        qty = int(e_qty.get())
        price = float(e_price.get())
        if not e_name.get() or not e_cat.get(): raise ValueError()
    except ValueError:
        messagebox.showerror("Помилка", "Перевірте дані: кількість і ціна мають бути числами, а назва — непорожньою!")
        return
    
    item_id = str(len(tree.get_children()) + 1)
    tree.insert("", tk.END, values=(item_id, e_name.get(), e_cat.get(), qty, price, e_loc.get()))
    save_data()
    clear_form()

def update_item():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Увага", "Оберіть рядок для оновлення!")
        return
    try:
        qty = int(e_qty.get())
        price = float(e_price.get())
    except ValueError:
        messagebox.showerror("Помилка", "Кількість і ціна мають бути числами!")
        return
    
    item_id = tree.item(selected[0], "values")[0]
    tree.item(selected[0], values=(item_id, e_name.get(), e_cat.get(), qty, price, e_loc.get()))
    save_data()
    clear_form()

def delete_item():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Увага", "Оберіть рядок для видалення!")
        return
    if messagebox.askyesno("Підтвердження", "Видалити цей товар?"):
        tree.delete(selected[0])
        save_data()
        clear_form()

def clear_form():
    for e in (e_name, e_cat, e_qty, e_price, e_loc): e.delete(0, tk.END)

def on_select(event):
    selected = tree.selection()
    if selected:
        vals = tree.item(selected[0], "values")
        clear_form()
        for e, val in zip((e_name, e_cat, e_qty, e_price, e_loc), vals[1:]):
            e.insert(0, val)

def search_item(event):
    q = e_search.get().lower()
    for row in tree.get_children():
        vals = tree.item(row)["values"]
        if q in str(vals[1]).lower() or q in str(vals[2]).lower():
            tree.reattach(row, "", tk.END)
        else:
            tree.detach(row)

# Головне вікно
root = tk.Tk()
root.title("Облік товарів")
root.geometry("850x450")

# Пошук
f_search = ttk.Frame(root, padding=5)
f_search.pack(fill=tk.X)
ttk.Label(f_search, text="Пошук (назва/категорія):").pack(side=tk.LEFT, padx=5)
e_search = ttk.Entry(f_search)
e_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
e_search.bind("<KeyRelease>", search_item)

# Таблиця
cols = ("ID", "Назва", "Категорія", "Кількість", "Ціна", "Склад")
tree = ttk.Treeview(root, columns=cols, show="headings")
for c in cols: tree.heading(c, text=c)
tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
tree.bind("<<TreeviewSelect>>", on_select)

# Форма вводу
f_form = ttk.Frame(root, padding=5)
f_form.pack(fill=tk.X)

e_name = ttk.Entry(f_form, width=12)
e_cat = ttk.Entry(f_form, width=12)
e_qty = ttk.Entry(f_form, width=8)
e_price = ttk.Entry(f_form, width=8)
e_loc = ttk.Entry(f_form, width=10)

for lbl, ent in zip(("Назва:", "Категорія:", "Кількість:", "Ціна:", "Склад:"), (e_name, e_cat, e_qty, e_price, e_loc)):
    ttk.Label(f_form, text=lbl).pack(side=tk.LEFT, padx=2)
    ent.pack(side=tk.LEFT, padx=2)

# Кнопки
f_btn = ttk.Frame(root, padding=5)
f_btn.pack(fill=tk.X)
ttk.Button(f_btn, text="Додати", command=add_item).pack(side=tk.LEFT, padx=5)
ttk.Button(f_btn, text="Оновити", command=update_item).pack(side=tk.LEFT, padx=5)
ttk.Button(f_btn, text="Видалити", command=delete_item).pack(side=tk.LEFT, padx=5)
ttk.Button(f_btn, text="Очистити", command=clear_form).pack(side=tk.LEFT, padx=5)

load_data()
root.mainloop()