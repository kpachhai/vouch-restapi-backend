from app import log
from app.api.common import BaseResource
from app.model import Provider
from app.errors import (
    AppError,
)

LOG = log.get_logger()


class ServicesFromProviderDid(BaseResource):
    """
    Handle for endpoint: /v1/services/provider_did/{provider_did}
    """

    def on_get(self, req, res, did):
        did = did.replace("did:elastos:", "").split("#")[0]
        result = {}
        rows = Provider.objects(did=did)
        if rows:
            row = rows[0]

            result["id"] = str(row.id)
            result["did"] = did
            result["validationTypes"] = list(row.validation.keys())
            self.on_success(res, result)
        else:
            raise AppError(description="Cannot retrieve services for the given did")