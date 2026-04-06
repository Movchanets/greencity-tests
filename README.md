# GreenCity Events Page Automated Tests

Автоматизовані тести для сторінки подій GreenCity.

🔗 **Сторінка для тестування:** https://www.greencity.cx.ua/#/greenCity/events

## Опис проєкту

Цей репозиторій містить автоматизовані тести для перевірки функціональності сторінки подій GreenCity. Тести реалізовані на Python з використанням Selenium WebDriver та стандартного модуля unittest.

### Покриті тест-кейси

| Тест | Опис |
|---|---|
| TC-01 | Перевірка відображення списку подій і відкриття картки |
| TC-02 | Перевірка роботи фільтрів подій |
| TC-05 | Перевірка помилок валідації при створенні події без обов'язкових даних |

### Додаткові тести (parameterized-style)

| Тест | Опис |
|---|---|
| test_page_title_contains_events_text | Перевірка заголовку сторінки |
| test_events_page_has_filter_elements | Перевірка наявності елементів фільтрації |
| test_event_card_has_required_data | Перевірка наявності обов'язкових даних в картках |

## Структура

```
greencity-tests/
├── README.md
├── requirements.txt
├── test-cases/
│   └── events-page-tests.md
└── tests/
    ├── test_events_page.py
    └── utils.py
```

## Вимоги

- Python 3.8+
- Chrome браузер
- ChromeDriver (автоматично встановлюється через selenium-manager)

## Встановлення

```bash
pip install -r requirements.txt
```

## Інструкція запуску тестів

Запуск всіх тестів:

```bash
python -m unittest discover tests
```

Запуск конкретного файлу тестів:

```bash
python -m unittest tests.test_events_page
```

Запуск з деталізованим виводом:

```bash
python -m unittest discover tests -v
```

## Технології

- **Python** — мова програмування
- **Selenium WebDriver** — автоматизація браузера
- **unittest** — стандартний тестовий фреймворк Python
- **WebDriverWait** — явні очікування

## Обмеження

- ❌ Page Object Pattern (PO)
- ❌ pytest
- ❌ Сторонні тестові фреймворки

## Автор

Мовчанець В'ячеслав Романович
