import os
from django.core.wsgi import get_wsgi_application
from website_ads.admin import admin_site
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_ads.settings')
application = get_wsgi_application()
admin_site.name = 'admin'
