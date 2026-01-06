import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import Config


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.TIMEOUT)
        self.base_url = Config.BASE_URL

    def open(self):
        """Открыть страницу"""

        with allure.step(f"Открыть страницу {self.base_url}"):
            self.driver.get(self.base_url)

    def find_element(self, locator):
        """Найти элемент с ожиданием"""

        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Найти все элементы с ожиданием"""

        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        """Кликнуть по элементу"""

        with allure.step(f"Кликнуть по элементу {locator}"):
            element = self.find_element(locator)
            element.click()

    def send_keys(self, locator, text):
        """Ввести текст в поле"""

        with allure.step(f"Ввести текст '{text}' в поле {locator}"):
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)

    def get_text(self, locator):
        """Получить текст элемента"""

        return self.find_element(locator).text

    def is_element_visible(self, locator, timeout=None):
        """Проверить видимость элемента"""

        wait = WebDriverWait(self.driver, timeout or Config.TIMEOUT)
        try:
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_current_url(self):
        """Получить текущий URL"""

        return self.driver.current_url
