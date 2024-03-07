from django.urls import path

from .views import new_dialog_view

app_name = 'bot'

_urlpatterns = [
    path('new_dialog/', new_dialog_view, name='new_dialog'),
]


def bot_urls():
    return _urlpatterns, app_name, app_name
