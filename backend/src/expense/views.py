from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils.helpers import dump_request
from .expense_helper import _get_expenses, _add_expense_in_group, _update_expense, _delete_expense, _settle_expense, \
    _settle_all, _get_expense_details, _get_total_to_pay, _get_total_to_receive, _add_expense_for_user, \
    _get_to_pay_details, _get_to_receive_details


@csrf_exempt
def get_expenses(request):
    try:
        return _get_expenses(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def add_expense_in_group(request):
    try:
        return _add_expense_in_group(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def delete_expense(request):
    try:
        return _delete_expense(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def update_expense(request):
    try:
        return _update_expense(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def settle_expense(request):
    try:
        return _settle_expense(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def settle_all(request):
    try:
        return _settle_all(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def get_expense_details(request):
    try:
        return _get_expense_details(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def get_total_to_receive(request):
    try:
        return _get_total_to_receive(request)
    except Exception as e:
        print(str(e))
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def get_total_to_pay(request):
    try:
        return _get_total_to_pay(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def add_expense_for_user(request):
    try:
        return _add_expense_for_user(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def get_to_pay_details(request):
    try:
        return _get_to_pay_details(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def get_to_receive_details(request):
    try:
        return _get_to_receive_details(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)
