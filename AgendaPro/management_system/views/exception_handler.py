from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.views import set_rollback

from management_system.services.service_exceptions import (
    AppointmentConflict,
    DomainException,
    EntityNotFound,
    InvalidRole,
    ProfessionalDoesNotOfferService,
)
from django.db import IntegrityError

HTTP_STATUS_BY_ERROR = {
    EntityNotFound: 404,
    AppointmentConflict: 409,
    ProfessionalDoesNotOfferService: 400,
    InvalidRole: 403,
    IntegrityError: 409
}


def domain_exception_handler(exc, context):
    if isinstance(exc, DomainException):

        for cls in type(exc).__mro__:
            if cls in HTTP_STATUS_BY_ERROR:
                set_rollback()
                body = {
                    "error": {
                        "code": exc.code,
                        "message": exc.default_message,
                    }
                }
                return Response(body, status=HTTP_STATUS_BY_ERROR[cls])
        return None

    return drf_exception_handler(exc, context)