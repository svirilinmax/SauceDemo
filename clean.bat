@echo off
echo ========================================
echo   Очистка проекта SauceDemo
echo ========================================
echo.

echo [1/3] Удаление кэша pytest...
if exist .pytest_cache rmdir /s /q .pytest_cache

echo [2/3] Удаление __pycache__...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"

echo [3/3] Удаление старых отчетов...
if exist allure-report rmdir /s /q allure-report
REM НЕ удаляем allure-results здесь!

echo.
echo ========================================
echo   Проект очищен!
echo ========================================
echo.
pause
