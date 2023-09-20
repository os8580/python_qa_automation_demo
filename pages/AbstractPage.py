from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AbstractPage:

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def load_page(self):
        self.driver.get(self.url)

    def is_page_loaded(self):
        return WebDriverWait(self.driver, 45).until(EC.url_to_be(self.url))

    def is_text_present(self, text):
        body_element = self.driver.find_element_by_tag_name("body")
        return text in body_element.text