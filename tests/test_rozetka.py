import re

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException

from pages.Pages import Pages
from utils.page_factory import PageFactory


class TestRozetkaSuite:

    def setup_method(self):

        # Setup before each test method

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()  # Максимизируйте окно браузера
        self.page_factory = PageFactory(self.driver)

    def teardown_method(self):
        # Teardown after each test method
        self.page_factory.tear_down()
        self.driver.quit()

    def test_rozetka(self):
        # Create pages
        google_page = self.page_factory.get(Pages.GOOGLE)
        rozetka_page = self.page_factory.get(Pages.ROZETKA)

        # Google search for 'rozetka ua'
        google_page.load_page()
        google_page.accept_cookies_if_present()
        google_page.set_search_value("rozetka ua")
        google_page.perform_search()

        search_results = google_page.get_search_results()
        assert len(search_results) > 1, "No search results found!"
        search_results[0].click()

        # Reinitialize rozetka_page after the page transition
        rozetka_page = self.page_factory.get(Pages.ROZETKA)

        # Rozetka search for 'Iphone'
        assert rozetka_page.is_page_loaded(), "Page is not loaded"
        rozetka_page.set_search_value("Iphone")
        rozetka_page.perform_search()

        search_results_rozetka = rozetka_page.get_search_results()
        assert search_results_rozetka, "No search results found on Rozetka page!"

        # Get product details
        product_details = {}
        product_details["name"] = rozetka_page.get_product_name()
        product_price = re.sub(r'\D', '', rozetka_page.get_product_price())
        product_details["price"] = int(product_price)

        # Add product to the cart and open it
        rozetka_page.click_add_to_cart_button()
        rozetka_page.wait_for_text_visibility("Товар добавлен в корзину")
        rozetka_page.open_cart()
        # rozetka_page.wait_for_text_visibility("Вместе дешевле")

        # Get product details from the cart
        product_details_in_cart = {}
        product_details_in_cart["name"] = rozetka_page.get_cart_product_name()
        product_price_in_cart = re.sub(r'\D', '', rozetka_page.get_cart_product_price())
        product_details_in_cart["price"] = int(product_price_in_cart)

        # Verify that product details from the cart match the initial product details
        assert product_details_in_cart == product_details, "Product details in the cart do not match the selected product details!"

        # Get initial quantity and price of a single product
        initial_quantity = rozetka_page.get_product_quantity()
        single_product_price = rozetka_page.get_single_product_price()
        assert initial_quantity == 1
        assert single_product_price == 33499

        # Increase product quantity by 1
        rozetka_page.increase_product_quantity_by_one()
        increased_quantity = rozetka_page.get_product_quantity()
        increased_price = rozetka_page.get_single_product_price() * rozetka_page.get_product_quantity()

        # Verify that the quantity increased by 1 and the price increased proportionally
        assert increased_quantity == initial_quantity + 1, "Product quantity did not increase by 1."
        # assert increased_price > initial_quantity * single_product_price, "Product price did not increase after adding another instance."

        # Decrease the quantity back to the initial
        rozetka_page.decrease_product_quantity_by_one()
        decreased_quantity = rozetka_page.get_product_quantity()
        decreased_price = rozetka_page.get_single_product_price() * rozetka_page.get_product_quantity()

        # Verify that the quantity decreased by 1 and the price returned to the initial value
        assert decreased_quantity == initial_quantity, "Product quantity did not decrease by 1."
        assert decreased_price == initial_quantity * single_product_price, "Product price did not return to the initial value after removing an instance."

        # Increase product quantity by three

        rozetka_page.increase_product_quantity_by_one()
        rozetka_page.increase_product_quantity_by_one()
        rozetka_page.increase_product_quantity_by_one()

        # Get the updated quantity and price
        increased_quantity_by_three = rozetka_page.get_product_quantity()
        increased_price_by_three = rozetka_page.get_single_product_price() * rozetka_page.get_product_quantity()

        # Verify that product quantity was increased by three and that total product price was increased proportionally
        assert increased_quantity_by_three == 4, "Product quantity did not increase by three."
        # assert increased_price_by_three == single_product_price * 3, "Product price did not increase proportionally."

        # Set product quantity to 7
        rozetka_page.set_product_quantity(11)

        # Get the updated quantity and price
        set_quantity = rozetka_page.get_product_quantity()
        set_price = rozetka_page.get_single_product_price() * set_quantity

        # Verify that product quantity was set to 7 and that total product price was updated accordingly
        assert set_quantity == 11, "Product quantity was not set to 7."
        assert set_price == single_product_price * 11, "Total product price was not updated correctly."

