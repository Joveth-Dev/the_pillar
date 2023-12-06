from celery.schedules import crontab
import config
from .common import *

# TESTING REVERT WHEN DONE
DEBUG = True  # Should be True

SECRET_KEY = "django-insecure-2ho(1l9=@8o1ml*66l=0xb+w1(s1*6v-z@^+g&t$^^p_zi6x($"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "the_pillar",
        "HOST": "localhost",
        "USER": "root",
        "PASSWORD": "@Sql09518342134",
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# (command) celery -A the_pillar beat
# CELERY_BEAT_SCHEDULE = {
#     'notify_readers': {
#         'task': 'playground.tasks.notify_readers',
#         # 'schedule': crontab(day_of_week=1, hour=7, minute=30) # Monday at 7:30am
#         'schedule': 10,
#         'args': ['Hello Readers!'],
#         # 'kwargs': {}
#     }
# }

# (command) celery -A the_pillar worker --loglevel=info
# "--loglevel=info" is only used in development
CELERY_BROKER_URL = "redis://localhost:6379/1"

# (BGtasks monitoring tool/command) celery -A the_pillar flower
# url: localhost:5555
# ------ UNCOMMENT THIS FOR PRODUCTION TO ENABLE CACHING ------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "TIMEOUT": 3,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
# ------------------------------------------------------------

# EMAIL_HOST = 'localhost'  # smtp4dev
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 2525

# FOR FORGOT PASSOWORD FEATURE
DOMAIN = "127.0.0.1:5500"
EMAIL_HOST_USER = config.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
PASSWORD_RESET_CONFIRM_URL = ("/password/reset/confirm/{uid}/{token}",)

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: True}

CUSTOM_DOMAIN_URL = "http://127.0.0.1:8800"

MEDIA_URL = "/media/"

DATA_UPLOAD_MAX_MEMORY_SIZE = 15728640  # 15MiB
