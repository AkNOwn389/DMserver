from __future__ import unicode_literals, absolute_import
from pathlib import Path
from datetime import timedelta
import os, json, sys
import dj_database_url

#BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from os.path import join
from django.core.management.utils import get_random_secret_key
#SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key()) #Always generate
SECRET_KEY = json.loads(open("secretKey.json").read())['SECRET_KEY'] 


DEBUG = True
DEVELOPMENT_MODE = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ["https://d16b-124-105-235-119.ngrok-free.app"]
CORS_ORIGIN_WHITELIST = ["https://d16b-124-105-235-119.ngrok-free.app"]

INSTALLED_APPS = [
    'daphne',
    'rest_framework_simplejwt.token_blacklist',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'cloudinary_storage',
    'django.contrib.admin',
    'django.contrib.auth',
    'django_extensions',
    'rest_framework',
    'Authentication',
    'corsheaders',
    'notifications',
    'cloudinary',
    'comments',
    'profiles',
    'imagekit',
    'myday',
    'users',
    'feeds',
    'chats',
    'posts',
    'news',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
ROOT_URLCONF = 'core.urls'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 36000,
        'KEY_PREFIX': 'django_mail_admin',
    },
    'django_mail_admin': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 36000,
        'KEY_PREFIX': 'django_mail_admin',
    }
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    #'loggers': {'django.db.backends': {'level': 'DEBUG','handlers': ['console'],}},'root': {'handlers': ['console'],'level': 'INFO',},
}


WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'
CHANNEL_LAYERS = {"default": {"BACKEND": "channels_redis.core.RedisChannelLayer","CONFIG": {"hosts": [("127.0.0.1", 6379)],},},}
#CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
#CHANNEL_LAYERS = {"default": {"BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer","CONFIG": {"hosts": [("localhost", 6379)],},},}
DIALOGS_PAGINATION = 50
MESSAGES_PAGINATION = 250
PAGE_LIMIT = 16
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'NIj2ojUWaWaIJUeLPTzG',
        'HOST': 'containers-us-west-109.railway.app',
        'PORT': '6494',
        'ATOMIC_REQUESTS': True,
    }
"""
if DEVELOPMENT_MODE  is True:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'directmessage',
        'USER': 'aknown',
        'PASSWORD': '8]ymiA2anzqrokF2',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
    'read_default_file': '/platform/auth/mysql.conf',
    'charset': 'utf8mb4',
        },
        'ATOMIC_REQUESTS': True,
    },
}
    """
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "example": dj_database_url.parse(os.environ.get("DATABASE_URL"),),
        'default': {
            'ENGINE':  os.getenv("DATABASE_ENGINE"),
            'NAME':  os.getenv("PGDATABASE"),
            'USER':  os.getenv("PGUSER"),
            'PASSWORD': os.getenv("PGPASSWORD"),
            'HOST': os.getenv("PGHOST"),
            'PORT':  os.getenv("PGPORT"),
            'ATOMIC_REQUESTS': True
        }
    }
    """












# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT =os.path.join(BASE_DIR, 'staticfiles')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'EXCEPTION_HANDLER': 'utils.exceptionHandler.custom_exception_handler',
    }

ALGORITHYM = "HS256"
ACCESSTOKEN_LIFE_TIME = timedelta(days=7)
REFRESH_TOKEN_LIFETIME = timedelta(days=30)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": ACCESSTOKEN_LIFE_TIME,
    "REFRESH_TOKEN_LIFETIME": REFRESH_TOKEN_LIFETIME,
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,

    "ALGORITHM": ALGORITHYM,
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "Authentication.serializers.MyTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True



EMAIL_BACKED = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'deejaygabriel776@gmail.com'
EMAIL_HOST_PASSWORD = 'xwfzhflvoeewnmhz'


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dsa3cmwpt',
    'API_KEY': '735453999715484',
    'API_SECRET': 'wobD2XopAYxAdasGI06NaZW4RA0'
}

NEWS_API_KEY = "010922d0ff0f42b8afa7ffcd0ed348db"
NEWS_API_KEY2 = "60c22c7d0eab4637b6263b1b84067351"

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


BASE_URL = "http://localhost:8000"

DEV_SERVER = len(sys.argv) > 1 and sys.argv[1] == "runserver"

USE_NGROK = os.environ.get("USE_NGROK", "False") == "True" and os.environ.get("RUN_MAIN", None) != "true"