from app import log, redisBroker
from app.api.common import BaseResource
from app.model import ValidationTx, ValidationStatus, Provider
from app.errors import (
    AppError,
)

LOG = log.get_logger()


class ValidationsFromDid(BaseResource):
    """
    Handle for endpoint: /v1/validationtx/did/{did}
    """

    def on_get(self, req, res, did):
        rows = ValidationTx.objects(did=did)
        if rows:
            obj = [each.as_dict() for each in rows]
            self.on_success(res, obj)
        else:
            raise AppError()

class ValidationFromId(BaseResource):
    """
    Handle for endpoint: /v1/validationtx/id/{did}
    """

    def on_get(self, req, res, confirmation_id):
        rows = ValidationTx.objects(id=confirmation_id)
        if rows:
            obj = [each.as_dict() for each in rows]
            self.on_success(res, obj)
        else:
            raise AppError()

class CreateValidation(BaseResource):
    """
    Handle for endpoint: /v1/validationtx/create
    """

    def on_post(self, req, res):
        data = req.media

        providerId = data["provider"]

        providersRows = Provider.objects(id=providerId)
        if not providersRows:
            provider = [each.as_dict() for each in providersRows][0]
        else:
            raise AppError()

        row = ValidationTx(
            did= data["didId"].replace("did:elastos:", "").split("#")[0],
            provider=data["provider"],
            validationType=data["validationType"],
            requestParams=data["requestParams"],
            status=ValidationStatus.PENDING
        )
        row.save()

        if data["validationType"] == "email":
           doc = {
               'transactionId': '{}'.format(row.id), 
               'email': row.requestParams["email"],
               'did': row.did
            }
           redisBroker.send_email_validation(doc, provider.apiKey)

        
        result = {
            "confirmation_id": str(row.id)
        }
        self.on_success(res, result)

