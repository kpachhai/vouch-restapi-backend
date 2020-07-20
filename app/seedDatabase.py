from app import log, config
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