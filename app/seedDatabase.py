from app import log, config
from app.model.validationtx import ValidationTx, ValidationStatus
from app.model.provider import Provider

LOG = log.get_logger()


def seed_database():
    LOG.info("Start seeding Database")

    providers = config.PROVIDERS
    for provider in providers:
        name = provider["name"]
        logo = provider["logo"]
        api_key = provider["api_key"]
        validation_types = provider["validation_types"]

        rows = Provider.objects(name=name, apikey=api_key)
        if rows:
            row = rows[0]
            if row.validationTypes.sort() != validation_types:
                row.validationTypes = validation_types
                row.save()
        else:
            LOG.info(f"Inserting a new provider: '{name}' with API Key '{api_key}'")
            row = Provider(
                name=name,
                logo=logo,
                apikey=api_key,
                validationTypes=validation_types
            )
            row.save()

    LOG.info("Finished seeding Database")


def update_pending_validation_status():
    LOG.info("Start updating pending validation status")

    transactions = ValidationTx.objects()

    for transaction in transactions:
        if transaction.status == "Pending":
            transaction.status = ValidationStatus.NEW

        if transaction.retries is None:
            transaction.retries = 0

        transaction.save()
