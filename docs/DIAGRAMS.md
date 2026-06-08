# Диаграммы

Три вида схемы — как в [dataroom-cms](https://github.com/sikuykus-lab/dataroom-cms):
**данные**, **взаимодействие пользователя**, **процессы администратора**.

Рендер: скопировать блок в [mermaid.live](https://mermaid.live).

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

## Процесс пользователя

```mermaid
flowchart LR
  A["Открыл отчёт BI"] --> B["Данные с листов\nвчерашний срез"]
  B --> C["Срез по типу /\nстатусу / дате"]
  C --> D["Решение по\nзаселению / приёмкам"]
```

## Процессы администратора

```mermaid
flowchart TD
  R1["Cron 17:00 / 17:15 UTC"] --> R2["Лог *.cron.log"]
  R2 --> R3{"Ошибка?"}
  R3 -->|да| R4["ServerConsole\nили SSH-прогон"]
  R3 -->|нет| R5["BI обновить\nRefresh dataset"]
```
