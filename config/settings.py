"""Настройки проекта"""

import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")

class Settings:
    """Класс настроек проекта"""
    
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "30000"))
    DEFAULT_WAIT_TIME = int(os.getenv("DEFAULT_WAIT_TIME", "5000"))
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    VIDEO_ON_FAILURE = os.getenv("VIDEO_ON_FAILURE", "true").lower() == "true"
    
    # Браузерные настройки
    BROWSER_CONFIG = {
        "headless": True,
        "viewport": {"width": 1280, "height": 720},
        "timeout": BROWSER_TIMEOUT,
    }
    
    # Директории
    REPORTS_DIR = "reports"
    SCREENSHOTS_DIR = f"{REPORTS_DIR}/screenshots"
    VIDEOS_DIR = f"{REPORTS_DIR}/videos"
    ALLURE_RESULTS_DIR = f"{REPORTS_DIR}/allure-results"
