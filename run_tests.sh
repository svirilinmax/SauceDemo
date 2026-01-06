#!/bin/bash

echo "========================================"
echo "   SauceDemo Automation Tests"
echo "========================================"
echo

echo "[1/3] Запуск тестов..."
pytest tests/ --alluredir=allure-results -v

if [ $? -ne 0 ]; then
    echo
    echo "[ОШИБКА] Тесты не прошли. Пропускаем генерацию отчета."
    exit 1
fi

echo
echo "[2/3] Запуск Allure сервера..."
echo "Отчет будет открыт в браузере автоматически..."
echo
echo "Если браузер не открылся:"
echo "1. В консоли появится ссылка вида http://127.0.0.1:59480 - откройте ее"
echo "2. Или для постоянного отчета выполните:"
echo "   allure generate allure-results -o allure-report --clean"
echo "   allure open allure-report"
echo

# Запускаем Allure сервер
allure serve allure-results

echo
echo "========================================"
echo "   Тесты выполнены успешно!"
echo "========================================"
