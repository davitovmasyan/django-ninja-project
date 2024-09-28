import logging

from django.conf import settings
from ninja import NinjaAPI
from ninja_jwt.authentication import JWTAuth

from accounts.api import accounts_router

api = NinjaAPI(auth=JWTAuth(), urls_namespace='api', docs_url='/docs/')
api.add_router('accounts/', accounts_router)

logger = logging.getLogger('api')


def service_unavailable(request, exc):
    if settings.DEBUG:
        raise exc

    logger.error(exc)
    return api.create_response(
        request,
        {"message": "Internal server error."},
        status=500,
    )


api.exception_handler(Exception)(service_unavailable)
