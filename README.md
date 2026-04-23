# GreenCity Events Page Automated Tests

Автоматизовані UI-тести для сторінки подій GreenCity на Selenium + Pytest.

🔗 **Сторінка для тестування:** <https://www.greencity.cx.ua/#/greenCity/events>

## Опис проєкту

Проєкт переведено з `unittest` на `pytest` за структурним підходом з репозиторію `/d/code/SeleniumPytestAllure`:

- Page Object + Component Object патерн
- `tests/conftest.py` для setup/teardown WebDriver
- централізована конфігурація через `data/config.py` і `.env`

## Структура

```text
TAQC/
|-- data/
|   |-- .env.example
|   `-- config.py
|-- pages/
|   |-- base_page.py
|   |-- eco_news_page.py
|   |-- events_page.py
|   `-- components/
|       |-- base_component.py
|       `-- event_card_components.py
|-- tests/
|   |-- conftest.py
|   |-- test_events_page.py
|   `-- screenshots/
|-- test-cases/
|   `-- events-page-tests.md
|-- pytest.ini
|-- requirements.txt
`-- README.md
```

## Вимоги

- Python 3.8+
- Google Chrome
- Selenium Manager / сумісний ChromeDriver

## Встановлення

```bash
pip install -r requirements.txt
```

## Конфігурація

1. Скопіюйте `data/.env.example` у `data/.env`.
2. За потреби змініть значення:

```env
BASE_UI_URL=https://www.greencity.cx.ua/#/greenCity/events
IMPLICIT_WAIT_TIMEOUT=3
EXPLICIT_WAIT_TIMEOUT=15
BROWSER_LANG=uk-UA
HEADLESS_MODE=False
```

## Запуск тестів

Запуск усіх тестів:

```bash
pytest
```

Запуск конкретного модуля:

```bash
pytest tests/test_events_page.py
```

Запуск конкретного тесту:

```bash
pytest tests/test_events_page.py::test_TC01_open_event_and_check_details
```

## Поточне покриття

| Тест | Опис |
| --- | --- |
| TC-01 | Відкриття події зі списку і перевірка деталей |
| TC-02 | Перевірка фільтрації та скидання фільтрів |
| TC-04 | Негативний сценарій: майбутні події + дата в минулому |
| Header | Перемикання мови та навігація по шапці |
| Login modal | Успішний та негативний сценарії авторизації |
