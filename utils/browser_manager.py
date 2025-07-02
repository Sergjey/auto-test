"""Управление браузером для тестов"""

import allure
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
from config.settings import Settings

class BrowserManager:
    """Менеджер браузера для тестов"""
    
    def __init__(self):
        self.settings = Settings()
        self.browser = None
        self.context = None
        self.page = None
        
    @allure.step("Инициализация браузера")
    def init_browser(self) -> Page:
        """Инициализация браузера и создание страницы"""
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(**self.settings.BROWSER_CONFIG)
        self.context = self.browser.new_context(
            record_video_dir=self.settings.VIDEOS_DIR if self.settings.VIDEO_ON_FAILURE else None
        )
        self.page = self.context.new_page()
        return self.page
        
    def close(self):
        """Закрытие браузера и всех ресурсов"""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()