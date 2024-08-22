"""Конфигурация URL диспетчера задач

Список `urlpatterns` направляет URL-адреса в представления. Для получения дополнительной информации см.:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Примеры:
Представления функций
     1. Добавить импорт: из представлений импорта my_app
     2. Добавить URL-адрес в urlpatterns: path('', views.home, name='home')
Представления на основе классов
     1. Добавить импорт: from other_app.views import Home
     2. Добавить URL-адрес в шаблоны URL-адресов: path('', Home.as_view(), name='home')
Включение другой конфигурации URL
     1. Импорт функции include(): из django.urls import include, path
     2. Добавить URL-адрес в urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('accounts/', include('user_accounts.urls')),
                  path('', include('tasks.urls')),
                  path('about/', include('about.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
