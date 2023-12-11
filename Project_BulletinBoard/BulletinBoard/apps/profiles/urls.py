from django.urls import path
from .views import RepliesList, action_reply

app_name = 'profiles'
urlpatterns = [
    path('<str:username>/replies', RepliesList.as_view(), name='replies'),
    path('<str:username>/<str:action>', action_reply, name='action_reply'),
]
