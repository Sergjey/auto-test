# Playwright + Pytest + Allure E2E Tests

Автотесты для [SauceDemo](https://www.saucedemo.com/)  
**Стек:** Python 3.11+, Playwright, Pytest, Allure

---

## 🚀 Быстрый старт (локально)

```bash
# 1. Клонируй репозиторий и перейди в папку проекта
git clone https://github.com/Sergjey/auto-test.git
cd auto-test

# 2. Создай и активируй виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate

# 3. Установи зависимости
pip install -r requirements.txt

# 4. Установи браузеры Playwright
playwright install

# 5. Скопируй .env.example -> .env и при необходимости отредактируй
cp .env.example .env

# 6. Запусти все тесты
pytest

# 7. Запусти тесты с генерацией Allure-отчёта
pytest --alluredir=reports/allure-results

# 8. Сгенерируй и открой Allure-отчёт (нужен установленный Allure CLI)
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report


##############

# Создать новую ветку и перейти в неё
git checkout -b feature/my-new-feature

# Посмотреть текущие ветки
git branch

# Добавить файлы в индекс
git add .

# Сделать коммит
git commit -m "описание изменений"

# Переключиться на другую ветку
git checkout main

# Запушить ветку на сервер
git push origin feature/my-new-feature

# Обновить main перед мерджем
git checkout main
git pull origin main

# Влить ветку в main (merge)
git merge feature/my-new-feature

# Удалить ветку локально и на сервере
git branch -d feature/my-new-feature
git push origin --delete feature/my-new-feature

# Сделать pull request (PR) – через интерфейс GitHub
