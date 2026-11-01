from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://opencart.abstracta.us/"


class BasePage:
    HEADER_SEARCH_INPUT = (By.CSS_SELECTOR, "#search input[name='search']")
    HEADER_SEARCH_BUTTON = (By.CSS_SELECTOR, "#search button")
    CART_TOTAL = (By.ID, "cart-total")
    CART_DROPDOWN_BUTTON = (By.CSS_SELECTOR, "#cart > button")
    CART_DROPDOWN_ITEMS = (By.CSS_SELECTOR, "#cart .dropdown-menu table.table-striped tr")
    CART_DROPDOWN_REMOVE = (By.CSS_SELECTOR, "#cart .dropdown-menu button[title='Remove']")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")

    def __init__(self, driver, timeout=20):
        # The public demo server can be slow, so allow generous waits.
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, route=""):
        self.driver.get(BASE_URL + route)
        # Buttons such as Add to Cart are wired up by jQuery once the page has loaded.
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        return self

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def search_from_header(self, keyword):
        box = self.find(self.HEADER_SEARCH_INPUT)
        box.clear()
        box.send_keys(keyword)
        self.find(self.HEADER_SEARCH_BUTTON).click()

    def cart_total_text(self):
        return self.find(self.CART_TOTAL).text.strip()

    def wait_cart_total_contains(self, text):
        self.wait.until(EC.text_to_be_present_in_element(self.CART_TOTAL, text))
        return self.cart_total_text()

    def open_cart_dropdown(self):
        """Open the header cart button's dropdown and return its item lines, e.g. ["iPhone x 1 $123.20"]."""
        self.find(self.CART_DROPDOWN_BUTTON).click()
        self.find(self.CART_DROPDOWN_REMOVE)
        return [r.text.strip() for r in self.find_all(self.CART_DROPDOWN_ITEMS)]

    def remove_from_cart_dropdown(self, index=0):
        self.find_all(self.CART_DROPDOWN_REMOVE)[index].click()

    def success_alert_text(self):
        text = self.find(self.SUCCESS_ALERT).text
        # OpenCart animates the page back to the top after the alert; wait so screenshots show the header.
        self.wait.until(lambda d: d.execute_script("return window.pageYOffset") == 0)
        return text
