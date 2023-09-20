from pages.GooglePage import GooglePage
from pages.RozetkaPage import RozetkaPage
from pages.Pages import Pages


class PageFactory:
    def __init__(self, driver):
        self.driver = driver

    def get(self, page):
        if page == Pages.GOOGLE:
            return GooglePage(self.driver)
        elif page == Pages.ROZETKA:
            return RozetkaPage(self.driver)
        else:
            raise Exception("Unsupported page requested")

    def tear_down(self):
        self.driver.quit()
