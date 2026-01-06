import allure
import pytest

from conftest import retry_on_failure
from utils.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)


@allure.epic("Авторизация пользователя")
@allure.feature("Функционал входа в систему")
@pytest.mark.login
class TestLogin:
    @allure.story("Успешная авторизация")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Тест 1: Успешный вход с валидными данными")
    @pytest.mark.smoke
    def test_successful_login(self, login_page):
        """Тест успешного входа"""

        logger.info("Начинаем тест успешного входа")

        with allure.step("Проверить элементы формы логина"):
            assert (
                login_page.check_login_form_elements()
            ), "Не все элементы формы отображаются"

        with allure.step("Выполнить вход с валидными данными"):
            inventory_page = login_page.login(Config.VALID_USER, Config.PASSWORD)

        with allure.step("Проверить успешный вход"):
            assert (
                inventory_page is not None
            ), "Не произошел переход на страницу инвентаря"
            assert inventory_page.is_page_loaded(), "Страница инвентаря не загрузилась"
            assert (
                inventory_page.get_current_url() == Config.INVENTORY_URL
            ), "Некорректный URL"
            assert (
                "Products" in inventory_page.get_page_title()
            ), "Некорректный заголовок страницы"
            assert (
                inventory_page.is_shopping_cart_visible()
            ), "Корзина покупок не отображается"

    @allure.story("Неудачная авторизация")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест 2: Вход с неверным паролем")
    @pytest.mark.regression
    def test_login_with_invalid_password(self, login_page):
        """Тест входа с неверным паролем"""

        logger.info("Начинаем тест входа с неверным паролем")

        with allure.step("Выполнить вход с неверным паролем"):
            login_page.login_without_redirect(
                Config.VALID_USER, Config.INVALID_PASSWORD
            )

        with allure.step("Проверить сообщение об ошибке"):
            error_message = login_page.get_error_message()
            current_url = login_page.get_current_url()

            assert (
                "Username and password do not match" in error_message
            ), f"Неверное сообщение об ошибке: {error_message}"
            assert current_url == Config.BASE_URL, (
                f"Произошел переход для заблокированного пользователя. "
                f"Ожидался {Config.BASE_URL}, получен {current_url}"
            )

    @allure.story("Блокировка пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест 3: Вход заблокированного пользователя")
    @pytest.mark.regression
    def test_locked_user_login(self, login_page):
        """Тест входа заблокированного пользователя"""

        logger.info("Начинаем тест входа заблокированного пользователя")

        with allure.step("Выполнить вход заблокированным пользователем"):
            login_page.login_without_redirect(Config.LOCKED_USER, Config.PASSWORD)

        with allure.step("Проверить сообщение об ошибке блокировки"):
            error_message = login_page.get_error_message()
            current_url = login_page.get_current_url()

            assert (
                "Sorry, this user has been locked out" in error_message
            ), f"Неверное сообщение об ошибке блокировки: {error_message}"
            assert current_url == Config.BASE_URL, (
                f"Произошел переход при неверном пароле. "
                f"Ожидался {Config.BASE_URL}, получен {current_url}"
            )

    @allure.story("Валидация полей")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Тест 4: Вход с пустыми полями")
    @pytest.mark.regression
    def test_login_with_empty_fields(self, login_page):
        """Тест входа с пустыми полями"""

        logger.info("Начинаем тест входа с пустыми полями")

        with allure.step("Нажать кнопку Login без заполнения полей"):
            login_page.click(login_page.LOGIN_BUTTON)

        with allure.step("Проверить сообщение об ошибке"):
            error_message = login_page.get_error_message()
            current_url = login_page.get_current_url()

            assert (
                "Username is required" in error_message
            ), f"Неверное сообщение об ошибке для пустых полей: {error_message}"
            assert current_url == Config.BASE_URL, (
                f"Произошел переход с пустыми полями. "
                f"Ожидался {Config.BASE_URL}, получен {current_url}"
            )

    @allure.story("Производительность")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Тест 5: Вход пользователем performance_glitch_user")
    @pytest.mark.timeout
    @pytest.mark.regression
    @retry_on_failure(max_attempts=3)
    def test_performance_glitch_user_login(self, login_page):
        """Тест входа пользователем с задержками"""

        logger.info("Начинаем тест входа пользователя с задержками")

        with allure.step("Выполнить вход пользователем performance_glitch_user"):
            inventory_page = login_page.login(Config.PERFORMANCE_USER, Config.PASSWORD)

        with allure.step("Проверить успешный вход несмотря на задержки"):
            assert (
                inventory_page is not None
            ), "Не произошел переход на страницу инвентаря"
            assert inventory_page.is_page_loaded(), "Страница инвентаря не загрузилась"
            assert (
                inventory_page.get_current_url() == Config.INVENTORY_URL
            ), "Некорректный URL"

        with allure.step("Проверить функциональность страницы"):
            assert (
                "Products" in inventory_page.get_page_title()
            ), "Некорректный заголовок"
            assert (
                inventory_page.is_shopping_cart_visible()
            ), "Корзина покупок не отображается"
