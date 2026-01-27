#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
  sleep 1
done

echo "PostgreSQL is ready!"

# Migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collecte des fichiers statiques
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Création d'un superutilisateur par défaut (optionnel)
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    echo "Creating superuser..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('Superuser created.')
else:
    print('Superuser already exists.')
END
fi

# Démarrage du serveur
exec "$@"
