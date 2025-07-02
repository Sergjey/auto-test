"""Базовый класс для всех страниц"""

import allure
from playwright.sync_api import Page, expect
from config.settings import Settings
from typing import Optional

class BasePage:
    """Базовый класс для всех страниц приложения"""
    
    def __init__(self, page: Page):
        self.page = page
        self.settings = Settings()
        
    @allure.step("Открыть страницу {url}")
    def goto(self, url: str = ""):
        """Переход на указанную страницу"""
        full_url = f"{self.settings.BASE_URL}{url}"
        self.page.goto(full_url)
        
    @allure.step("Получить заголовок страницы")
    def get_title(self) -> str:
        """Получить заголовок текущей страницы"""
        return self.page.title()
        
    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        """Получить текущий URL страницы"""
        return self.page.url
        
    @allure.step("Ожидать элемент {selector}")
    def wait_for_element(self, selector: str, timeout: int = None):
        """Ожидание появления элемента на странице"""
        timeout = timeout or self.settings.DEFAULT_WAIT_TIME
        self.page.wait_for_selector(selector, timeout=timeout)
        
    @allure.step("Ожидать исчезновения элемента {selector}")
    def wait_for_element_to_disappear(self, selector: str, timeout: int = None):
        """Ожидание исчезновения элемента со страницы"""
        timeout = timeout or self.settings.DEFAULT_WAIT_TIME
        self.page.wait_for_selector(selector, state="detached", timeout=timeout)
        
    @allure.step("Проверить видимость элемента {selector}")
    def is_element_visible(self, selector: str) -> bool:
        """Проверить видимость элемента"""
        return self.page.is_visible(selector)
        
    @allure.step("Получить текст элемента {selector}")
    def get_element_text(self, selector: str) -> str:
        """Получить текст элемента"""
        return self.page.text_content(selector) or ""
        
    @allure.step("Кликнуть по элементу {selector}")
    def click_element(self, selector: str):
        """Кликнуть по элементу"""
        self.page.click(selector)
        
    @allure.step("Ввести текст '{text}' в поле {selector}")
    def fill_field(self, selector: str, text: str):
        """Заполнить поле текстом"""
        self.page.fill(selector, text)
        
    @allure.step("Сделать скриншот")
    def take_screenshot(self, name: str = "screenshot"):
        """Сделать скриншот страницы"""
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        
    @allure.step("Ожидать загрузки страницы")
    def wait_for_page_load(self):
        """Ожидать полной загрузки страницы"""
        self.page.wait_for_load_state("networkidle")