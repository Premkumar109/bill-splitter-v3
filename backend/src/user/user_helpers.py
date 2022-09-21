from django.http import HttpResponse
from billsplitter.settings import CLIENT_ID
from user.models import User
from utils.helpers import dump_request
from google.oauth2 import id_token
from google.auth.transport import requests
import json


def _add_new_user(request):
    try:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return HttpResponse(dump_request({
                'message': 'User Email already exists, please login',
                'status': 'success'
            }), status=409)
        user_obj = User(firstname=first_name, lastname=last_name, email=email, is_active='1')
        _is_success = user_obj.save()
        if _is_success:
            return HttpResponse(dump_request({
                'user_id': user_obj.id,
                'status': 'success'
            }), status=200)
        else:
            return HttpResponse(dump_request({
                'message': 'Invalid User details',
                'status': 'success'
            }), status=422)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _delete_existing_user(request):
    try:
        user_id = request.POST.get('userid')
        if not user_id:
            return HttpResponse(dump_request({
                'message': 'No User ID provided',
                'status': 'fail'
            }), status=400)
        _user_deleted = False
        _message = 'User deleted'
        if User.objects.filter(id=user_id).exists():
            _user_deleted = True
            User.objects.filter(id = user_id).update(is_active = 0)
        if not _user_deleted:
            _message = 'User with ID does not exist'
        return HttpResponse(dump_request({
            'message': _message,
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _update_existing_user(request):
    try:
        _user_id = request.POST.get('userid')
        if not _user_id:
            return HttpResponse(dump_request({
                'message': 'No User ID provided',
                'status': 'fail'
            }), status=400)
        _update_param = request.POST.get('col_name')
        _updated_value = request.POST.get('new_value')
        _user_obj = User.objects.filter(id=_user_id, is_active = 1).first()
        if _user_obj:
            User.objects.filter(id = _user_id).update(**{
                _update_param: _updated_value
            })
        else:
            return HttpResponse(dump_request({
                'message': 'User does not exist',
                'status': 'fail'
            }), status=404)
        return HttpResponse(dump_request({
            'message': 'User Updated Successfully',
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _get_active_user_list(request):
    try:
        _user_data = User.objects.filter(is_active = 1).values_list('firstname', 'lastname', 'email')
        _user_list = list(_user_data)
        return HttpResponse(dump_request({'data': _user_list}), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _google_login(request):
    try:
        body_unicode = request.body
        request = json.loads(body_unicode)
        token = request.get('token')
        try:
            user_data = None
            user_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
            email = user_info.get('email')
            if User.objects.filter(email=email).exists():
                user_data = list(User.objects.filter(email=email).values())[0]
            elif user_info.get('email_verified'):
                user_meta = {
                    'googleid': user_info['sub'],
                    'email': user_info['email'],
                    'pictureurl': user_info['picture'],
                    'firstname': user_info['given_name'],
                    'lastname': user_info['family_name'],
                    'is_active': True
                }
                user_data = User(**user_meta)
                user_data.save()
            if user_data:
                response = {
                    'data': user_data,
                    'status': 'success'
                }
                return HttpResponse(dump_request(response), status=200)
            else:
                error_msg = "Authentication Error Occurred"
                return HttpResponse(dump_request({
                    'message': error_msg,
                    'status': 'fail'
                }), status=400)
        except:
            error_msg = "Authentication Error Occurred"
            return HttpResponse(dump_request({
                'message': error_msg,
                'status': 'fail'
            }), status=400)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)
