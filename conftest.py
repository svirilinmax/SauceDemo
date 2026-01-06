import os

import allure
import pytest
from tenacity import retry, stop_after_attempt, wait_fixed


def pytest_addoption(parser):
    """Регистрация опций командной строки"""

    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox", "edge"],
        help="Браузер для тестов: chrome, firefox, edge",
    )


@pytest.fixture(scope="function")
def driver(request):
    """Фикстура для создания экземпляра драйвера"""

    browser = request.config.getoption("--browser")
    headless = os.getenv("HEADLESS", "true").lower() == "true"

    if browser == "firefox":
        from selenium.webdriver import Firefox
        from selenium.webdriver.firefox.options import Options

        options = Options()
        if headless:
            options.add_argument("--headless")
        driver = Firefox(options=options)

    elif browser == "edge":
        from selenium.webdriver import Edge
        from selenium.webdriver.edge.options import Options

        options = Options()
        if headless:
            options.add_argument("--headless")
        driver = Edge(options=options)

    else:  # chrome по умолчанию
        from selenium.webdriver import Chrome
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()

        if os.getenv("HEADLESS", "true").lower() == "true":
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        driver = Chrome(options=chrome_options)

    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def login_page(driver):
    """Фикстура для создания страницы логина"""

    from pages.login_page import LoginPage

    return LoginPage(driver)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для скриншотов при падении тестов"""

    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs["driver"]
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")


def retry_on_failure(max_attempts=3, wait_time=2):
    """Декоратор для повторного выполнения функции при возникновении исключения."""

    return retry(
        stop=stop_after_attempt(max_attempts), wait=wait_fixed(wait_time), reraise=True
    )
