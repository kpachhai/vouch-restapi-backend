from app import log
from app.api.common import BaseResource
from app.model.provider import Provider
from app.errors import (
    AppError,
)

LOG = log.get_logger()

class ProvidersCollection(BaseResource):
    """
    Handle for endpoint: /v1/providers
    """

    def on_get(self, req, res):
        rows = Provider.objects()
        if rows:
            obj = [each.as_readonly_dict() for each in rows]
            self.on_success(res, obj)
        else:
            raise AppError()

class ProvidersFromValidationTypeCollection(BaseResource):
    """
    Handle for endpoint: /v1/providers/valiationtype/{validationType}
    """

    def on_get(self, req, res, validationType):
        rows = Provider.objects(validationTypes__contains=validationType)
        if rows:
            obj = [each.as_readonly_dict() for each in rows]

            self.on_success(res, obj)
        else:
            raise AppError()

