# E-commerce Test Automation Framework

[![CI](https://github.com/Anychos/ecommerce_automation_testing/actions/workflows/tests.yml/badge.svg)](https://github.com/Anychos/ecommerce_automation_testing/actions/workflows/tests.yml)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Playwright](https://img.shields.io/badge/UI-Playwright-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/python/)

Учебный проект Automation QA на Python: API-, UI- и end-to-end тесты e-commerce приложения, единый Allure Report и запуск в GitHub Actions.

[Открыть Allure Report](https://anychos.github.io/ecommerce_automation_testing/)

## Что проверяется

Последняя выполненная коллекция проекта содержит 94 теста:

| Уровень | Тестов | Покрытие |
|---|---:|---|
| API | 58 | Authentication, users, products, carts, orders; positive и negative cases |
| UI / E2E | 30 | Registration, login, catalog, product, cart, checkout, orders, header, footer |
| Unit | 6 | Маскирование sensitive data в Allure cURL и environment metadata |

Ключевые технические решения:

- отдельные API clients и Pydantic-схемы для доменных сущностей;
- Factory fixtures для подготовки независимых test data;
- Page Object Model вместе с Page Component Pattern;
- параллельный запуск через `pytest-xdist` и повтор нестабильных integration tests через `pytest-rerunfailures`;
- cURL requests, Allure labels и Playwright trace для диагностики падений;
- маскирование passwords, tokens, cookies и authorization headers в публичном отчёте;
- revisions тестируемых приложений передаются в CI через GitHub Repository Variables;
- dependencies framework, API target и UI target установлены в изолированные virtual environments.

## Test targets

Код приложений намеренно хранится отдельно от проекта автоматизации. Workflow ожидает следующие GitHub Repository Variables:

| Variable | Значение |
|---|---|
| `API_APP_REPOSITORY` | URL совместимого REST API repository |
| `API_APP_REF` | протестированный commit SHA API target |
| `UI_APP_REPOSITORY` | URL совместимого Web UI repository |
| `UI_APP_REF` | протестированный commit SHA UI target |

Так репозиторий остаётся сфокусированным на AQA-коде, а GitHub Actions поднимает воспроизводимое test environment из указанных revisions. Пока variables не настроены, CI выполняет только независимые unit tests; API/UI jobs пропускаются. Для локального полного прогона оба приложения должны быть запущены: API на `http://localhost:8080`, UI на `http://127.0.0.1:5000`.

## Стек

- Python 3.12, Pytest, pytest-xdist, pytest-rerunfailures
- HTTPX, Pydantic, Faker, JSON Schema
- Playwright, pytest-playwright
- Allure Pytest, Swagger Coverage Tool
- GitHub Actions, PostgreSQL 16, GitHub Pages

Версии Python-пакетов закреплены в [`requirements.txt`](requirements.txt).

## Архитектура

```text
src/
├── api/
│   ├── clients/       # HTTP clients и Pydantic schemas
│   ├── fixtures/      # API fixtures и factories
│   └── tools/         # assertions, routes, cURL, data generation
└── ui/
    ├── pages/         # Page Objects
    ├── components/    # переиспользуемые UI components
    ├── fixtures/      # browser contexts и storage state
    └── models/        # UI test data models
tests/
├── api/               # API integration tests
├── ui/                # UI и E2E tests
└── unit/              # isolated framework tests
utils/
├── allure/            # labels и безопасный environment.properties
└── fixtures/          # общие Pytest plugins
```

## Быстрый старт

Требования:

- Python 3.12;
- Git;
- Chromium для Playwright;
- запущенные API/UI test targets для integration tests;
- Allure CLI — только если отчёт нужно открыть локально.

```bash
git clone https://github.com/Anychos/ecommerce_automation_testing.git
cd ecommerce_automation_testing

python -m venv .venv
```

Активация окружения:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Установка зависимостей и Chromium:

```bash
python -m pip install -r requirements.txt
playwright install chromium
```

Создание локальной конфигурации:

```bash
# Linux / macOS
cp .env.example .env

# Windows PowerShell
Copy-Item .env.example .env
```

В `.env.example` находятся только local URLs и synthetic test credentials. Nested settings используют разделитель `__`, например `HTTP_CLIENT__BASE_URL` и `TEST_USER__EMAIL`.

Инструкции запуска test targets следует хранить в их отдельных репозиториях. Их URL и commit SHA должны совпадать с Repository Variables, используемыми в CI.

## Запуск тестов

```bash
# Unit tests без внешних сервисов
pytest tests/unit --reruns 0

# API tests — требуется REST API
pytest tests/api

# UI tests — требуются REST API, Web UI и Chromium
pytest tests/ui

# Полный прогон с Allure results
pytest tests --alluredir=allure-results
```

Примеры выборочного запуска:

```bash
pytest tests/api -m authentication_api
pytest tests/ui -m smoke
pytest tests/ui -m e2e
pytest tests/api -n 3
pytest tests/ui -n 2
```

Основные markers объявлены в [`pytest.ini`](pytest.ini): `api`, `ui`, `smoke`, `regression`, `e2e` и markers отдельных сущностей или страниц.

## Отчётность и CI

Локальный Allure Report:

```bash
pytest tests --alluredir=allure-results
allure serve allure-results
```

В отчёт добавляются steps, severity, feature/story labels и безопасные cURL-команды. Playwright trace прикладывается только к упавшим тестам. Использовать framework следует только на изолированном test environment, а не с production credentials.

Workflow `.github/workflows/tests.yml` выполняет:

1. unit tests;
2. API tests с PostgreSQL и revision из `API_APP_REF`, если target настроен;
3. UI/E2E tests с Chromium и revision из `UI_APP_REF`, если target настроен;
4. объединение результатов и публикацию Allure Report в GitHub Pages;
5. optional Telegram notification, если настроены repository secrets.

## Назначение проекта

Репозиторий создан как часть портфолио Python Automation QA Engineer. Он демонстрирует проектирование test framework, работу с REST API и browser automation, организацию test data, диагностику падений и CI-интеграцию.
