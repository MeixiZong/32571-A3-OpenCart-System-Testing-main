from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CartPage(BasePage):
    """https://opencart.abstracta.us/index.php?route=checkout/cart"""

    ROUTE = "index.php?route=checkout/cart"
    ITEM_ROWS = (By.CSS_SELECTOR, "#content form tbody tr")
    ITEM_NAME = (By.CSS_SELECTOR, "td:nth-child(2) a")
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input[name^='quantity']")
    UPDATE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button.btn-danger")
    TOTALS_ROWS = (By.CSS_SELECTOR, "#content > .row table tr")
    EMPTY_MESSAGE = (By.CSS_SELECTOR, "#content > p")

    def open_cart(self):
        return self.open(self.ROUTE)

    def item_names(self):
        return [r.find_element(*self.ITEM_NAME).text.strip() for r in self.find_all(self.ITEM_ROWS)]

    def quantity(self, row=0):
        return self.find_all(self.ITEM_ROWS)[row].find_element(*self.QUANTITY_INPUT).get_attribute("value")

    def update_quantity(self, qty, row=0):
        item = self.find_all(self.ITEM_ROWS)[row]
        box = item.find_element(*self.QUANTITY_INPUT)
        box.clear()
        box.send_keys(str(qty))
        item.find_element(*self.UPDATE_BUTTON).click()
        self.wait.until(EC.staleness_of(item))

    def remove_item(self, row=0):
        item = self.find_all(self.ITEM_ROWS)[row]
        item.find_element(*self.REMOVE_BUTTON).click()
        self.wait.until(EC.staleness_of(item))

    def totals(self):
        """Return the totals table as {"Sub-Total": "$101.00", ..., "Total": "$123.20"}."""
        result = {}
        for row in self.find_all(self.TOTALS_ROWS):
            label, value = row.find_elements(By.TAG_NAME, "td")
            result[label.text.strip().rstrip(":")] = value.text.strip()
        return result

    def scroll_to_totals(self):
        rows = self.find_all(self.TOTALS_ROWS)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", rows[-1])

    def empty_message(self):
        return self.find(self.EMPTY_MESSAGE).text.strip()
