import json
from datetime import datetime, date
from decimal import Decimal


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            return super().default(obj)


def dump_request(data):
    return json.dumps(data, cls= JsonEncoder)


def validate_email(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        _valid_email = validate_email(email)
        return True
    except ValidationError:
        return False
