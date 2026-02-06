from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@admin.fr', '3RUwJfGr14KWVv0n')
    print('Superuser created successfully!')
else:
    print('Superuser already exists!')