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


class CreateProvider(BaseResource):
    """
    Handle for endpoint: /v1/providers/create
    """

    def on_post(self, req, res):
        data = req.media
        did = data["did"].replace("did:elastos:", "").split("#")[0]
        name = data["name"]
        logo = data["logo"]

        logo = f"data:{logo['content-type']};{logo['type']},{logo['data']}"        

        validation = data["validation"]
        for validation_type, values in validation.items():
            if validation[validation_type]["manual"] is True:
                validation[validation_type]["next_steps"] = [
                    "Wait for the validator to verify you manually",
                    "Once the validator signs your DID, you can save the verified credential to your Identity "
                    "app "
                ]

        rows = Provider.objects(did=did)
        if rows:
            row = rows[0]
            if row.name != name or sorted(row.validation.keys()) != sorted(validation.keys()):
                LOG.info(f"Updating the provider: '{name}' with DID'{did}' with updated details...")
                row.name = name
                row.logo = logo
                row.validation = validation
                row.save()
        else:
            LOG.info(f"Inserting a new provider: '{name}' with DID'{did}'")
            row = Provider(
                did=did,
                name=name,
                logo=logo,
                validation=validation
            )
            row.save()
        stats = get_stats_from_validationtx(str(row.id))
        result = row.as_readonly_dict(stats)
        self.on_success(res, result)


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

