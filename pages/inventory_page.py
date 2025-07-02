"""Страница каталога товаров"""

import allure
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from typing import List

class InventoryPage(BasePage):
    """Страница каталога товаров"""
    
    # Локаторы элементов
    INVENTORY_CONTAINER = ".inventory_container"
    INVENTORY_LIST = ".inventory_list"
    INVENTORY_ITEM = ".inventory_item"
    INVENTORY_ITEM_NAME = ".inventory_item_name"
    INVENTORY_ITEM_PRICE = ".inventory_item_price"
    INVENTORY_ITEM_DESC = ".inventory_item_desc"
    ADD_TO_CART_BUTTON = "button[id*='add-to-cart']"
    REMOVE_BUTTON = "button[id*='remove']"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    SORT_DROPDOWN = ".product_sort_container"
    BURGER_MENU = "#react-burger-menu-btn"
    APP_LOGO = ".app_logo"
    
    # Опции сортировки
    SORT_NAME_A_Z = "az"
    SORT_NAME_Z_A = "za"
    SORT_PRICE_LOW_HIGH = "lohi"
    SORT_PRICE_HIGH_LOW = "hilo"
    
    def __init__(self, page: Page):
        super().__init__(page)
        
    @allure.step("Проверить загрузку страницы каталога")
    def is_loaded(self) -> bool:
        """Проверить, что страница каталога загружена"""
        return (self.is_element_visible(self.INVENTORY_CONTAINER) and 
                self.is_element_visible(self.APP_LOGO))
        
    @allure.step("Получить список названий всех товаров")
    def get_product_names(self) -> List[str]:
        """Получить список всех названий товаров на странице"""
        product_elements = self.page.query_selector_all(self.INVENTORY_ITEM_NAME)
        return [element.inner_text() for element in product_elements]
        
    @allure.step("Получить список цен всех товаров")
    def get_product_prices(self) -> List[str]:
        """Получить список всех цен товаров на странице"""
        price_elements = self.page.query_selector_all(self.INVENTORY_ITEM_PRICE)
        return [element.inner_text() for element in price_elements]
        
    @allure.step("Добавить товар '{product_name}' в корзину")
    def add_product_to_cart(self, product_name: str):
        """Добавить товар в корзину по названию"""
        # Находим товар по названию и кликаем кнопку добавления
        product_locator = f".inventory_item:has(.inventory_item_name:text('{product_name}'))"
        add_button = f"{product_locator} button[id*='add-to-cart']"
        
        self.wait_for_element(add_button)
        self.click_element(add_button)
        
    @allure.step("Добавить товар в корзину по ID: {product_id}")
    def add_product_to_cart_by_id(self, product_id: str):
        """Добавить товар в корзину по ID"""
        button_selector = f"[data-test='add-to-cart-{product_id}']"
        self.click_element(button_selector)
        
    @allure.step("Удалить товар '{product_name}' из корзины")
    def remove_product_from_cart(self, product_name: str):
        """Удалить товар из корзины по названию"""
        product_locator = f".inventory_item:has(.inventory_item_name:text('{product_name}'))"
        remove_button = f"{product_locator} button[id*='remove']"
        
        self.wait_for_element(remove_button)
        self.click_element(remove_button)
        
    @allure.step("Получить количество товаров в корзине")
    def get_cart_items_count(self) -> int:
        """Получить количество товаров в корзине из badge"""
        if self.is_element_visible(self.SHOPPING_CART_BADGE):
            count_text = self.get_element_text(self.SHOPPING_CART_BADGE)
            return int(count_text) if count_text.isdigit() else 0
        return 0
        
    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        """Перейти в корзину"""
        self.click_element(self.SHOPPING_CART_LINK)
        
    @allure.step("Сортировать товары по: {sort_option}")
    def sort_products(self, sort_option: str):
        """Сортировать товары по выбранному критерию"""
        self.page.select_option(self.SORT_DROPDOWN, sort_option)
        self.wait_for_page_load()
        
    @allure.step("Получить цену товара '{product_name}'")
    def get_product_price(self, product_name: str) -> str:
        """Получить цену конкретного товара"""
        product_locator = f".inventory_item:has(.inventory_item_name:text('{product_name}'))"
        price_locator = f"{product_locator} .inventory_item_price"
        return self.get_element_text(price_locator)
        
    @allure.step("Проверить наличие товара '{product_name}' на странице")
    def is_product_displayed(self, product_name: str) -> bool:
        """Проверить отображение товара на странице"""
        product_locator = f".inventory_item_name:text('{product_name}')"
        return self.is_element_visible(product_locator)
        
    @allure.step("Кликнуть по названию товара '{product_name}'")
    def click_product_name(self, product_name: str):
        """Кликнуть по названию товара для перехода на детальную страницу"""
        product_name_locator = f".inventory_item_name:text('{product_name}')"
        self.click_element(product_name_locator)