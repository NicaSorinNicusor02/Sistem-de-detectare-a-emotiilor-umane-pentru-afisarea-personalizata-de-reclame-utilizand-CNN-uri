"""
WSGI config for website_ads project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from website_ads.admin import admin_site
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_ads.settings')

application = get_wsgi_application()
admin_site.name = 'admin'