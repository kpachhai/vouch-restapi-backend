from app import log
from app.api.common import BaseResource
#from app.model.provider import Provider
from app.model import ValidationTx, Provider
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
        responseObj = []
        if rows:
            for row in rows:
                providerId = str(row.id)
                providerData = row

                providerData.stats = {}
                validationTxRows = ValidationTx.objects(provider=providerId)

                if validationTxRows:
                    for validationTxRow in validationTxRows:
                        status = validationTxRow.status
                        if status in row.stats.keys():
                            providerData.stats[status] += 1
                        else:
                            providerData.stats[status] = 1 

                responseObj.append(providerData.as_readonly_dict())

            self.on_success(res, responseObj)
        else:
            raise AppError(description="Cannot retrieve providers from the database")


class ProvidersFromValidationTypeCollection(BaseResource):
    """
    Handle for endpoint: /v1/providers/validationType/{validationType}
    """

    def on_get(self, req, res, validationType):
        rows = Provider.objects()
        if rows:
            response = []
            for row in rows:
                if validationType in row.validationTypes:
                    response.append(row.as_readonly_dict())

            self.on_success(res, response)
        else:
            raise AppError(description="Cannot retrieve providers for the given validationType")
