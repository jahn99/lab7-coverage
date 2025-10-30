import pytest
from order_processor import calculate_discount, update_order_status

# --- calculate_discount tests ---

def test_regular_low_amount_zero_discount():
    assert calculate_discount("regular", 500) == 0

def test_regular_high_amount_five_percent():
    assert calculate_discount("regular", 1500) == 75

def test_premium_ten_percent():
    assert calculate_discount("premium", 2000) == 200

@pytest.mark.parametrize("amount,expected", [(6000, 1200), (3000, 300)])
def test_vip_discounts(amount, expected):
    assert calculate_discount("vip", amount) == expected

def test_unknown_customer_type_raises():
    with pytest.raises(ValueError):
        calculate_discount("student", 1000)

# --- update_order_status tests ---

def test_pending_paid_true_moves_to_processing():
    order = {"status": "pending", "paid": True}
    assert update_order_status(order) == "processing"
    assert order["status"] == "processing"

def test_pending_paid_false_moves_to_awaiting_payment():
    order = {"status": "pending", "paid": False}
    assert update_order_status(order) == "awaiting_payment"
    assert order["status"] == "awaiting_payment"

def test_processing_items_available_true_moves_to_shipped():
    order = {"status": "processing", "items_available": True}
    assert update_order_status(order) == "shipped"
    assert order["status"] == "shipped"

def test_processing_items_available_false_moves_to_backorder():
    order = {"status": "processing", "items_available": False}
    assert update_order_status(order) == "backorder"
    assert order["status"] == "backorder"
