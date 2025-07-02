"""Основные фикстуры для проекта"""

import pytest
import os
from playwright.sync_api import Page, Browser
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Настройка тестового окружения"""
    # Создание необходимых директорий
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/videos", exist_ok=True)
    os.makedirs("reports/allure-results", exist_ok=True)
    
    yield
    
    # Очистка после тестов (если необходимо)
    print("Test environment cleanup completed")

@pytest.fixture(scope="function")
def page_with_screenshot_on_failure(page: Page, request):
    """Фикстура для автоматического создания скриншотов при падении тестов"""
    yield page
    
    if request.node.rep_call.failed:
        screenshot_path = f"reports/screenshots/{request.node.name}.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")

def pytest_runtest_makereport(item, call):
    """Хук для сохранения результатов тестов"""
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item

def pytest_runtest_setup(item):
    """Хук для настройки перед запуском тестов"""
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail(f"previous test failed ({previousfailed.name})")

# Добавляем результат в объект request для использования в фикстурах
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)