from app import log , redisBroker
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
    Handle for endpoint: /v1/validationtx/confirmation_id/{confirmation_id}
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
        LOG.info("provider id {0}".format(providerId))
        providersRows = Provider.objects(id=providerId)
        
        if providersRows:
            LOG.info("found")
            provider = [each.as_dict() for each in providersRows][0]
        else:
            LOG.info("Provider not found")
            raise AppError()

        

        row = ValidationTx(
            did=data["did"].replace("did:elastos:", "").split("#")[0],
            provider=data["provider"],
            validationType=data["validationType"],
            requestParams=data["requestParams"],
            status=ValidationStatus.PENDING
        )
        row.save()

        LOG.info("Confirmation ID {0}".format(str(row.id)))

        if data["validationType"] == "email":
           doc = {
               'transactionId': '{}'.format(row.id), 
               'email': row.requestParams["email"],
               'did': data["did"]
            }
           LOG.info(doc)
           redisBroker.send_email_validation(doc, provider["apiKey"])

        
        result = {
            "confirmation_id": str(row.id)
        }
        self.on_success(res, result)

