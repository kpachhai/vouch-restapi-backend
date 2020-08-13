from app import log, config
from app.model.validationtx import ValidationTx, ValidationStatus
from app.model.provider import Provider

LOG = log.get_logger()


def seed_database():
    LOG.info("Start seeding Database")

    providers = config.PROVIDERS
    for provider in providers:
        did = provider["did"]
        name = provider["name"]
        logo = provider["logo"]
        validation = provider["validation"]

        rows = Provider.objects(did=did)
        if rows:
            row = rows[0]
            if row.name != name or list(row.validation.keys()).sort() != list(validation.keys()).sort():
                row.name = name
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
