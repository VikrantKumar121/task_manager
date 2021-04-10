from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

        #replace detail key with message key by delete detail key
        response.data['message'] = response.data['detail']
        del response.data['detail']

    return response


class CustomApiException(APIException):
    #public fields
    message = None
    status_code = None

    # create constructor
    def __init__(self, status_code, message):
        #override public fields
        CustomApiException.status_code = status_code
        CustomApiException.detail = message



class CustomNotFound(CustomApiException):
    status_code = 404
    message = None
    def __init__(self, message="Not Found"):
        CustomNotFound.detail = message



