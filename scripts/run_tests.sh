#!/bin/bash

# Установка зависимостей и запуск E2E тестов

echo "Installing dependencies..."
pip install -r requirements.txt
playwright install

echo "Running E2E tests..."
pytest tests/ \
    --alluredir=reports/allure-results \
    --browser=chromium \
    --headed=false \
    --screenshot=only-on-failure \
    --video=retain-on-failure \
    -v

echo "Generating Allure report..."
allure generate reports/allure-results -o reports/allure-report --clean

echo "Tests completed. Report available at: reports/allure-report/index.html"