"""Shared pytest fixtures: a fresh Chrome session per test and a step screenshot helper."""
import os
import re
from pathlib import Path

import pytest
from selenium import webdriver

BASE_URL = "https://opencart.abstracta.us/"
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"


@pytest.fixture
def driver():
    # A new browser per test gives every scenario an empty cart and clean session.
    options = webdriver.ChromeOptions()
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,1000")
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(0)
    yield drv
    drv.quit()


@pytest.fixture
def shot(driver, request):
    """Call shot("label") to save screenshots/<test name>/NN_label.png."""
    folder = SCREENSHOT_DIR / re.sub(r"[^\w-]", "_", request.node.name)
    folder.mkdir(parents=True, exist_ok=True)
    counter = {"n": 0}

    def take(label):
        counter["n"] += 1
        path = folder / f"{counter['n']:02d}_{label}.png"
        driver.save_screenshot(str(path))
        return path

    return take


def add_products_to_cart(driver, *product_ids):
    from pages.product_page import ProductPage

    for count, product_id in enumerate(product_ids, start=1):
        product = ProductPage(driver).open_product(product_id)
        product.set_quantity(1)
        product.add_to_cart()
        product.wait_cart_total_contains(f"{count} item(s)")


@pytest.fixture
def cart_with_iphone(driver):
    """Precondition for TC08/TC09: one iPhone in the cart, then open the cart page."""
    from pages.cart_page import CartPage

    add_products_to_cart(driver, IPHONE_ID)
    cart = CartPage(driver).open_cart()
    assert cart.item_names() == ["iPhone"]
    return cart


IPHONE_ID = 40
MACBOOK_ID = 43


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Attach a screenshot to the HTML report when a test fails.
    outcome = yield
    report = outcome.get_result()
    drv = item.funcargs.get("driver")
    if report.when == "call" and report.failed and drv is not None:
        pytest_html = item.config.pluginmanager.getplugin("html")
        if pytest_html is not None:
            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.png(drv.get_screenshot_as_base64()))
            report.extras = extras
