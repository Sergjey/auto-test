"""Тесты корзины покупок"""

import pytest
import allure
from playwright.sync_api import Page, expect
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from config.test_data import Products

@allure.epic("SauceDemo E2E Tests")
@allure.feature("Shopping Cart")
class TestCartFlow:
    """Тесты функционала корзины"""
    
    @allure.story("Добавление товаров в корзину")
    @allure.severity("critical")
    def test_add_products_to_cart(self, authenticated_standard_user: Page):
        """Тест добавления товаров в корзину"""
        inventory_page = InventoryPage(authenticated_standard_user)
        cart_page = CartPage(authenticated_standard_user)
        
        # Добавляем товары
        inventory_page.add_product_to_cart_by_id(Products.BACKPACK["id"])
        inventory_page.add_product_to_cart_by_id(Products.BIKE_LIGHT["id"])
        
        # Проверяем количество
        assert inventory_page.get_cart_items_count() == 2
        
        # Проверяем корзину
        inventory_page.go_to_cart()
        assert cart_page.is_product_in_cart(Products.BACKPACK["name"])
        assert cart_page.is_product_in_cart(Products.BIKE_LIGHT["name"])
        
    @allure.story("Удаление товаров из корзины")
    @allure.severity("normal")
    def test_remove_products_from_cart(self, user_with_items_in_cart: Page):
        """Тест удаления товаров из корзины"""
        cart_page = CartPage(user_with_items_in_cart)
        
        # Удаляем товар
        cart_page.remove_product_from_cart(Products.BACKPACK["name"])
        
        # Проверяем что товар удален
        assert not cart_page.is_product_in_cart(Products.BACKPACK["name"])
        assert cart_page.get_total_items_count() == 1