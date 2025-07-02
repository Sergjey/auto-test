"""Страница авторизации SauceDemo"""

import allure
from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Страница авторизации"""
    
    # Локаторы элементов
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"
    ERROR_BUTTON = ".error-button"
    LOGIN_LOGO = ".login_logo"
    LOGIN_CONTAINER = ".login_container"
    
    def __init__(self, page: Page):
        super().__init__(page)
        
    @allure.step("Открыть страницу авторизации")
    def open(self):
        """Открыть главную страницу (страницу логина)"""
        self.goto("/")
        self.wait_for_element(self.LOGIN_CONTAINER)
        
    @allure.step("Ввести имя пользователя: {username}")
    def enter_username(self, username: str):
        """Ввести имя пользователя"""
        self.fill_field(self.USERNAME_INPUT, username)
        
    @allure.step("Ввести пароль")
    def enter_password(self, password: str):
        """Ввести пароль"""
        self.fill_field(self.PASSWORD_INPUT, password)
        
    @allure.step("Нажать кнопку 'Войти'")
    def click_login_button(self):
        """Нажать кнопку входа"""
        self.click_element(self.LOGIN_BUTTON)
        
    @allure.step("Выполнить авторизацию пользователя {username}")
    def login(self, username: str, password: str):
        """Выполнить полную авторизацию"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        
    @allure.step("Проверить отображение ошибки авторизации")
    def is_error_displayed(self) -> bool:
        """Проверить наличие сообщения об ошибке"""
        return self.is_element_visible(self.ERROR_MESSAGE)
        
    @allure.step("Получить текст ошибки авторизации")
    def get_error_message(self) -> str:
        """Получить текст сообщения об ошибке"""
        if self.is_error_displayed():
            return self.get_element_text(self.ERROR_MESSAGE)
        return ""
        
    @allure.step("Закрыть сообщение об ошибке")
    def close_error_message(self):
        """Закрыть сообщение об ошибке"""
        if self.is_element_visible(self.ERROR_BUTTON):
            self.click_element(self.ERROR_BUTTON)
            
    @allure.step("Проверить загрузку страницы авторизации")
    def is_login_page_loaded(self) -> bool:
        """Проверить, что страница авторизации загружена"""
        return (self.is_element_visible(self.LOGIN_LOGO) and 
                self.is_element_visible(self.USERNAME_INPUT) and
                self.is_element_visible(self.PASSWORD_INPUT) and
                self.is_element_visible(self.LOGIN_BUTTON))