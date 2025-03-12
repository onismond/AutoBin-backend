from .base import *
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']

CHANNEL_LAYERS = {
    "default": {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        # "CONFIG": {
        #     "hosts": [("127.0.0.1", 6379)],
        # },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

TRUSTPAY_API_KEY = os.environ.get('TRUSTPAY_API_KEY')
TRUSTPAY_API_SECRET = os.environ.get('TRUSTPAY_API_SECRET')
TRUSTPAY_API_URL = os.environ.get('TRUSTPAY_API_URL')
