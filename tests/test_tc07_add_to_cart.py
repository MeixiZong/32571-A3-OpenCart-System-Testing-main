"""TC07 - F7 Add to Shopping Cart
https://opencart.abstracta.us/index.php?route=product/product&product_id=40
"""
import pytest

from pages.product_page import ProductPage
from pages.search_page import SearchPage

pytestmark = pytest.mark.tc07

IPHONE_ID = 40
APPLE_CINEMA_ID = 42  # has required options


def test_s1_add_product_from_product_page(driver, shot):
    """Scenario 1: add one iPhone from its product page."""
    page = ProductPage(driver).open_product(IPHONE_ID)
    shot("iphone_product_page")
    assert page.title() == "iPhone"
    assert page.cart_total_text() == "0 item(s) - $0.00"

    page.set_quantity(1)
    page.add_to_cart()

    alert = page.success_alert_text()
    shot("added_to_cart")
    assert "Success: You have added iPhone to your shopping cart!" in alert
    assert page.wait_cart_total_contains("1 item(s)") == "1 item(s) - $123.20"


def test_s2_add_product_from_search_results(driver, shot):
    """Scenario 2: search for 'iPhone' and use the result's ADD TO CART button."""
    page = SearchPage(driver).open()
    page.search_from_header("iPhone")
    shot("search_results_iphone")
    assert page.result_names() == ["iPhone"]

    page.add_result_to_cart(0)

    alert = page.success_alert_text()
    shot("added_from_results")
    assert "Success: You have added iPhone to your shopping cart!" in alert
    assert page.wait_cart_total_contains("1 item(s)") == "1 item(s) - $123.20"


def test_s3_add_product_without_required_options_is_rejected(driver, shot):
    """Scenario 3: Apple Cinema 30" cannot be added until its required options are chosen."""
    page = ProductPage(driver).open_product(APPLE_CINEMA_ID)
    shot("apple_cinema_page")

    page.add_to_cart()

    errors = page.field_errors()
    shot("required_option_errors")
    for expected in ["Radio required!", "Checkbox required!", "Select required!",
                     "Textarea required!", "File required!"]:
        assert expected in errors
    assert page.cart_total_text() == "0 item(s) - $0.00"
