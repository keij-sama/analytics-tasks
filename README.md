# Analytics Test Tasks

Примеры моих задач по SQL, Python, A/B-тестам, продуктовой аналитике, Excel и планированию отчётов в Power BI.

## Содержание

### SQL

- [`sql/retention-cohort`](sql/retention-cohort) — семидневный Retention Rate по когорте пользователей.
- [`sql/median-monthly-spend`](sql/median-monthly-spend) — медианные месячные траты постоянных клиентов без встроенной функции медианы.
- [`sql/revenue-price-history`](sql/revenue-price-history) — восстановление выручки через временное соединение транзакций с историей цен.

### Python

- [`python/app-launch-aggregation`](python/app-launch-aggregation) — агрегация запусков приложения по платформам, источникам и городам.
- [`python/currency-cleaning`](python/currency-cleaning) — очистка цен в USD и EUR, обработка разных числовых форматов и расчёт общей выручки.

### A/B-тесты

- [`ab-testing/email-campaign`](ab-testing/email-campaign) — z-тест двух долей и доверительный интервал для конверсии email-рассылки.

### Продуктовая аналитика и визуализация

- [`product-analytics/mobile-release-review`](product-analytics/mobile-release-review) — разбор падения мобильной конверсии после запуска функции и подготовка вывода для руководителя.

### Excel и Power BI

- [`excel-power-bi/mining-equipment`](excel-power-bi/mining-equipment) — анализ объёма работ, ремонтов, производительности, КТГ и КИО парка горной техники.

## Запуск Python-проектов

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

Команды запуска приведены в README каждого проекта.
