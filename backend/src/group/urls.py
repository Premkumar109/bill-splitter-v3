from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'create_group/', create_group),
    url(r'add_member/', add_member),
    url(r'delete_group/', delete_group),
    url(r'leave_group/', leave_group),
    url(r'remove_member/', remove_member),
    url(r'update_group/', update_group),
    url(r'get_user_groups/', get_user_groups),
    url(r'get_group_details/', get_group_details),
]
