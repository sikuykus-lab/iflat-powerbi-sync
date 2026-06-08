# Запас прочности — Power BI pipeline

| Ситуация | Поведение |
|----------|-----------|
| OAuth 401 | Падение с traceback в cron.log |
| Пустой ответ API | Не затираем лист целиком без явного флага |
| Rate limit Sheets | batch update, паузы между чанками |
| Долгий прогон | timeout в ServerConsole 2h |
