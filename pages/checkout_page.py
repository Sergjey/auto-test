"""Страницы процесса оформления заказа"""

import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import List

class CheckoutPage(BasePage):
    """Страницы оформления заказа"""
    
    # Локаторы для первого шага (информация о покупателе)
    CHECKOUT_INFO_CONTAINER = ".checkout_info_container"
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    CANCEL_BUTTON = "[data-test='cancel']"
    
    # Локаторы для второго шага (обзор заказа)
    CHECKOUT_SUMMARY_CONTAINER = ".checkout_summary_container"
    CART_LIST = ".cart_list"
    CART_ITEM = ".cart_item"
    CART_ITEM_NAME = ".inventory_item_name"
    CART_ITEM_PRICE = ".inventory_item_price"
    ITEM_TOTAL = ".summary_subtotal_label"
    TAX_LABEL = ".summary_tax_label"
    TOTAL_LABEL = ".summary_total_label"
    FINISH_BUTTON = "[data-test='finish']"
    
    # Локаторы для страницы завершения
    CHECKOUT_COMPLETE_CONTAINER = ".checkout_complete_container"
    COMPLETE_HEADER = ".complete-header"
    COMPLETE_TEXT = ".complete-text"
    BACK_HOME_BUTTON = "[data-test='back-to-products']"
    
    # Сообщения об ошибках
    ERROR_MESSAGE = "[data-test='error']"
    
    def __init__(self, page: Page):
        super().__init__(page)
        
    # Методы для первого шага оформления заказа
    @allure.step("Проверить загрузку страницы информации о покупателе")
    def is_checkout_info_loaded(self) -> bool:
        """Проверить загрузку первого шага оформления заказа"""
        return self.is_element_visible(self.CHECKOUT_INFO_CONTAINER)
        
    @allure.step("Заполнить имя: {first_name}")
    def fill_first_name(self, first_name: str):
        """Заполнить поле 'Имя'"""
        self.fill_field(self.FIRST_NAME_INPUT, first_name)
        
    @allure.step("Заполнить фамилию: {last_name}")
    def fill_last_name(self, last_name: str):
        """Заполнить поле 'Фамилия'"""
        self.fill_field(self.LAST_NAME_INPUT, last_name)
        
    @allure.step("Заполнить почтовый индекс: {postal_code}")
    def fill_postal_code(self, postal_code: str):
        """Заполнить поле 'Почтовый индекс'"""
        self.fill_field(self.POSTAL_CODE_INPUT, postal_code)
        
    @allure.step("Заполнить информацию о покупателе")
    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str):
        """Заполнить всю информацию о покупателе"""
        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_postal_code(postal_code)
        
    @allure.step("Продолжить оформление заказа")
    def continue_checkout(self):
        """Нажать кнопку 'Continue'"""
        self.click_element(self.CONTINUE_BUTTON)
        
    @allure.step("Отменить оформление заказа")
    def cancel_checkout(self):
        """Нажать кнопку 'Cancel'"""
        self.click_element(self.CANCEL_BUTTON)
        
    # Методы для второго шага (обзор заказа)
    @allure.step("Проверить загрузку страницы обзора заказа")
    def is_checkout_overview_loaded(self) -> bool:
        """Проверить загрузку второго шага оформления заказа"""
        return self.is_element_visible(self.CHECKOUT_SUMMARY_CONTAINER)
        
    @allure.step("Получить список товаров в обзоре заказа")
    def get_overview_items(self) -> List[str]:
        """Получить список товаров на странице обзора"""
        item_elements = self.page.query_selector_all(self.CART_ITEM_NAME)
        return [element.inner_text() for element in item_elements]
        
    @allure.step("Проверить наличие товара '{product_name}' в обзоре")
    def is_product_in_overview(self, product_name: str) -> bool:
        """Проверить наличие товара в обзоре заказа"""
        overview_items = self.get_overview_items()
        return product_name in overview_items
        
    @allure.step("Получить сумму товаров")
    def get_item_total(self) -> str:
        """Получить сумму всех товаров"""
        return self.get_element_text(self.ITEM_TOTAL)
        
    @allure.step("Получить сумму налога")
    def get_tax_amount(self) -> str:
        """Получить сумму налога"""
        return self.get_element_text(self.TAX_LABEL)
        
    @allure.step("Получить общую сумму заказа")
    def get_total_amount(self) -> str:
        """Получить общую сумму заказа"""
        return self.get_element_text(self.TOTAL_LABEL)
        
    @allure.step("Завершить заказ")
    def finish_order(self):
        """Нажать кнопку 'Finish'"""
        self.click_element(self.FINISH_BUTTON)
        
    # Методы для страницы завершения заказа
    @allure.step("Проверить успешное завершение заказа")
    def is_order_complete(self) -> bool:
        """Проверить, что заказ успешно завершен"""
        return self.is_element_visible(self.CHECKOUT_COMPLETE_CONTAINER)
        
    @allure.step("Получить заголовок страницы завершения")
    def get_complete_header(self) -> str:
        """Получить заголовок страницы завершения заказа"""
        return self.get_element_text(self.COMPLETE_HEADER)
        
    @allure.step("Получить текст подтверждения заказа")
    def get_complete_message(self) -> str:
        """Получить текст подтверждения заказа"""
        return self.get_element_text(self.COMPLETE_TEXT)
        
    @allure.step("Вернуться на главную страницу")
    def back_to_home(self):
        """Нажать кнопку 'Back Home'"""
        self.click_element(self.BACK_HOME_BUTTON)
        
    # Общие методы для работы с ошибками
    @allure.step("Проверить наличие ошибки")
    def is_error_displayed(self) -> bool:
        """Проверить наличие сообщения об ошибке"""
        return self.is_element_visible(self.ERROR_MESSAGE)
        
    @allure.step("Получить текст ошибки")
    def get_error_message(self) -> str:
        """Получить текст сообщения об ошибке"""
        if self.is_error_displayed():
            return self.get_element_text(self.ERROR_MESSAGE)
        return ""