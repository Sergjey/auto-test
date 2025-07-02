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

git checkout -b feature/my-task
# Работаешь, коммитишь изменения:
git add .
git commit -m "feat: реализовал фичу Х"
git push origin feature/my-task

#пулл реквест на гитхабе + мердж
#либо 
git checkout main
git pull origin main
git merge feature/my-task
git push origin main

#Синхронизируешь свой локальный main
git checkout main
git pull origin main

#Удаляешь свою локальную ветку
git branch -d feature/my-task
