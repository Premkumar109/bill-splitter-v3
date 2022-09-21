from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'get_expenses/', get_expenses),
    url(r'add_expense/', add_expense_in_group),
    url(r'update_expense/', update_expense),
    url(r'delete_expense/', delete_expense),
    url(r'settle_expense/', settle_expense),
    url(r'settle_all/', settle_all),
    url(r'get_expense_details/', get_expense_details),
    url(r'get_total_to_receive/', get_total_to_receive),
    url(r'get_total_to_pay/', get_total_to_pay),
    url(r'add_expense_for_user/', add_expense_for_user),
    url(r'get_to_pay_details/', get_to_pay_details),
    url(r'get_to_receive_details/', get_to_receive_details),
]
