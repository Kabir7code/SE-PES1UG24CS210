"""Code (line) coverage tests for shopping_cart.py.

Goal: execute every line of shopping_cart.py at least once.
"""
import pytest
from shopping_cart import item_total, cart_discount, shipping_fee


# ---------- item_total ----------

def test_food_item():
    # starter test: 200 + 5% GST
    assert item_total("food", 100, 2) == 210


def test_unknown_category_raises():
    # line 6: category not in GST_RATE
    with pytest.raises(ValueError, match="unknown category"):
        item_total("books", 100, 1)


def test_negative_price_raises():
    # line 8: price < 0
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", -1, 1)


def test_bulk_discount_clothing():
    # line 11: qty >= 10 gives 10% off, then 12% GST
    # 100 * 10 = 1000 -> 900 -> 900 + 108
    assert item_total("clothing", 100, 10) == 1008


# ---------- cart_discount ----------

def test_cart_discount_above_5000():
    # line 17
    assert cart_discount(6000, False, "") == 500


def test_cart_discount_above_2000_prime():
    # lines 19 and 23: 200 + 100 prime
    assert cart_discount(3000, True, "") == 300


def test_cart_discount_small_with_coupon():
    # lines 21 and 25: 0 + 10% of 1500
    assert cart_discount(1500, False, "FLAT10") == 150


# ---------- shipping_fee ----------

def test_free_shipping():
    # starter test: line 33, cart >= 500
    assert shipping_fee(1000, False, False) == 0


def test_shipping_small_cart():
    # line 35: non-prime, cart < 500
    assert shipping_fee(200, False, False) == 40


def test_prime_express_shipping():
    # lines 31, 37, 39: prime is free, express +100, prime gets 50 off
    assert shipping_fee(200, True, True) == 50
