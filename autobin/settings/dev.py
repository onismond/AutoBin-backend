from .base import *

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-g_jmngdghv6ggxkrn2dxbsdf84o^3&7@yw0k21f*yrrd56g50l'

DEBUG = True

ALLOWED_HOSTS = ['*']

CHANNEL_LAYERS = {
    "default": {
        # 'BACKEND': 'channels.layers.InMemoryChannelLayer',
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

TRUSTPAY_API_KEY = 'key'
TRUSTPAY_API_SECRET = 'key'
TRUSTPAY_API_URL = 'key'
TRUSTPAY_API_URL_RETURN = 'key'
