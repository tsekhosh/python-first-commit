import pytest
from service_body_test import Order

# --- Тестування методу total() ---
def test_total_valid_items():
    order = Order(1, [{'price': 100, 'quantity': 2}, {'price': 50, 'quantity': 1}])
    assert order.total() == 250

def test_total_empty_items():
    order = Order(2, [])
    assert order.total() == 0

def test_total_zero_quantity():
    order = Order(3, [{'price': 100, 'quantity': 0}])
    assert order.total() == 0

# --- Тестування методу most_expensive() ---
def test_most_expensive():
    order = Order(4, [
        {'price': 10, 'quantity': 5},
        {'price': 150, 'quantity': 1},
        {'price': 50, 'quantity': 2}
    ])
    assert order.most_expensive() == {'price': 150, 'quantity': 1}

def test_most_expensive_empty():
    order = Order(5, [])
    # Стандартна поведінка Python: max() від порожнього списку викликає ValueError
    with pytest.raises(ValueError):
        order.most_expensive()

# --- Тестування методу apply_discount() ---
def test_apply_discount_valid():
    order = Order(6, [{'price': 100, 'quantity': 2}, {'price': 50, 'quantity': 1}])
    order.apply_discount(20)  # Знижка 20%
    assert order.items[0]['price'] == 80.0
    assert order.items[1]['price'] == 40.0

def test_apply_discount_boundaries():
    # Перевірка межових значень: 0% та 100%
    order_zero = Order(7, [{'price': 100, 'quantity': 1}])
    order_zero.apply_discount(0)
    assert order_zero.items[0]['price'] == 100.0

    order_full = Order(8, [{'price': 100, 'quantity': 1}])
    order_full.apply_discount(100)
    assert order_full.items[0]['price'] == 0.0

def test_apply_discount_invalid_negative():
    order = Order(9, [{'price': 100, 'quantity': 1}])
    with pytest.raises(ValueError, match="Invalid discount"):
        order.apply_discount(-10)

def test_apply_discount_invalid_over_100():
    order = Order(10, [{'price': 100, 'quantity': 1}])
    with pytest.raises(ValueError, match="Invalid discount"):
        order.apply_discount(101)

def test_apply_discount_empty_items():
    order = Order(11, [])
    order.apply_discount(15) # Не повинно викликати помилок, просто нічого не робить
    assert order.items == []

# --- Тестування методу __repr__() ---
def test_repr():
    order = Order(12, [{'price': 10, 'quantity': 1}, {'price': 20, 'quantity': 2}])
    assert repr(order) == "<Order 12: 2 items>"

def test_repr_empty():
    order = Order(13, [])
    assert repr(order) == "<Order 13: 0 items>"