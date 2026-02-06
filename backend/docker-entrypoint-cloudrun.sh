#!/bin/bash
set -e

echo "🚀 Starting ChatAgentB Backend on Cloud Run..."

# Note: Cloud SQL Proxy is automatically configured by Cloud Run
# No need to wait - Django will retry connections automatically

# Migrations
echo "🔄 Running migrations..."
python manage.py migrate --noinput

# Créer le superuser si spécifié
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "👤 Creating superuser..."
  python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD');
    print('Superuser created successfully');
else:
    print('Superuser already exists');
" || echo "⚠️ Superuser creation skipped"
fi

# Collecte des fichiers statiques
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput || true

# Démarrer l'application avec Gunicorn
echo "🎉 Starting Gunicorn..."
exec gunicorn chatagentb.asgi:application \
  --bind 0.0.0.0:${PORT:-8080} \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --timeout 300 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
