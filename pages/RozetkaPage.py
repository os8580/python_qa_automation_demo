from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.AbstractPage import AbstractPage
import re


class RozetkaPage(AbstractPage):
    def __init__(self, driver):
        super().__init__(driver, "https://rozetka.com.ua/")
        self.wait = WebDriverWait(self.driver, 10)

    def find_element(self, element_type, value):
        return self.wait.until(EC.presence_of_element_located((element_type, value)))

    def set_search_value(self, value):
        search_box = self.find_element(By.NAME, 'search')
        search_box.send_keys(value)

    def perform_search(self):
        search_box = self.find_element(By.NAME, 'search')
        search_box.send_keys(Keys.ENTER)

    def get_search_results(self):
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.goods-tile')))
        except TimeoutException:
            return []
        return [e for e in elements if e.is_displayed()]

    def get_product_info_element(self, element_selector):
        first_product = self.get_search_results()[0]
        return self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, element_selector)))

    def get_product_name(self):
        return self.get_product_info_element('.goods-tile__title').text

    def get_product_price(self):
        return self.get_product_info_element('.goods-tile__price').text

    def click_add_to_cart_button(self):
        self.find_element(By.CSS_SELECTOR, '.buy-button').click()

    def wait_for_text_visibility(self, text):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), '" + text + "')]")))

    def open_cart(self):
        self.find_element(By.CSS_SELECTOR, "li[class*='item--cart']").click()

    def get_cart_product_name(self):
        return self.find_element(By.CSS_SELECTOR, ".cart-product__title").text

    def get_cart_product_price(self):
        return self.find_element(By.CSS_SELECTOR, ".cart-product__price").text

    def process_quantity(self, adjust_value):
        quantity_input = self.find_element(By.CSS_SELECTOR, "[data-testid='cart-counter-input']")
        initial_quantity = int(quantity_input.get_attribute("value"))
        quantity_input.clear()
        quantity_input.send_keys(str(initial_quantity + adjust_value))
        quantity_input.send_keys(Keys.ENTER)

    def increase_product_quantity_by_one(self):
        self.process_quantity(1)

    def decrease_product_quantity_by_one(self):
        self.process_quantity(-1)

    def get_product_quantity(self):
        quantity_element = self.find_element(By.CSS_SELECTOR, "[data-testid='cart-counter-input']")
        return int(quantity_element.get_attribute("value"))

    def get_single_product_price(self):
        product_price_element = self.find_element(By.CSS_SELECTOR, "div[class='cart-receipt__sum-price']")
        product_price_text = product_price_element.text
        non_numeric_removed = re.sub("\\D+", "", product_price_text)
        return int(non_numeric_removed) / self.get_product_quantity()

    def get_cart_total_price(self):
        return self.find_element(By.CSS_SELECTOR, "div[class*='sum-price']").text

    def wait_for_cart_total_price_to_change(self, initial_price):
        self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div[class*='sum-price']"), initial_price))

    def set_product_quantity(self, quantity):
        quantity_input = self.find_element(By.CSS_SELECTOR, "input[data-testid='cart-counter-input']")
        initial_quantity = quantity_input.get_attribute("value")
        initial_price = self.get_cart_total_price()

        quantity_input.clear()
        quantity_input.send_keys(str(quantity))

        self.wait.until(lambda _: quantity_input.get_attribute("value") != initial_quantity)
        self.wait.until(lambda _: self.get_cart_total_price() != initial_price)