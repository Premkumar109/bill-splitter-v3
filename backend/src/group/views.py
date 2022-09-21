from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils.helpers import dump_request
from .group_helpers import _create_new_group, _delete_group, _get_user_groups, _add_new_member, \
    _remove_member_from_group, _update_group, _leave_group, _get_group_details


@csrf_exempt
def create_group(request):
    try:
        return _create_new_group(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def add_member(request):
    try:
        return _add_new_member(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def delete_group(request):
    try:
        return _delete_group(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def get_user_groups(request):
    try:
        return _get_user_groups(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def get_group_details(request):
    try:
        return _get_group_details(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
@csrf_exempt
def leave_group(request):
    try:
        return _leave_group(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def remove_member(request):
    try:
        return _remove_member_from_group(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)


@csrf_exempt
def update_group(request):
    try:
        return _update_group(request)
    except Exception as e:
        return HttpResponse(dump_request({'status': 'fail'}), status=500)
