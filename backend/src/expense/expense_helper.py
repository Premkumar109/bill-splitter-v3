import json
from django.http import HttpResponse
from datetime import datetime
from utils.helpers import dump_request
from group.models import Group
from .models import Expense, ExpenseGroupUser
from django.db.models import Q, Sum, Count


def _get_expenses(request):
    try:
        _group_id = request.POST.get('groupid')
        group_obj = Group.objects.filter(id=_group_id, is_active=1).first()
        if not group_obj:
            return HttpResponse(dump_request({
                'message': 'Group Does not exist',
                'status': 'fail'
            }), status=400)
        list_expenses = list(ExpenseGroupUser.objects.filter(groupid=group_obj, is_active=1, issettled=0)
                             .values_list('expenseid_id', flat = True))
        if not list_expenses:
            return HttpResponse(dump_request({
                'data': [],
                'status': 'fail'
            }), status=200)
        else:
            final_list_expenses = list(set(list_expenses))
            _expense_obj = Expense.objects.filter(id__in=final_list_expenses, is_active=1)\
                .order_by('-createdtime').values()
            return HttpResponse(dump_request({
                'data': list(_expense_obj),
                'status': 'success'
            }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _get_final_shares(total_amount, type, share_logic):
    try:
        total_amount = float(total_amount)
        final_shares = []
        users = [share['userid'] for share in share_logic]
        if type == 'EQUAL':
            per_amount = float(total_amount/len(users))
            final_shares = [{
                'user': int(user),
                'amount': per_amount
            } for user in users]
        if type == 'PERCENT':
            for share in share_logic:
                user = share['userid']
                final_shares.append({
                    'user': int(user),
                    'amount': float(total_amount*share['percent'])
                })
        return final_shares
    except Exception as e:
        return []


def _add_expense_in_group(request):
    try:
        _userid = request.POST.get('userid')
        _group_id = request.POST.get('groupid')
        _total_amount = request.POST.get('total_amount')
        _share_dict = request.POST.get('share_dict')
        _paid_by = request.POST.get('paidby')
        _expense_name = request.POST.get('expensename')
        _group_obj = Group.objects.filter(id=_group_id).first()
        if None in [_userid, _group_id, _total_amount, _share_dict, _paid_by, _expense_name]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        _dict_share_logic = json.loads(_share_dict)
        share_type = _dict_share_logic['type']
        shared_bw = _dict_share_logic['share']
        _list_final_shares = _get_final_shares(_total_amount, share_type, shared_bw)
        expense_obj = Expense(expensename=_expense_name, totalamount = _total_amount, addedby=_userid,
                              createdtime = datetime.utcnow(), issettled=0, is_active=1)
        expense_obj.save()
        for share in _list_final_shares:
            user_expense = ExpenseGroupUser(expenseid = expense_obj, groupid = _group_obj, paidby= _paid_by,
                                            amountshared=share['amount'], amountowedby=share['user'], is_active=1,
                                            issettled = 0)
            user_expense.save()
        return HttpResponse(dump_request({
            'message': 'Expense Added Successfully',
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _add_expense_for_user(request):
    try:
        _userid = request.POST.get('userid')
        _total_amount = request.POST.get('total_amount')
        _share_dict = request.POST.get('share_dict')
        _paid_by = request.POST.get('paidby')
        _expense_name = request.POST.get('expensename')
        if None in [_userid, _total_amount, _share_dict, _paid_by, _expense_name]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        _dict_share_logic = json.loads(_share_dict)
        share_type = _dict_share_logic['type']
        shared_bw = _dict_share_logic['share']
        _list_final_shares = _get_final_shares(_total_amount, share_type, shared_bw)
        expense_obj = Expense(expensename=_expense_name, totalamount=_total_amount, addedby=_userid,
                              createdtime=datetime.utcnow(), issettled=0, is_active=1)
        expense_obj.save()
        for share in _list_final_shares:
            user_expense = ExpenseGroupUser(expenseid=expense_obj, groupid=None, paidby=_paid_by,
                                            amountshared=share['amount'], amountowedby=share['user'], is_active=1,
                                            issettled=0)
            user_expense.save()
        return HttpResponse(dump_request({
            'message': 'Expense Added Successfully',
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _update_expense(request):
    try:
        _userid = request.POST.get('userid')
        _group_id = request.POST.get('groupid')
        _total_amount = request.POST.get('total_amount')
        _share_dict = request.POST.get('share_dict')
        _paid_by = request.POST.get('paidby')
        _expense_name = request.POST.get('expensename')
        _expense_id = request.POST.get('expenseid')
        _group_obj = Group.objects.filter(id=_group_id).first()
        if None in [_userid, _group_id, _total_amount, _share_dict, _paid_by, _expense_name]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        _dict_share_logic = json.loads(_share_dict)
        share_type = _dict_share_logic['type']
        shared_bw = _dict_share_logic['share']
        _list_final_shares = _get_final_shares(_total_amount, share_type, shared_bw)
        expense_obj = Expense.objects.filter(id=_expense_id)
        expense_obj.update(totalamount = _total_amount)
        for share in _list_final_shares:
            user = share['user']
            ExpenseGroupUser.objects.filter(expenseid = expense_obj.first(), groupid=_group_obj, amountowedby = user)\
                .update(paidby = _paid_by, amountshared=share['amount'], is_active=1, issettled=0)
        return HttpResponse(dump_request({
            'message': 'Expense Updated Successfully',
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _delete_expense(request):
    try:
        _expenseid = request.POST.get('expenseid')
        _userid = request.POST.get('userid')
        if None in [_userid, _expenseid]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        expense_obj = Expense.objects.filter(id=_expenseid)
        ExpenseGroupUser.objects.filter(expenseid=expense_obj.first()).update(is_active=0)
        expense_obj.update(is_active=0)
        return HttpResponse(dump_request({
            'message': 'Expense Deleted Successfully',
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _settle_expense(request):
    try:
        _user_id = request.POST.get('userid')
        _expense_id = request.POST.get('expenseid')
        if None in [_user_id, _expense_id]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        ExpenseGroupUser.objects.filter(expenseid=_expense_id, amountowedby=_user_id).update(issettled = 1)
        return HttpResponse(dump_request({
            'message': 'Expense Settled Successfully',
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _settle_all(request):
    try:
        _user_id = request.POST.get('userid')
        if None in [_user_id]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        ExpenseGroupUser.objects.filter(amountowedby=_user_id).update(issettled=1)
        return HttpResponse(dump_request({
            'message': 'All Expenses Settled',
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _get_expense_details(request):
    try:
        _user_id = request.POST.get('userid')
        _expenseid = request.POST.get('expenseid')
        _group_id = request.POST.get('groupid')
        if None in [_user_id, _expenseid]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        expense_obj = Expense.objects.filter(id=_expenseid)
        group_obj = Group.objects.filter(id=_group_id).first()
        expense_share_details = ExpenseGroupUser.objects.filter(expenseid = expense_obj.first(), groupid = group_obj,
                                                                is_active=1).values()
        expense_details = list(expense_obj.values())[0]
        expense_details['details'] = list(expense_share_details)
        return HttpResponse(dump_request({
            'data': expense_details,
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _build_filter_pay_receive(request):
    try:
        filter_kwargs = {}
        _groupid = request.POST.get('groupid')
        _fromuserid = request.POST.get('fromuser')
        _touserid = request.POST.get('touser')
        if _groupid:
            group_obj = Group.objects.filter(id=_groupid).first()
            filter_kwargs['groupid'] = group_obj
        if _fromuserid:
            filter_kwargs['amountowedby'] = _fromuserid
        if _touserid:
            filter_kwargs['paidby'] = _touserid
        return filter_kwargs
    except Exception as e:
        return {}


def _get_total_to_pay(request):
    try:
        _userid = request.POST.get('userid')
        if None in [_userid]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        kwargs = _build_filter_pay_receive(request)
        group_user_owed = ExpenseGroupUser.objects\
            .filter(~Q(paidby=_userid), amountowedby=_userid, issettled = 0, **kwargs)\
            .aggregate(sum=Sum('amountshared'))
        return HttpResponse(dump_request({
            'data': {
                'total_amount': group_user_owed['sum'],
            },
            'status': 'success'
        }), status=200)
    except Exception as e:
        print(str(e))
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _get_total_to_receive(request):
    try:
        _userid = request.POST.get('userid')
        if None in [_userid]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        kwargs = _build_filter_pay_receive(request)
        group_user_owed = ExpenseGroupUser.objects\
            .filter(~Q(amountowedby=_userid), paidby=_userid, issettled=0, **kwargs)\
            .aggregate(sum=Sum('amountshared'))
        return HttpResponse(dump_request({
            'data': {
                'total_amount': group_user_owed['sum'],
            },
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _get_to_pay_details(request):
    try:
        _userid = request.POST.get('userid')
        _groupid = request.POST.get('groupid')
        if None in [_userid]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        to_pay_details = ExpenseGroupUser.objects \
            .filter(~Q(paidby=_userid), amountowedby=_userid, issettled=0) \
            .values('paidby') \
            .order_by('paidby') \
            .annotate(sum=Sum('amountshared'))
        return HttpResponse(dump_request({
            'data': list(to_pay_details),
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)


def _get_to_receive_details(request):
    try:
        _userid = request.POST.get('userid')
        _groupid = request.POST.get('groupid')
        if None in [_userid]:
            return HttpResponse(dump_request({
                'message': 'Invalid Request',
                'status': 'fail'
            }), status=400)
        to_receive_details = ExpenseGroupUser.objects\
            .filter(~Q(amountowedby=_userid), paidby=_userid, issettled=0)\
            .values('amountowedby')\
            .order_by('amountowedby')\
            .annotate(sum=Sum('amountshared'))
        return HttpResponse(dump_request({
            'data': list(to_receive_details),
            'status': 'success'
        }), status=200)
    except Exception as e:
        error_msg = "Internal Error Occurred"
        return HttpResponse(dump_request({
            'message': error_msg,
            'status': 'fail'
        }), status=500)
