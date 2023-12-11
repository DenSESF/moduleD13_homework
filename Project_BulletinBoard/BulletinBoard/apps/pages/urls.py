from django.urls import path
from .views import PostsList, PostDetail, PostDelete, PostCreate, PostEdit, ReplyCreate

app_name = 'pages'
urlpatterns = [
    path('', PostsList.as_view(), name='advert_all'),
    path('advert/<int:pk>', PostDetail.as_view(), name='advert_detail'),
    path('advert/<int:pk>/delete', PostDelete.as_view(), name='advert_delete'),
    path('advert/create', PostCreate.as_view(), name='advert_create'),
    path('advert/<int:pk>/edit', PostEdit.as_view(), name='advert_edit'),
    path('advert/<int:pk>/send_reply', ReplyCreate.as_view(), name='advert_reply'),
]