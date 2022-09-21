from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'add_user/', add_user),
    url(r'update_user/', update_user),
    url(r'delete_user/', delete_user),
    url(r'get_active_users/', get_active_user_list),
    url(r'google_login/', google_login)
]
