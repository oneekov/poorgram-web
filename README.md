[English](./README_en.md) | Russian

# PoorGram Web
Telegram веб-клиент на Django и Telethon для любого устройства, способного выйти в интернет

## Установка
### 1. Docker
TODO: разобраться с докером, брух
### 2. Ручная установка
### 2.0. Подготовка
1. Установите Python 3.x с официального сайта: https://www.python.org/downloads/
2. Установите Git с официального сайта: https://git-scm.com/downloads
3. Склонируйте репозиторий
```
git clone https://github.com/oneekov/poorgram-web.git
```
4. Получите api_id и api_hash от Telegram (см. https://core.telegram.org/api/obtaining_api_id)
### 2.1. Настройка Python
1. Создайте виртуальное окружение в папке с репозиторием
```
python -m venv .venv
```
*Это необязательно, но рекомендуется, так как у вас могут быть конфликты с версиями библиотек*
2. Войдите в venv
```
source .\.venv\Scripts\activate (если у вас Linux)
.\.venv\Scripts\activate.bat (если у вас командная строка Windows)
.\.venv\Scripts\activate.ps1 (если у вас Powershell)
```
3. Установите зависимости
```
pip install -r requirements.txt
```
4. Создайте в папке core (не core/core, а именно core) файл .env и введите в него следующие данные
```
DJANGO_SECRET_KEY=*случайный набор из 50 букв и цифр*
APIID=*был получен ранее от Telegram, см. пункт 2.0.4*
APIHASH=*аналогично с APIID*
```
### 2.2. Настройка Nginx
TODO: написать пункт 2.2
### 2.3. Развёртывание
В данный момент развернуть PoorGram Web можно при помощи любого удобного WSGI-сервера. Можно также использовать встроенный WSGI-сервер в Django: `python manage.py runserver` (рекомендуется исключительно для разработки, не использовать в продакшене)
TODO: дополнить пункт 2.3