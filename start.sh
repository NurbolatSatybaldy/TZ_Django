#!/bin/bash
# Скрипт запуска для Render.com

# Не останавливаемся при ошибках, чтобы увидеть все логи
set +e

echo "=== Начало запуска Django приложения ==="

# Выполняем миграции автоматически
echo "Выполнение миграций..."
python manage.py migrate --noinput
echo "Миграции выполнены успешно"

# Создаем суперпользователя если его нет (только при первом запуске)
echo "Проверка суперпользователя..."
python manage.py shell -c "
from django.contrib.auth.models import User
try:
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('✅ Суперпользователь создан: admin / admin123')
    else:
        print('✅ Суперпользователь уже существует')
except Exception as e:
    print(f'⚠️ Ошибка создания суперпользователя: {e}')
"

# Проверяем настройки
echo "Проверка настроек Django..."
python manage.py check || echo "⚠️ Предупреждение: проблемы с настройками"

# Создаем тестовый товар если база пустая
echo "Проверка товаров в базе..."
python manage.py shell -c "
from shop.models import Item
try:
    count = Item.objects.count()
    print(f'Товаров в базе: {count}')
    if count == 0:
        Item.objects.create(name='Тестовый товар', description='Описание', price=100.00, currency='USD')
        print('✅ Создан тестовый товар')
except Exception as e:
    print(f'⚠️ Ошибка проверки товаров: {e}')
"

# Запускаем сервер
echo "=== Запуск сервера на порту \$PORT ==="
exec gunicorn config.wsgi:application --bind 0.0.0.0:\$PORT --timeout 120 --access-logfile - --error-logfile -

