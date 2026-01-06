@echo off
echo ========================================
echo   Запуск тестов SauceDemo
echo ========================================
echo.

echo [1/3] Запуск тестов...
pytest tests/ --alluredir=allure-results -v

echo.
echo [2/3] Запуск Allure сервера...
echo Отчет будет открыт в браузере автоматически...
echo.
echo Если браузер не открылся:
echo 1. В консоли появится ссылка вида http://127.0.0.1:59480 - откройте ее
echo 2. Или запустите: allure generate allure-results -o allure-report --clean
echo 3. Затем: allure open allure-report
echo.

REM Запускаем Allure сервер
allure serve allure-results

pause
