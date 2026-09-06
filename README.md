# 🛒 E-commerce Test Automation Framework

[CI](https://github.com/Anychos/ecommerce_automation_testing/actions/workflows/tests.yml) · [Python 3.12](https://www.python.org/) · [Pytest](https://docs.pytest.org/) · [Playwright](https://playwright.dev/python/) · [Allure](https://docs.qameta.io/allure/)

**Проект-портфолио Python Automation QA Engineer.** Репозиторий содержит Python-фреймворк для API-, UI- и end-to-end автоматизации e-commerce приложения. Код приложений-целей намеренно хранится отдельно: этот репозиторий сфокусирован на тестовой архитектуре, тестовых данных, диагностике и отчётности.

🔗 [Allure Report](https://anychos.github.io/ecommerce_automation_testing/)

## Содержание

- [Покрытие](#покрытие)
- [Технический стек](#технический-стек)
- [Архитектурные решения](#архитектурные-решения)
- [Структура репозитория](#структура-репозитория)
- [Быстрый старт](#быстрый-старт)
- [Запуск тестов](#запуск-тестов)
- [Маркеры](#маркеры)
- [Отчётность](#отчётность)
- [CI и test targets](#ci-и-test-targets)
- [Развитие API AQA](#развитие-api-aqa)

## Покрытие

### API

API-слой разделён на доменные клиенты, Pydantic-схемы, фикстуры и проверки ответов. Покрываются следующие области:

| Домен | Проверяемые возможности |
| --- | --- |
| Authentication | Регистрация, вход пользователя и администратора, невалидные учётные данные |
| Users | Управление пользователями и профилем, валидация данных |
| Products | CRUD товаров, каталог, обязательные поля и формат image URL |
| Carts | Добавление, изменение и удаление позиций, ограничения остатков |
| Orders | Создание, получение и список заказов, сценарии с пустой корзиной и недоступным товаром |
| Checkout | Последовательность заказ → доставка → оплата, статусы delivery/payment и тестовые переходы checkout |

Поток checkout строится на создании заказа, выборе доставки и последующем создании оплаты. Детали запросов и схем инкапсулированы в API-клиентах; README не заменяет API-контракт.

### UI и E2E

UI-слой использует Page Object Model и переиспользуемые page components. Сценарии охватывают регистрацию, вход, каталог и карточку товара, корзину, checkout, историю и детали заказов, а также навигацию в header и footer. Сквозной сценарий соединяет пользовательский путь от регистрации до оформления заказа.

## Технический стек

| Инструмент | Назначение |
| --- | --- |
| Python 3.12 | Язык реализации |
| Pytest, pytest-xdist, pytest-rerunfailures | Запуск, параллелизация и управляемые повторные попытки |
| HTTPX | HTTP-клиент API-тестов |
| Pydantic и pydantic-settings | DTO и типизированная конфигурация из `.env` |
| Playwright и pytest-playwright | Браузерная автоматизация Chromium |
| Faker | Генерация тестовых данных |
| jsonschema | Проверка JSON-схем ответов |
| Allure Pytest | Steps, labels, severity и вложения |
| Swagger Coverage Tool | Отчёт о покрытии API по Swagger/OpenAPI |
| GitHub Actions, PostgreSQL 16, GitHub Pages | CI, БД API-target и публикация отчёта |

Точные версии зависимостей зафиксированы в [requirements.txt](requirements.txt).

## Архитектурные решения

- **Доменные API-клиенты и Pydantic-схемы** скрывают детали HTTP и делают контракт теста явным.
- **Фикстуры и фабрики** создают данные для API-сценариев и передают проверяемые request/response-модели.
- **Page Object Model + Page Component Pattern** отделяют сценарии от селекторов и переиспользуемых частей страниц.
- **Общие assertions** проверяют статусы, бизнес-инварианты и JSON-схемы.
- **Allure-диагностика** добавляет labels и вложения; чувствительные значения в cURL, cookie и заголовках маскируются.
- **Раздельные окружения** позволяют устанавливать зависимости framework, API target и UI target независимо.

## Структура репозитория

```text
├── config.py                # типизированная конфигурация из .env
├── conftest.py              # регистрация общих pytest fixtures
├── pytest.ini               # пути поиска тестов, параметры и маркеры
├── .env.example             # шаблон локальной конфигурации
├── src/
│   ├── api/
│   │   ├── clients/         # HTTP-клиенты и Pydantic-схемы доменов
│   │   ├── fixtures/        # fixtures и фабрики API-данных
│   │   └── tools/           # assertions, маршруты, HTTP-утилиты, генераторы
│   └── ui/
│       ├── pages/           # Page Objects
│       ├── components/      # компоненты страниц
│       ├── fixtures/        # browser, page и data fixtures
│       ├── models/          # UI-модели тестовых данных
│       └── tools/           # маршруты и генераторы UI-данных
├── tests/
│   ├── api/                 # integration-тесты API, включая checkout
│   └── ui/                  # UI- и E2E-тесты
└── utils/
    ├── allure/              # labels, environment и redaction
    └── fixtures/            # общие pytest-плагины
```

## Быстрый старт

Требуются Python 3.12 и Git. Для UI-тестов нужен Chromium; Allure CLI необходим только для локального просмотра отчёта. Integration-тестам требуются запущенные test targets, а не production-окружения.

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

Создайте локальную конфигурацию:

```bash
# Linux / macOS
cp .env.example .env
# Windows PowerShell
Copy-Item .env.example .env
```

Шаблон [.env.example](.env.example) содержит локальные URL и синтетические test credentials. Для вложенных настроек используется разделитель `__`, например `HTTP_CLIENT__BASE_URL` и `TEST_USER__EMAIL`. По умолчанию API доступен на `http://localhost:8080`, UI — на `http://127.0.0.1:5000`.

## Запуск тестов

```bash
# API: требуется запущенный REST API
python -m pytest tests/api -q -rA -o addopts=

# UI: требуются API, Web UI и Chromium
python -m pytest tests/ui

# Полный набор с результатами Allure
python -m pytest tests --alluredir=allure-results
```

Для выборочного и параллельного запуска используйте маркеры и xdist:

```bash
python -m pytest tests/api -m authentication_api
python -m pytest tests/ui -m smoke
python -m pytest tests/ui -m e2e
python -m pytest tests/api -n 3
python -m pytest tests/ui -n 2
```

## Маркеры

Объявленные маркеры приведены в [pytest.ini](pytest.ini).

| Категория | Маркеры |
| --- | --- |
| Общие | `smoke`, `regression`, `e2e` |
| Уровни | `api`, `ui` |
| API-сущности | `authentication_api`, `user_api`, `product_api`, `cart_api`, `order_api` |
| UI-страницы | `registration`, `login`, `home`, `product_detail`, `cart`, `checkout`, `order_detail`, `orders_list`, `header`, `footer` |

## Отчётность

```bash
python -m pytest tests --alluredir=allure-results
allure serve allure-results
```

Allure объединяет steps, severity, feature/story labels и безопасные cURL-вложения. Для упавших UI-тестов сохраняются Playwright traces. Пароли, токены, cookies и заголовки авторизации должны оставаться скрытыми в публикуемых артефактах.

> ⚠️ Используйте framework только с изолированными тестовыми окружениями и синтетическими учётными данными.

## CI и test targets

Workflow [.github/workflows/tests.yml](.github/workflows/tests.yml) выполняет API-тесты с PostgreSQL, UI/E2E-тесты с Chromium, формирует Swagger coverage, собирает результаты Allure и публикует отчёт в GitHub Pages. При наличии Telegram secrets workflow отправляет уведомление о статусе.

Для запуска API-job необходимы обе переменные `API_APP_REPOSITORY` и `API_APP_REF`. UI-job дополнительно требует `UI_APP_REPOSITORY` и `UI_APP_REF`.

| GitHub Repository Variable | Назначение |
| --- | --- |
| `API_APP_REPOSITORY` | Репозиторий API test target |
| `API_APP_REF` | Ревизия API test target |
| `UI_APP_REPOSITORY` | Репозиторий UI test target |
| `UI_APP_REF` | Ревизия UI test target |

## Развитие API AQA

Контекст, критерии готовности и список рисков собраны в [API_AQA_project_review_ru.md](API_AQA_project_review_ru.md). Ближайшие направления работы:

- независимо проверить checkout-поток delivery/payment и его контракт с API target;
- расширить матрицу доступа: `401`, `403`, invalid/expired token, ownership/IDOR и удалённый пользователь;
- сделать контрактную валидацию независимой от тех же Pydantic-моделей, которые используются для разбора ответа;
- выделить последовательный запуск без reruns и параллельный запуск с reruns в явные команды;
- сделать негативные сценарии детерминированными и уточнить типы моделей после подтверждения OpenAPI-контракта.

## Назначение проекта

Репозиторий демонстрирует проектирование Python AQA framework, работу с REST API и browser automation, организацию тестовых данных, диагностику падений, безопасную отчётность и интеграцию с CI/CD.
