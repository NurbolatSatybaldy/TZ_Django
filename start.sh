#!/usr/bin/env bash
set -euo pipefail

echo "=== Django boot ==="

PORT="${PORT:-10000}"
export PORT

RUN_COLLECTSTATIC="${RUN_COLLECTSTATIC:-1}"
RUN_MIGRATIONS="${RUN_MIGRATIONS:-1}"
DJANGO_CHECK_DEPLOY="${DJANGO_CHECK_DEPLOY:-0}"

echo "PORT=$PORT"

if [[ "${RUN_MIGRATIONS}" == "1" ]]; then
  echo "Миграции..."
  python manage.py migrate --noinput
fi

if [[ "${RUN_COLLECTSTATIC}" == "1" ]]; then
  echo "Статика..."
  python manage.py collectstatic --noinput || true
fi

if [[ "${DJANGO_CHECK_DEPLOY}" == "1" ]]; then
  echo "Проверки..."
  python manage.py check --deploy || true
fi

CREATE_SUPERUSER="${CREATE_SUPERUSER:-0}"
if [[ "${CREATE_SUPERUSER}" == "1" ]]; then
  echo "Админ..."
  python manage.py shell -c "
import os
from django.contrib.auth import get_user_model

User = get_user_model()
u = os.getenv('DJANGO_SUPERUSER_USERNAME')
p = os.getenv('DJANGO_SUPERUSER_PASSWORD')
e = os.getenv('DJANGO_SUPERUSER_EMAIL', '')

if not u or not p:
    raise SystemExit('Нужны DJANGO_SUPERUSER_USERNAME и DJANGO_SUPERUSER_PASSWORD')

user, created = User.objects.get_or_create(username=u, defaults={'email': e})
user.is_staff = True
user.is_superuser = True
if e:
    user.email = e
user.set_password(p)
user.save()
print('OK:', u, 'created=' + str(created))
"
fi

echo "Gunicorn..."
exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT}" \
  --workers "${GUNICORN_WORKERS:-1}" \
  --threads "${GUNICORN_THREADS:-4}" \
  --timeout "${GUNICORN_TIMEOUT:-120}" \
  --access-logfile "-" \
  --error-logfile "-"