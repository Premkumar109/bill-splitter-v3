from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils.helpers import dump_request
from .user_helpers import _add_new_user, _delete_existing_user, _update_existing_user, _get_active_user_list, \
    _google_login


@csrf_exempt
def add_user(request):
    try:
        return _add_new_user(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def delete_user(request):
    try:
        return _delete_existing_user(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def update_user(request):
    try:
        return _update_existing_user(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def get_active_user_list(request):
    try:
        return _get_active_user_list(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def google_login(request):
    try:
        return _google_login(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)
