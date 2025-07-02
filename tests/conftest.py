"""Локальные фикстуры для тестов"""

import pytest
import allure
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.test_data import Users, Products

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Фикстура для страницы авторизации"""
    return LoginPage(page)

@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    """Фикстура для страницы каталога"""
    return InventoryPage(page)

@pytest.fixture
def authenticated_standard_user(page: Page) -> Page:
    """Фикстура для авторизованного стандартного пользователя"""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(
        Users.STANDARD_USER["username"], 
        Users.STANDARD_USER["password"]
    )
    
    # Проверяем успешную авторизацию
    inventory_page = InventoryPage(page)
    assert inventory_page.is_loaded(), "Не удалось авторизоваться"
    
    return page

@pytest.fixture
def user_with_items_in_cart(authenticated_standard_user: Page) -> Page:
    """Фикстура для пользователя с товарами в корзине"""
    inventory_page = InventoryPage(authenticated_standard_user)
    
    # Добавляем товары в корзину
    inventory_page.add_product_to_cart_by_id(Products.BACKPACK["id"])
    inventory_page.add_product_to_cart_by_id(Products.BIKE_LIGHT["id"])
    
    # Проверяем, что товары добавлены
    assert inventory_page.get_cart_items_count() == 2, "Товары не добавлены в корзину"
    
    return authenticated_standard_user

@pytest.fixture(autouse=True)
def test_setup_teardown(page: Page, request):
    """Фикстура для настройки и очистки после каждого теста"""
    # Настройка перед тестом
    allure.attach(
        body=f"Запуск теста: {request.node.name}",
        name="Начало теста",
        attachment_type=allure.attachment_type.TEXT
    )
    
    yield
    
    # Очистка после теста
    try:
        # Создаем скриншот после каждого теста
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name=f"Screenshot_after_{request.node.name}",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        print(f"Не удалось сделать скриншот: {e}")