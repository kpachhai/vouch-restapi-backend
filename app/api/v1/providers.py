from app import log
from app.api.common import BaseResource
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
        if rows:
            response = []
            for row in rows:
                stats = get_stats_from_validationtx(str(row.id))
                response.append(row.as_readonly_dict(stats))

            self.on_success(res, response)
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
                    stats = get_stats_from_validationtx(str(row.id))
                    response.append(row.as_readonly_dict(stats))

            self.on_success(res, response)
        else:
            raise AppError(description="Cannot retrieve providers for the given validationType")

def get_stats_from_validationtx(provider_id):
    stats = {}
    validationTxRows = ValidationTx.objects(provider=provider_id)
    if validationTxRows:
        for validationTxRow in validationTxRows:
            status = validationTxRow.status
            if status in stats.keys():
                stats[status] += 1
            else:
                stats[status] = 1
    return stats