"""Фикстуры для работы с пользователями"""

import pytest
from typing import Generator
from playwright.sync_api import Page
from pages.login_page import LoginPage
from config.test_data import Users

@pytest.fixture
def authenticated_performance_user(page: Page) -> Page:
    """Фикстура для авторизации performance_glitch_user"""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(
        Users.PERFORMANCE_GLITCH_USER["username"],
        Users.PERFORMANCE_GLITCH_USER["password"]
    )
    return page

@pytest.fixture
def authenticated_problem_user(page: Page) -> Page:
    """Фикстура для авторизации problem_user"""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(
        Users.PROBLEM_USER["username"],
        Users.PROBLEM_USER["password"]
    )
    return page