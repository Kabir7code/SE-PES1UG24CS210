"""Branch coverage tests for shopping_cart.py.

Goal: make every decision (if / elif / else) take both its True and
False outcome, and check the boundary values of each condition.
"""
import pytest
from shopping_cart import item_total, cart_discount, shipping_fee


# ---------- item_total ----------
# Decisions: category known?  price/qty valid?  qty >= 10?

def test_food_item():
    # known category, valid input, qty < 10 (no bulk discount)
    assert item_total("food", 100, 2) == 210


def test_unknown_category_raises():
    # category NOT in GST_RATE -> True branch of first if
    with pytest.raises(ValueError, match="unknown category"):
        item_total("books", 100, 1)


def test_negative_price_raises():
    # price < 0 is True
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", -1, 1)


def test_zero_quantity_raises():
    # price is fine but qty <= 0 is True (other half of the "or")
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("electronics", 100, 0)


def test_zero_price_is_allowed():
    # boundary: price == 0 is valid (price < 0 is False)
    assert item_total("food", 0, 1) == 0


def test_bulk_discount_boundary_qty_10():
    # boundary: qty == 10 -> bulk discount applies
    # 1000 -> 900 -> 900 + 12% GST (108)
    assert item_total("clothing", 100, 10) == 1008


def test_no_bulk_discount_qty_9():
    # boundary: qty == 9 -> no bulk discount
    # 900 + 18% GST (162)
    assert item_total("electronics", 100, 9) == 1062


# ---------- cart_discount ----------
# Decisions: >= 5000 / >= 2000 / else,  is_prime?,  coupon AND value >= 1000?

def test_cart_discount_boundary_5000():
    # boundary: exactly 5000 -> top tier
    assert cart_discount(5000, False, "") == 500


def test_cart_discount_boundary_2000_prime():
    # boundary: exactly 2000 -> middle tier, plus prime bonus
    assert cart_discount(2000, True, "") == 300


def test_cart_discount_below_2000_no_extras():
    # else tier, not prime, no coupon -> every condition False
    assert cart_discount(1999, False, "") == 0


def test_coupon_boundary_1000():
    # coupon valid and cart_value == 1000 -> 10% off
    assert cart_discount(1000, False, "FLAT10") == 100


def test_coupon_below_minimum():
    # coupon correct but cart_value < 1000 -> coupon ignored
    assert cart_discount(999, False, "FLAT10") == 0


def test_wrong_coupon_code():
    # big enough cart but wrong code -> coupon ignored
    assert cart_discount(1500, False, "SAVE20") == 0


def test_all_discounts_stack():
    # top tier + prime + coupon: 500 + 100 + 600
    assert cart_discount(6000, True, "FLAT10") == 1200


# ---------- shipping_fee ----------
# Decisions: is_prime / cart >= 500 / else,  is_express?,  is_prime (inside express)?

def test_prime_standard_shipping():
    # prime, not express -> free
    assert shipping_fee(200, True, False) == 0


def test_free_shipping_boundary_500():
    # boundary: non-prime, exactly 500 -> free
    assert shipping_fee(500, False, False) == 0


def test_shipping_below_500():
    # boundary: non-prime, 499 -> 40
    assert shipping_fee(499, False, False) == 40


def test_express_non_prime():
    # express, inner "if is_prime" is False -> 40 + 100
    assert shipping_fee(200, False, True) == 140


def test_express_prime():
    # express, inner "if is_prime" is True -> 0 + 100 - 50
    assert shipping_fee(200, True, True) == 50


def test_express_free_standard_non_prime():
    # non-prime, cart >= 500 (free standard), express -> 100
    assert shipping_fee(1000, False, True) == 100
