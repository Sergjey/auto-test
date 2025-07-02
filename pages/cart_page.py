"""Страница корзины"""

import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import List

class CartPage(BasePage):
    """Страница корзины покупок"""
    
    # Локаторы элементов
    CART_CONTAINER = ".cart_contents_container"
    CART_LIST = ".cart_list"
    CART_ITEM = ".cart_item"
    CART_ITEM_NAME = ".inventory_item_name"
    CART_ITEM_PRICE = ".inventory_item_price"
    CART_ITEM_QUANTITY = ".cart_quantity"
    REMOVE_BUTTON = "button[id*='remove']"
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    CART_BADGE = ".shopping_cart_badge"
    
    def __init__(self, page: Page):
        super().__init__(page)
        
    @allure.step("Проверить загрузку страницы корзины")
    def is_loaded(self) -> bool:
        """Проверить, что страница корзины загружена"""
        return self.is_element_visible(self.CART_CONTAINER)
        
    @allure.step("Получить список товаров в корзине")
    def get_cart_items(self) -> List[str]:
        """Получить список названий товаров в корзине"""
        if not self.is_element_visible(self.CART_LIST):
            return []
            
        item_elements = self.page.query_selector_all(self.CART_ITEM_NAME)
        return [element.inner_text() for element in item_elements]
        
    @allure.step("Проверить наличие товара '{product_name}' в корзине")
    def is_product_in_cart(self, product_name: str) -> bool:
        """Проверить наличие товара в корзине"""
        cart_items = self.get_cart_items()
        return product_name in cart_items
        
    @allure.step("Получить количество товара '{product_name}' в корзине")
    def get_product_quantity(self, product_name: str) -> int:
        """Получить количество конкретного товара в корзине"""
        product_locator = f".cart_item:has(.inventory_item_name:text('{product_name}'))"
        quantity_locator = f"{product_locator} .cart_quantity"
        
        if self.is_element_visible(quantity_locator):
            quantity_text = self.get_element_text(quantity_locator)
            return int(quantity_text) if quantity_text.isdigit() else 0
        return 0
        
    @allure.step("Получить цену товара '{product_name}' в корзине")
    def get_product_price_in_cart(self, product_name: str) -> str:
        """Получить цену товара в корзине"""
        product_locator = f".cart_item:has(.inventory_item_name:text('{product_name}'))"
        price_locator = f"{product_locator} .inventory_item_price"
        return self.get_element_text(price_locator)
        
    @allure.step("Удалить товар '{product_name}' из корзины")
    def remove_product_from_cart(self, product_name: str) -> None:
        """Удалить товар из корзины"""
        with allure.step(f"Удаление товара '{product_name}' из корзины"):
            # Проверить, что мы на странице корзины
            assert self.is_loaded(), "Не удалось загрузить страницу корзины"
            
            # Более специфичный селектор для надежного нахождения кнопки удаления
            remove_button = f"//div[contains(@class, 'cart_item')]//div[text()='{product_name}']/ancestor::div[contains(@class, 'cart_item')]//button[contains(@id, 'remove')]"
            
            try:
                # Увеличить таймаут и использовать xpath для более надежного выбора
                self.page.wait_for_selector(remove_button, timeout=10000, state="visible")
                self.page.locator(remove_button).click()
                
                # Ждать, пока товар будет удален
                self.page.wait_for_selector(
                    f"//div[contains(@class, 'cart_item')]//div[text()='{product_name}']",
                    state="detached",
                    timeout=5000
                )
            except Exception as e:
                allure.attach(
                    self.page.screenshot(),
                    name="remove_product_failure",
                    attachment_type=allure.attachment_type.PNG
                )
                raise Exception(f"Не удалось удалить товар '{product_name}' из корзины: {str(e)}")

    @allure.step("Продолжить покупки")
    def continue_shopping(self):
        """Нажать кнопку 'Продолжить покупки'"""
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)
        
    @allure.step("Перейти к оформлению заказа")
    def proceed_to_checkout(self):
        """Нажать кнопку 'Checkout'"""
        self.click_element(self.CHECKOUT_BUTTON)
        
    @allure.step("Получить общее количество товаров в корзине")
    def get_total_items_count(self) -> int:
        """Получить общее количество товаров в корзине"""
        cart_items = self.page.query_selector_all(self.CART_ITEM)
        return len(cart_items)
        
    @allure.step("Проверить пустоту корзины")
    def is_cart_empty(self) -> bool:
        """Проверить, пуста ли корзина"""
        return self.get_total_items_count() == 0
        
    @allure.step("Очистить корзину")
    def clear_cart(self):
        """Удалить все товары из корзины"""
        while not self.is_cart_empty():
            remove_buttons = self.page.query_selector_all(self.REMOVE_BUTTON)
            if remove_buttons:
                remove_buttons[0].click()
                self.wait_for_page_load()
            else:
                break