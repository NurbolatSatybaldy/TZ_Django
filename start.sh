#!/bin/bash
# Скрипт запуска для Render.com

set -e  # Остановка при ошибке

echo "Начало запуска..."

# Выполняем миграции автоматически
echo "Выполнение миграций..."
python manage.py migrate --noinput || echo "Предупреждение: ошибка миграций"

# Создаем суперпользователя если его нет (только при первом запуске)
echo "Проверка суперпользователя..."
python manage.py shell -c "
from django.contrib.auth.models import User
try:
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Суперпользователь создан: admin / admin123')
    else:
        print('Суперпользователь уже существует')
except Exception as e:
    print(f'Ошибка создания суперпользователя: {e}')
" || echo "Предупреждение: ошибка создания суперпользователя"

# Проверяем настройки
echo "Проверка настроек..."
python manage.py check --deploy || echo "Предупреждение: проблемы с настройками"

# Запускаем сервер
echo "Запуск сервера на порту \$PORT..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:\$PORT --timeout 120

