from rest_framework.views import exception_handler
from django.http import JsonResponse


def custom_exception_handler(exc, context):
    handlers = {
        #'ValidationError': _handler_generic_error,
        'Http404':_handle_http404__error,
        'PermissionDenied':_handler_generic_error,
        'NotAuthenticated':_handle_authentication_error,
        'Unauthorized':_handle_authentication_error,
        'AuthenticationFailed':_handle_invalidated_,
        'TypeError':_handle_Type__error_,
        'InvalidToken': _handle_invalidated_,
        'MethodNotAllowed': _handle_method_error_,
        'DoesNotExist': _handle_http404__error,
        'UnicodeDecodeError': _handle_unicodeError__,
        'InvalidToken': __handle_invalid_token__,
    }

    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    exception_class = exc.__class__.__name__
    print(f"\033[1;91mException detected: \033[1;93m{exception_class}\033[1;97m")

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response






#CHILD

def __handle_invalid_token__(exc, context, response):
    data = {"status":False,
        "status_code": response.status_code,
        "message": str(exc.__class__.__name__),
        "id": None,
        "username": None}
    return JsonResponse(data=data)

def _handle_unicodeError__(exc, context, response):
    data = {"status":False,
        "status_code": response.status_code,
        "message":"unicodeError",
        "id": None,
        "username": None}
    return JsonResponse(data=data)

def _handle_invalidated_(exc, context, response):
    data = {"status":False,
        "status_code": response.status_code,
        "message":"invalidated",
        "id": None,
        "username": None}
    return JsonResponse(data=data)

def _handle_authentication_error(exc, context, response):
    data = {"status":False,
        "status_code": response.status_code,
        "message":"invalidated"}
    return JsonResponse(data=data)


def _handler_generic_error(exc, context, response):
    return JsonResponse({"status": False,
                         #"status_code": response.status_code,
                         "message": exc.__class__.__name__})

def _handle_http404__error(exc, content, response):
    return JsonResponse({"status": False,
                         "status_code": 404,
                         "message": exc.__class__.__name__})

def _handle_Type__error_(exc, content, response):
    return JsonResponse({"status": False,
                         "status_code": 400,
                         "message": exc.__class__.__name__})

def _handle_method_error_(exc, content, response):
    return JsonResponse({"status": False,
                         #"status_code": response.status_code,
                         "message": exc.__class__.__name__})