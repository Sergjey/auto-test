"""E2E тесты процесса покупки товаров"""

import pytest
import allure
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config.test_data import Users, Products, CheckoutData

@allure.epic("SauceDemo E2E Tests")
@allure.feature("Shopping Flow")
class TestShoppingFlow:
    """Тесты процесса покупки товаров"""
    
    @allure.story("Успешная покупка одного товара")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_successful_single_item_purchase(self, page: Page):
        """E2E тест полного процесса покупки одного товара"""
        
        # Arrange
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)
        checkout_page = CheckoutPage(page)
        
        with allure.step("Авторизация пользователя"):
            login_page.open()
            login_page.login(Users.STANDARD_USER["username"], Users.STANDARD_USER["password"])
            assert inventory_page.is_loaded(), "Авторизация не прошла"
            
        with allure.step("Добавление товара в корзину"):
            product_name = Products.BACKPACK["name"]
            inventory_page.add_product_to_cart_by_id(Products.BACKPACK["id"])
            assert inventory_page.get_cart_items_count() == 1, "Товар не добавлен в корзину"
            
        with allure.step("Переход в корзину"):
            inventory_page.go_to_cart()
            expect(page).to_have_url("https://www.saucedemo.com/cart.html")
            assert cart_page.is_loaded(), "Страница корзины не загружена"
            
        with allure.step("Проверка товара в корзине"):
            assert cart_page.is_product_in_cart(product_name), f"Товар {product_name} не найден в корзине"
            assert cart_page.get_total_items_count() == 1, "Неверное количество товаров в корзине"
            
        with allure.step("Начало оформления заказа"):
            cart_page.proceed_to_checkout()
            expect(page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")
            assert checkout_page.is_checkout_info_loaded(), "Страница информации о покупателе не загружена"
            
        with allure.step("Заполнение информации о покупателе"):
            checkout_page.fill_customer_info(
                CheckoutData.VALID_USER_INFO["first_name"],
                CheckoutData.VALID_USER_INFO["last_name"],
                CheckoutData.VALID_USER_INFO["postal_code"]
            )
            checkout_page.continue_checkout()
            
        with allure.step("Проверка страницы обзора заказа"):
            expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")
            assert checkout_page.is_checkout_overview_loaded(), "Страница обзора заказа не загружена"
            assert checkout_page.is_product_in_overview(product_name), f"Товар {product_name} не найден в обзоре"
            
        with allure.step("Проверка корректности сумм"):
            item_total = checkout_page.get_item_total()
            tax_amount = checkout_page.get_tax_amount()
            total_amount = checkout_page.get_total_amount()
            
            assert item_total, "Сумма товаров не отображается"
            assert tax_amount, "Сумма налога не отображается"
            assert total_amount, "Общая сумма не отображается"
            
        with allure.step("Завершение заказа"):
            checkout_page.finish_order()
            expect(page).to_have_url("https://www.saucedemo.com/checkout-complete.html")
            assert checkout_page.is_order_complete(), "Страница завершения заказа не загружена"
            
        with allure.step("Проверка успешного завершения заказа"):
            complete_header = checkout_page.get_complete_header()
            complete_message = checkout_page.get_complete_message()
            
            assert "Thank you for your order!" in complete_header, f"Неверный заголовок: {complete_header}"
            assert complete_message, "Сообщение о завершении заказа не отображается"
    
    @allure.story("Покупка нескольких товаров")
    @allure.severity(allure.severity_level.NORMAL)  # Changed from HIGH to NORMAL
    @pytest.mark.regression
    def test_multiple_items_purchase(self, page: Page):
        """E2E тест покупки нескольких товаров"""
        
        # Arrange
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)
        checkout_page = CheckoutPage(page)
        
        products_to_buy = [
            Products.BACKPACK,
            Products.BIKE_LIGHT,
            Products.BOLT_TSHIRT
        ]
        
        with allure.step("Авторизация пользователя"):
            login_page.open()
            login_page.login(Users.STANDARD_USER["username"], Users.STANDARD_USER["password"])
            assert inventory_page.is_loaded(), "Авторизация не прошла"
            
        with allure.step("Добавление нескольких товаров в корзину"):
            for product in products_to_buy:
                inventory_page.add_product_to_cart_by_id(product["id"])
                
            expected_count = len(products_to_buy)
            actual_count = inventory_page.get_cart_items_count()
            assert actual_count == expected_count, f"Ожидалось {expected_count} товаров, получено {actual_count}"
            
        with allure.step("Переход в корзину и проверка всех товаров"):
            inventory_page.go_to_cart()
            assert cart_page.is_loaded(), "Страница корзины не загружена"
            
            for product in products_to_buy:
                assert cart_page.is_product_in_cart(product["name"]), f"Товар {product['name']} не найден в корзине"
                
        with allure.step("Оформление заказа с несколькими товарами"):
            cart_page.proceed_to_checkout()
            
            # Заполняем информацию
            checkout_page.fill_customer_info(
                CheckoutData.VALID_USER_INFO["first_name"],
                CheckoutData.VALID_USER_INFO["last_name"],
                CheckoutData.VALID_USER_INFO["postal_code"]
            )
            checkout_page.continue_checkout()
            
            # Проверяем все товары в обзоре
            for product in products_to_buy:
                assert checkout_page.is_product_in_overview(product["name"]), f"Товар {product['name']} не найден в обзоре"
                
        with allure.step("Завершение заказа"):
            checkout_page.finish_order()
            assert checkout_page.is_order_complete(), "Заказ не завершен успешно"
    
    @allure.story("Сортировка товаров перед покупкой")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_shopping_with_sorting(self, authenticated_standard_user: Page):
        """E2E тест покупки с предварительной сортировкой товаров"""
        
        # Arrange
        inventory_page = InventoryPage(authenticated_standard_user)
        cart_page = CartPage(authenticated_standard_user)
        
        with allure.step("Сортировка товаров по цене (от низкой к высокой)"):
            inventory_page.sort_products(inventory_page.SORT_PRICE_LOW_HIGH)
            
        with allure.step("Получение списка товаров после сортировки"):
            product_names = inventory_page.get_product_names()
            assert len(product_names) > 0, "Товары не отображаются после сортировки"
            
        with allure.step("Добавление первого товара в корзину"):
            if product_names:
                inventory_page.add_product_to_cart(product_names[0])
                assert inventory_page.get_cart_items_count() == 1, "Товар не добавлен в корзину"