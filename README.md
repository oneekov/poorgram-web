# Poorgram Web
[EN] (./README_EN.)
Клиент для любой картошки на Flask & Telethon
## Что это?
Если кратко, то это Telegram клиент в браузере, но все действия выполняются на сервере, клиент лишь отдаёт команды. Благодаря этому, можно использовать Telegram на устаревших телефонах, которые не имеют какой-либо реализации MTProto и/или могут вовсе её не потянуть. Наглядный аналог проекта - MPGram.
## Развёртывание через Docker
Для разработки: `docker compose up -d --build`. Стандартный docker-compose сильно упрощён и почти не отличается от `pip install -r requirements.txt && python app.py`.
Для продакшена используется docker-compose-prod.yml: `docker compose -f docker-compose-prod.yml up -d --build`. Тут используется gunicorn, nginx и добавлены healthcheck.
**ВАЖНО:** По умолчанию, в продакшене нет HTTPS. Если вам нужен HTTPS, то скопируйте сертификат и ключ в папку nginx (как cert.crt и private.key соответственно) и отредактируйте yml и nginx.conf для работы с HTTPS (можно расдокументировать уже имеющиеся части кода)
