from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class SearchPage(BasePage):
    """https://opencart.abstracta.us/index.php?route=product/search"""

    HEADING = (By.CSS_SELECTOR, "#content h1")
    KEYWORD_INPUT = (By.ID, "input-search")
    CATEGORY_SELECT = (By.NAME, "category_id")
    DESCRIPTION_CHECKBOX = (By.ID, "description")
    SEARCH_BUTTON = (By.ID, "button-search")
    RESULT_NAMES = (By.CSS_SELECTOR, ".product-layout .caption h4 a")
    RESULT_ADD_TO_CART = (By.CSS_SELECTOR, ".product-layout .button-group button:first-child")
    # The message shown under the "Search" results heading when nothing matches.
    EMPTY_MESSAGE = (By.CSS_SELECTOR, "#content > h2 + p")

    def heading(self):
        return self.find(self.HEADING).text.strip()

    def result_names(self):
        return [a.text.strip() for a in self.find_all(self.RESULT_NAMES)]

    def empty_message(self):
        return self.find(self.EMPTY_MESSAGE).text.strip()

    def advanced_search(self, keyword, in_description=False, category=None):
        box = self.find(self.KEYWORD_INPUT)
        box.clear()
        box.send_keys(keyword)
        if category:
            Select(self.find(self.CATEGORY_SELECT)).select_by_visible_text(category)
        checkbox = self.find(self.DESCRIPTION_CHECKBOX)
        if checkbox.is_selected() != in_description:
            checkbox.click()
        self.find(self.SEARCH_BUTTON).click()

    def add_result_to_cart(self, index=0):
        self.find_all(self.RESULT_ADD_TO_CART)[index].click()
