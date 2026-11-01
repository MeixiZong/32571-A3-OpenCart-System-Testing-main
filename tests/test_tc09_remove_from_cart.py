"""TC09 - F9 Remove from Cart
https://opencart.abstracta.us/index.php?route=checkout/cart
"""
import pytest

from conftest import IPHONE_ID, MACBOOK_ID, add_products_to_cart
from pages.cart_page import CartPage
from pages.product_page import ProductPage

pytestmark = pytest.mark.tc09


def test_s1_remove_only_item_empties_cart(cart_with_iphone, shot):
    """Scenario 1: the Remove button deletes the only item and the cart becomes empty."""
    cart = cart_with_iphone
    shot("cart_before_remove")

    cart.remove_item()
    shot("cart_after_remove")

    assert cart.empty_message() == "Your shopping cart is empty!"
    assert cart.cart_total_text() == "0 item(s) - $0.00"


def test_s2_remove_one_of_two_items_keeps_the_other(driver, shot):
    """Scenario 2: removing the iPhone from a cart holding an iPhone and a MacBook leaves only the MacBook."""
    add_products_to_cart(driver, IPHONE_ID, MACBOOK_ID)
    cart = CartPage(driver).open_cart()
    shot("cart_with_two_items")
    assert cart.item_names() == ["iPhone", "MacBook"]

    cart.remove_item(row=0)
    shot("cart_after_removing_iphone")

    assert cart.item_names() == ["MacBook"]
    assert cart.totals()["Total"] == "$602.00"
    assert cart.cart_total_text() == "1 item(s) - $602.00"


def test_s3_remove_item_from_header_cart_dropdown(driver, shot):
    """Scenario 3: an item can be removed from the header cart dropdown without opening the cart page."""
    add_products_to_cart(driver, IPHONE_ID)
    page = ProductPage(driver).open_product(MACBOOK_ID)

    lines = page.open_cart_dropdown()
    shot("cart_dropdown_open")
    assert lines[0].startswith("iPhone")

    page.remove_from_cart_dropdown(0)

    assert page.wait_cart_total_contains("0 item(s)") == "0 item(s) - $0.00"
    shot("cart_after_dropdown_remove")
    assert CartPage(driver).open_cart().empty_message() == "Your shopping cart is empty!"
