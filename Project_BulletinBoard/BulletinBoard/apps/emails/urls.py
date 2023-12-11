from django.urls import path

from .views import News, NewsSuccess


app_name = 'emails'
urlpatterns = [
    path('newsletter/', News.as_view(), name='newsletter'),
    path('newsletter/send_success/', NewsSuccess.as_view(), name='send_success'),
]