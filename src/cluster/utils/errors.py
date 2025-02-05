from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException, ErrorDetail, ValidationError


class UniqueTogetherValidationError(ValidationError):
    """
    Custom exception class to handle validation errors for fields that should be unique
    together. Inherits from DRF's ValidationError.

    Args:
        message (str): The error message explaining the uniqueness violation.
        code (str, optional): The error code (default is 'unique').

    Attributes:
        The error is passed as a dictionary with the "non_field_errors" key, containing
        a list of ErrorDetail objects with the message and code.
    """

    def __init__(self, message, code="unique"):
        super().__init__({"non_field_errors": [ErrorDetail(message, code)]})


class GenericError(APIException):
    """
    A generic error class for raising API exceptions with custom status codes, messages,
    and error codes. Inherits from DRF's APIException.

    Args:
        status_code (status): The HTTP status code for the error response.
        detail (str): The error message.
        code (str): The error code.

    Attributes:
        status_code (int): The HTTP status code for the error.
    """

    def __init__(self, status_code: status, detail: str, code: str):
        super().__init__(detail=_(detail), code=code)
        self.status_code = status_code


class AssociatedError(APIException):
    """
    Custom API exception raised when an associated object causes a conflict.
    Inherits from DRF's APIException.

    Attributes:
        status_code (int): The HTTP status code (default is 409 Conflict).
        default_detail (str): A default error message, which can be localized.
        default_code (str): The default error code (set to "object_associated").
    """

    status_code = status.HTTP_409_CONFLICT
    default_detail = _("An associated error occurred.")
    default_code = "object_associated"
