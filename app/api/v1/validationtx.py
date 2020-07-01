from app import log , redisBroker
from app.api.common import BaseResource
from app.model import ValidationTx, ValidationStatus, Provider
from datetime import datetime, timedelta
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
            raise AppError(description="Cannot retrieve requests for the given did")

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
            raise AppError(description="Cannot retrieve requests for the given confirmation ID")

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
            raise AppError(description="Provider not found for the given ID")

        transactionSended = self.transaction_already_sended(data)
        result = {}
        if transactionSended:
            result["duplicate"] = True
            result["validationtx"] = transactionSended
        else:
            result["duplicate"] = False
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
                
            result["validationtx"] = row.as_dict()
        
        
        self.on_success(res, result)
    
    def transaction_already_sended(self, data):
        time = datetime.now() - timedelta(minutes=10)
        rows = ValidationTx.objects(did=data["did"].replace("did:elastos:", "").split("#")[0], 
                                    validationType=data["validationType"],
                                    provider=data["provider"],
                                    modified__gte=time )
        if rows:
           print("rows found") 
           for row in rows:
               obj = row.as_dict()
               print("row id {}".format(obj["id"])) 
               if obj["requestParams"] == data["requestParams"]:
                  return obj
        return None    
class SetIsSavedOnProfile(BaseResource):
    """
    Handle for endpoint: /v1/validationtx/is_saved/confirmation_id/{confirmation_id}
    """

    def on_post(self, req, res, confirmation_id):
        print("enter /v1/validationtx/is_saved/confirmation_id/{}".format(confirmation_id))
        
        rows = ValidationTx.objects(id=confirmation_id)
        row =rows[0]
        row.isSavedOnProfile = True
        row.save()
        
        
        result = row.as_dict()
        self.on_success(res, result)

