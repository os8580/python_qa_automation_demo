from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.AbstractPage import AbstractPage


class GooglePage(AbstractPage):
    def __init__(self, driver):
        super().__init__(driver, "http://google.com")


    def accept_cookies_if_present(self):
        try:
            buttons = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "button")))

            if len(buttons) == 5:
                buttons[3].click()
        except TimeoutException:
            # Если кнопки для файлов cookie не найдены, продолжите выполнение теста
            pass

    def set_search_value(self, value):
        search_field = self.driver.find_element(By.NAME, 'q')
        search_field.send_keys(value)

    def perform_search(self):
        search_field = self.driver.find_element(By.NAME, 'q')
        search_field.send_keys(Keys.RETURN)

    def get_search_results(self):
        elements = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//h3/..")))
        return [e for e in elements if e.is_displayed()]