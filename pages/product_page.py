from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ProductPage(BasePage):
    """https://opencart.abstracta.us/index.php?route=product/product&product_id=<id>"""

    TITLE = (By.CSS_SELECTOR, "#content h1")
    QUANTITY_INPUT = (By.ID, "input-quantity")
    ADD_TO_CART_BUTTON = (By.ID, "button-cart")
    FIELD_ERRORS = (By.CSS_SELECTOR, "#product .text-danger")

    def open_product(self, product_id):
        return self.open(f"index.php?route=product/product&product_id={product_id}")

    def title(self):
        return self.find(self.TITLE).text.strip()

    def set_quantity(self, qty):
        box = self.find(self.QUANTITY_INPUT)
        box.clear()
        box.send_keys(str(qty))

    def add_to_cart(self):
        self.find(self.ADD_TO_CART_BUTTON).click()

    def field_errors(self):
        self.wait.until(EC.visibility_of_element_located(self.FIELD_ERRORS))
        return [e.text.strip() for e in self.find_all(self.FIELD_ERRORS)]
