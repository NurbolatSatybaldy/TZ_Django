Django + Stripe — Инструкция для проверяющих

Это тестовое задание: Django‑приложение с интеграцией Stripe Checkout.


1) Деплой (как проверить быстро)

Сайт: `https://<ВАШ_RENDER_URL>.onrender.com`  
Админка: `https://<ВАШ_RENDER_URL>.onrender.com/admin`

Данные для входа в админку
- Логин: `admin`
- Пароль: `admin123`



2) Что проверять (основной функционал)

2.1 Страница товара
Откройте:
- `GET /item/<id>`

Ожидаемо:
- HTML‑страница товара (name/description/price/currency)
- кнопка/ссылка на покупку

Пример:
- `https://<ВАШ_RENDER_URL>.onrender.com/item/1`

2.2 Создание Stripe Checkout Session
Откройте:
- `GET /buy/<id>`

Ожидаемо:
- создаётся Stripe Checkout Session и возвращается `session_id` (или происходит редирект на Stripe Checkout — зависит от реализации)

Пример:
- `https://<ВАШ_RENDER_URL>.onrender.com/buy/1`

2.3 Админ‑панель
Откройте `/admin`, войдите под `admin/admin123`, проверьте:
- наличие модели `Item`
- создание/редактирование `Item`
- что изменения отображаются на странице `/item/<id>`


3) Локальный запуск (если нужно проверить без деплоя)

Вариант A — Docker (рекомендуется)
**Требования:** Docker Desktop

1) В корне проекта:
```bash
docker compose up --build
```

2) Открыть:
- http://localhost:8000
- http://localhost:8000/admin

---

Вариант B — без Docker
**Требования:** Python 3.11+ (или близко), pip

1) Создать и активировать окружение:
```bash
python -m venv .venv
source .venv/bin/activate
```

2) Установить зависимости:
```bash
pip install -r requirements.txt
```

3) Применить миграции:
```bash
python manage.py migrate
```

4) Запустить сервер:
```bash
python manage.py runserver
```

5) Открыть:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/admin


4) Переменные окружения 

Проект читает настройки из env (используется `python-decouple`).

Минимально:
- `DJANGO_SECRET_KEY` — любой секрет
- `DJANGO_DEBUG` — `True`
- `DJANGO_ALLOWED_HOSTS` — `localhost,127.0.0.1`

Stripe (если хотите проверить покупку локально):
- `STRIPE_PUBLISHABLE_KEY_RUB`
- `STRIPE_SECRET_KEY_RUB`
- `STRIPE_PUBLISHABLE_KEY_USD`
- `STRIPE_SECRET_KEY_USD`

Пример (macOS/Linux):
```bash
export DJANGO_SECRET_KEY="dev"
export DJANGO_DEBUG=True
export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"
```


5) Если локально нет админа

Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

Рекомендуемые данные для проверки:
- username: `admin`
- password: `admin123`


6) Кратко по стеку
- Django (web + admin)
- Stripe Checkout (создание Session)
- WhiteNoise (статические файлы в проде)
- Docker / docker-compose
- Gunicorn (в проде)

