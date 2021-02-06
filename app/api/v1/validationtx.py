from app import log, redisBroker
from app.api.common import BaseResource
from app.model import ValidationTx, ValidationStatus, Provider
from datetime import datetime, timedelta
from app.errors import (
    AppError,
)

LOG = log.get_logger()


class CreateValidationTx(BaseResource):
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
                status=ValidationStatus.NEW,
                isSavedOnProfile=False,
                retries=0
            )
            row.save()

            doc = {
                "type": "email",
                "action": "create",
                "transactionId": '{}'.format(row.id),
                "params": data["requestParams"],
                'did': data["did"]
            }
            redisBroker.send_validator_message(doc, provider["did"])

            result["validationtx"] = row.as_dict()

        self.on_success(res, result)

    def transaction_already_sent(self, data):
        time = datetime.utcnow() - timedelta(minutes=10)
        rows = ValidationTx.objects(did=data["did"].replace("did:elastos:", "").split("#")[0],
                                    validationType=data["validationType"],
                                    provider=data["provider"],
                                    modified__gte=time)
        if rows:
            for row in rows:
                obj = row.as_dict()
                if obj["status"] == ValidationStatus.CANCELED or obj[
                    "status"] == ValidationStatus.CANCELATION_IN_PROGRESS:
                    return None
                if obj["requestParams"] == data["requestParams"]:
                    return obj
        return None


class ValidationTxFromDid(BaseResource):
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


class ValidationTxFromProviderId(BaseResource):
    """
    Handle for endpoint: /v1/validationtx/provider_id/{provider_id}
    """

    def on_get(self, req, res, provider_id):
        rows = ValidationTx.objects(provider=provider_id)
        if rows:
            result = []
            for row in rows:
                # if row.status == ValidationStatus.NEW:
                result.append(row.as_dict())
            self.on_success(res, result)
        else:
            raise AppError(description="Cannot retrieve requests for the given provider_id")


class ValidationTxFromProviderDid(BaseResource):
    """
    Handle for endpoint: /v1/validationtx/provider_did/{provider_did}
    """

    def on_get(self, req, res, provider_did):

        providerId = ''

        # Get provider id by provider DID
        rows = Provider.objects(did=provider_did)
        if rows:
            providerId = rows[0].id
            
            # Get validation requests using above provider id
            # TODO: remove redundancy as the below is quite similar to ValidationTxFromProviderId on_get
            if providerId:
                rows2 = ValidationTx.objects(provider=str(providerId))
                if rows2:
                    result = []
                    for row in rows2:
                        result.append(row.as_dict())
                    self.on_success(res, result)
                else:
                    raise AppError(description="Cannot retrieve requests for the given provider_id")


class ValidationTxFromConfirmationId(BaseResource):
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


class ValidationTxCountFromProviderId(BaseResource):
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


class SetIsSavedValidationTx(BaseResource):
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


class ApproveValidationTx(BaseResource):
    """
    Handle for endpoint: /v1/validationtx/approve/confirmation_id/{confirmation_id}
    """

    def on_post(self, req, res, confirmation_id):
        rows = ValidationTx.objects(id=confirmation_id)

        if not rows:
            raise AppError(description="Validation not found")

        request = rows[0]

        if request.status == ValidationStatus.APPROVED:
            raise AppError(description="Validation is already approved")
        elif request.status == ValidationStatus.REJECTED:
            raise AppError(description="Validation cannot be approved after it has already been rejected")
        elif request.status == ValidationStatus.NEW:
            request.status = ValidationStatus.APPROVED
            request.verifiedCredential = req.media
            request.save()
        self.on_success(res, request.as_dict())


class RejectValidationTx(BaseResource):
    """
    Handle for endpoint: /v1/validationtx/reject/confirmation_id/{confirmation_id}
    """

    def on_post(self, req, res, confirmation_id):
        rows = ValidationTx.objects(id=confirmation_id)

        if not rows:
            raise AppError(description="Validation not found")

        request = rows[0]

        if request.status == ValidationStatus.REJECTED:
            raise AppError(description="Validation is already rejected")
        elif request.status == ValidationStatus.APPROVED or request.status == ValidationStatus.REJECTED:
            raise AppError(description="Validation cannot be rejected after it has been processed")
        elif request.status == ValidationStatus.NEW:
            request.status = ValidationStatus.REJECTED
            request.save()
        self.on_success(res, request.as_dict())


class CancelValidationTx(BaseResource):
    """
    Handle for endpoint: /v1/validationtx/cancel/confirmation_id/{confirmation_id}
    """

    def on_post(self, req, res, confirmation_id):
        rows = ValidationTx.objects(id=confirmation_id)

        if not rows:
            raise AppError(description="Validation not found")

        request = rows[0]

        if request.status == ValidationStatus.CANCELED:
            raise AppError(description="Validation is already canceled")
        elif request.status == ValidationStatus.APPROVED or request.status == ValidationStatus.REJECTED:
            raise AppError(description="Validation cannot be canceled after it has been processed")
        elif request.status == ValidationStatus.NEW:
            request.status = ValidationStatus.CANCELED
            request.save()
            self.on_success(res, request.as_dict())
            return

        providers = Provider.objects(id=request.provider)

        if not providers:
            raise AppError(description="Provider not found")

        redisBroker.send_validator_message({
            "type": "email",
            "action": "cancel",
            "transactionId": f'{request.id}',
        }, providers[0].did)

        request.status = ValidationStatus.CANCELATION_IN_PROGRESS
        request.retries = 0
        request.save()

        self.on_success(res, request.as_dict())