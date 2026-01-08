#!/usr/bin/env bash
# Production старт-скрипт (Render / Docker)
set -euo pipefail

echo "=== Django boot ==="

# Render sets $PORT (default 10000). For local docker-compose we can set PORT=8000.
PORT="${PORT:-10000}"
export PORT

# Optional toggles (safe defaults)
RUN_COLLECTSTATIC="${RUN_COLLECTSTATIC:-1}"
RUN_MIGRATIONS="${RUN_MIGRATIONS:-1}"
DJANGO_CHECK_DEPLOY="${DJANGO_CHECK_DEPLOY:-0}"

echo "Using PORT=$PORT"

if [[ "${RUN_MIG
UN_MIGRATIONS}" == "1" ]]; then
  echo "Running migrations..."
  python manage.py migrate --noinput
fi

if [[ "${RUN_COLLECTSTATIC}" == "1" ]]; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput || true
fi

if [[ "${DJANGO_CHECK_DEPLOY}" == "1" ]]; then
  echo "Running Django system checks..."
  python manage.py check --deploy || true
fi

# Optional: create/ensure superuser ONLY if explicitly enabled and credentials provided
# This version is safe for free Render (no shell needed) and also can reset password.
CREATE_SUPERUSER="${CREATE_SUPERUSER:-0}"
if [[ "${CREATE_SUPERUSER}" == "1" ]]; then
  echo "CREATE_SUPERUSER=1: ensuring superuser exists (and syncing password)..."
  python manage.py shell -c "
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv('DJANGO_SUPERUSER_USERNAME')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', '')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

if not username or not password:
    raise SystemExit('Set DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD (and optionally DJANGO_SUPERUSER_EMAIL).')

user, created = User.objects.get_or_create(username=username, defaults={'email': email})

# Ensure permissions
user.is_staff = True
user.is_superuser = True

# Sync email if provided
if email:
    user.email = email

# Always set password (useful to reset access without shell)
user.set_password(password)
user.save()

print('Superuser ensured:', username, 'created=' + str(created))
"
fi

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT}" \
  --workers "${GUNICORN_WORKERS:-2}" \
  --threads "${GUNICORN_THREADS:-4}" \
  --timeout "${GUNICORN_TIMEOUT:-120}" \
  --access-logfile "-" \
  --error-logfile "-"