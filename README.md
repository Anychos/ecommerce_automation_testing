# 🛒 E-commerce Test Automation Framework

[CI](https://github.com/Anychos/ecommerce_automation_testing/actions/workflows/tests.yml)
[Python 3.12](https://www.python.org/)
[Pytest](https://docs.pytest.org/)
[Playwright](https://playwright.dev/python/)
[Allure](https://docs.qameta.io/allure/)

**Проект-портфолио Python Automation QA Engineer.** Фреймворк автоматизации тестирования e-commerce приложения: API-, UI- и end-to-end тесты, единый Allure Report и полный CI-пайплайн в GitHub Actions с публикацией отчёта.

🔗 **[Allure Report последнего прогона](https://anychos.github.io/ecommerce_automation_testing/)**

## Содержание

- [Что покрывают тесты](#что-покрывают-тесты)
- [План развития API AQA](#план-развития-api-aqa)
- [Стек](#стек)
- [Ключевые технические решения](#ключевые-технические-решения)
- [Структура репозитория](#структура-репозитория)
- [Быстрый старт](#быстрый-старт)
- [Запуск тестов](#запуск-тестов)
- [Маркеры](#маркеры)
- [Отчётность](#отчётность)
- [CI и test targets](#ci-и-test-targets)

---

## План развития API AQA

Проект находится в активной доработке. Ниже — публичный план по результатам
[API AQA review](API_AQA_project_review_ru.md). Пункт отмечается выполненным
только после изменения кода и независимой проверки результата.

- [ ] **Высокий:** определить границы API-покрытия: реализовать один сквозной поток payments/deliveries либо удалить пустые заглушки и явно ограничить scope портфолио.
- [ ] **Высокий:** привести README и task-артефакты в соответствие с фактическим деревом; восстановить либо убрать заявления о несуществующих unit- и mutation-тестах.
- [ ] **Высокий:** перевести успешное создание пользователей, товаров и корзин на отслеживаемые фабрики с детерминированной очисткой.
- [ ] **Высокий:** добавить матрицу проверок доступа: `401`, `403`, invalid/expired token, ownership/IDOR и удалённый пользователь.
- [ ] **Средний:** сделать контрактную валидацию независимой: строгие Pydantic-модели и/или проверки против зафиксированного OpenAPI.
- [ ] **Средний:** унифицировать публичный интерфейс API-клиентов и диагностику ошибок аутентификации.
- [ ] **Средний:** сделать последовательный запуск без reruns настройкой по умолчанию; вынести xdist и reruns в явные команды.
- [ ] **Средний:** сделать негативные сценарии детерминированными: создавать и удалять ресурс для `404`, различать отсутствующее поле, пустое значение, `null` и неверный тип.
- [ ] **Низкий:** уточнить типы моделей ответов (`datetime`, статусы, URL и денежные значения) после подтверждения OpenAPI-контракта и убрать неиспользуемый код.

Полный контекст, критерии готовности и исходные наблюдения доступны в [API_AQA_project_review_ru.md](API_AQA_project_review_ru.md).

---

## Что покрывают тесты

API-набор содержит **58 сценариев**. Последний подтверждённый API-прогон выполнен **2026-08-31** против
`[Anychos/test_automation__app](https://github.com/Anychos/test_automation__app/tree/b52fcdedd37060418e27942ce86ef88a5993a595/pizza_shop_test_api_3)`
на commit `b52fcdedd37060418e27942ce86ef88a5993a595`: **58 passed, 0 failed, 2 warnings**.


| Уровень      | Тестов | Покрытие                                                                                          |
| ------------ | ------ | ------------------------------------------------------------------------------------------------- |
| 🔌 API       | 58     | Authentication, users, products, carts, orders; positive + negative cases, валидация схем ответов |
| 🖥️ UI / E2E | 30     | Registration, login, каталог, карточка товара, корзина, checkout, orders, header, footer          |


### API-тесты (`tests/api/`)


| Файл                     | Что проверяется                                                         |
| ------------------------ | ----------------------------------------------------------------------- |
| `test_authentication.py` | Регистрация и логин пользователя/админа, невалидные учётные данные      |
| `test_user.py`           | Создание, профиль, обновление, удаление и валидация данных пользователя |
| `test_product.py`        | CRUD товаров, список, обязательные поля, форматы данных и image URL     |
| `test_cart.py`           | Добавление, получение, обновление, удаление и ограничения остатков      |
| `test_order.py`          | Создание, получение и список заказов, пустая корзина, недоступный товар |


### UI / E2E-тесты (`tests/ui/`)


| Файл                                            | Что проверяется                                          |
| ----------------------------------------------- | -------------------------------------------------------- |
| `test_authentication/test_registration_page.py` | Регистрация нового пользователя                          |
| `test_authentication/test_login_page.py`        | Логин, валидация формы                                   |
| `test_home_page.py`                             | Каталог на главной, пагинация                            |
| `test_product_detail_page.py`                   | Карточка товара, добавление в корзину                    |
| `test_cart_page.py`                             | Корзина: изменение количества, удаление позиций          |
| `test_checkout_page.py`                         | Оформление заказа, валидация данных                      |
| `test_orders/…`                                 | История заказов и детали заказа                          |
| `test_header.py`, `test_footer.py`              | Навигация и элементы шапки/футера                        |
| `test_e2e.py`                                   | Сквозной сценарий: регистрация → логин → корзина → заказ |


---

## Стек


| Инструмент                                    | Назначение                                                |
| --------------------------------------------- | --------------------------------------------------------- |
| Python 3.12                                   | Основной язык                                             |
| Pytest + pytest-xdist + pytest-rerunfailures  | Тестовый раннер, параллельный запуск, авто-ретраи         |
| HTTPX                                         | HTTP-клиент для API-тестов                                |
| Pydantic + pydantic-settings                  | Схемы API-ответов и типизированная конфигурация из `.env` |
| Playwright + pytest-playwright                | Браузерная автоматизация (Chromium)                       |
| Faker                                         | Генерация тестовых данных                                 |
| JSON Schema (jsonschema)                      | Валидация контрактов API-ответов                          |
| Allure Pytest                                 | Отчётность: steps, labels, severity, вложения             |
| Swagger Coverage Tool                         | Проверка покрытия endpoints по Swagger-спецификации       |
| GitHub Actions + PostgreSQL 16 + GitHub Pages | CI, БД для API-target, хостинг отчёта                     |


Версии пакетов закреплены в `[requirements.txt](requirements.txt)`.

## Ключевые технические решения

- **API clients + Pydantic-схемы** — типизированные клиенты и доменные модели вместо «сырых» запросов;
- **Factory fixtures** — независимая подготовка test data для каждого теста;
- **Page Object Model + Page Component Pattern** — страницы собраны из переиспользуемых компонентов;
- **Параллельный запуск** (`pytest-xdist`) и **повтор нестабильных integration-тестов** (`pytest-rerunfailures`);
- **Диагностика падений** — cURL-команды, Allure labels, Playwright trace (только для упавших тестов);
- **Безопасность отчёта** — маскирование passwords, tokens, cookies и authorization headers в публичном Allure Report;
- **Изолированные окружения** — зависимости framework, API target и UI target установлены в отдельные virtual environments.

## Структура репозитория

```text
├── config.py                # типизированные nested-настройки (pydantic-settings, .env)
├── conftest.py              # корневые fixtures
├── pytest.ini               # конфигурация запуска и маркеры
├── .env.example             # шаблон локальной конфигурации
│
├── src/                     # сам фреймворк
│   ├── api/
│   │   ├── clients/         # HTTP-клиенты по сущностям + Pydantic-схемы, base client, event hooks
│   │   ├── fixtures/        # API fixtures и factory-фабрики test data (auth, user, product, cart, order)
│   │   └── tools/           # assertions, маршруты, HTTP-обёртки, генерация данных
│   └── ui/
│       ├── pages/           # Page Objects (home, registration, login, product, cart, checkout, orders)
│       ├── components/      # переиспользуемые UI-компоненты страниц
│       ├── fixtures/        # browser context, page fixtures, storage state
│       ├── models/          # модели UI test data
│       └── tools/           # UI-маршруты и генерация данных
│
├── tests/                   # сами тесты
│   ├── api/                 # API integration-тесты (auth, user, product, cart, order)
│   ├── ui/                  # UI- и E2E-тесты
│   └── unit/                # изолированные unit-тесты фреймворка (без внешних сервисов)
│
└── utils/
    ├── allure/              # labels (epic/feature/story/severity), environment.properties, redaction
    └── fixtures/            # общие pytest-плагины для Allure
```

---

## Быстрый старт

**Требования:** Python 3.12, Git, Chromium для Playwright; для integration-тестов — запущенные API/UI test targets; Allure CLI — только для локального просмотра отчёта.

```bash
git clone https://github.com/Anychos/ecommerce_automation_testing.git
cd ecommerce_automation_testing

python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
playwright install chromium
```

Создать локальную конфигурацию:

```bash
# Linux / macOS
cp .env.example .env
# Windows PowerShell
Copy-Item .env.example .env
```

`.env.example` содержит только local URLs и synthetic test credentials. Nested settings используют разделитель `__`, например `HTTP_CLIENT__BASE_URL`, `TEST_USER__EMAIL`.

Для полного локального прогона оба приложения-цели должны быть запущены: **API** — `http://localhost:8080`, **UI** — `http://127.0.0.1:5000`.

## Запуск тестов

```bash
# Unit-тесты (без внешних сервисов)
pytest tests/unit --reruns 0

# API-тесты без параллелизма и автоматических reruns (нужен запущенный REST API)
python -m pytest tests/api -q -rA -o addopts=

# UI-тесты (нужны REST API, Web UI и Chromium)
pytest tests/ui

# Полный прогон с Allure results
pytest tests --alluredir=allure-results
```

Выборочный запуск по маркерам и параллельно:

```bash
pytest tests/api -m authentication_api   # только API-тесты аутентификации
pytest tests/ui -m smoke                 # smoke-тесты UI
pytest tests/ui -m e2e                   # end-to-end сценарии
pytest tests/api -n 3                    # параллельный запуск API
pytest tests/ui -n 2                     # параллельный запуск UI
```

## Маркеры

Объявлены в `[pytest.ini](pytest.ini)`:


| Категория    | Маркеры                                                                                                                  |
| ------------ | ------------------------------------------------------------------------------------------------------------------------ |
| Общие        | `smoke`, `regression`, `e2e`                                                                                             |
| Уровни       | `api`, `ui`                                                                                                              |
| API-сущности | `authentication_api`, `user_api`, `product_api`, `cart_api`, `order_api`                                                 |
| UI-страницы  | `registration`, `login`, `home`, `product_detail`, `cart`, `checkout`, `order_detail`, `orders_list`, `header`, `footer` |


## Отчётность

Локально:

```bash
pytest tests --alluredir=allure-results
allure serve allure-results
```

В отчёт входят steps, severity, feature/story labels и безопасные cURL-команды; Playwright trace прикрепляется только к упавшим тестам. Пароли, токены, cookies и authorization headers маскируются — отчёт можно публиковать.

> ⚠️ Framework предназначен для изолированного test environment. Не используйте его с production-окружением и production credentials.

## CI и test targets

Workflow `[.github/workflows/tests.yml](.github/workflows/tests.yml)`:

1. запускает unit-тесты;
2. API-тесты с PostgreSQL и ревизией API-target из `API_APP_REF` (если target настроен);
3. UI/E2E-тесты с Chromium и ревизией UI-target из `UI_APP_REF` (если target настроен);
4. генерирует Swagger coverage HTML/JSON и загружает артефакт `swagger-coverage-api`;
5. объединяет результаты и публикует Allure Report в GitHub Pages;
6. опционально шлёт Telegram-уведомление (если настроены secrets).

Код самих приложений намеренно хранится в отдельных репозиториях — этот репозиторий сфокусирован только на AQA-коде. CI ожидает GitHub Repository Variables:


| Variable         | Значение                                                                                           |
| ---------------- | -------------------------------------------------------------------------------------------------- |
| `APP_REPOSITORY` | [https://github.com/Anychos/test_automation__app](https://github.com/Anychos/test_automation__app) |


GitHub Actions поднимает воспроизводимое test environment из указанного репозитория.

---

## Назначение проекта

Репозиторий создан как часть портфолио **Python Automation QA Engineer** и демонстрирует: проектирование test framework с нуля, работу с REST API и browser automation, организацию test data, диагностику падений, обеспечение безопасности отчётов и интеграцию с CI/CD.