from app import log, config
from app.model.provider import Provider

LOG = log.get_logger()

def seed_database():
    LOG.info("Start seeding Database")
    
    rows = Provider.objects()

    if rows:
       return

    LOG.info("Inserting providers")

    row = Provider(
                name="Tuum Tech",
                logo="data:image/png;base64,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",
                apikey="eyvc79BEYdycHYQFhqCKXKsdzqt",
                validationTypes=["Email"],
        )
    row.save()