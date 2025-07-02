"""Компонент хедера сайта"""

import allure
from playwright.sync_api import Page
from pages.base_page import BasePage

class Header(BasePage):
    """Компонент хедера с навигацией"""
    
    # Локаторы
    APP_LOGO = ".app_logo"
    BURGER_MENU_BUTTON = "#react-burger-menu-btn"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    
    # Элементы бургер-меню
    BURGER_MENU_CONTAINER = ".bm-menu"
    ALL_ITEMS_LINK = "#inventory_sidebar_link"
    ABOUT_LINK = "#about_sidebar_link"
    LOGOUT_LINK = "#logout_sidebar_link"
    RESET_APP_LINK = "#reset_sidebar_link"
    CLOSE_MENU_BUTTON = "#react-burger-cross-btn"
    
    def __init__(self, page: Page):
        super().__init__(page)
        
    @allure.step("Открыть бургер-меню")
    def open_burger_menu(self):
        """Открыть боковое меню"""
        self.click_element(self.BURGER_MENU_BUTTON)
        self.wait_for_element(self.BURGER_MENU_CONTAINER)
        
    @allure.step("Закрыть бургер-меню")
    def close_burger_menu(self):
        """Закрыть боковое меню"""
        self.click_element(self.CLOSE_MENU_BUTTON)
        
    @allure.step("Выйти из системы")
    def logout(self):
        """Выполнить выход из системы"""
        self.open_burger_menu()
        self.click_element(self.LOGOUT_LINK)
        
    @allure.step("Перейти на страницу 'Все товары'")
    def go_to_all_items(self):
        """Перейти на страницу всех товаров"""
        self.open_burger_menu()
        self.click_element(self.ALL_ITEMS_LINK)
        
    @allure.step("Сбросить состояние приложения")
    def reset_app_state(self):
        """Сбросить состояние приложения"""
        self.open_burger_menu()
        self.click_element(self.RESET_APP_LINK)
        
    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        """Перейти в корзину через хедер"""
        self.click_element(self.SHOPPING_CART_LINK)
        
    @allure.step("Получить количество товаров в корзине")
    def get_cart_items_count(self) -> int:
        """Получить количество товаров в корзине из badge"""
        if self.is_element_visible(self.SHOPPING_CART_BADGE):
            count_text = self.get_element_text(self.SHOPPING_CART_BADGE)
            return int(count_text) if count_text.isdigit() else 0
        return 0