import json
from datetime import datetime
from django.http import HttpResponse
from user.models import User
from .models import Group, GroupType, GroupToUser
from utils.helpers import dump_request


def _same_groupname_user_exists(user, group_name):
    try:
        group_name_list = list(GroupToUser.objects.filter(userid = user).values_list('groupid_id__groupname',
                                                                                     flat = True))
        if group_name in group_name_list:
            return True
        return False
    except Exception as e:
        return True


def _create_new_group(request):
    try:
        _user_id = request.POST.get('userid')
        _group_name = request.POST.get('groupname')
        _group_type = request.POST.get('type')
        _purpose = request.POST.get('purpose')
        _user_ids_list = json.loads(request.POST.get('users'))
        group_type_obj = GroupType.objects.filter(id=_group_type).first()
        createdby = User.objects.filter(id = _user_id).first()
        if not _same_groupname_user_exists(createdby, _group_name):
            _group_obj = Group(groupname = _group_name, grouppurpose= _purpose, grouptype=group_type_obj,
                               createdby=createdby, createdat = datetime.utcnow(), is_active=1)
            _group_obj.save()
            _user_ids_list.append(_user_id)
            list_user_obj = User.objects.filter(id__in=_user_ids_list)
            for user_obj in list_user_obj:
                GroupToUser.objects.create(groupid=_group_obj, userid=user_obj)
            return HttpResponse(dump_request({
                'message': 'Group Created Successfully',
                'status': 'success'
            }), status=200)
        else:
            return HttpResponse(dump_request({
                'message': 'Same Name Group already exists for user',
                'status': 'fail'
            }), status=400)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _get_user_groups(request):
    try:
        _user_id = request.POST.get('userid')
        _user = User.objects.filter(id = _user_id, is_active = 1).first()
        if not _user:
            return HttpResponse(dump_request({
                'message': 'User Invalid / Inactive',
                'status': 'fail'
            }), status=400)
        _group_obj_list = GroupToUser.objects.filter(userid=_user).values_list('groupid', flat = True)
        _list_group_ids = list(_group_obj_list)
        _group_data = Group.objects.filter(id__in=_list_group_ids).values()
        return HttpResponse(dump_request({
            'data': list(_group_data),
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _get_group_details(request):
    try:
        _group_id = request.POST.get('groupid')
        _group_obj = Group.objects.filter(id=_group_id, is_active = 1).values()
        _group_details = list(_group_obj)[0]
        if None in [_group_obj]:
            return HttpResponse(dump_request({
                'message': 'User Invalid / Inactive',
                'status': 'fail'
            }), status=400)
        _group_users = GroupToUser.objects.filter(groupid = _group_obj.first()['id'], isactive = 1).values_list('userid', flat = True)
        _list_users = list(_group_users)
        _list_user_objs = list(User.objects.filter(id__in=_list_users).values())
        _group_details['users'] = _list_user_objs
        return HttpResponse(dump_request({
            'data': _group_details,
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _update_group(request):
    try:
        _user_id = request.POST.get('userid')
        _group_id = request.POST.get('groupid')
        _user_obj = User.objects.filter(id=_user_id, is_active=1).first()
        _group_obj = Group.objects.filter(id=_group_id, is_active=1)
        if None in [_user_obj, _group_obj]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        _update_param = request.POST.get('col_name')
        _updated_value = request.POST.get('new_value')
        _group_obj.update(**{
            _update_param: _updated_value
        })
        return HttpResponse(dump_request({
            'message': 'Group Updated Successfully',
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _delete_group(request):
    try:
        _user_id = request.POST.get('userid')
        _group_id = request.POST.get('groupid')
        _user_obj = User.objects.filter(id=_user_id, is_active=1).first()
        _group_obj = Group.objects.filter(id=_group_id, is_active=1)
        if None in [_user_obj, _group_obj]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        _group_obj.update(**{
            'is_active': 0,
            'deletedat': datetime.utcnow()
        })
        return HttpResponse(dump_request({
            'message': 'Group Deleted Successfully',
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _leave_group(request):
    try:
        _user_id = request.POST.get('userid')
        _group_id = request.POST.get('groupid')
        _user_obj = User.objects.filter(id=_user_id, is_active=1).first()
        _group_obj = Group.objects.filter(id=_group_id, is_active=1).first()
        if None in [_user_obj, _group_obj]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        GroupToUser.objects.filter(groupid=_group_obj, userid=_user_obj).update(isactive=0)
        return HttpResponse(dump_request({
            'message': 'Group Left Successfully',
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)

def _remove_member_from_group(request):
    try:
        _user_id = request.POST.get('userid')
        _group_id = request.POST.get('groupid')
        _to_remove_userid = request.POST.get('memberid')
        _user_obj = User.objects.filter(id=_user_id, is_active=1).first()
        _group_obj = Group.objects.filter(id=_group_id, is_active=1).first()
        _member_obj = User.objects.filter(id=_to_remove_userid, is_active=1).first()
        if None in [_user_obj, _group_obj]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        GroupToUser.objects.filter(groupid=_group_obj, userid=_member_obj).update(isactive=0)
        return HttpResponse(dump_request({
            'message': 'Member Removed Successfully',
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _add_new_member(request):
    try:
        _user_id = request.POST.get('userid')
        _group_id = request.POST.get('groupid')
        _to_remove_userid = request.POST.get('memberid')
        _user_obj = User.objects.filter(id=_user_id, is_active=1).first()
        _group_obj = Group.objects.filter(id=_group_id, is_active=1).first()
        _member_obj = User.objects.filter(id=_to_remove_userid, is_active=1).first()
        if None in [_user_obj, _member_obj, _group_obj]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        if GroupToUser.objects.filter(userid=_member_obj, groupid=_group_obj, isactive=1).exists():
            return HttpResponse(dump_request({
                'message': 'Member already exists',
                'status': 'success'
            }), status=400)
        elif GroupToUser.objects.filter(userid=_member_obj, groupid=_group_obj, isactive=0).exists():
            GroupToUser.objects.filter(userid=_member_obj, groupid=_group_obj).update(isactive=1)
        else:
            GroupToUser.objects.create(userid=_member_obj, groupid=_group_obj)
        return HttpResponse(dump_request({
            'message': 'Member Added Successfully',
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)
