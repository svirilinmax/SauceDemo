import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage
from utils.config import Config


class LoginPage(BasePage):
    # Локаторы
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message-container")
    ERROR_BUTTON = (By.CLASS_NAME, "error-button")

    def __init__(self, driver):
        super().__init__(driver)
        self.open()

    @allure.step("Войти с username: {username} и password: {password}")
    def login(self, username, password):
        """Выполнить вход"""

        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

        if username == Config.PERFORMANCE_USER:
            WebDriverWait(self.driver, Config.PERFORMANCE_TIMEOUT).until(
                lambda d: d.current_url == Config.INVENTORY_URL
            )

        return InventoryPage(self.driver) if self.is_login_successful() else None

    def is_login_successful(self):
        """Проверить успешность входа по URL"""

        return Config.INVENTORY_URL in self.get_current_url()

    def get_error_message(self):
        """Получить текст сообщения об ошибке"""

        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def login_without_redirect(self, username, password):
        """Войти без перехода на следующую страницу"""

        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    @allure.step("Проверить отображение элементов формы логина")
    def check_login_form_elements(self):
        """Проверить наличие всех элементов формы логина"""

        elements = [
            ("Поле username", self.USERNAME_INPUT),
            ("Поле password", self.PASSWORD_INPUT),
            ("Кнопка Login", self.LOGIN_BUTTON),
        ]

        results = {}
        for name, locator in elements:
            is_visible = self.is_element_visible(locator)
            results[name] = is_visible
            allure.attach(
                f"{name}: {'виден' if is_visible else 'не виден'}",
                name="Видимость элементов",
            )

        return all(results.values())
