#!/bin/bash

echo "========================================"
echo "   Очистка проекта SauceDemo"
echo "========================================"
echo

echo "[1/3] Удаление кэша pytest..."
rm -rf .pytest_cache

echo "[2/3] Удаление __pycache__..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

echo "[3/3] Удаление старых отчетов..."
rm -rf allure-report
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
find . -name "*.pyd" -delete

echo
echo "========================================"
echo "   Проект очищен!"
echo "========================================"
