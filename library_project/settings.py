"""
Django settings for library_project project.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-9x@3!k8p^mz4vq#l5h&j@n$w6r*t2y+u7i1o0p4a8s(d=f-g+c'

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library_app',  # Наше приложение для системы управления библиотекой
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'library_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Кастомные шаблоны проекта
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

WSGI_APPLICATION = 'library_project.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'ru-ru'  # Русский язык

TIME_ZONE = 'Europe/Moscow'  # Московское время

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Дополнительные директории со статическими файлами
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Директория для сбора статических файлов (для продакшена)
STATIC_ROOT = BASE_DIR / "staticfiles"


# Media files (User uploads)
MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Authentication settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'catalog'
LOGOUT_REDIRECT_URL = 'home'


# Session settings
SESSION_COOKIE_AGE = 1209600  # 2 недели в секундах
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_NAME = 'library_sessionid'
SESSION_COOKIE_SECURE = False  # True для продакшена с HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'


# CSRF settings
CSRF_COOKIE_NAME = 'library_csrftoken'
CSRF_COOKIE_HTTPONLY = False


# Messages framework (для совместимости с Bootstrap)
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',  # 'danger' для совместимости с Bootstrap
}


# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 МБ
DATA_UPLOAD_MAX_MEMORY_SIZE = 15728640  # 15 МБ


# Логирование (упрощённая конфигурация без файлового хендлера)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'library_app': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


# Custom application settings
MAX_BOOKS_PER_READER = 5          # Макс. книг на одного читателя
DEFAULT_BOOK_LOAN_PERIOD = 14     # Срок выдачи по умолчанию (дней)
FINE_PER_DAY = 10                 # Штраф за день просрочки (руб.)
REMINDER_DAYS_BEFORE = 3          # За сколько дней напоминать о возврате