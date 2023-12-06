import os
from celery import Celery
from django.conf import settings

if settings.DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_pillar.settings.dev')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_pillar.settings.prod')


celery = Celery('the_pillar')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
