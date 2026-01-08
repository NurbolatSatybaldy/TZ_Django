Django + Stripe API Тестовое задание

Простой Django сервер с интеграцией Stripe для создания платежных форм.

## Функционал

### Основные возможности:
- Модель `Item` с полями (name, description, price, currency)
- API эндпоинты:
  - `GET /item/{id}` - получение HTML страницы с информацией о товаре и кнопкой покупки
  - `GET /buy/{id}` - получение Stripe Session ID для оплаты товара
- Интеграция со Stripe Checkout для обработки платежей

### Бонусные возможности:
- Docker и docker-compose для запуска
- Использование environment variables для конфигурации
- Django Admin панель для управления моделями
- Модель `Order` для объединения нескольких товаров
- Модели `Discount` и `Tax` для применения скидок и налогов в Stripe
- Поддержка мультивалютности (USD и RUB) с разными Stripe ключами

## Установка и запуск

### Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd TZ_
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

5. Заполните `.env` файл своими Stripe ключами:
```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

STRIPE_PUBLISHABLE_KEY_USD=pk_test_your_usd_publishable_key
STRIPE_SECRET_KEY_USD=sk_test_your_usd_secret_key

STRIPE_PUBLISHABLE_KEY_RUB=pk_test_your_rub_publishable_key
STRIPE_SECRET_KEY_RUB=sk_test_your_rub_secret_key
```

6. Выполните миграции:
```bash
python manage.py migrate
```

7. Создайте суперпользователя для доступа к админ-панели:
```bash
python manage.py createsuperuser
```

8. Запустите сервер:
```bash
python manage.py runserver
```

Сервер будет доступен по адресу: http://localhost:8000

### Запуск через Docker

1. Создайте файл `.env` (см. шаг 4 выше)

2. Запустите через docker-compose:
```bash
docker-compose up --build
```

3. Выполните миграции в контейнере:
```bash
docker-compose exec web python manage.py migrate
```

4. Создайте суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

Сервер будет доступен по адресу: http://localhost:8000

## Использование

### Доступ к админ-панели

Админ-панель доступна по адресу: http://localhost:8000/admin/

Войдите с учетными данными суперпользователя, созданного ранее.

### Создание товаров

1. Перейдите в админ-панель: http://localhost:8000/admin/
2. Откройте раздел "Товары" (Items)
3. Нажмите "Добавить товар"
4. Заполните поля:
   - Название
   - Описание
   - Цена
   - Валюта (USD или RUB)
5. Сохраните товар

### Просмотр товара и покупка

1. Откройте в браузере: http://localhost:8000/item/1/ (где 1 - ID товара)
2. На странице отобразится информация о товаре и кнопка "Купить"
3. При нажатии на кнопку произойдет редирект на Stripe Checkout форму

### API эндпоинты

#### Получить HTML страницу товара:
```bash
curl http://localhost:8000/item/1/
```

#### Получить Stripe Session ID для оплаты:
```bash
curl http://localhost:8000/buy/1/
```

Ответ:
```json
{"id": "cs_test_..."}
```

### Работа с заказами

1. В админ-панели создайте заказ (Order)
2. Добавьте несколько товаров в заказ
3. При необходимости добавьте скидку (Discount) и налог (Tax)
4. Для оплаты заказа используйте эндпоинт: `/order/{id}/buy/`

### Настройка скидок и налогов в Stripe

Для использования скидок и налогов необходимо:

1. Создать купон в Stripe Dashboard (для скидок)
2. Создать налоговую ставку в Stripe Dashboard (для налогов)
3. В админ-панели Django создать запись Discount или Tax с соответствующим Stripe ID

## Структура проекта

```
TZ_/
├── config/              # Настройки Django проекта
│   ├── settings.py      # Основные настройки
│   ├── urls.py          # Главный URL конфиг
│   └── wsgi.py          # WSGI конфигурация
├── shop/                # Основное приложение
│   ├── models.py        # Модели данных
│   ├── views.py         # Представления (views)
│   ├── urls.py          # URL маршруты приложения
│   └── admin.py         # Настройки админ-панели
├── templates/           # HTML шаблоны
│   └── shop/
│       └── item_detail.html
├── manage.py            # Django управляющий скрипт
├── requirements.txt     # Зависимости Python
├── Dockerfile           # Конфигурация Docker образа
├── docker-compose.yml   # Конфигурация Docker Compose
├── .env.example         # Пример файла с переменными окружения
└── README.md            # Документация
```

## Тестирование

Для тестирования используйте тестовые ключи Stripe (начинаются с `pk_test_` и `sk_test_`).

Тестовые карты для Stripe:
- Успешная оплата: `4242 4242 4242 4242`
- Отклоненная карта: `4000 0000 0000 0002`

## Развертывание на сервере (Онлайн публикация)

Для выполнения требования "Опубликовать свое решение онлайн" нужно развернуть приложение на публичном хостинге. Ниже инструкции для популярных платформ:

### Деплой на Railway (Рекомендуется - бесплатный тариф)

1. Зарегистрируйтесь на https://railway.app
2. Создайте новый проект и подключите ваш GitHub репозиторий
3. Railway автоматически определит Django проект
4. Добавьте переменные окружения в настройках проекта:
   ```
   DJANGO_SECRET_KEY=ваш-секретный-ключ
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=ваш-домен.railway.app
   STRIPE_PUBLISHABLE_KEY_USD=pk_test_...
   STRIPE_SECRET_KEY_USD=sk_test_...
   STRIPE_PUBLISHABLE_KEY_RUB=pk_test_...
   STRIPE_SECRET_KEY_RUB=sk_test_...
   ```
5. Railway автоматически запустит деплой
6. После деплоя выполните миграции через Railway CLI или добавьте команду в настройки:
   ```bash
   railway run python manage.py migrate
   railway run python manage.py createsuperuser
   ```
7. Получите URL вашего приложения (например: `https://your-app.railway.app`)

### Деплой на Render

1. Зарегистрируйтесь на https://render.com
2. Создайте новый Web Service и подключите GitHub репозиторий
3. Настройки:
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
4. Добавьте переменные окружения в разделе Environment
5. После деплоя выполните миграции через Shell:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

### Деплой на Heroku

1. Установите Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Войдите в Heroku:
   ```bash
   heroku login
   ```
3. Создайте приложение:
   ```bash
   heroku create your-app-name
   ```
4. Добавьте переменные окружения:
   ```bash
   heroku config:set DJANGO_SECRET_KEY=ваш-ключ
   heroku config:set DJANGO_DEBUG=False
   heroku config:set DJANGO_ALLOWED_HOSTS=your-app-name.herokuapp.com
   heroku config:set STRIPE_PUBLISHABLE_KEY_USD=pk_test_...
   heroku config:set STRIPE_SECRET_KEY_USD=sk_test_...
   ```
5. Деплой:
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### Деплой на собственном VPS (DigitalOcean, AWS, etc.)

1. Подключитесь к серверу по SSH
2. Установите зависимости:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```
3. Клонируйте репозиторий и настройте:
   ```bash
   git clone <your-repo-url>
   cd TZ_
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. Настройте переменные окружения в `.env`
5. Выполните миграции и создайте суперпользователя
6. Настройте systemd service для gunicorn
7. Настройте nginx как reverse proxy

### После деплоя

1. Обновите `DJANGO_ALLOWED_HOSTS` с вашим доменом
2. Установите `DJANGO_DEBUG=False` для production
3. Проверьте работу всех эндпоинтов
4. Предоставьте ссылку на работающее приложение и данные для входа в админ-панель

## Технические детали

- Django 5.0+
- Stripe API для обработки платежей
- SQLite база данных (по умолчанию)
- Поддержка мультивалютности через разные Stripe аккаунты/ключи

## Лицензия

Тестовое задание для отбора кандидатов.



## Deploy на Render

Проект уже содержит `render.yaml`, `Dockerfile` и `start.sh`, поэтому деплой делается через Render Blueprint:

1. Залей репозиторий в GitHub.
2. В Render выбери **New → Blueprint** и укажи репозиторий.
3. При создании Blueprint Render попросит ввести секреты (`sync: false`) — укажи Stripe ключи.
4. После деплоя приложение будет доступно по `.onrender.com` домену.

Переменные окружения (минимум):
- `DJANGO_SECRET_KEY` (генерируется автоматически в Blueprint)
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS` (добавь твой домен + `.onrender.com`)
- `STRIPE_PUBLISHABLE_KEY_USD`, `STRIPE_SECRET_KEY_USD`
- `STRIPE_PUBLISHABLE_KEY_RUB`, `STRIPE_SECRET_KEY_RUB`

Примечание: по умолчанию используется SQLite. Для настоящего продакшна лучше подключить Postgres и переключить настройки базы.

В этом репозитории `render.yaml` уже **создаёт Postgres** (ресурс `tz-django-db`) и прокидывает его URL в переменную `DATABASE_URL`. Чтобы Django реально начал использовать Postgres, в `config/settings.py` (или где у тебя `DATABASES`) должно быть чтение `DATABASE_URL` через `dj-database-url`.

⚠️ Важно: **Free Postgres на Render автоматически истекает через 30 дней** (после этого база недоступна, пока не обновишь план). Для учебного/пет-проекта ок; для продакшна — сразу выбирай платный план. 
