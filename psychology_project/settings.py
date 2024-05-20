from pathlib import Path
import os
import logging
from django.utils import timezone

logger = logging.getLogger('usage')


BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates', )
STATIC_DIR = os.path.join(BASE_DIR, 'static')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--b)k5wxa(5l-x#vvfmxcmlzs9i23&#nwrzx*+affy)zl_+f#)4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['sentia.pythonanywhere.com', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'accounts',
    'psychology_tests',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
]

AUTH_USER_MODEL = 'accounts.Users'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "auth.account.middleware.AccountMiddleware",  
    # "allauth.account.middleware.AccountMiddleware",  
]


ROOT_URLCONF = 'psychology_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'psychology_project.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'usage.log',
        },
    },
    'loggers': {
        'usage': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    STATIC_DIR
]
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     BASE_DIR / 'static'
# ]

LOGIN_URL = '/accounts/user_login'
LOGIN_REDIRECT_URL = '/psychology_tests/quiz_list'
LOGOUT_REDIRECT_URL = '/accounts/user_login'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'info.psycho2024@gmail.com' 
EMAIL_HOST_PASSWORD = 'yhiumkikyvsabhhx'

# EMAIL_HOST_USER = 'e0429ri@gmail.com' 
# EMAIL_HOST_PASSWORD = 'ocjgolsdiuyeitpu' 


# BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:8000')

# # settings/production.py
# BASE_URL = 'https://sentia.pythonanywhere.com'

# # settings/development.py
# BASE_URL = 'http://127.0.0.1:8000'

# 遷移先指定
# DEBUG = bool(os.environ.get('DEBUG', False))

if DEBUG:
    BASE_URL = 'http://127.0.0.1:8000'
else:
    BASE_URL = 'https://sentia.pythonanywhere.com'

# メール内のリンク1
LINK_URL_1 = f'{BASE_URL}/psychology_tests/quizzes/quiz_list/'

# もう一つのリンクの設定
LINK_URL_2 = f'{BASE_URL}/accounts/user/'
