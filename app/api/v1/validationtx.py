from app import log, redisBroker
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

class ValidationCountFromProvider(BaseResource):
    """
    Handle for endpoint: /v1/validationtx/count/provider_id/{provider_id}
    """

    def on_get(self, req, res, provider_id):
        rows = ValidationTx.objects(provider=provider_id)
        if rows:
            result = {}
            for row in rows:
                status = row.status
                if status in result.keys():
                    result[status] += 1
                else:
                    result[status] = 1 
            self.on_success(res, result)
        else:
            raise AppError(description="Cannot retrieve total request count for the given provider ID")


class CreateValidation(BaseResource):
    """
    Handle for endpoint: /v1/validationtx/create
    """

    def on_post(self, req, res):
        data = req.media
        providerId = data["provider"]
        providersRows = Provider.objects(id=providerId)

        if providersRows:
            provider = [each.as_dict() for each in providersRows][0]
        else:
            raise AppError(description="Provider not found for the given ID")

        transactionSent = self.transaction_already_sent(data)
        result = {}
        if transactionSent:
            result["duplicate"] = True
            result["validationtx"] = transactionSent
        else:
            result["duplicate"] = False
            row = ValidationTx(
                did=data["did"].replace("did:elastos:", "").split("#")[0],
                provider=data["provider"],
                validationType=data["validationType"],
                requestParams=data["requestParams"],
                status=ValidationStatus.PENDING,
                isSavedOnProfile=False
            )
            row.save()

            if data["validationType"] == "email":
                doc = {
                    'transactionId': '{}'.format(row.id),
                    'email': row.requestParams["email"],
                    'did': data["did"]
                }
                redisBroker.send_email_validation(doc, provider["apiKey"])

            result["validationtx"] = row.as_dict()

        self.on_success(res, result)

    def transaction_already_sent(self, data):
        time = datetime.now() - timedelta(minutes=10)
        rows = ValidationTx.objects(did=data["did"].replace("did:elastos:", "").split("#")[0],
                                    validationType=data["validationType"],
                                    provider=data["provider"],
                                    modified__gte=time)
        if rows:
            for row in rows:
                obj = row.as_dict()
                if obj["requestParams"] == data["requestParams"]:
                    return obj
        return None


class SetIsSavedOnProfile(BaseResource):
    """
    Handle for endpoint: /v1/validationtx/is_saved/confirmation_id/{confirmation_id}
    """

    def on_post(self, req, res, confirmation_id):
        result = {}
        rows = ValidationTx.objects(id=confirmation_id)
        if rows:
            row = rows[0]
            row.isSavedOnProfile = True
            row.save()
            result = row.as_dict()
        self.on_success(res, result)


