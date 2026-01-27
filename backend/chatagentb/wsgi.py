"""
WSGI config for chatagentb project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatagentb.settings')

application = get_wsgi_application()
