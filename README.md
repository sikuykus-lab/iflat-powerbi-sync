# CRM → Google Sheets → Power BI

Короче: **REST API CRM → листы таблицы → Power BI Import** по cron, без ручного Excel.

Задача: каждый день нужен один срез — помещения, приёмки, группа статуса, даты сделок. Ручная выгрузка не масштабируется; BI должен читать стабильные колонки, а не живой API.

---

## Что сделано

- **OAuth к CRM** — секреты в JSON/env, не в теле скрипта.
- **Два refresh-скрипта** — комнаты + цветовая группа; fact приёмок (строка = приёмка).
- **Общие модули** — метрики, группировка статусов, переиспользование в парсерах отчётов.
- **Cron на VPS** — вечерний прогон без участия человека.
- **Документация колонок** — стратегия BI и чеклист под срезы.

---

## Фишки и удобство

| Фишка | Зачем |
|-------|-------|
| Service Account → Sheets | BI не дергает API при каждом открытии отчёта |
| `IFLAT_COLOR_MODE` / аналог | Одна логика цвета для BI и отчётов |
| Пагинация + embed | Меньше запросов на комнату |
| Ручной refresh из бота | Внеплановый прогон без SSH |
| `.example` для секретов | Репозиторий без паролей |

**Плюс по нагрузке:** CRM вызывается **2–4 раза в сутки** (cron + ручной), не при каждом пользователе BI.

---

## Схема данных

```mermaid
flowchart TB
  subgraph extract ["Выгрузка (редко, cron)"]
    O["CRM OAuth"]
    API["REST API\n/rooms · /inspections"]
    PY["Python refresh"]
  end

  subgraph store ["Хранение"]
    SA["Service Account"]
    SH1["Лист Rooms"]
    SH2["Лист Inspections"]
  end

  subgraph consume ["Потребление (часто)"]
    PBI["Power BI Import"]
    USR["Аналитики"]
  end

  O --> API
  API --> PY
  PY --> SA
  SA --> SH1
  SA --> SH2
  SH1 --> PBI
  SH2 --> PBI
  PBI --> USR
```

---

## Процесс пользователя

```mermaid
flowchart LR
  A["Открыл отчёт BI"] --> B["Данные с листов\nвчерашний срез"]
  B --> C["Срез по типу /\nстатусу / дате"]
  C --> D["Решение по\nзаселению / приёмкам"]
```

**Администратор:**

```mermaid
flowchart TD
  R1["Cron 17:00 / 17:15 UTC"] --> R2["Лог *.cron.log"]
  R2 --> R3{"Ошибка?"}
  R3 -->|да| R4["ServerConsole\nили SSH-прогон"]
  R3 -->|нет| R5["BI обновить\nRefresh dataset"]
```

---

## Стек

| Слой | Технология |
|------|------------|
| Источник | REST API CRM |
| ETL | Python 3, requests |
| Запись | gspread / google-auth |
| Расписание | cron на VPS |
| BI | Power BI Import |
| Секреты | JSON + env |

---

## Структура репозитория

```
README.md
LICENSE
.gitignore
rooms_refresh.py          — комнаты + цвет группы
inspections_refresh.py    — fact приёмок
crm_oauth.py              — OAuth и service account
docs/                     — BI-стратегия, DATA-SCHEMA, DIAGRAMS.md
examples/                 — crm_secrets.json.example, env.example
```

---

## Быстрый старт

```bash
export CRM_SECRETS_JSON="./path/to/crm_secrets.json"
export GOOGLE_SERVICE_ACCOUNT_JSON="./path/to/service-account.json"
python3 rooms_refresh.py
python3 inspections_refresh.py
```

На VPS — те же env в `cron.env` или unit-окружении; логи рядом со скриптом.
