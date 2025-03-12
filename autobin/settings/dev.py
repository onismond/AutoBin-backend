from .base import *

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-g_jmngdghv6ggxkrn2dxbsdf84o^3&7@yw0k21f*yrrd56g50l'

DEBUG = True

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

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

TRUSTPAY_API_KEY = 'key'
TRUSTPAY_API_SECRET = 'key'
TRUSTPAY_API_URL = 'key'
