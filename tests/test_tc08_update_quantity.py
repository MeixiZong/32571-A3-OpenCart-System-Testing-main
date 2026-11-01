"""TC08 - F8 Update Cart Quantity
https://opencart.abstracta.us/index.php?route=checkout/cart
"""
import pytest

pytestmark = pytest.mark.tc08


def test_s1_update_quantity_recalculates_totals(cart_with_iphone, shot):
    """Scenario 1: changing the quantity from 1 to 3 updates line and order totals."""
    cart = cart_with_iphone
    shot("cart_with_one_iphone")
    assert cart.totals()["Total"] == "$123.20"

    cart.update_quantity(3)
    shot("quantity_updated_to_3")
    cart.scroll_to_totals()
    shot("totals_after_update")

    assert cart.quantity() == "3"
    totals = cart.totals()
    assert totals["Sub-Total"] == "$303.00"
    assert totals["Total"] == "$369.60"
    assert cart.cart_total_text() == "3 item(s) - $369.60"


def test_s2_update_quantity_to_zero_removes_item(cart_with_iphone, shot):
    """Scenario 2 (boundary value): setting the quantity to 0 removes the item from the cart."""
    cart = cart_with_iphone
    shot("cart_before_zero")

    cart.update_quantity(0)
    shot("cart_after_zero")

    assert cart.empty_message() == "Your shopping cart is empty!"
    assert cart.cart_total_text() == "0 item(s) - $0.00"


def test_s3_non_numeric_quantity_is_rejected(cart_with_iphone, shot):
    """Scenario 3 (invalid input): a non-numeric quantity must not change the cart."""
    cart = cart_with_iphone
    shot("cart_before_invalid")

    cart.update_quantity("abc")
    shot("cart_after_invalid")

    assert cart.item_names() == ["iPhone"], "the item was removed instead of the input being rejected"
    assert cart.quantity() == "1"
    assert cart.cart_total_text() == "1 item(s) - $123.20"
