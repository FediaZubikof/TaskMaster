"""
Конфигурация WSGI.

Он предоставляет вызываемый WSGI как переменную уровня модуля с именем ``application``.

Дополнительные сведения об этом файле см.
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_master.settings')

application = get_wsgi_application()
