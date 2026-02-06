#!/usr/bin/env python
"""
Simple script to create a Django superuser.
Upload this to your Cloud Run service and execute it.
"""

import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatagentb.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "admin"
email = "admin@admin.fr"
password = "3RUwJfGr14KWVv0n"

if User.objects.filter(username=username).exists():
    print(f'⚠️  User "{username}" already exists!')
    user = User.objects.get(username=username)
    print(f"   Email: {user.email}")
    print(f"   Is superuser: {user.is_superuser}")
    print(f"   Is staff: {user.is_staff}")
else:
    user = User.objects.create_superuser(
        username=username, email=email, password=password
    )
    print(f'✅ Superuser "{username}" created successfully!')
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(
        f"\n🔗 Login at: https://chatagentb-backend-548740531838.europe-west1.run.app/admin/"
    )
