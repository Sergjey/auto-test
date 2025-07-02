#!/bin/bash

echo "Running smoke tests..."
pytest tests/ -m smoke \
    --alluredir=reports/allure-results \
    --browser=chromium \
    --headed=false \
    -v

allure generate reports/allure-results -o reports/allure-report --clean