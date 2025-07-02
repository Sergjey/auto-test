"""Тестовые данные для SauceDemo"""
import os

class Users:
    """Пользователи системы"""
    
    STANDARD_USER = {
        "username": os.getenv("USERNAME_STANDARD_USER"),
        "password": os.getenv("PASSWORD_STANDARD_USER")
    }
    LOCKED_OUT_USER = {
        "username": os.getenv("USERNAME_LOCKED_OUT_USER"),
        "password": os.getenv("PASSWORD_LOCKED_OUT_USER")
    }
    PROBLEM_USER = {
        "username": os.getenv("USERNAME_PROBLEM_USER"),
        "password": os.getenv("PASSWORD_PROBLEM_USER")
    }
    PERFORMANCE_GLITCH_USER = {
        "username": os.getenv("USERNAME_PERFORMANCE_GLITCH_USER"),
        "password": os.getenv("PASSWORD_PERFORMANCE_GLITCH_USER")
    }

class Products:
    """Товары в каталоге"""
    
    BACKPACK = {
        "name": "Sauce Labs Backpack",
        "price": "$29.99",
        "id": "sauce-labs-backpack"
    }
    
    BIKE_LIGHT = {
        "name": "Sauce Labs Bike Light", 
        "price": "$9.99",
        "id": "sauce-labs-bike-light"
    }
    
    BOLT_TSHIRT = {
        "name": "Sauce Labs Bolt T-Shirt",
        "price": "$15.99", 
        "id": "sauce-labs-bolt-t-shirt"
    }
    
    FLEECE_JACKET = {
        "name": "Sauce Labs Fleece Jacket",
        "price": "$49.99",
        "id": "sauce-labs-fleece-jacket"
    }
    
    ONESIE = {
        "name": "Sauce Labs Onesie",
        "price": "$7.99",
        "id": "sauce-labs-onesie"
    }
    
    RED_TSHIRT = {
        "name": "Test.allTheThings() T-Shirt (Red)",
        "price": "$15.99",
        "id": "test.allthethings()-t-shirt-(red)"
    }

class CheckoutData:
    """Данные для оформления заказа"""
    
    VALID_USER_INFO = {
        "first_name": "John",
        "last_name": "Doe", 
        "postal_code": "12345"
    }
    
    INVALID_USER_INFO = {
        "first_name": "",
        "last_name": "Doe",
        "postal_code": "12345"
    }

class ErrorMessages:
    """Сообщения об ошибках"""
    
    LOCKED_OUT_ERROR = "Epic sadface: Sorry, this user has been locked out."
    INVALID_CREDENTIALS = "Epic sadface: Username and password do not match any user in this service"
    MISSING_USERNAME = "Epic sadface: Username is required"
    MISSING_PASSWORD = "Epic sadface: Password is required"
    MISSING_FIRST_NAME = "Error: First Name is required"
    MISSING_LAST_NAME = "Error: Last Name is required"
    MISSING_POSTAL_CODE = "Error: Postal Code is required"