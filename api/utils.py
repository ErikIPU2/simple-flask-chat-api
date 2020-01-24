import sys
from functools import wraps

from flask import request

""" Check if all fields are in form request, if not send a error """
def check_fields(fields: tuple=()):

    def decorator(f):

        @wraps(f)
        def wrap(*args, **kwargs):
            if not fields:
                raise Exception("Expected at least 1 field")

            error_message = {
                "error": "Invalid payload",
                "detail": {}
            }

            has_error: bool = False

            fields_with_content: dict = {}

            # check the valid of each field
            # and add a error if is somenthing wrong
            for field in fields:
                if field not in request.form:
                    error_message['detail'][field] = "This field is required"
                    has_error = True

                elif len(request.form[field]) == 0:
                    error_message['detail'][field] = "This field cannot be empty"
                    has_error = True

                else:
                    fields_with_content[field] = request.form[field]

            # if have some missing field, return the message with 400 response code
            if has_error:
                return error_message, 400
            else:
                kwargs['fields'] = fields_with_content
                return f(*args, **kwargs)

        return wrap
    return decorator