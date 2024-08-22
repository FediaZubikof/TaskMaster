from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Задаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_master.settings')

app = Celery('task_master')

# Загружаем конфигурацию из настроек Django, используя пространство имен CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в установленых приложениях
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
