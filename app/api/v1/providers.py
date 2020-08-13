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
    Handle for endpoint: /v1/providers/validationType/{validation_type}
    """

    def on_get(self, req, res, validation_type):
        rows = Provider.objects()
        if rows:
            response = []
            for row in rows:
                if validation_type in row.validation.keys():
                    stats = get_stats_from_validationtx(str(row.id))
                    response.append(row.as_readonly_dict(stats))

            self.on_success(res, response)
        else:
            raise AppError(description="Cannot retrieve providers for the given validationType")


def get_stats_from_validationtx(provider_id):
    stats = {}
    validation_tx_rows = ValidationTx.objects(provider=provider_id)
    if validation_tx_rows:
        for validation_tx_row in validation_tx_rows:
            status = validation_tx_row.status
            if status in stats.keys():
                stats[status] += 1
            else:
                stats[status] = 1
    return stats
