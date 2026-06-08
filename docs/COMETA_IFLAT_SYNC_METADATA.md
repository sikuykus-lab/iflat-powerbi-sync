# Метаданные: выгрузка CRM → Google Sheets (`cometa_iflat_sheets_sync.py`)

Документ описывает **откуда берутся данные**, **как они запрашиваются**, **какие константы и переменные окружения управляют поведением**, и **что править**, чтобы изменить фильтры, статусы, таблицу или поля. Рядом лежит модуль `iflat_inspection_labels.py` — подписи типов приёмки по `type_id`.

---

## 1. Файлы и роль

| Файл | Назначение |
|------|------------|
| `cometa_iflat_sheets_sync.py` | Вся логика HTTP к CRM, сбор строк, запись в Google Sheets. |
| `iflat_inspection_labels.py` | Соответствие `type_id` приёмки ↔ человекочитаемое название (`inspection_type_label`). Не трогает API. |

Точка входа: `python3 cometa_iflat_sheets_sync.py` из каталога, где лежит скрипт (или с `PYTHONPATH` к нему).

---

## 2. Целевая таблица Google

Задаётся **жёстко в коде** (менять здесь, если нужна другая книга):

- `SPREADSHEET_ID` — ID документа в URL `docs.google.com/spreadsheets/d/...`
- `WS_ROOMS`, `WS_INSPECTIONS`, `WS_HOUSES`, `WS_REFS` — **числовые id листов** (не имена вкладок). Их можно посмотреть в URL листа или через API.
- Опционально: **`COMETA_WS_STATUSES`** — id отдельного листа для полного списка статусов API (`--only statuses`).

Запись идёт с колонки **B** (столбец A в книге может быть под формулы/служебку).

**Google-учётные данные:** service account JSON — `GOOGLE_SA_JSON` или файл `service-account.json` рядом со скриптом (или `~/Downloads/service-account.json`). У аккаунта должен быть доступ **редактора** к таблице.

---

## 3. Авторизация CRM

1. **OAuth:** `POST https://YOUR_CRM_API_HOST/api/v1/oauth/token` с телом формы из `load_iflat_oauth()` (поля как в `template_b`: `username`, `password`, `account_id`, `client_id`, `client_secret`, `grant_type=login`).
2. Ответ: `access_token` → в заголовок `Authorization: Bearer ...` для всех GET.

**Откуда берутся секреты** (порядок в `load_iflat_oauth()`):

1. `CRM_SECRETS_JSON` — путь к JSON с теми же ключами.
2. Иначе файл `iflat_secrets.json` рядом со скриптом.
3. Иначе разбор `template_b.py`: словарь `data = {...}` внутри `def template_b()` (литералы, без вызовов функций).
4. Иначе переменные `CRM_USERNAME`, `CRM_PASSWORD`, `CRM_ACCOUNT_ID`, `CRM_CLIENT_ID`, `CRM_CLIENT_SECRET`.

Функция: `load_iflat_oauth()` → `iflat_token(sess, oauth)`.

---

## 4. Базовый HTTP к CRM

- База: **`API_BASE = "https://YOUR_CRM_API_HOST/api/v1"`**
- Сессия: `session_headers()` — `User-Agent`, `Accept: application/json`, ретраи на адаптере для 429/5xx.
- Постраничные GET: **`paginate_get(sess, path, params, max_pages=...)`** — ожидает JSON с `data` (список или один объект) и `meta.last_page`; между страницами пауза ~0.05 с.

---

## 5. Embed: что «подмешивается» в ответ API

Чтобы в объектах были вложенные сущности, в query передаётся параметр **`embed`** (строка через запятую).

| Константа | Где используется | Содержимое |
|-----------|------------------|------------|
| `ROOM_EMBED` | `GET /rooms` | `room_type,status,floor,section,house,deal,decoration,tags,custom_fields,sale_type` |
| `HOUSE_EMBED` | `GET /houses` | `district,sections,house_state,floors` (этажи для подписи к `floor_id`, если в комнате пусто) |
| `INSPECTION_EMBED` | `GET /inspections` (отчёт по приёмкам) | `status,responsible,users,room,room.house,room.house.house_state,room.room_type,room.deal,room.decoration,room.custom_fields` |

**Что менять:** если в листе не хватает поля из API — сначала проверьте Swagger CRM, есть ли связь; затем **добавьте имя связи в соответствующий `*_EMBED`**. После этого в `build_room_row` / `build_inspection_row` / `house_row` можно читать новые вложенные поля.

---

## 6. Дома (`GET /houses`)

- Функция: **`fetch_houses`** → `paginate_get(..., "/houses", {"embed": HOUSE_EMBED})`.
- Строка таблицы: **`house_row(h)`** — поля из корня `house` и вложенных `district`, `house_state`, `sections`.

**Ограничение объёма:** переменная **`COMETA_HOUSE_MAX_PAGES`** (целое число страниц) или флаг **`--sample`** (2 страницы).

---

## 7. Справочники

Функция **`fetch_refs`**: несколько GET без пагинации в текущей реализации:

| Ключ в словаре | Endpoint | Назначение |
|----------------|----------|------------|
| `room_types` | `/rooms/types` | Типы помещений |
| `room_statuses` | `/rooms/statuses` | Статусы помещений |
| `inspection_statuses` | `/inspections/statuses` | Статусы приёмок |
| `contract_types` | `/deals/contractTypes` | Типы договора (ДДУ/ДКП и т.д.) |
| `districts` | `GET /districts` (постранично) | Районы/ЖК по `district_id`, если в embed дома нет имени |

После загрузки **домов и комнат** вызывается **`augment_ref_maps_from_entities`**: в `ref_maps` добавляются словари **`house_states`**, **`sale_types`**, **`decorations`** — id→имя из уже полученных вложенных объектов (чтобы подписать id даже без отдельного endpoint).

Лист «Справочники» собирается в **`write_refs_sheet`**: колонка «раздел» + данные из этих списков.

**Добавить новый справочник:** расширьте `fetch_refs` новым `one("/path")` и цикл в `write_refs_sheet` (или отдельный лист — тогда нужен новый `WS_*` и ветка в `main`).

---

## 8. Комнаты (`GET /rooms`)

### 8.1. Фильтр по статусу помещения

Комнаты **не** качаются одним запросом «все». Для каждого **`statusId`** из списка делается отдельная пагинация:

- Список статусов: **`CRM_ROOM_STATUS_IDS`** (строка через запятую).  
  **По умолчанию в коде:** в режиме f17 (`COMETA_F17K3_RELAX_STATUS` не включён) — **`5,6,11,12`**; в relax — тоже **`5,6,11,12`**, если переменная не задана (см. `main()`, `room_statuses`).

Параллельность: **`ROOM_STATUS_WORKERS`** (константа в начале файла, по умолчанию 3) — число одновременных потоков, каждый со своей сессией.

**Как взять другие статусы комнат:** задайте окружение, например:

```bash
export CRM_ROOM_STATUS_IDS=2,4,6
```

или измените значение по умолчанию в `main()` в списке `room_statuses`.

### 8.2. Параметры запроса `/rooms`

Кроме `statusId` и `embed`:

- **`orderBy`: `-updated_at`** — сортировка (можно поменять в `_download_rooms` внутри `paginate_get` params).

### 8.3. Служебное поле

Каждой строке добавляется **`_query_status_id`** — по какому `statusId` запрос пришла эта строка (для отладки; в Google не выводится).

### 8.4. Агрегация клиентских приёмок по `room_id`

После загрузки всех комнат собираются `room_id`, затем:

- Функция **`inspection_stats_by_rooms`**: чанки по **`INSP_CHUNK`** (50 id), параллель **`INSP_WORKERS`** (4).
- Внутри чанка: цикл по страницам **`GET /inspections`** с параметрами:
  - **`roomId`** — список id через запятую
  - **`typeId`: `1`** — **только клиентская приёмка** (жёстко в коде)
  - **`embed`**: `user,responsible,status` (отдельно от основного `INSPECTION_EMBED`)

Результат по каждому `room_id`: **`count`** (число таких приёмок), **`last_user`** (ФИО с последней по `updated_at`/`created_at`).

Дополнительно для ОН со **`status_id == 12`** (синие в колонке «цветовая группа») по **`claims`** в ответе считаются флаги **`blue_claim_inwork`** / **`blue_claim_done`** (см. `F17K3_CLAIM_STATUS_*` в коде).

**Отключить** (быстрее, но в листе «Комнаты» нули/пусто в колонках приёмок):

```bash
export COMETA_SKIP_INSP_STATS=1
```

**Поменять тип приёмки для счётчика:** в **`_insp_chunk_worker`** замените `"typeId": 1` на другой id (см. `iflat_inspection_labels.py`: 1=клиентская, 2=внутренняя, 3=УК).

### 8.5. Справочники для подписей id → текст

Перед сборкой строк **«Комнаты»** и **«Приёмка»** вызывается **`fetch_refs`**, если ещё не загружено (в т.ч. при `--only rooms` / `--only inspections`).

**`build_id_name_maps(refs)`** строит словари `id → name` для:

- `room_statuses`, `room_types`, `inspection_statuses`, `contract_types`

В **`build_room_row`** и **`build_inspection_row`** текст подставляется из вложенных объектов API (`status.name`, `room_type.name`, …), а если пусто — **из справочника по id**.

### 8.6. Custom fields без JSON-столбца

- Колонка **`custom_fields_json` удалена** из выгрузки.
- Список кодов полей задаётся **`COMETA_CF_CODES`** (через запятую). По умолчанию: **`preparation_stage`**.  
  Пустое значение, **`-`** или **`none`** — **не добавлять** столбцы `cf_*`.
- Для каждого кода создаётся столбец **`cf_<code>`** (в имени недопустимые символы заменяются на `_`).
- Для полей типа **list** в значение подставляется **подпись из `options`** по совпадению `value` с `id` опции (как в вашем примере «Выпуск ЭП»).

Добавить поле: `export COMETA_CF_CODES=preparation_stage,другой_code` (коды как в JSON, поле `code`).

### 8.7. Строка листа «Комнаты»

Функция **`build_room_row(room, houses_by_id, insp_stats, ref_maps, cf_codes)`**:

- Подмешивает дом из **`houses_by_id`**, вложенные объекты для подписей.
- **`жк`**: название ЖК / района из embed `house.district` или справочника **`districts`**.
- После **`take_date_from` / `take_date_to`**: **`дата_АПП`**, **`дата_ОАПП`** (`deal.act_date` / `deal.one_sided_act_date`), **`подпись_АПП_или_ОАПП`** (`_deal_app_oapp_label`: **ОАПП** / **АПП** / пусто), **`дата_договора`**, **`кол_во_клиентских_приёмок`**, **`ответственный_последней_приёмки`**, **`дата_оси_заселения`** (`_settlement_axis`).
- Затем **`contract_type_id`**, **`договор_ДДУ_ДКП`** (`_contract_label_deal`), каналы подписания, отделка, **`white_box`**, блок **`cf_*`**, **`статус_дома`**.

Заголовки: **`build_rooms_sheet_header(cf_codes)`** — порядок совпадает с `return` в **`build_room_row`**.

**Добавить колонку:** расширить `build_rooms_sheet_header`, `build_room_row` и при необходимости `ROOM_EMBED`.

---

## 9. Приёмки для листа «Приёмка» (`GET /inspections`)

Функция **`fetch_inspections_report(sess, date_from, date_to, status_ids, max_pages_per_query)`**.

### 9.1. Период дат

В **`main()`** задаётся:

- **`date_from`** — 1 января **текущего года** в формате `dd.mm.yyyy`
- **`date_to`** — **сегодня**

Оба уходят в API как **`takeDateFrom`** / **`takeDateTo`**.

**Изменить период:** правьте блок в `main()` (например, прошлый год, фиксированный квартал) или вынесите в переменные окружения (сейчас не вынесены — потребуется доп. код).

### 9.2. Тип приёмки в запросе

Везде в запросах приёмок для этого отчёта стоит **`typeId: 1`** (клиентская). Это в **`fetch_inspections_report`** и дублируется в **`_insp_chunk_worker`** для агрегации.

**Взять внутренние приёмки в лист:** замените `1` на `2` (и синхронизируйте оба места), либо сделайте цикл по нескольким `typeId` и объединяйте результаты (с дедупликацией по `id`, как сейчас).

### 9.3. Фильтр по статусу приёмки (`statusId`)

Логика в **`main()`** зависит от **`COMETA_F17K3_RELAX_STATUS`**:

| Режим | `CRM_INSPECTION_STATUS_IDS` не задана | `insp_statuses` | Поведение `fetch_inspections_report` |
|-------|------------------------------------------|-----------------|----------------------------------------|
| **f17** (по умолчанию) | да | **`[5, 7, 8]`** | Три запроса: Не принята / Отменена / Принята с замечаниями; затем на лист — только строки с этими `status_id` (`inspection_row_for_template_b_color_export`). |
| **relax** (`COMETA_F17K3_RELAX_STATUS=1`) | да | **`[4, 8]`** | Как раньше: Принята без замечаний и Принята с замечаниями. |
| любой | **непустая** строка, напр. `5,7` | список int | Отдельная пагинация на каждый `statusId`. В режиме **f17** после загрузки строки всё равно фильтруются до **`F17K3_INSPECTION_SHEET_STATUS_IDS`** `{5,7,8}` — при наборе вне этого множества лист может оказаться пустым. |
| любой | **пустая** строка `CRM_INSPECTION_STATUS_IDS=` | `None` | Один запрос **без** `statusId` (все статусы в периоде; осторожно с объёмом). |

**Как взять другие статусы:** например:

```bash
export CRM_INSPECTION_STATUS_IDS=5,6,7
```

или для «все статусы в периоде»:

```bash
export CRM_INSPECTION_STATUS_IDS=
```

Справочник имён статусов — с листа «Справочники» (`inspection_statuses`) или Swagger.

### 9.4. Строка листа «Приёмка»

**`build_inspection_row(inspection, houses_by_id, ref_maps, room_insp_stats_by_id, cf_codes)`** — по встроенной **`room`** вызывается **`build_room_row`** (тот же набор колонок, что лист «Комнаты»), затем в конец добавляется **`дата_обновления`**: **`format_date(inspection.get("updated_at"), missing="-")`**.

Заголовки: **`build_inspections_sheet_header(cf_codes)`** = **`build_rooms_sheet_header(cf_codes)`** + **`["дата_обновления"]`**.

При **`--only inspections`** при необходимости подгружаются **дома** (`fetch_houses`), чтобы слияние `house` с `houses_by_id` совпадало с листом «Комнаты».

Подпись типа приёмки в колонках **не выводится** (лист совпадает с «Комнатами»); тип по-прежнему участвует в **`fetch_inspections_report`** (`typeId: 1` и т.д., см. §9.2).

## 10. Вычисляемые поля (кратко, где править)

| Логика | Функция | Комментарий |
|--------|---------|-------------|
| ДДУ/ДКП по `contract_type_id` | `_contract_label_deal`, `_deal_contract_type_id` | Сначала 1→ДДУ, 2→ДКП; иначе имя из справочника `contract_types`. |
| Подписание ЭЦП/бумага | `_sign_channel_value`, `_deal_sign_type`, `_deal_inspection_sign_type`, `_signing_group_from_channels` | Столбцы `sign_type`, `inspection_sign_type`; группа «ЭЦП (ЭДО)» / «бумага». |
| Цветовая группа (лист Комнаты) | `room_f17_color_single` | Красные при `status_id==5` помещения; зелёные **6 и 11**; синие **12**; иначе красные при **`has_red_insp`** (подмес по приёмке «Не принята»). Константы: `F17K3_ROOM_STATUS_*`. |
| Цветовая группа (лист Приёмка) | `room_f17_color_single` в **`build_room_row`** | Те же столбцы, что «Комнаты»; цвет по статусу помещения и агрегату `room_id`. |
| White box | `white_box_flag` | Эвристика по отделке, тегам, `custom_fields`, текстам. |
| Дата в таблице | `format_date(..., missing=...)` | Как `Rooms_Refresh.format_date`: ISO / timestamp / строки → `DD.MM.YYYY`; для осей сделки, `take_date_*` и дат приёмки пусто/ошибка → `-` (параметр `missing`). |
| Адрес дома в строках ОН/приёмки | `_house_address_display` | `address` → `full_address` → `street` + `, д.{house}` (паритет с `Rooms_Refresh`). |
| Ось заселения для BI | `_settlement_axis` | Приоритет `take_date_to`, иначе `take_date_from`; значения `-` считаются пустыми. |
| АПП / ОАПП по датам сделки | `_deal_app_oapp_label` | По `deal`: при валидной `one_sided_act_date` → **ОАПП**, иначе при валидной `act_date` → **АПП**, иначе **пусто**. |

Паритет с серверными `Rooms_Refresh.py` / `Acceptance_Refresh.py` в `/opt/scripts` (целевая схема колонок — как в §8–9 этого файла).

Любое из этих правил меняется **только в Python**, не в Google.

---

## 11. Запись в Google Sheets

- Клиент: **`gspread`** + **`oauth2client`** service account.
- Надёжность: **`google_retry`**, параметры `COMETA_GOOGLE_*`, `COMETA_SHEETS_*` (см. docstring в начале `cometa_iflat_sheets_sync.py`).
- Основная запись: **`write_sheet_with_header`** — пакетно через **`worksheet.batch_update`** (несколько диапазонов за один вызов API), если не включён `COMETA_SHEETS_LEGACY_UPDATES=1`.
- Справочники: **`write_refs_sheet`** — сначала `clear`, затем одна заливка диапазона.
- Каталог статусов API (`--only statuses`, лист id из **`COMETA_WS_STATUSES`**): **`build_status_catalog_rows`** + **`write_sheet_with_header`** — строки с `категория` = `rooms` / `inspections` и полями из `/rooms/statuses` и `/inspections/statuses`.

## 12. Запуск по расписанию и из Telegram

**Команда в shell (сервер):**

```bash
/opt/scripts/run_cometa_iflat_sync.sh
```

Скрипт пишет лог в `cometa_iflat_sync.log` в той же папке (переопределение: `COMETA_CRM_SYNC_LOG`). Рабочий каталог и путь к `cometa_iflat_sheets_sync.py` задаются переменными `COMETA_CRM_SYNC_DIR`, `COMETA_CRM_SYNC_SCRIPT` (см. `run_cometa_iflat_sync.sh` в каталоге Google Sheets в репозитории).

**Cron (пример, каждый день в 20:00):**

```cron
0 20 * * * /opt/scripts/run_cometa_iflat_sync.sh
```

**Telegram — бот вех** (`/root/tg_manager/main.py`, `tg_bot.service`): кнопки **«Refresh Rooms»** и **«Accept Rooms»** запускают `Rooms_Refresh.py` и `Acceptance_Refresh.py` в `/opt/scripts` (рабочий каталог: **`ILFLAT_SCRIPTS_CWD`** или **`COMETA_CRM_SYNC_DIR`** для совместимости). В чат — хвост stdout (до ~3500 символов) и код выхода. Полный `cometa_iflat_sheets_sync.py` из этого бота **не** вызывается.

**Telegram — ServerConsoleBot** (`/root/ServerConsoleBot/`, см. `scripts.json`): отчёты **template_b** / **template_a** и те же **Refresh Rooms** / **Accept Rooms** по отдельным правам пользователя. Владелец: **Настройки** → «Права пользователей (скрипты)» — в любой момент список одобренных пользователей и галочки по скриптам; **Конструктор** — у каждого пользователя видимость кнопок скриптов и служебных («Расписание», «Закрыть», для владельца «Настройки»); кнопка «Конструктор» в reply-клавиатуре всегда видна.

---

## 13. Режимы запуска

| Команда | Эффект |
|---------|--------|
| `python3 cometa_iflat_sheets_sync.py` | Полный цикл + запись в Google. |
| `python3 cometa_iflat_sheets_sync.py --only rooms` | Только комнаты (и нужные для них данные внутри ветки `main`). |
| `--only inspections` / `houses` / `refs` / `statuses` | Частичное обновление листов. Для `statuses` задайте **`COMETA_WS_STATUSES`** (id вкладки). |
| `--dry-run` | **Без Google**; в JSON (`COMETA_SYNC_REPORT` или `./cometa_sync_dry_run_report.json`) сводка **`build_analytics_report`**. |
| `--sample` | Урезанные страницы API (быстрая проверка). |

---

## 14. Чеклист: «хочу изменить X»

| Задача | Где смотреть |
|--------|----------------|
| Другая Google-таблица / лист | `SPREADSHEET_ID`, `WS_*` |
| Другие статусы **комнат** в выборке | `CRM_ROOM_STATUS_IDS` или дефолт в `main()` |
| Другие статусы **приёмок** в листе | `CRM_INSPECTION_STATUS_IDS`; в f17 без переменной — **`5,7,8`**; в relax — **`4,8`**; пустая строка = все в периоде |
| Другой период приёмок | `date_from` / `date_to` в `main()` |
| Внутренние приёмки вместо клиентских | `typeId` в `fetch_inspections_report` и `_insp_chunk_worker` |
| Больше полей из API | `ROOM_EMBED` / `INSPECTION_EMBED` / `HOUSE_EMBED` + строки сборки |
| Новый столбец в листе | `build_rooms_sheet_header` / `build_inspections_sheet_header` + `build_*_row` |
| Какие custom fields вынести в колонки | **`COMETA_CF_CODES`** (коды из `custom_fields[].code`) |
| Меньше нагрузки на Google | `COMETA_SHEETS_CHUNK`, паузы, `COMETA_GOOGLE_RETRIES` |
| Не считать приёмки по комнатам | `COMETA_SKIP_INSP_STATS=1` |

---

## 15. Отладка без записи в таблицу

```bash
export CRM_SECRETS_JSON=/path/to/secrets.json   # или локальные template_b / iflat_secrets.json
python3 cometa_iflat_sheets_sync.py --dry-run --sample
```

В JSON смотрите `samples.room_api_keys`, `inspection_api_keys`, счётчики и `recommendations` — так видно, какие поля реально приходят от API.

---

*Файл согласован с логикой `cometa_iflat_sheets_sync.py` и `iflat_inspection_labels.py`. При больших изменениях кода имеет смысл обновить этот документ.*
