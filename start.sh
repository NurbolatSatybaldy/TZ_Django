#!/bin/bash
# Скрипт запуска для Render.com

# Выполняем миграции автоматически
python manage.py migrate --noinput

# Создаем суперпользователя если его нет (только при первом запуске)
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Суперпользователь создан: admin / admin123')
else:
    print('Суперпользователь уже существует')
"

# Запускаем сервер
exec gunicorn config.wsgi:application --bind 0.0.0.0:\$PORT

