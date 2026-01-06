import os


class Config:
    BASE_URL = "https://www.saucedemo.com/"
    INVENTORY_URL = "https://www.saucedemo.com/inventory.html"

    # Данные пользователей
    VALID_USER = "standard_user"
    LOCKED_USER = "locked_out_user"
    PERFORMANCE_USER = "performance_glitch_user"
    PASSWORD = "secret_sauce"
    INVALID_PASSWORD = "wrong_password"

    # Таймауты
    TIMEOUT = 10
    PERFORMANCE_TIMEOUT = int(os.getenv("PERFORMANCE_TIMEOUT", 30))
