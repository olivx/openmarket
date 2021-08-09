from rest_framework.exceptions import APIException


class FeiraApiException(APIException):
    pass


class CannotPatchApiException(APIException):
    status_code = 400
    default_detail = "Cannot patch specified field"
    default_code = "cannot_patch"
