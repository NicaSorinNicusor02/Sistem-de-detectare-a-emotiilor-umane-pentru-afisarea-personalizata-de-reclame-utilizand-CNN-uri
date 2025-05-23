import os
from pathlib import Path

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' # l-am adaugat cand am creat reclamele_mele, incarca o reclama noua, deschide tichet

# seteaza calea de baza pentru proiect
BASE_DIR = Path(__file__).resolve().parent.parent

# aecret key(important pentru securitatea aplicatiei)
SECRET_KEY = 'your-secret-key'

DEBUG = True

# lista de domenii si adrese ip permise
ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'accounts.CustomUser'

# Aplicațiile instalate (cele implicite ale Django si cele instalate de mine)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',  # aplicatia customizata pentru conturi
    'website_ads',
    'rosetta',
    'bootstrap4',
]

# MIDDLEWARE, proceseaza cererile HTTP
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]
LANGUAGE_CODE = 'ro'

# URL-root, este folosit pentru paginile site-ului
ROOT_URLCONF = 'website_ads.urls'

# Templatele, epentru interfetele web
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'website_ads.wsgi.application'

# baza de date, am folosit MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'baza_date_website',  # numele bazei de date
        'USER': 'root',  # utilizatorul
        'PASSWORD': 'parola',  # parola
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

#setarile pentru parola utilizatorilor
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#setarile pentru fisiere statice
STATIC_URL = '/static/'

# setarile pentru fisiere media, sunt pentru incarcarea fisierelor de catre useri
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# setarile pentru CSRF
CSRF_TRUSTED_ORIGINS = ['http://localhost', 'https://localhost']

#setarile pentru sesiuni
SESSION_COOKIE_AGE = 3600  # durata sesiunii 3600 secunde/o ora

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"