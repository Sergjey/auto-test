"""E2E тесты процесса авторизации"""

import pytest
import allure
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.components.header import Header
from config.test_data import Users, ErrorMessages

@allure.epic("SauceDemo E2E Tests")
@allure.feature("Authentication Flow")
class TestAuthFlow:
    """Тесты процесса авторизации и выхода из системы"""
    
    @allure.story("Успешная авторизация стандартного пользователя")
    @allure.severity("critical")
    @pytest.mark.smoke
    def test_successful_login_standard_user(self, page: Page):
        """E2E тест успешной авторизации стандартного пользователя"""
        
        # Arrange
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        
        with allure.step("Открытие страницы авторизации"):
            login_page.open()
            assert login_page.is_login_page_loaded(), "Страница авторизации не загружена"
            
        with allure.step("Ввод валидных учетных данных"):
            login_page.login(
                Users.STANDARD_USER["username"], 
                Users.STANDARD_USER["password"]
            )
            
        with allure.step("Проверка успешной авторизации"):
            expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
            assert inventory_page.is_loaded(), "Страница каталога не загружена"
            
        with allure.step("Проверка отсутствия ошибок"):
            assert not login_page.is_error_displayed(), "Отображается ошибка авторизации"
    
    @allure.story("Авторизация заблокированного пользователя")
    @allure.severity("normal")
    @pytest.mark.auth
    def test_locked_out_user_login(self, page: Page):
        """E2E тест авторизации заблокированного пользователя"""
        
        # Arrange
        login_page = LoginPage(page)
        
        with allure.step("Открытие страницы авторизации"):
            login_page.open()
            
        with allure.step("Попытка авторизации заблокированного пользователя"):
            login_page.login(
                Users.LOCKED_OUT_USER["username"], 
                Users.LOCKED_OUT_USER["password"]
            )
            
        with allure.step("Проверка отображения ошибки блокировки"):
            assert login_page.is_error_displayed(), "Ошибка блокировки не отображается"
            error_message = login_page.get_error_message()
            assert ErrorMessages.LOCKED_OUT_ERROR in error_message, f"Неверное сообщение об ошибке: {error_message}"
            
        with allure.step("Проверка, что пользователь остался на странице авторизации"):
            expect(page).to_have_url("https://www.saucedemo.com/")
    
    @allure.story("Авторизация с пустыми полями")
    @allure.severity("minor")
    @pytest.mark.auth
    def test_empty_credentials_login(self, page: Page):
        """E2E тест авторизации с пустыми учетными данными"""
        
        # Arrange
        login_page = LoginPage(page)
        
        with allure.step("Открытие страницы авторизации"):
            login_page.open()
            
        with allure.step("Попытка авторизации с пустыми полями"):
            login_page.login("", "")
            
        with allure.step("Проверка отображения ошибки о необходимости ввода имени пользователя"):
            assert login_page.is_error_displayed(), "Ошибка не отображается"
            error_message = login_page.get_error_message()
            assert ErrorMessages.MISSING_USERNAME in error_message, f"Неверное сообщение об ошибке: {error_message}"
    
    @allure.story("Авторизация с невалидными данными")
    @allure.severity("normal")
    @pytest.mark.auth
    def test_invalid_credentials_login(self, page: Page):
        """E2E тест авторизации с невалидными учетными данными"""
        
        # Arrange
        login_page = LoginPage(page)
        
        with allure.step("Открытие страницы авторизации"):
            login_page.open()
            
        with allure.step("Попытка авторизации с невалидными данными"):
            login_page.login("invalid_user", "invalid_password")
            
        with allure.step("Проверка отображения ошибки о неверных учетных данных"):
            assert login_page.is_error_displayed(), "Ошибка не отображается"
            error_message = login_page.get_error_message()
            assert ErrorMessages.INVALID_CREDENTIALS in error_message, f"Неверное сообщение об ошибке: {error_message}"
    
    @allure.story("Полный цикл авторизации и выхода")
    @allure.severity("critical")
    @pytest.mark.smoke
    def test_login_logout_flow(self, page: Page):
        """E2E тест полного цикла авторизации и выхода из системы"""
        
        # Arrange
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        header = Header(page)
        
        with allure.step("Авторизация пользователя"):
            login_page.open()
            login_page.login(
                Users.STANDARD_USER["username"], 
                Users.STANDARD_USER["password"]
            )
            assert inventory_page.is_loaded(), "Авторизация не прошла"
            
        with allure.step("Выход из системы"):
            header.logout()
            
        with allure.step("Проверка возврата на страницу авторизации"):
            expect(page).to_have_url("https://www.saucedemo.com/")
            assert login_page.is_login_page_loaded(), "Не вернулись на страницу авторизации"
            
        with allure.step("Проверка невозможности доступа к защищенной странице"):
            # Попытка прямого перехода на страницу каталога
            page.goto("https://www.saucedemo.com/inventory.html")
            expect(page).to_have_url("https://www.saucedemo.com/")