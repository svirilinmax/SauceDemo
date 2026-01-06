import allure
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utils.config import Config


class InventoryPage(BasePage):
    # Локаторы
    TITLE = (By.CLASS_NAME, "title")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    SHOPPING_CART = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        super().__init__(driver)
        try:
            self.wait.until(lambda d: d.current_url == Config.INVENTORY_URL)
        except TimeoutException:
            raise Exception(
                f"Не удалось загрузить страницу инвентаря. "
                f"Текущий URL: {driver.current_url}"
            )

    @allure.step("Проверить, что страница инвентаря загружена")
    def is_page_loaded(self):
        """Проверить загрузку страницы инвентаря"""

        return (
            self.is_element_visible(self.TITLE)
            and self.is_element_visible(self.INVENTORY_CONTAINER)
            and Config.INVENTORY_URL in self.get_current_url()
        )

    @allure.step("Получить заголовок страницы")
    def get_page_title(self):
        """Получить текст заголовка"""

        return self.get_text(self.TITLE)

    @allure.step("Выполнить выход")
    def logout(self):
        """Выйти из системы"""

        self.click(self.MENU_BUTTON)
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK)).click()

    @allure.step("Проверить наличие корзины покупок")
    def is_shopping_cart_visible(self):
        """Проверить видимость корзины"""

        return self.is_element_visible(self.SHOPPING_CART)
